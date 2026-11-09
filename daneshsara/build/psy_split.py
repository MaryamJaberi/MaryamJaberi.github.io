# -*- coding: utf-8 -*-
"""One-time: give the flat psy wiki a real folder structure and move the separate
product out of it, keeping every old URL alive with a redirect stub."""
import os, re, glob, html, subprocess, json
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.chdir(R)
TOOLS = {'atlas2','body','debate','effect','emotions','evidence','graph','guess','heat','lab','land',
         'learn','library','lineage','path','prism','river','scales','timeline'}
def dest(n):
    if n in TOOLS: return f'psy/tools/{n}.html'
    if re.fullmatch(r's\d+', n): return f'psy/lessons/{n}.html'
    if n == 'orgsvc': return f'wellbeing/{n}.html'   # the product, not wiki content
    return f'psy/topics/{n}.html'

MOVES = {}
for p in sorted(glob.glob('psy/*.html')):
    n = os.path.splitext(os.path.basename(p))[0]
    if n == 'index': continue
    MOVES[p] = dest(n)
for d in {os.path.dirname(v) for v in MOVES.values()}: os.makedirs(d, exist_ok=True)

ALLFILES = [p for p in glob.glob('**/*.html', recursive=True) + glob.glob('**/*.js', recursive=True) + glob.glob('**/*.json', recursive=True)
            if not p.startswith('build/')]

def rewrite_links(text, from_old, from_new):
    """Repoint every relative link so it still resolves after the move."""
    base_old, base_new = os.path.dirname(from_old), os.path.dirname(from_new)
    def fix(m):
        attr, q, url = m.group(1), m.group(2), m.group(3)
        if re.match(r'(https?:|mailto:|tel:|javascript:|data:|#|/)', url) or '${' in url or '{{' in url:
            return m.group(0)
        path, frag = (url.split('#', 1) + [''])[:2]
        if not path: return m.group(0)
        target = os.path.normpath(os.path.join(base_old, path))
        target = MOVES.get(target, target)                     # follow the move, if any
        new = os.path.relpath(target, base_new or '.').replace(os.sep, '/')
        if path.endswith('/') and not new.endswith('/'): new += '/'
        return f'{attr}={q}{new}{"#" + frag if frag else ""}{q}'
    return re.sub(r'(?<![-\w])(href|src)=(["\'])([^"\']*)\2', fix, text)

# 1. move the files, fixing their own relative links for the new depth
for old, new in MOVES.items():
    s = open(old, encoding='utf-8').read()
    open(new, 'w', encoding='utf-8').write(rewrite_links(s, old, new))
    os.remove(old)
print('moved', len(MOVES), 'pages')

# 2. repoint every other file that linked to them
n = 0
for p in ALLFILES:
    if p in MOVES or not os.path.exists(p): continue
    s = open(p, encoding='utf-8', errors='ignore').read()
    if p.endswith('.html'):
        t = rewrite_links(s, p, p)
    else:  # js / json: plain string paths like "psy/habits.html" or "habits.html"
        t = s
        for old, new in MOVES.items():
            ob, nb = os.path.basename(old), new
            t = t.replace('"' + old + '"', '"' + new + '"').replace("'" + old + "'", "'" + new + "'")
            t = t.replace('"../' + old + '"', '"../' + new + '"')
    if t != s: open(p, 'w', encoding='utf-8').write(t); n += 1
print('rewrote links in', n, 'files')

# 3. a redirect stub at every old URL, so nothing anyone saved breaks
STUB = ('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">'
        '<meta name="robots" content="noindex"><link rel="canonical" href="__U__">'
        '<meta http-equiv="refresh" content="0; url=__U__"><title>__T__</title>'
        '<meta name="description" content="این صفحه جابه‌جا شده است.">'
        '<style>body{font:16px/1.8 system-ui;margin:0;padding:40px;text-align:center}a{color:#0a6b60}</style></head>'
        '<body><p>این صفحه جابه‌جا شده است.</p><p><a href="__U__">__T__</a></p>'
        '<script>location.replace("__U__");</script></body></html>')
for old, new in MOVES.items():
    url = os.path.relpath(new, os.path.dirname(old)).replace(os.sep, '/')
    t = re.search(r'<title>(.*?)</title>', open(new, encoding='utf-8').read(), re.S)
    title = html.escape(re.sub('<[^>]*>', '', t.group(1)).strip()) if t else 'ادامه'
    open(old, 'w', encoding='utf-8').write(STUB.replace('__U__', html.escape(url)).replace('__T__', title))
print('redirect stubs:', len(MOVES))
