# -*- coding: utf-8 -*-
"""Compact data bundle for the interactive tools: core/tools/data.json (+ lib.js is hand-written)."""
import json, glob, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
L = lambda p: json.load(open(p, encoding='utf-8'))
src = L(f'{R}/core/sources.json'); reg = L(f'{R}/core/registry.json')['entries']
con = []; fields = {}
for p in sorted(glob.glob(f'{R}/data/*/concepts/*.json')):
    c = L(p); w = c['id'].split(':')[0]
    if c['kind'] == 'subfield' or c['kind'] == 'field':
        fields[c['id']] = {'id': c['id'], 'w': w, 't': c['title'], 'parent': c.get('parent')}
        continue
    pts = []
    for q in c.get('points', []):
        ts = [src[s]['tier'] for s in q.get('sources', []) if s in src]
        pts.append({'t': q['text'].get('fa', ''), 'e': q['text'].get('en', ''), 'f': q.get('flags', []), 'tier': min(ts) if ts else 0, 'n': len(ts)})
    con.append({'id': c['id'], 'w': w, 'field': c.get('field'), 't': c['title'], 'al': c.get('aliases', []), 's': c.get('summary', {}),
                'st': c.get('status'), 'pts': pts, 'lk': [[l['to'], l['rel']] for l in c.get('links', [])], 'u': reg.get(c['id'], {}).get('url'), 'ir': c.get('iran'), 'np': len(c.get('people', []))})
for fid, f in list(fields.items()):
    pass
for k, v in reg.items():
    if v.get('type') in ('field', 'subfield') and k not in fields:
        fields[k] = {'id': k, 'w': v['wiki'], 't': v['title'], 'parent': None}
iran = []
for p in sorted(glob.glob(f'{R}/iran/*.json')):
    n = L(p)
    if isinstance(n, dict) and 'question' in n:
        iran.append({'id': n['id'], 'domain': n.get('domain'), 'q': n['question'], 'f': n.get('finding', {}), 'year': n.get('year'), 'grade': n.get('grade'), 'method': n.get('method'), 'contested': bool(n.get('contested'))})
br = []
for p in sorted(glob.glob(f'{R}/atlas/bridges/*.json')):
    b = L(p); br.append({'id': b['id'], 'between': b.get('between', []), 't': b['title'], 'q': b.get('question', {})})
af = L(f'{R}/atlas/fields.json')
out = {'concepts': con, 'fields': list(fields.values()), 'iran': iran, 'bridges': br, 'atlas': af, 'wikis': {'psy': 'روان', 'soc': 'جامعه', 'phil': 'فلسفه', 'tabar': 'تبار', 'tarikh': 'تاریخ'}, 'tiers': {'1': 'فراتحلیل/تکرار', '2': 'مقالهٔ داوری‌شده/آمار رسمی', '3': 'کتاب یا سخنرانی', '4': 'سرنخ', '0': 'بی‌منبع'}}
os.makedirs(f'{R}/core/tools', exist_ok=True)
json.dump(out, open(f'{R}/core/tools/data.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('tools data', len(con), 'concepts', len(fields), 'fields', len(iran), 'iran', len(br), 'bridges', os.path.getsize(f'{R}/core/tools/data.json') // 1024, 'KB')
