# -*- coding: utf-8 -*-
"""One breadcrumb bar on every page: python3 build/crumbs.py
Rewrites the <nav class="ds-crumbs"> block (idempotent) just after <body> so a reader
always sees where they are and what they can click back to."""
import os, re, html, glob
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
E = html.escape
PSY_TOOLS = {'graph','land','body','emotions','timeline','heat','river','lineage','prism','path','effect','evidence',
             'debate','guess','lab','scales','learn','library','atlas2','explore','compare-theories'}
WIKI = {'psy':'ویکی روان‌شناسی','soc':'ویکی جامعه','phil':'ویکی فلسفه','tabar':'ویکی تبار و ژنتیک',
        'tarikh':'ویکی تاریخ و ایران‌شناسی','miyan':'ویکی ارتباط رشته‌ها','iran':'ویکی ایران','simorgh':'ویکی سیمرغ','sakht':'ساخت ایران'}
LAYER = {'psy':('لایهٔ علم','index.html#layers'),'soc':('لایهٔ علم','index.html#layers'),
         'phil':('لایهٔ علم','index.html#layers'),'tabar':('لایهٔ علم','index.html#layers'),
         'tarikh':('لایهٔ علم','index.html#layers'),
         'miyan':('لایهٔ علم','index.html#layers'),'atlas':('لایهٔ علم','index.html#layers'),
         'iran':('لایهٔ ایران','index.html#layers'),'simorgh':('لایهٔ سیمرغ','index.html#layers'),'sakht':('لایهٔ ساخت','index.html#layers'),
         'core':('هستهٔ مشترک','atlas/sitemap.html')}

CSS = ('<style id="ds-crumbs-css">.ds-crumbs{font:400 .82rem/1.7 inherit;padding:7px max(16px,env(safe-area-inset-right,0px)) 7px max(16px,env(safe-area-inset-left,0px));'
 'border-bottom:1px solid var(--line,#e5e1d8);background:var(--paper,#faf8f3);color:var(--ink-3,#8a8578);display:flex;flex-wrap:wrap;gap:6px;align-items:baseline}'
 '.ds-crumbs a{color:var(--ink-2,#5c574c);text-decoration:none}.ds-crumbs a:hover{text-decoration:underline}'
 '.ds-crumbs i{font-style:normal;opacity:.5}.ds-crumbs b{font-weight:600;color:var(--ink,#2b2922)}'
 '@media (prefers-color-scheme:dark){.ds-crumbs{border-color:var(--line,#33312c);background:var(--paper,#1b1a17)}}</style>')

def title_of(s, fallback):
    m = re.search(r'<title[^>]*>(.*?)</title>', s, re.S)
    t = re.sub(r'\s+', ' ', re.sub('<[^>]*>', '', m.group(1))).strip() if m else ''
    if not t:
        m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        t = re.sub(r'\s+', ' ', re.sub('<[^>]*>', '', m.group(1))).strip() if m else fallback
    t = re.split(r'\s*[|]\s*', t)[0].strip()
    t = re.sub(r'^ویکی\s[^—–|]{0,40}[—–]\s*', '', t).strip()
    t = re.sub(r'\s*[—–]\s*دانش‌سرا\s*$', '', t).strip()
    return t[:70] or fallback

def trail(rel, s):
    parts = rel.split('/'); d = parts[0] if len(parts) > 1 else ''
    sub = parts[1] if len(parts) > 2 else ''
    f = os.path.splitext(parts[-1])[0]
    depth = len(parts) - 1
    pre = '../' * depth
    out = [('دانش‌سرا', pre + 'index.html')]
    if rel == 'index.html': return [('دانش‌سرا', None)]
    if d in LAYER:
        ln, lu = LAYER[d]; out.append((ln, pre + lu))
    if d in WIKI:
        if f == 'index' and depth == 1: out.append((WIKI[d], None)); return out
        out.append((WIKI[d], pre + d + '/'))
    elif d == 'atlas':
        if f == 'index' and depth == 1: out.append(('اطلس‌ها', None)); return out
        out.append(('اطلس‌ها', pre + 'atlas/'))
    elif d == 'core':
        pass
    if sub == 'tools':
        if f == 'index': out.append(('ابزارها', None)); return out
        out.append(('ابزارها', pre + d + '/tools/'))
    elif d == 'psy' and depth == 1 and f != 'index':
        # a psy content page carries its own domain/topic trail; reuse it instead of a coarse guess
        m = re.search(r'<nav class="crumb"[^>]*>(.*?)</nav>', s, re.S)
        own = re.findall(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', m.group(1), re.S) if m else []
        own = [(re.sub(r'\s+', ' ', re.sub('<[^>]*>', '', t)).strip(), u) for u, t in own]
        own = [(t, pre + 'psy/' + u) for t, u in own if t and not t.startswith('⌂')]
        if own: out.extend(own)
        elif f in PSY_TOOLS: out.append(('ابزارها', pre + 'psy/tools/'))
        elif f in ('orgsvc', 'orgpsych'): out.append(('سنجش سازمان', pre + 'psy/#subs'))
        else: out.append(('کتاب‌ها و موضوع‌ها', pre + 'psy/#subs'))
    elif d in WIKI and f == 'entries': out.append(('همهٔ مدخل‌ها', None)); return out
    out.append((title_of(s, f), None))
    return out

n = 0
for p in sorted(glob.glob(f'{R}/**/*.html', recursive=True)):
    rel = os.path.relpath(p, R).replace(os.sep, '/')
    if rel.startswith('build/') or rel == 'index.html': continue
    s = open(p, encoding='utf-8').read()
    if 'http-equiv="refresh"' in s: continue   # a redirect stub needs no breadcrumb
    s = re.sub(r'<nav class="ds-crumbs".*?</nav>\s*', '', s, flags=re.S)
    s = re.sub(r'<style id="ds-crumbs-css">.*?</style>\s*', '', s, flags=re.S)
    s = re.sub(r'<script src="[^"]*core/nav\.js" defer></script>\s*', '', s)
    # drop the older, inconsistent breadcrumb bars so there is only one
    s = re.sub(r'<div class="crumbs"[^>]*>.*?</div>\s*', '', s, count=1, flags=re.S)
    tr = trail(rel, s)
    s = re.sub(r'<nav class="crumb"[^>]*>.*?</nav>\s*', '', s, count=1, flags=re.S)
    s = re.sub(r'<div class="crumb"[^>]*>.*?</div>\s*', '', s, count=1, flags=re.S)
    # an older static bar near the top of the page only; never one built inside a script
    mb = re.search(r'<body[^>]*>', s)
    head_end = (mb.end() + 3000) if mb else 0
    mo = re.search(r'<nav class="crumbs"[^>]*>.*?</nav>\s*', s, re.S)
    if mo and mo.start() < head_end: s = s[:mo.start()] + s[mo.end():]
    items = []
    for i, (t, u) in enumerate(tr):
        last = i == len(tr) - 1
        items.append(f'<b>{E(t)}</b>' if last or not u else f'<a href="{E(u)}">{E(t)}</a>')
    bar = CSS + '<nav class="ds-crumbs" aria-label="مسیر صفحه">' + '<i>›</i>'.join(items) + '</nav>'
    bar += '<script src="' + '../' * (rel.count('/')) + 'core/nav.js" defer></script>'
    # one title convention everywhere:  <page> | <wiki> | دانش‌سرا
    names = [t for t, _ in tr[1:]]
    mid = [n for n in names[:-1] if n.startswith('ویکی') or n in ('اطلس‌ها', 'هستهٔ مشترک')]
    want = ' | '.join(dict.fromkeys([names[-1]] + mid[:1] + ['دانش‌سرا'])) if names else 'دانش‌سرا'
    s = re.sub(r'<title[^>]*>.*?</title>', lambda _: '<title>' + E(want) + '</title>', s, count=1, flags=re.S)
    # a missing meta description, taken from the page's own opening paragraph (never invented)
    md = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not md or len(md.group(1).strip()) < 20:
        body = s[s.find('<body'):]
        lead = ''
        for pat in (r'<p class="(?:lede|lead|sub|what)"[^>]*>(.*?)</p>', r'<p[^>]*>(.*?)</p>'):
            for mm in re.finditer(pat, body, re.S):
                txt = re.sub(r'\s+', ' ', re.sub('<[^>]*>', '', mm.group(1))).strip()
                if len(txt) >= 40 and '{' not in txt and '$' not in txt: lead = txt; break
            if lead: break
        if lead:
            if len(lead) > 155: lead = lead[:152].rsplit(' ', 1)[0] + '…'
            tag = '<meta name="description" content="' + E(lead) + '">'
            if md: s = s[:md.start()] + tag + s[md.end():]
            else:
                hm = re.search(r'<meta charset[^>]*>|<head[^>]*>', s)
                if hm: s = s[:hm.end()] + '\n' + tag + s[hm.end():]
    m = re.search(r'<body[^>]*>', s)
    if not m: continue
    s = s[:m.end()] + '\n' + bar + s[m.end():]
    open(p, 'w', encoding='utf-8').write(s); n += 1
print('breadcrumbs on', n, 'pages')
