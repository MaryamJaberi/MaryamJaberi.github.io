# خواندن کامل یک کتاب از درایو

1. `download_file_content` با شناسهٔ فایل. نتیجه در یک فایل tool-results ذخیره می‌شود (base64 درون JSON).
   تا حدود ۶ مگابایت آزموده شده و کار می‌کند؛ فایل ۸٫۷ مگابایتی رد شد.
2. `python3 -I build/library/drive_decode.py <tool-results file> <dir>/book.pdf`
3. اگر `pdftotext` متن داد همان را بخوان؛ اگر کتاب اسکن است: `build/library/ocr.sh <dir>` (tesseract، زبان fas) که `book.txt` با نشانهٔ `==== page N ====` می‌سازد.
4. متن را تکه‌تکه و کامل بخوان؛ شمارهٔ صفحه‌ها را در مدخل و در books.json ثبت کن.

خود PDF و متن OCR در مخزن ذخیره نمی‌شوند (حق نشر).
