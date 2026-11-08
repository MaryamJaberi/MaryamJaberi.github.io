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

## خط ساخت خودکار
`.github/workflows/daneshsara.yml`: با هر push به `daneshsara/`، اعتبارسنجی (schema + ارجاع‌ها + رجیستری) اجرا می‌شود و در صورت خطا شکست می‌خورد؛ سپس خواننده‌های ویکی و نقشهٔ سرزمین‌ها دوباره ساخته و در صورت تغییر کامیت می‌شوند.

## ویکی جامعه (soc)
- `build/soc_seed.py` (با `build/seedlib.py`) → ۲۹ گره (ریشه، ۶ حوزه، ۲۱ مدخل)، ۵ یادداشت «برای ایران» (اعتماد، جینی، تغییر ارزش‌ها، دین‌داری، شهرنشینی)، ۴۵ منبع. `python3 build/reader.py soc` → `soc/index.html`.

## ویکی فلسفه (phil)
- `build/phil_seed.py` → ۳۰ گره (ریشه، ۷ حوزه، ۲۲ مدخل) از معرفت‌شناسی و ذهن تا فلسفهٔ ایرانی‌اسلامی؛ ۴۵ منبع. `python3 build/reader.py phil` → `phil/index.html`.

## لایهٔ «برای ایران»
- یادداشت‌ها در `iran/*.json` (طرح‌وارهٔ `core/schema/iran.schema.json`: پرسش، یافته، سال، روش، ردهٔ A–D، محل بحث، نقد، منبع، قابلیت‌های نوسبام ۱–۱۰).
- `python3 build/iran_page.py` → `iran/index.html` (به تفکیک حوزه و قابلیت).

## دفترهای مشترک
- `python3 build/core_pages.py` → `core/people.html` (۶۲۹ چهره با مدخل‌هایشان) و `core/sources.html` (۶۶۹ منبع با رده و مدخل‌های استفاده‌کننده).

## بررسی پیوندها
- `node build/linkcheck.js` (نیاز به Playwright): صفحه‌ها را رندر می‌کند و همهٔ پیوندهای داخلی را می‌آزماید؛ آخرین اجرا: ۶۴۴ پیوند، صفر شکسته.
