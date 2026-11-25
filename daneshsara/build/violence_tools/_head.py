# -*- coding: utf-8 -*-
import os
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
BASE = """
:root{--c:var(--fam-psy);--vh:#9F1239;--vr:#2F6B4F;--va:#B45309;--vm:#4E6E8E;--vz:color-mix(in srgb,var(--ink-3) 22%,var(--paper))}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--vh:#F0708C;--vr:#6FBF95;--va:#E8A04A;--vm:#8FB0D0}}
:root[data-theme=dark]{--vh:#F0708C;--vr:#6FBF95;--va:#E8A04A;--vm:#8FB0D0}
h1{font-size:var(--h1);margin:var(--s8) 0 var(--s3);line-height:var(--lh-tight);text-wrap:balance}
p.lead{color:var(--ink-2);max-width:46em;line-height:2;margin:0 0 var(--s4);font-size:1.05rem}
.note{padding:var(--s3) var(--s4);border-radius:var(--r-md);font-size:var(--small);line-height:1.9;color:var(--ink-2);max-width:60em;margin:0 0 var(--s3)}
.note.w{background:color-mix(in srgb,var(--warn) 10%,var(--paper));border:1px solid color-mix(in srgb,var(--warn) 45%,var(--line))}
.note.r{background:color-mix(in srgb,var(--err) 8%,var(--paper));border:1px solid color-mix(in srgb,var(--err) 38%,var(--line))}
.note.g{background:var(--surface);border:1px solid var(--line)}
section{padding-block:var(--s5);border-top:1px solid var(--line)}
h2{font-size:var(--h3);margin:0 0 var(--s3)}
button{font:inherit}
.pb{font-size:var(--small);padding:8px 16px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:var(--paper);color:var(--ink);cursor:pointer}
.pb[aria-pressed=true],.pb.on{background:var(--c);border-color:var(--c);color:var(--paper);font-weight:650}
.pb.go{background:var(--c);border-color:var(--c);color:var(--paper);font-weight:700}
.row{display:flex;gap:8px;flex-wrap:wrap}
.back{display:inline-block;margin:var(--s5) 0;font-size:var(--small)}
.off{display:none!important}
input[type=range]{width:100%;direction:ltr;accent-color:var(--c)}
"""
def page(slug, title, desc, css, body, js):
    out = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} | ویکی روان‌شناسی | دانش‌سرا</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="../../core/design/tokens.css">
<style>{BASE}{css}</style>
</head>
<body>
<main class="wrap">
{body}
<a class="back" href="../violence.html">→ بازگشت به پروندهٔ خشونت</a>
</main>
<script>
(function(){{const $=id=>document.getElementById(id),fa=n=>String(n).replace(/[0-9]/g,d=>"۰۱۲۳۴۵۶۷۸۹"[d]).replace(".","٫");
{js}
}})();
</script>
</body>
</html>
'''
    open(f'{R}/psy/tools/{slug}.html', 'w', encoding='utf-8').write(out); print(slug)
