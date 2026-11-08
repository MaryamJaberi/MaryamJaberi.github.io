# -*- coding: utf-8 -*-
"""Validate every data file against its schema, check cross-references, and build core/registry.json.
Exit code 1 on any error. Run from anywhere: python3 build/validate.py"""
import json, glob, os, sys, re, subprocess, datetime
from jsonschema import Draft202012Validator
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
def load(p): return json.load(open(p, encoding='utf-8'))
S = {k: Draft202012Validator(load(f'{R}/core/schema/{k}.schema.json')) for k in ['concept', 'field', 'bridge', 'person', 'source', 'iran']}
errors = []
def check(v, obj, where):
    for e in sorted(v.iter_errors(obj), key=str):
        errors.append(f'{where}: {"/".join(map(str, e.path))}: {e.message[:140]}')

people = load(f'{R}/core/people.json'); sources = load(f'{R}/core/sources.json')
for k, p in people.items(): check(S['person'], p, f'people:{k}')
for k, s in sources.items(): check(S['source'], s, f'sources:{k}')
atlas = load(f'{R}/atlas/fields.json'); fields = {f['id']: f for f in atlas['fields']}
for f in atlas['fields']:
    check(S['field'], f, f'field:{f["id"]}')
    for p in f.get('par', []):
        if p not in fields: errors.append(f'field:{f["id"]}: parent {p} missing')
bridges = {}
for p in glob.glob(f'{R}/atlas/bridges/*.json'):
    b = load(p); bridges[b['id']] = b; check(S['bridge'], b, f'bridge:{b["id"]}')
    if b['field'] not in fields: errors.append(f'bridge:{b["id"]}: field {b["field"]} missing')
concepts = {}
for wiki in ['psy', 'soc', 'tabar', 'phil']:
    for p in glob.glob(f'{R}/data/{wiki}/concepts/*.json'):
        c = load(p); concepts[c['id']] = c; check(S['concept'], c, c['id'])
        if not c['id'].startswith(wiki + ':'): errors.append(f'{c["id"]}: wrong prefix for folder {wiki}')
irans = {}
for p in glob.glob(f'{R}/iran/*.json'):
    i = load(p); irans[i['id']] = i; check(S['iran'], i, i['id'])
# cross references
redirects = load(f'{R}/core/redirects.json') if os.path.exists(f'{R}/core/redirects.json') else {}
known = set(concepts) | set(people) | set(sources) | set(irans) | {'atlas:' + k for k in fields}
titles = {}
for c in concepts.values():
    for l in c.get('links', []):
        if l['to'] not in concepts and l['to'] not in redirects: errors.append(f'{c["id"]}: link to unknown {l["to"]}')
    for pid in c.get('people', []):
        if pid not in people: errors.append(f'{c["id"]}: unknown person {pid}')
    for sid in c.get('sources', []):
        if sid not in sources: errors.append(f'{c["id"]}: unknown source {sid}')
    if c.get('parent') and c['parent'] not in concepts: errors.append(f'{c["id"]}: unknown parent {c["parent"]}')
    if c.get('iran') and c['iran'] not in irans: errors.append(f'{c["id"]}: unknown iran note {c["iran"]}')
    if c['status'] != 'draft' and c['kind'] == 'concept' and not c.get('sources'):
        errors.append(f'{c["id"]}: status {c["status"]} but no sources')
    t = c['title']['fa']
    if t in titles and not any(l['rel'] == 'same-as' for l in c.get('links', [])):
        errors.append(f'{c["id"]}: duplicate Persian title with {titles[t]} (add same-as)')
    titles.setdefault(t, c['id'])
for b in bridges.values():
    for w, ids in b.get('concepts', {}).items():
        for cid in ids:
            if cid not in concepts: errors.append(f'bridge:{b["id"]}: unknown concept {cid}')
# registry
def url_of(cid):
    w, slug = cid.split(':', 1)
    if w == 'atlas': return f'atlas/#{slug}'
    if w == 'iran': return f'iran/#{slug}'
    if w == 'core': return f'core/people.html#{slug}'
    if w == 'src': return f'core/sources.html#{slug}'
    return f'{w}/graph.html#{slug}'
reg = {}
for c in concepts.values():
    reg[c['id']] = {'wiki': c['id'].split(':')[0], 'type': c['kind'], 'title': c['title'], 'url': url_of(c['id']), 'status': c['status'], 'wikidata': c.get('wikidata')}
for f in fields.values():
    reg['atlas:' + f['id']] = {'wiki': 'atlas', 'type': 'bridge' if f.get('b') else 'field', 'title': {'fa': f['fa'], 'en': f.get('en'), 'nl': f.get('nl')}, 'url': url_of('atlas:' + f['id']), 'status': 'reviewed', 'wikis': f.get('wikis', [])}
for i in irans.values():
    reg[i['id']] = {'wiki': 'iran', 'type': 'iran', 'title': i['question'], 'url': url_of(i['id']), 'grade': i['grade']}
for p in people.values():
    reg[p['id']] = {'wiki': 'core', 'type': 'person', 'title': p['name'], 'url': url_of(p['id']), 'wikis': p.get('wikis', [])}
stats = {
    'concepts': len(concepts), 'concepts_with_sources': sum(1 for c in concepts.values() if c.get('sources')),
    'cross_wiki_links': sum(1 for c in concepts.values() for l in c.get('links', []) if l['to'].split(':')[0] != c['id'].split(':')[0]),
    'bridge_links': sum(len(v) for b in bridges.values() for v in b.get('concepts', {}).values()),
    'iran_notes': len(irans), 'fields': len(fields), 'bridges': len(bridges), 'people': len(people), 'sources': len(sources),
    'built': datetime.date.today().isoformat(),
}
json.dump({'stats': stats, 'entries': reg}, open(f'{R}/core/registry.json', 'w'), ensure_ascii=False, indent=0)
for e in errors[:60]: print('ERR', e)
print('registry', len(reg), 'entries;', json.dumps(stats, ensure_ascii=False))
print(f'{len(errors)} errors')
sys.exit(1 if errors else 0)
