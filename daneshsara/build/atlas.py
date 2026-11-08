# -*- coding: utf-8 -*-
"""Build the shared atlas: atlas/fields.json (52 existing + 25 new) and atlas/bridges/*.json.
Also writes an extended atlas2.data.js for the visual atlas tool (path given as argv[2])."""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = HERE + '/..'
RAW = json.load(open(sys.argv[1]))
sys.path.insert(0, HERE)
from new_fields import NEW
F = RAW['F']; FAM = RAW['FAM']
existing = {f['id'] for f in F}
fields = []
for f in F:
    g = dict(f); g.setdefault('wikis', ['psy']); fields.append(g)
# concepts in the other wikis that each bridge connects (added phase 2/3)
XC = {
 'crosscult': {'soc': ['soc:value-change'], 'phil': ['phil:knobe-effect']},
 'commpsy': {'soc': ['soc:social-capital', 'soc:collective-action']},
 'psygen': {'tabar': ['tabar:gwas-polygenic', 'tabar:heritability', 'tabar:twin-adoption']},
 'evopsychiatry': {'tabar': ['tabar:social-brain-evolution']},
 'evomed': {'tabar': ['tabar:lactase-gene-culture', 'tabar:neanderthal-admixture']},
 'cogarch': {'tabar': ['tabar:out-of-africa', 'tabar:social-brain-evolution']},
 'sociobio': {'tabar': ['tabar:social-brain-evolution'], 'phil': ['phil:three-theories']},
 'sociogenomics': {'tabar': ['tabar:gwas-polygenic', 'tabar:nature-of-nurture'], 'soc': ['soc:mobility', 'soc:gini-inequality']},
 'biosocial': {'tabar': ['tabar:gene-environment', 'tabar:epigenetic-marks'], 'soc': ['soc:inequality-health']},
 'cultevo': {'tabar': ['tabar:social-brain-evolution', 'tabar:lactase-gene-culture'], 'soc': ['soc:protestant-ethic', 'soc:weak-ties']},
 'geneculture': {'tabar': ['tabar:lactase-gene-culture', 'tabar:consanguinity'], 'soc': ['soc:protestant-ethic']},
 'hbe': {'tabar': ['tabar:social-brain-evolution'], 'soc': ['soc:migration-theories']},
 'archaeogen': {'tabar': ['tabar:ancient-dna', 'tabar:zagros-neolithic', 'tabar:steppe-indo-iranian', 'tabar:iranian-genetic-diversity', 'tabar:haplogroups']},
 'xphi': {'phil': ['phil:knobe-effect', 'phil:gettier', 'phil:trolley', 'phil:free-will']},
 'embodied': {'phil': ['phil:hard-problem', 'phil:flying-man']},
 'philsocsci': {'phil': ['phil:paradigms', 'phil:falsification'], 'soc': ['soc:social-construction', 'soc:sociological-imagination']},
 'socknow': {'soc': ['soc:social-construction'], 'phil': ['phil:paradigms', 'phil:epistemic-injustice']},
 'socepist': {'phil': ['phil:epistemic-injustice', 'phil:gettier'], 'soc': ['soc:preference-falsification', 'soc:network-society']},
 'crittheory': {'soc': ['soc:social-movements', 'soc:institutions-inclusive'], 'phil': ['phil:two-liberties', 'phil:veil-of-ignorance']},
 'sts': {'phil': ['phil:paradigms', 'phil:falsification'], 'soc': ['soc:social-construction']},
 'philbio': {'tabar': ['tabar:heritability', 'tabar:race-biology'], 'phil': ['phil:falsification']},
 'evoethics': {'phil': ['phil:trolley', 'phil:three-theories', 'phil:moral-luck'], 'tabar': ['tabar:social-brain-evolution']},
 'genethics': {'tabar': ['tabar:eugenics', 'tabar:thalassemia-screening', 'tabar:ancestry-tests', 'tabar:genetic-essentialism'], 'phil': ['phil:capabilities']},
 'anthroethics': {'phil': ['phil:three-theories', 'phil:stoicism'], 'soc': ['soc:presentation-of-self']},
 'bighistory': {'tabar': ['tabar:out-of-africa', 'tabar:ancient-dna'], 'soc': ['soc:institutions-inclusive']},
}
BR = {}
for n in NEW:
    assert n['id'] not in existing, n['id']
    for p in n['par']:
        assert p in existing, (n['id'], p)
    b = n.pop('bridge')
    f = dict(n); f['b'] = True; f['bridge'] = n['id']; f.setdefault('aud', ['stu'])
    fields.append(f)
    BR[n['id']] = {
        'id': n['id'], 'field': n['id'], 'between': n['par'],
        'title': {'fa': n['fa'], 'en': n['en'], 'nl': n['nl']},
        'question': {'fa': n['q'], 'en': b['question_en']},
        'definition': {'fa': b['definition']},
        'landmark': {'fa': b['landmark'], 'url': b['landmark_url']},
        'reference': {'fa': b['reference']},
        'venue': {'fa': b['venue']},
        'people': n['ppl'],
        'finding': {'fa': b['finding'], 'replication': b['replication'], 'url': b['finding_url']},
        'persian': [{'title': t, 'publisher': p, 'url': u, 'verified': v} for (t, p, u, v) in b['persian']],
        'concepts': {'psy': ['psy:' + g for g in n.get('g', [])], **XC.get(n['id'], {})},
        'iran': {'fa': b['iran']} if b['iran'] else {},
        'status': 'established' if n['id'] not in ('sociogenomics',) else 'emerging',
        'review': 'draft',
    }
json.dump({'fam': FAM, 'fields': fields}, open(OUT + '/atlas/fields.json', 'w'), ensure_ascii=False, indent=1)
os.makedirs(OUT + '/atlas/bridges', exist_ok=True)
for k, v in BR.items():
    json.dump(v, open(f'{OUT}/atlas/bridges/{k}.json', 'w'), ensure_ascii=False, indent=1)
json.dump(BR, open(OUT + '/atlas/bridges.json', 'w'), ensure_ascii=False, indent=1)
# extended data file for the visual tool
if len(sys.argv) > 2:
    tool = [{k: v for k, v in f.items() if k in ('id', 'b', 'par', 'fam', 'fa', 'en', 'q', 's', 'm', 'jobs', 'study', 'ppl', 'wiki', 'g', 'aud', 'subs', 'bridge', 'wikis')} for f in fields]
    js = 'window.FAM=' + json.dumps(FAM, ensure_ascii=False) + ';\nwindow.F=' + json.dumps(tool, ensure_ascii=False) + ';\n'
    open(sys.argv[2], 'w').write(js)
print('fields', len(fields), 'bridges', len(BR))
