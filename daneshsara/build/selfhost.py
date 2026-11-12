# -*- coding: utf-8 -*-
"""No third-party requests: rewrite Google Fonts links to core/fonts/fonts.css and CDN scripts to core/vendor/.
Runs after every other step (idempotent), so a page that reintroduces a third-party link is fixed at build time,
and the build fails loudly if any third-party script, stylesheet or font request is left."""
import os, re, glob, sys
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
VENDOR = {'https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js': 'core/vendor/d3.min.js'}
CSP = ('<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\' \'unsafe-inline\'; '
       'style-src \'self\' \'unsafe-inline\'; img-src \'self\' data: blob:; font-src \'self\'; connect-src \'self\'; '
       'object-src \'none\'; base-uri \'self\'; form-action \'self\'">')
n = 0; left = []
for p in sorted(glob.glob(f'{R}/**/*.html', recursive=True)):
    rel = os.path.relpath(p, R).replace(os.sep, '/')
    if rel.startswith('build/'): continue
    pre = '../' * rel.count('/')
    s = o = open(p, encoding='utf-8').read()
    s = re.sub(r'<link[^>]*rel="preconnect"[^>]*fonts\.g(?:oogleapis|static)\.com[^>]*>\s*', '', s)
    s = re.sub(r'<link[^>]*href="https://fonts\.googleapis\.com/[^"]*"[^>]*>', f'<link rel="stylesheet" href="{pre}core/fonts/fonts.css">', s)
    for u, v in VENDOR.items(): s = s.replace(f'src="{u}"', f'src="{pre}{v}"')
    if 'http-equiv="Content-Security-Policy"' not in s and 'http-equiv="refresh"' not in s:
        s = re.sub(r'(<meta charset=[^>]*>)', r'\1\n' + CSP, s, count=1, flags=re.I)
    if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
    for m in re.finditer(r'<(?:script|link|img|iframe)[^>]+(?:src|href)="(https?://[^"]+)"[^>]*>', s):
        tag = m.group(0)
        if tag.startswith('<link') and 'stylesheet' not in tag and 'preconnect' not in tag and 'font' not in tag: continue
        left.append(f'{rel}: {m.group(1)}')
    if re.search(r'@import\s+url\(["\']?https?://', s): left.append(f'{rel}: css @import')
print(f'selfhost: rewrote {n} pages; third-party requests left: {len(left)}')
if left:
    print('\n'.join(left[:20])); sys.exit(1)
