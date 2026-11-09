# -*- coding: utf-8 -*-
"""Wiki home pages, one shared structure for every wiki: python3 build/wiki_home.py [wiki ...]
Wikis: soc phil tabar (data/<w>/concepts)  |  miyan (atlas/bridges)  |  iran (iran/*.json)  |  simorgh (shell only)
<wiki>/index.html = home; the entry list stays where it already lives."""
import json, glob, os, sys, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
load = lambda p: json.load(open(p, encoding='utf-8'))
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
NAME = {'soc': 'جامعه', 'phil': 'فلسفه', 'tabar': 'تبار و ژنتیک', 'psy': 'روان', 'miyan': 'ارتباط رشته‌ها', 'iran': 'ایران', 'simorgh': 'سیمرغ'}
VAR = {'soc': 'var(--fam-soc)', 'phil': 'var(--fam-hum)', 'tabar': 'var(--fam-bio)', 'psy': 'var(--fam-psy)',
       'miyan': 'var(--fam-formal)', 'iran': 'var(--primary)', 'simorgh': '#b7791f'}
BASE = ['psy', 'soc', 'tabar', 'phil']
ALL = BASE + ['miyan', 'iran', 'simorgh']
HREF = {k: f'../{k}/' for k in ALL}

def h1_of(p):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', open(p, encoding='utf-8').read(), re.S)
    return re.sub('<[^>]*>', '', m.group(1)).strip() if m else os.path.basename(p)
def desc_of(p):
    s = open(p, encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>.*?</h1>\s*<p[^>]*>(.*?)</p>', s, re.S) or re.search(r'<meta name="description" content="([^"]*)"', s)
    return re.sub(r'\s+', ' ', re.sub('<[^>]*>', '', m.group(1))).strip()[:160] if m else ''
def tools_from(folder, base):
    out = []
    for p in sorted(glob.glob(f'{R}/{folder}/*.html')):
        if p.endswith('index.html'): continue
        out.append((base + os.path.basename(p), h1_of(p), desc_of(p)))
    return out

# ---------- spec builders: each returns the same shape ----------
def spec_base(W):
    cs = [load(p) for p in glob.glob(f'{R}/data/{W}/concepts/*.json')]
    by = {c['id']: c for c in cs}
    root = next((c for c in cs if c['kind'] == 'root'), None)
    entries = [c for c in cs if c['kind'] == 'concept']
    order = load(f'{R}/data/{W}/order.json') if os.path.exists(f'{R}/data/{W}/order.json') else []
    fids = [f for f in order if f in by] or [c['id'] for c in cs if c['kind'] == 'field']
    people = {p for c in cs for p in (c.get('people') or [])}
    srcs = {s for c in cs for s in (c.get('sources') or [])} | {s for c in cs for p in (c.get('points') or []) for s in (p.get('sources') or [])}
    irans = {c['iran'] for c in cs if c.get('iran')}
    xl = {}
    for c in cs:
        for l in (c.get('links') or []):
            t = l['to'].split(':')[0]
            if t != W and t in NAME: xl[t] = xl.get(t, 0) + 1
    url = lambda c: 'entries.html#' + c['id'].split(':')[1]
    fields = []
    for fid in fids:
        es = sorted([c for c in entries if c.get('field') == fid or c.get('parent') == fid], key=lambda c: c['title']['fa'])
        if es: fields.append((by[fid]['title']['fa'], (by[fid].get('summary') or {}).get('fa', ''), [(c['title']['fa'], url(c)) for c in es]))
    idx = [(t, url(c)) for c in entries for t in [c['title']['fa']] + list(c.get('aliases') or [])]
    return dict(title=root['title']['fa'] if root else NAME[W], lead=(root.get('summary') or {}).get('fa', '') if root else '',
        entriesurl='entries.html', entrieslabel='همهٔ مدخل‌ها',
        stats=[(len(entries), 'مدخل'), (len(fields), 'شهر دانش'), (len(people), 'چهره'), (len(srcs), 'منبع'), (len(irans), 'دادهٔ ایران')],
        questions=[(c['title']['fa'], url(c)) for c in entries if c['title']['fa'].rstrip().endswith('؟')][:12],
        qlead='هر کدام یک مدخل است با خلاصه، نکته‌ها، منبع و پیوند به ویکی‌های دیگر.',
        tools=tools_from(f'{W}/tools', 'tools/'), bridges=[(HREF[k], NAME[k], f'{fa(v)} پیوند از این ویکی') for k, v in sorted(xl.items(), key=lambda x: -x[1])],
        bridgelead=f'{fa(sum(xl.values()))} پیوند از مدخل‌های این ویکی به ویکی‌های دیگر دانش‌سرا می‌رود.',
        fields=fields, fieldslead='مدخل‌ها به تفکیک شهرهای دانش این سرزمین.', index=idx, roadmap=[])

def spec_miyan():
    bs = load(f'{R}/atlas/bridges.json'); fl = load(f'{R}/atlas/fields.json')
    famname = {f['id']: f['fa'] for f in fl['fam']}
    fldfam = {f['id']: f.get('fam') for f in fl['fields']}
    B = sorted(bs.values(), key=lambda b: b['title']['fa'])
    url = lambda b: '../atlas/bridge.html#' + b['id']
    people = {p for b in B for p in (b.get('people') or [])}
    nref = sum(1 for b in B if b.get('reference'))
    nfa = sum(len(b.get('persian') or []) for b in B)
    nir = sum(1 for b in B if b.get('iran'))
    xl = {}
    for b in B:
        for k, v in (b.get('concepts') or {}).items():
            if k in NAME: xl[k] = xl.get(k, 0) + len(v)
    def pair(b):
        fams = sorted({fldfam.get(d) for d in b.get('between', []) if fldfam.get(d)}, key=lambda x: list(famname).index(x))
        if not fams: return 'سایر'
        return ('درون ' + famname[fams[0]]) if len(fams) == 1 else ' ↔ '.join(famname[f] for f in fams)
    grp = {}
    for b in B: grp.setdefault(pair(b), []).append(b)
    fields = [(k, '', [(b['title']['fa'], url(b)) for b in v]) for k, v in sorted(grp.items(), key=lambda x: -len(x[1]))]
    return dict(title='ارتباط رشته‌ها', entriesurl='../atlas/bridge.html', entrieslabel='همهٔ پل‌ها',
        lead='جایی که دو علم به هم می‌رسند، رشتهٔ تازه‌ای زاده می‌شود. این ویکی همان مرزها را می‌گیرد: روان‌شناسی بین‌فرهنگی، ژنتیک جامعه‌شناختی، باستان‌ژنتیک، فلسفهٔ تجربی و باقی. هر پل یک پرسش دارد، یک تعریف، نشانهٔ تاریخی‌اش، یافتهٔ محکمش، منبع فارسی اگر باشد، و پیوند به مفهوم‌های دو طرف.',
        stats=[(len(B), 'پل'), (len(fields), 'خانوادهٔ دانش'), (len(people), 'چهره'), (nref, 'منبع مرجع'), (nfa, 'منبع فارسی'), (nir, 'یادداشت ایران')],
        questions=[(b['question']['fa'], url(b)) for b in B if b.get('question', {}).get('fa')][:12],
        qlead='هر پل با یک پرسش شروع می‌شود؛ پرسشی که هیچ‌کدام از دو رشته به‌تنهایی جوابش را ندارد.',
        tools=tools_from('atlas/tools', '../atlas/tools/') + [('../atlas/', 'اطلس رشته‌ها', '۷۷ رشته در پنج خانواده، با پرسش و خلاصهٔ هرکدام.'), ('../atlas/world.html', 'جهان دانش', 'نقشهٔ زوم‌پذیر سرزمین‌ها، شهرها و راه‌های میان‌رشته‌ای.')],
        bridges=[(HREF[k], NAME[k], f'{fa(v)} مفهوم از این ویکی در پل‌ها') for k, v in sorted(xl.items(), key=lambda x: -x[1])],
        bridgelead='پل‌ها به مفهوم‌های هر دو طرف وصل‌اند؛ این‌ها شمار مفهوم‌هایی است که از هر ویکی در پل‌ها آمده.',
        fields=fields, fieldslead='پل‌ها به تفکیک خانوادهٔ دانشی که از آن می‌آیند.',
        index=[(b['title']['fa'], url(b)) for b in B], roadmap=[])

def spec_iran():
    ns = sorted((load(p) for p in glob.glob(f'{R}/iran/*.json')), key=lambda n: n['question']['fa'])
    url = lambda n: 'entries.html#' + n['id'].split(':')[1]
    doms = {'psy': 'روان', 'soc': 'جامعه', 'tabar': 'تبار و ژنتیک', 'phil': 'فلسفه'}
    srcs = sum(len(n.get('source') or []) for n in ns)
    nviz = sum(1 for n in ns if (n.get('viz') or {}).get('kind') not in (None, 'none'))
    cx = {}
    for n in ns:
        for c in (n.get('concepts') or []):
            k = c.split(':')[0]
            if k in NAME: cx[k] = cx.get(k, 0) + 1
    fields = []
    for d, dn in doms.items():
        es = [n for n in ns if n['domain'] == d]
        if es: fields.append((dn, '', [(n['question']['fa'], url(n)) for n in es]))
    return dict(title='ایران', entriesurl='entries.html', entrieslabel='همهٔ یادداشت‌ها',
        lead='همان مفهوم‌هایی که در ویکی‌های دیگر خوانده‌اید، این بار در ایران: عدد و آمار واقعی، ریشه‌یابی اینکه چه شد که این‌طور شد، و شرح وضع موجود. هر عدد با سال، روش، ردهٔ کیفیت از A تا D و منبع اصلی می‌آید؛ جایی که داده‌ای نیست، نبودنش نوشته شده.',
        stats=[(len(ns), 'یادداشت'), (len(fields), 'حوزه'), (nviz, 'نمودار'), (srcs, 'منبع'), (sum(1 for n in ns if n.get('contested')), 'یافتهٔ مورد مناقشه')],
        questions=[(n['question']['fa'], url(n)) for n in ns][:12],
        qlead='هر یادداشت یک پرسش دربارهٔ ایران است که با دادهٔ واقعی جواب داده می‌شود.',
        tools=tools_from('iran/tools', 'tools/'),
        bridges=[(HREF[k], NAME[k], f'{fa(v)} مفهوم از این ویکی') for k, v in sorted(cx.items(), key=lambda x: -x[1])],
        bridgelead='هر یادداشت به مفهوم‌هایی وصل است که آن را توضیح می‌دهند؛ این‌ها شمار مفهوم‌های هر ویکی در این لایه است.',
        fields=fields, fieldslead='یادداشت‌ها به تفکیک حوزهٔ دانشی که به آن می‌پردازند.',
        index=[(n['question']['fa'], url(n)) for n in ns], roadmap=[
            'ریشه‌یابی و شرح وضع موجود برای هر یادداشت، به‌صورت بخش جدا',
            'یادداشت تازه برای حوزه‌هایی که هنوز دادهٔ ایرانی ندارند (فلسفه هیچ یادداشتی ندارد)',
            'سری زمانی برای یادداشت‌هایی که فعلاً فقط یک عدد دارند'])

def spec_simorgh():
    return dict(title='سیمرغ', entriesurl='', entrieslabel='',
        lead='آخرین لایهٔ دانش‌سرا: آنچه در لایهٔ علم فهمیده‌ایم و در لایهٔ ایران سنجیده‌ایم، اینجا به یک تمثیل، یک راه‌حل و یک بازی تبدیل می‌شود — ابزارها و وسایلی برای آزادی و آیندهٔ ایران. این ویکی هنوز محتوایی ندارد؛ این صفحه جای خالی‌اش را نگه می‌دارد و می‌گوید چه چیزی باید در آن بیاید.',
        stats=[(0, 'مدخل'), (0, 'ابزار'), (3, 'بخش برنامه‌ریزی‌شده')],
        questions=[], qlead='', tools=[],
        bridges=[(HREF['iran'], 'ایران', 'وضعیتی که سیمرغ از آن شروع می‌کند'), (HREF['miyan'], 'ارتباط رشته‌ها', 'پل‌هایی که راه‌حل از آن‌ها می‌آید')] + [(HREF[k], NAME[k], 'لایهٔ علم') for k in BASE],
        bridgelead='سیمرغ از دو لایهٔ زیرش می‌خواند؛ تا وقتی آن دو کامل نشده‌اند، این لایه هم نمی‌تواند کامل شود.',
        fields=[], fieldslead='', index=[],
        roadmap=['تمثیل: سی مرغ و سیمرغ — چرا این داستان قالب کار است',
                 'راه‌حل: از هر مسئلهٔ لایهٔ ایران به یک اقدام مشخص، با شرط و هزینه‌اش',
                 'بازی: نقشهٔ بزرگ ایران و ابزارهایی که دانش دو لایهٔ پایین را به کار می‌گیرند',
                 'معیار: از کجا بفهمیم یک پیشنهاد جواب داده یا نه'])

SPEC = {'miyan': spec_miyan, 'iran': spec_iran, 'simorgh': spec_simorgh}
TPL = open(f'{HERE}/wiki_home.tpl.html', encoding='utf-8').read()

for W in (sys.argv[1:] or ['soc', 'phil', 'tabar', 'miyan', 'iran', 'simorgh']):
    s = SPEC[W]() if W in SPEC else spec_base(W)
    sibs = [k for k in ALL if k != W and k in NAME]
    idx = sorted({(re.sub(r'^[«"\'\s]+', '', t), u) for t, u in s['index']}, key=lambda x: x[0])
    groups = []
    for t, u in idx:
        if not groups or groups[-1][0] != t[0]: groups.append((t[0], []))
        groups[-1][1].append((t, u))
    out = (TPL.replace('__W__', W).replace('__NAME__', E(NAME[W])).replace('__COLOR__', VAR[W])
        .replace('__TITLE__', E(s['title'])).replace('__LEAD__', E(s['lead']))
        .replace('__ENTRIES_URL__', E(s['entriesurl'] or '#contents')).replace('__ENTRIES_LABEL__', E(s['entrieslabel'] or 'فهرست'))
        .replace('__STATS__', ''.join(f'<div><b>{fa(n)}</b><span>{E(l)}</span></div>' for n, l in s['stats']))
        .replace('__QHIDE__', ' hidden' if len(s['questions']) < 3 else '').replace('__NQ__', fa(len(s['questions'])))
        .replace('__QLEAD__', E(s['qlead']))
        .replace('__QS__', ''.join(f'<a class="q" href="{E(u)}">{E(t)}<i>←</i></a>' for t, u in s['questions']))
        .replace('__THIDE__', ' hidden' if not s['tools'] else '').replace('__NT__', fa(len(s['tools'])))
        .replace('__TOOLS__', ''.join(f'<a class="tool" href="{E(u)}"><h3>{E(t)}</h3><p>{E(d)}</p><span class="go">باز کردن ←</span></a>' for u, t, d in s['tools']))
        .replace('__BRIDGELEAD__', E(s['bridgelead']))
        .replace('__BRIDGES__', ''.join(f'<a class="br" href="{E(u)}"><b>{E(t)}</b><span>{E(d)}</span></a>' for u, t, d in s['bridges']))
        .replace('__CHIDE__', ' hidden' if not s['fields'] else '').replace('__FIELDSLEAD__', E(s['fieldslead']))
        .replace('__SECS__', ''.join(f'<section class="fld"><h3>{E(t)} <small>{fa(len(es))}</small></h3>' + (f'<p>{E(sm)}</p>' if sm else '') +
            '<div class="lst">' + ''.join(f'<a href="{E(u)}">{E(n)}</a>' for n, u in es) + '</div></section>' for t, sm, es in s['fields']))
        .replace('__IHIDE__', ' hidden' if not idx else '').replace('__NI__', fa(len(idx)))
        .replace('__INDEX__', ''.join(f'<div class="ig"><b>{E(k)}</b><div>' + ''.join(f'<a href="{E(u)}">{E(t)}</a>' for t, u in v) + '</div></div>' for k, v in groups))
        .replace('__RHIDE__', ' hidden' if not s['roadmap'] else '')
        .replace('__ROAD__', ''.join(f'<li>{E(x)}</li>' for x in s['roadmap']))
        .replace('__SIB__', ''.join(f'<a href="{HREF[k]}">{E(NAME[k])}</a>' for k in sibs)))
    os.makedirs(f'{R}/{W}', exist_ok=True)
    open(f'{R}/{W}/index.html', 'w', encoding='utf-8').write(out)
    print(f'{W:8} home: {len(s["stats"])} stats, {len(s["questions"])} questions, {len(s["tools"])} tools, {len(s["fields"])} groups, {len(idx)} index terms')
