# -*- coding: utf-8 -*-
"""Inject an «ابزارها» strip into each layer's page (idempotent). Run AFTER reader/tabar_home/iran_page/atlas builders.
Tools live only in their own layer; the landing page never links to them."""
import re, os
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
CSS = '<style>.dstools{margin:20px 0;padding:14px 16px;border:1px solid var(--line);border-radius:16px;background:var(--primary-soft)}.dstools b{display:block;margin-bottom:8px;font-size:1rem}.dstools .r{display:flex;flex-wrap:wrap;gap:8px}.dstools a{padding:7px 16px;border-radius:999px;border:1px solid var(--primary);background:var(--surface);color:var(--primary);text-decoration:none;font-size:.92rem}.dstools a:hover{background:var(--primary);color:#fff}</style>'
L = {
 'atlas': ('اطلس', [('compare', 'مقایسهٔ دو مفهوم'), ('path', 'مسیر بین دو مفهوم'), ('evidence', 'نقشهٔ شواهد'), ('bridges', 'یابندهٔ پل‌ها'), ('library', 'کتابخانه و اعتبار منابع'), ('contested', 'پیشخوان محل‌بحث‌ها')]),
 'iran': ('برای ایران', [('lens', 'ایران از دید هر رشته'), ('timeline', 'خط زمانی'), ('matrix', 'ماتریس مسئله × رشته'), ('check', 'راستی‌آزمای ادعا')]),
 'tabar': ('تبار', [('explore', 'کاوشگر'), ('timeline', 'خط زمانی'), ('glossary', 'واژه‌نامه و کارت مرور')]),
 'psy': ('روان', [('../learn', 'مرکز یادگیری'), ('../scales', 'خودسنجی'), ('explore', 'کاوشگر'), ('compare-theories', 'مقایسهٔ رویکردها')]),
 'soc': ('جامعه', [('explore', 'کاوشگر'), ('thinkers', 'اندیشمندان')]),
 'phil': ('فلسفه', [('explore', 'کاوشگر'), ('debates', 'مناظره‌ها'), ('thinkers', 'اندیشمندان')]),
}
for w, (name, tools) in L.items():
    p = f'{R}/{w}/index.html'; s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!--dstools-->.*?<!--/dstools-->', '', s, flags=re.S)
    links = ''.join(f'<a href="tools/{t}.html">{n}</a>' if not t.startswith('../') else f'<a href="{t[3:]}.html">{n}</a>' for t, n in tools)
    html = f'<!--dstools-->{CSS}<nav class="dstools" aria-label="ابزارهای {name}"><b>ابزارهای {name}</b><div class="r">{links}<a href="tools/">همهٔ ابزارها ←</a></div></nav><!--/dstools-->'
    m = re.search(r'<main[^>]*>', s) if w != 'atlas' else re.search(r'<h1>اطلس رشته‌ها</h1>', s)
    if not m: print('NO ANCHOR', w); continue
    s = s[:m.end()] + html + s[m.end():]
    open(p, 'w', encoding='utf-8').write(s); print('tools strip', w)
