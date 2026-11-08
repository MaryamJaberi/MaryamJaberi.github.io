# -*- coding: utf-8 -*-
"""Align core/people.json with Wikidata (needs internet; run locally or via the align-wikidata workflow).
For every person without a QID: search by English name, keep the first result whose description looks like a
scholar, and store {qid, label, description} in core/wikidata_review.json for a human to check; set people[pid].wikidata."""
import json, os, re, sys, time, urllib.request, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
people = json.load(open(f'{R}/core/people.json', encoding='utf-8'))
rev_path = f'{R}/core/wikidata_review.json'
review = json.load(open(rev_path, encoding='utf-8')) if os.path.exists(rev_path) else {}
KEY = re.compile(r'psycholog|philosoph|sociolog|genetic|scientist|econom|anthropolog|neuro|physician|psychiatr|biolog|historian|writer|academic|professor|researcher|statistic|mathematic|linguist|archaeolog|theolog|educator|physiolog|primatolog|demograph|political|journalist|author|poet|polymath|thinker|logician', re.I)
UA = {'User-Agent': 'Daneshsara/0.1 (https://maryamjaberi.github.io/daneshsara/; wikidata alignment script)'}
def search(q):
    url = 'https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbsearchentities', 'search': q, 'language': 'en', 'format': 'json', 'limit': 5, 'type': 'item'})
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return json.load(r).get('search', [])
done = 0; limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
for pid, p in people.items():
    if p.get('wikidata') or pid in review: continue
    name = (p['name'].get('en') or '').strip()
    if not name or re.search(r'[؀-ۿ]', name) or len(name) < 4: continue
    try:
        hits = search(name)
    except Exception as e:
        print('ERR', pid, e); time.sleep(2); continue
    pick = next((h for h in hits if KEY.search(h.get('description', ''))), None)
    review[pid] = {'name': name, 'qid': pick['id'] if pick else None, 'label': pick.get('label') if pick else None, 'description': pick.get('description') if pick else None,
                   'candidates': [{'qid': h['id'], 'label': h.get('label'), 'description': h.get('description')} for h in hits[:3]], 'status': 'auto' if pick else 'none'}
    if pick: p['wikidata'] = pick['id']
    done += 1; time.sleep(0.25)
    if done >= limit: break
json.dump(review, open(rev_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(people, open(f'{R}/core/people.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
matched = sum(1 for v in review.values() if v['qid'])
print('searched', done, '| reviewed total', len(review), '| matched', matched, '| people with QID', sum(1 for p in people.values() if p.get('wikidata')))
