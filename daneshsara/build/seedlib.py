# -*- coding: utf-8 -*-
"""Shared helpers for seeding a wiki on the core (used by soc_seed.py, phil_seed.py).
Everything written is status 'draft' until reviewed. People/sources are added to core additively."""
import json, os, re, hashlib
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')

class Seed:
    def __init__(self, wiki):
        self.W = wiki
        self.people = self._load(f'{R}/core/people.json', {}); self.sources = self._load(f'{R}/core/sources.json', {})
        self.C = []; self.IRAN = []; self.fields = []
    @staticmethod
    def _load(p, d): return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else d
    def src(self, cite, tier=1, url=None):
        year = re.search(r'\((\d{4})\)', cite); year = int(year.group(1)) if year else None
        for k, v in self.sources.items():
            if v['cite'] == cite:
                if self.W not in v['wikis']: v['wikis'].append(self.W)
                if url and not v.get('url'): v['url'] = url
                return k
        sid = 'src:' + hashlib.md5(cite.encode()).hexdigest()[:10]
        self.sources[sid] = {'id': sid, 'cite': cite, 'year': year, 'tier': tier, 'wikis': [self.W]}
        if url: self.sources[sid]['url'] = url
        return sid
    def person(self, latin, fa, years='', note=''):
        pid = 'core:' + re.sub(r'[^a-z0-9]+', '-', latin.lower()).strip('-')
        if pid not in self.people:
            self.people[pid] = {'id': pid, 'name': {'fa': fa, 'en': latin, 'nl': latin}, 'years': years, 'note': {'fa': note}, 'wikidata': None, 'wikis': []}
        if self.W not in self.people[pid]['wikis']: self.people[pid]['wikis'].append(self.W)
        return pid
    @staticmethod
    def t(fa, en, nl=None): return {'fa': fa, 'en': en, 'nl': nl or en}
    def pt(self, fa, en, srcs, flags=()): return {'text': self.t(fa, en), 'sources': list(srcs), 'flags': list(flags)}
    def ln(self, to, rel, fa, en): return {'to': to, 'rel': rel, 'note': self.t(fa, en)}
    def add(self, id, kind, title, summary, parent=None, field=None, points=(), links=(), people=(), iran=None, origin=None, aliases=(), wikidata=None):
        srcs = sorted({s for p in points for s in p['sources']})
        W = self.W
        self.C.append({'id': f'{W}:{id}', 'kind': kind, 'title': title, 'aliases': list(aliases), 'parent': parent and f'{W}:{parent}', 'field': field and f'{W}:{field}',
                       'summary': summary, 'points': list(points), 'links': list(links), 'people': list(people), 'sources': srcs, 'booklets': [],
                       'origin': origin, 'iran': iran, 'wikidata': wikidata, 'status': 'draft'})
        if kind == 'field': self.fields.append(f'{W}:{id}')
    def iran(self, id, question, finding, year, method, grade, sources, concepts, capability, contested=False, critique=None, fields=()):
        note = {'id': f'iran:{id}', 'domain': self.W, 'question': question, 'finding': finding, 'year': year, 'method': method, 'grade': grade,
                'contested': contested, 'source': [{'title': self.sources[s]['cite'], 'url': self.sources[s].get('url', '')} for s in sources],
                'fields': list(fields), 'concepts': concepts, 'capability': capability}
        if critique: note['critique'] = critique
        self.IRAN.append(note)
    def write(self):
        W = self.W
        os.makedirs(f'{R}/data/{W}/concepts', exist_ok=True); os.makedirs(f'{R}/iran', exist_ok=True)
        for c in self.C:
            json.dump(c, open(f"{R}/data/{W}/concepts/{c['id'].split(':')[1]}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        for i in self.IRAN:
            json.dump(i, open(f"{R}/iran/{i['id'].split(':')[1]}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        json.dump(self.fields, open(f'{R}/data/{W}/order.json', 'w'), ensure_ascii=False)
        json.dump(self.people, open(f'{R}/core/people.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        json.dump(self.sources, open(f'{R}/core/sources.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(W, 'concepts', len(self.C), 'iran notes', len(self.IRAN), 'people', len(self.people), 'sources', len(self.sources))
