# -*- coding: utf-8 -*-
"""Merge a raw list of IranAzadAbad discussions into data/sakht/sakht.json.
usage: python3 build/sakht_ideas_merge.py <raw.txt> <pages e.g. 1-9>
raw line: number | title | category | upvotes | comments | author   (author is dropped: no usernames on the site)"""
import json, sys, os
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
CAT = {'Infrastructure': 'زیرساخت', 'General': 'عمومی', 'finance': 'مالی', 'health & biotech': 'سلامت', 'education': 'آموزش', 'smart cities': 'شهر هوشمند', 'Energy': 'انرژی', 'AI': 'هوش مصنوعی', 'Tourism': 'گردشگری', 'Social': 'اجتماعی', 'Environment': 'محیط‌زیست', 'art & culture': 'هنر و فرهنگ', 'manufacturing': 'تولید', 'Agriculture': 'کشاورزی', 'Startup Ecosystem': 'زیست‌بوم استارتاپی', 'Internet': 'اینترنت', 'media': 'رسانه', 'Media': 'رسانه'}
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
p = R + '/data/sakht/sakht.json'; d = json.load(open(p, encoding='utf-8'))
old = [i for i in d['ideas'] if 'n' not in i]; new = {}
for l in open(sys.argv[1], encoding='utf-8'):
    a = [x.strip() for x in l.strip().split(' | ')]
    if len(a) < 6: continue
    n = int(a[0]); new[n] = {"t": ' | '.join(a[1:-4]), "c": CAT[a[-4]], "v": int(a[-3]), "m": int(a[-2]), "n": n}
tt = {x['t'] for x in new.values()}
d['ideas'] = [i for i in old if i['t'] not in tt] + list(new.values())
lo, hi = sys.argv[2].split('-'); d['ideas_pages'] = list(range(int(lo), int(hi) + 1))
d['ideas_note'] = f"مخزن IranAzadAbad حدود ۳۲۵ ایده در ۱۳ صفحه و ۱۷ دسته دارد. این‌ها ایده‌اند، نه یافتهٔ بررسی‌شده (ردهٔ ۴)، و تعداد رأی فقط نشان می‌دهد چند نفر در همان مخزن پسندیده‌اند. تا این‌جا صفحه‌های {fa(lo)} تا {fa(hi)} خوانده شده (۱۱ نوامبر ۲۰۲۶، ۲۰ آبان ۱۴۰۵)؛ فقط عنوان و شمارش‌ها، نه متن ایده‌ها."
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(len(d['ideas']), 'ideas')
