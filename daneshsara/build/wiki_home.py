# -*- coding: utf-8 -*-
"""Wiki home pages with one shared structure (the psy wiki's): python3 build/wiki_home.py [wiki ...]
<wiki>/index.html  = home: hero + stats, questions, tools, bridges, contents by city, word index
<wiki>/entries.html = the filterable entry list (build/reader.py)
Old deep links <wiki>/#slug are forwarded to entries.html#slug."""
import json, glob, os, sys, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
load = lambda p: json.load(open(p, encoding='utf-8'))
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
WIKIS = sys.argv[1:] or ['soc', 'phil', 'tabar']
NAME = {'soc': 'جامعه', 'phil': 'فلسفه', 'tabar': 'تبار و ژنتیک', 'psy': 'روان'}
VAR = {'soc': 'var(--fam-soc)', 'phil': 'var(--fam-hum)', 'tabar': 'var(--fam-bio)', 'psy': 'var(--fam-psy)'}
SIB = {'soc': ['psy', 'phil', 'tabar'], 'phil': ['psy', 'soc', 'tabar'], 'tabar': ['psy', 'soc', 'phil']}
HREF = {'psy': '../psy/', 'soc': '../soc/', 'phil': '../phil/', 'tabar': '../tabar/'}
# per-wiki extras kept from the older hand-written landing pages
XBRIDGE = {'tabar': [('https://maryamjaberi.github.io/earth-through-time/', 'زمین در گذر زمان', 'اطلس زمان: از مهبانگ تا هزار سال آینده')]}
ROADMAP = {'tabar': ['کتابخانه و بخش دانشمندان (کتاب‌ها، مقاله‌ها، زندگی‌نامهٔ پژوهشگران)',
                     'ابزارهای بصری خلاق برای مسیر مهاجرت‌ها و درخت تبار',
                     'فهرست خلأهای محتوایی برای تکمیل با داده و منبع بیشتر']}

def h1_of(p):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', open(p, encoding='utf-8').read(), re.S)
    return re.sub('<[^>]*>', '', m.group(1)).strip() if m else os.path.basename(p)

def desc_of(p):
    s = open(p, encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>.*?</h1>\s*<p[^>]*>(.*?)</p>', s, re.S)
    if not m: m = re.search(r'<meta name="description" content="([^"]*)"', s)
    return re.sub(r'\s+', ' ', re.sub('<[^>]*>', '', m.group(1))).strip()[:160] if m else ''

TPL = open(f'{HERE}/wiki_home.tpl.html', encoding='utf-8').read()

for W in WIKIS:
    cs = [load(p) for p in glob.glob(f'{R}/data/{W}/concepts/*.json')]
    by = {c['id']: c for c in cs}
    root = next((c for c in cs if c['kind'] == 'root'), None)
    entries = [c for c in cs if c['kind'] == 'concept']
    order = load(f'{R}/data/{W}/order.json') if os.path.exists(f'{R}/data/{W}/order.json') else []
    fields = [f for f in order if f in by] or [c['id'] for c in cs if c['kind'] == 'field']
    people = {p for c in cs for p in (c.get('people') or [])}
    srcs = {s for c in cs for s in (c.get('sources') or [])} | {s for c in cs for p in (c.get('points') or []) for s in (p.get('sources') or [])}
    irans = {c['iran'] for c in cs if c.get('iran')}
    xl = {}
    for c in cs:
        for l in (c.get('links') or []):
            t = l['to'].split(':')[0]
            if t != W and t in NAME: xl[t] = xl.get(t, 0) + 1
    qs = [c for c in entries if c['title']['fa'].rstrip().endswith('؟')][:12]

    stats = [(len(entries), 'مدخل'), (len(fields), 'شهر دانش'), (len(people), 'چهره'), (len(srcs), 'منبع'), (len(irans), 'دادهٔ ایران')]
    statsh = ''.join(f'<div><b>{fa(n)}</b><span>{E(l)}</span></div>' for n, l in stats)

    qsec_hide = ' hidden' if len(qs) < 3 else ''
    qh = ''.join(f'<a class="q" href=""entries.html#{E(c["id"].split(":")[1])}">{E(c["title"]["fa"])}<i>←</i></a>' for c in qs)

    tools = [p for p in sorted(glob.glob(f'{R}/{W}/tools/*.html')) if not p.endswith('index.html')]
    th = ''.join(f'<a class="tool" href="tools/{E(os.path.basename(p))}"><h3>{E(h1_of(p))}</h3><p>{E(desc_of(p))}</p><span class="go">باز کردن ←</span></a>' for p in tools)

    bh = ''.join(f'<a class="br" href="{HREF[k]}"><b>{E(NAME[k])}</b><span>{fa(v)} پیوند از این ویکی</span></a>' for k, v in sorted(xl.items(), key=lambda x: -x[1]))
    bh += ''.join(f'<a class="br" href="{E(u)}" target="_blank" rel="noopener"><b>{E(t)}</b><span>{E(d)}</span></a>' for u, t, d in XBRIDGE.get(W, []))
    rm = ROADMAP.get(W) or []
    extra = ('<section class="sec" id="roadmap"><h2 class="sh">در راه</h2><p class="sub">کارهایی که برای این ویکی مانده.</p><ul class="road">'
             + ''.join(f'<li>{E(x)}</li>' for x in rm) + '</ul></section>') if rm else ''

    secs = ''
    for fid in fields:
        f = by[fid]
        es = sorted([c for c in entries if c.get('field') == fid or c.get('parent') == fid], key=lambda c: c['title']['fa'])
        if not es: continue
        sm = (f.get('summary') or {}).get('fa', '')
        items = ''.join(f'<a href="entries.html#{E(c["id"].split(":")[1])}">{E(c["title"]["fa"])}</a>' for c in es)
        secs += f'<section class="fld"><h3>{E(f["title"]["fa"])} <small>{fa(len(es))}</small></h3>{f"<p>{E(sm)}</p>" if sm else ""}<div class="lst">{items}</div></section>'

    idx = []
    for c in entries:
        for t in [c['title']['fa']] + list(c.get('aliases') or []):
            idx.append((re.sub(r'^[«"\'\s]+', '', t), c['id'].split(':')[1]))
    idx.sort(key=lambda x: x[0])
    groups, cur = [], None
    for t, s in idx:
        k = t[0]
        if k != cur: cur = k; groups.append((k, []))
        groups[-1][1].append((t, s))
    ih = ''.join(f'<div class="ig"><b>{E(k)}</b><div>' + ''.join(f'<a href="entries.html#{E(s)}">{E(t)}</a>' for t, s in v) + '</div></div>' for k, v in groups)

    out = (TPL.replace('__W__', W).replace('__NAME__', E(NAME[W])).replace('__COLOR__', VAR[W])
        .replace('__TITLE__', E(root['title']['fa'] if root else NAME[W]))
        .replace('__LEAD__', E((root.get('summary') or {}).get('fa', '') if root else ''))
        .replace('__STATS__', statsh).replace('__QS__', qh).replace('__NQ__', fa(len(qs)))
        .replace('__TOOLS__', th).replace('__NT__', fa(len(tools)))
        .replace('__BRIDGES__', bh).replace('__NX__', fa(sum(xl.values())))
        .replace('__QHIDE__', qsec_hide).replace('__EXTRA__', extra).replace('__SECS__', secs).replace('__INDEX__', ih).replace('__NI__', fa(len(idx)))
        .replace('__SIB__', ''.join(f'<a href="{HREF[k]}">{E(NAME[k])}</a>' for k in SIB[W])))
    open(f'{R}/{W}/index.html', 'w', encoding='utf-8').write(out)
    print(W, 'home:', len(entries), 'entries,', len(fields), 'cities,', len(tools), 'tools,', len(qs), 'questions,', len(idx), 'index terms')
