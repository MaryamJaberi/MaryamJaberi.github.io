#!/usr/bin/env python3
"""گاوصندوق: بسته‌بندی و رمزنگاری بخش‌های خصوصی دانش‌سرا.

هر چیزی که نباید عمومی دیده شود در یک بستهٔ gzip+JSON جمع و با
AES-256-GCM رمز می‌شود. کلید با PBKDF2-SHA256 (۶۰۰٬۰۰۰ دور) از
رمز عبور ساخته می‌شود. فقط فایل رمزشده در مخزن می‌ماند.

ساختار فایل:  b"DSV1" + salt(16) + iv(12) + ciphertext

استفاده:
    DS_VAULT_PASS='…' python3 build/vault.py <پوشهٔ منبع> [خروجی]

پوشهٔ منبع باید ساختار daneshsara/ را داشته باشد (مثلاً src/daneshsara/iran/…)
"""
import gzip
import json
import os
import secrets
import sys
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

MAGIC = b"DSV1"
ITERATIONS = 600_000
TEXT_SUFFIXES = {".html", ".json", ".js", ".css", ".py", ".md", ".txt", ".svg"}


def derive(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=salt, iterations=ITERATIONS)
    return kdf.derive(password.encode("utf-8"))


def collect(src: Path) -> dict:
    root = src / "daneshsara"
    if not root.is_dir():
        root = src
    files = {}
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = p.relative_to(root).as_posix()
        files[rel] = p.read_text(encoding="utf-8")
    return files


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    password = os.environ.get("DS_VAULT_PASS")
    if not password:
        print("DS_VAULT_PASS تعیین نشده است", file=sys.stderr)
        return 1

    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("vault/bundle.enc")
    files = collect(src)
    if not files:
        print("هیچ فایلی پیدا نشد", file=sys.stderr)
        return 1

    payload = gzip.compress(
        json.dumps({"v": 1, "files": files}, ensure_ascii=False).encode("utf-8"), 9
    )
    salt = secrets.token_bytes(16)
    iv = secrets.token_bytes(12)
    blob = MAGIC + salt + iv + AESGCM(derive(password, salt)).encrypt(iv, payload, MAGIC)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(blob)
    print(f"{len(files)} فایل → {out} ({len(blob)/1024:.0f} کیلوبایت)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
