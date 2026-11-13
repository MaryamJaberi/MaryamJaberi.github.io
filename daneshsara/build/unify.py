# -*- coding: utf-8 -*-
"""One look for the whole site: map the older psychology-wiki palette and type onto the Daneshsara
design tokens by injecting a small override block into every light psy page. Idempotent."""
import glob, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
LIGHT = '--paper:#F7F4EF;--bg:#F7F4EF;--card:#FFFFFF;--wash:#F1EDE6;--ink:#1C1915;--muted:#5C574F;--rule:#E8E4DC;--link:#0A6B60;--link-bg:#E6F2F0;--accent:#0A6B60;--accent-bg:#E6F2F0;--accent-ink:#fff'
DARK = '--paper:#141210;--bg:#141210;--card:#1C1915;--wash:#25211C;--ink:#F7F4EF;--muted:#C9C3B8;--rule:#2E2A24;--link:#4FB3A6;--link-bg:#0F2E2A;--accent:#4FB3A6;--accent-bg:#0F2E2A;--accent-ink:#141210'
FONT = '--f-display:"Vazirmatn","IRANSansX",Tahoma,system-ui,sans-serif;--f-body:"Vazirmatn","IRANSansX",Tahoma,system-ui,sans-serif'
CSS = ('<style id="ds-unify">:root{' + LIGHT + ';' + FONT + '}'
       '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){' + DARK + '}}:root[data-theme="dark"]{' + DARK + '}'
       'body{font-size:17px;background:var(--paper)}'
       ':root body h1{font-size:clamp(2rem,4.6vw,3rem)!important;line-height:1.35!important;letter-spacing:0!important;font-weight:800}'
       'h2{line-height:1.5!important;font-weight:700}h3{font-weight:700}'
       '</style>')
n = skip = 0
for p in sorted(glob.glob(f'{R}/psy/**/*.html', recursive=True)):
    s = open(p, encoding='utf-8').read()
    s2 = re.sub(r'<style id="ds-unify">.*?</style>\n?', '', s, flags=re.S)
    dark = re.search(r'--(bg2|panel)\s*:', s2) is not None
    stub = 'http-equiv="refresh"' in s2[:1500] or '</body>' not in s2
    if dark or stub: skip += 1
    else:
        i = s2.rfind('</body>'); s2 = s2[:i] + CSS + '\n' + s2[i:]; n += 1
    if s2 != s: open(p, 'w', encoding='utf-8').write(s2)
print(f'unify: {n} psy pages on the shared look, {skip} skipped (dark canvases and redirects)')
