"""Add Persian summaries of ideas read in full. Usage: python3 build/sakht_idea_add.py <new.json>
new.json = [{"n": 51, "s": "خلاصه…"}, …]. No author names are stored."""
import json, sys, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sp, bp = R + '/data/sakht/sakht.json', R + '/data/sakht/ideas_bodies.json'
d = json.load(open(sp, encoding='utf-8')); b = json.load(open(bp, encoding='utf-8'))
byn = {i['n']: i for i in d['ideas'] if i.get('n')}; have = {x.get('n') for x in b['items']}
k = 0
for x in json.load(open(sys.argv[1], encoding='utf-8')):
    t = byn.get(x['n'])
    if not t or not x.get('s', '').strip(): continue
    t['s'] = x['s'].strip()
    if x['n'] in have:
        for y in b['items']:
            if y.get('n') == x['n']: y['s'] = t['s']
    else: b['items'].append({'n': x['n'], 't': t['t'], 's': t['s']})
    k += 1
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
import re
ns = sum(1 for i in d['ideas'] if i.get('s'))
d['ideas_note'] = re.sub(r'برای [۰-۹]+ ایده متن کامل', f'برای {fa(ns)} ایده متن کامل', d['ideas_note'])
json.dump(d, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(b, open(bp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
todo = sorted([i for i in d['ideas'] if i.get('n') and not i.get('s')], key=lambda i: -i['v'])
print(f'added {k}; summarised {ns}/{len(d["ideas"])}; next:', [i['n'] for i in todo[:6]])
