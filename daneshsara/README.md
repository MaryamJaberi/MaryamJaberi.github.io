# دانش‌سرا

چند ویکی فارسی به‌هم‌پیوسته دربارهٔ انسان (روان، جامعه، تبار و ژنتیک، فلسفه) روی یک هستهٔ مشترک، با پل‌های میان‌رشته‌ای و لایهٔ «برای ایران».
سایت: https://maryamjaberi.github.io/daneshsara/

## ساختار
- `core/` طرح‌واره‌ها (`schema/`)، سیستم طراحی (`design/`)، چهره‌ها و منابع مشترک، رجیستری و هدایت‌ها (تولیدی)
- `data/<wiki>/concepts/*.json` یک مفهوم در هر فایل؛ شناسه `psy:slug`
- `atlas/` رشته‌ها (`fields.json`)، صفحه‌های پل (`bridges/*.json` + `bridge.html`)، اطلس دیداری (`index.html`)
- `psy/` ویکی روان (ساخته‌شده)
- `iran/` برگه‌های ایران (فاز ۴)
- `build/` اسکریپت‌ها: `export_psy.py` (مهاجرت از گراف)، `atlas.py`، `validate.py` (اعتبارسنجی + رجیستری)، `site.py`

## ساخت
```
python3 build/atlas.py raw.json ../wiki/atlas2.data.js
python3 build/validate.py        # خطا = منتشر نشود
python3 build/site.py <site dir>
```
متن CC BY-SA 4.0 · کد MIT · فونت وزیرمتن OFL


## ویکی تبار (tabar) — فاز ۲
- `build/tabar_seed.py` → `data/tabar/concepts/*.json` (۳۲ گره: ریشه، ۷ حوزه، ۲۴ مدخل)، `iran/*.json` (۶ یادداشت)، و افزودنِ افراد/منابع به هسته (افزایشی).
- `build/reader.py tabar` → `tabar/index.html` خوانندهٔ عمومی ویکی (برای soc و phil هم همین اسکریپت).
- همهٔ مدخل‌ها `status: draft` تا بازبینی کارشناس.
