#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""گراف زندهٔ کل مسئله را از خودِ محتوا می‌سازد.

خروجی: data/graph/graph.json
هر بار که مطلبی اضافه یا کم شود، با اجرای دوبارهٔ این فایل گراف به‌روز می‌شود.
متن‌های دست‌نویس (مسئلهٔ باز، منابع لازم، به چه دردی می‌خورد) در data/graph/open.json
می‌آیند و اینجا فقط به گره‌ها چسبانده می‌شوند.
"""
import json, os, glob, re, datetime, collections, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)
def load(p, d=None):
    try:
        with open(p, encoding='utf-8') as f: return json.load(f)
    except Exception: return d
def fa(x, k='fa'):
    if isinstance(x, dict): return x.get(k) or x.get('fa') or ''
    return x or ''

RING = {
 'danesh': {'id':'danesh','fa':'دانش','note':'چه می‌دانیم دربارهٔ انسان، جامعه و تاریخ'},
 'iran':   {'id':'iran','fa':'ایران امروز','note':'این دانش دربارهٔ وضع امروز ایران چه می‌گوید'},
 'farda':  {'id':'farda','fa':'فردای ایران','note':'از اینجا به کجا می‌شود رفت و چطور'},
}

def concepts():
    out = []
    for f in sorted(glob.glob(P('data','*','concepts','*.json'))):
        d = load(f)
        if isinstance(d, dict) and d.get('id'): out.append(d)
    return out

def build():
    C = concepts()
    by_id = {d['id']: d for d in C}
    nodes, edges = [], []

    # ---------- حلقهٔ دانش: ریشه → شاخه → زیرشاخه ----------
    kids = collections.Counter()      # شمار مفهوم‌های هر شاخه
    rev  = collections.Counter()      # از آن‌ها چندتا بازبینی‌شده
    for d in C:
        if d.get('kind') != 'concept': continue
        f = d.get('field') or d.get('parent')
        if f:
            kids[f] += 1
            if d.get('status') == 'reviewed': rev[f] += 1
    # شمار شاخه را به ریشه هم بیفزا
    for d in C:
        if d.get('kind') in ('field','subfield'):
            p = d.get('parent')
            if p: kids[p] += kids[d['id']]; rev[p] += rev[d['id']]

    WIKI_DIR = {'psy':'psy','soc':'soc','phil':'phil','tabar':'tabar','tarikh':'tarikh'}
    for d in C:
        k = d.get('kind')
        if k not in ('root','field','subfield'): continue
        ns = d['id'].split(':')[0]
        nodes.append({
            'id': d['id'], 'ring':'danesh', 'kind':k,
            'label': fa(d.get('title')), 'note': fa(d.get('summary'))[:220],
            'parent': d.get('parent'),
            'n': kids[d['id']], 'reviewed': rev[d['id']],
            'href': f"{WIKI_DIR.get(ns,ns)}/entries.html#{d['id']}" if k!='root' else f"{WIKI_DIR.get(ns,ns)}/index.html",
        })

    # پیوندهای میان‌رشته‌ای: هر لینکِ مفهوم به مفهومی در شاخهٔ دیگر، یک وزن به یال شاخه‌ها
    w = collections.Counter()
    for d in C:
        if d.get('kind') != 'concept': continue
        a = d.get('field') or d.get('parent')
        for L in (d.get('links') or []):
            t = by_id.get(L.get('to'))
            if not t: continue
            b = t.get('field') or t.get('parent')
            if a and b and a != b: w[tuple(sorted((a,b)))] += 1
    for (a,b),n in w.items():
        if n >= 2: edges.append({'a':a,'b':b,'rel':'پیوند میان‌رشته‌ای','w':n})

    # ---------- حلقهٔ ایران: حلقه‌های علّی ----------
    for f in sorted(glob.glob(P('data','flows','*.json'))):
        if os.path.basename(f).startswith('_'): continue
        d = load(f) or {}
        if not d.get('id'): continue
        nid = 'flow:'+d['id']
        inner = d.get('nodes') or []
        nodes.append({
            'id': nid, 'ring':'iran', 'kind':'flow',
            'label': d.get('title',''), 'note': (d.get('q') or d.get('summary',''))[:220],
            'parent': None, 'n': len(inner), 'reviewed': 0 if d.get('status')=='draft' else len(inner),
            'href': 'iran/index.html#'+d['id'],
        })
        seen = set()
        for nd in inner:
            for wk in (nd.get('wiki') or []):
                t = by_id.get(wk)
                if not t: continue
                fld = t.get('field') or t.get('parent')
                if fld and fld not in seen:
                    seen.add(fld); edges.append({'a':nid,'b':fld,'rel':'تکیه بر دانش','w':1})

    # ابزارهای لایهٔ ایران
    for h in sorted(glob.glob(P('iran','tools','*.html'))):
        b = os.path.basename(h)
        if b == 'index.html': continue
        raw = open(h,encoding='utf-8',errors='ignore').read()
        if 'بخش خصوصی' in raw: continue   # نشانهٔ صفحهٔ خصوصی؛ در نسخهٔ عمومی چیزی از آن نشان نده
        t = re.search(r'<title>(.*?)</title>', raw, re.S)
        nodes.append({'id':'tool:'+b[:-5], 'ring':'iran', 'kind':'tool',
            'label': (t.group(1).split('—')[0].split('·')[0].strip() if t else b[:-5]),
            'note':'ابزاری برای اینکه خودت وارسی کنی، نه اینکه حرف ما را باور کنی.',
            'parent':None,'n':1,'reviewed':1,'href':'iran/tools/'+b})

    # ---------- حلقهٔ فردا ----------
    FARDA = [
      ('sakht/index.html','ساخت ایران','کارِ عملی: مسئله‌ها را به کارهای کوچکِ قابل‌برداشتن بشکنیم.'),
      ('sakht/map.html','نقشهٔ ساخت','کدام کار به کدام وصل است و از کجا می‌شود شروع کرد.'),
      ('sakht/work.html','کارها','فهرست کارهایی که روی زمین مانده.'),
      ('simorgh/index.html','پَرِ سیمرغ','بازی‌ای برای اینکه گروه‌های آدم‌ها مسئله را با هم بفهمند.'),
      ('simorgh/why.html','چرا سیمرغ','چرا بازی، و نه بیانیه.'),
      ('simorgh/birds.html','سی مرغ','سی گروه، سی زاویهٔ دید.'),
      ('simorgh/transitions.html','گذارها','جاهایی از تاریخ که کشوری از این وضع بیرون آمده.'),
      ('simorgh/poll.html','نبض میز','یک پرسش، ماهی یک بار، برای اندازه‌گیری چیزی که هیچ‌کس اندازه نمی‌گیرد.'),
    ]
    for href, lab, note in FARDA:
        if os.path.exists(P(*href.split('/'))):
            nodes.append({'id':'farda:'+href.replace('/','-')[:-5],'ring':'farda','kind':'page',
                'label':lab,'note':note,'parent':None,'n':1,'reviewed':1,'href':href})

    # ---------- چسباندن متن‌های دست‌نویس ----------
    OPEN = load(P('data','graph','open.json'), {}) or {}
    missing = []
    for nd in nodes:
        o = OPEN.get(nd['id'])
        if o:
            nd['q']    = o.get('q','')            # مسئلهٔ باز
            nd['state']= o.get('state')           # ۰ تا ۴: تا کجای پازل رفته‌ایم
            nd['need'] = o.get('need',[])         # چه منبعی لازم داریم
            nd['use']  = o.get('use','')          # به چه دردی می‌خورد
        else:
            if nd['kind'] in ('root','field','flow'): missing.append(nd['id'])

    G = {
      'built': datetime.date.today().isoformat(),
      'rings': list(RING.values()),
      'nodes': nodes, 'edges': edges,
      'stats': {
        'concepts': sum(1 for d in C if d.get('kind')=='concept'),
        'reviewed': sum(1 for d in C if d.get('status')=='reviewed'),
        'fields': sum(1 for d in C if d.get('kind')=='field'),
        'flows': sum(1 for n in nodes if n['kind']=='flow'),
        'links': len(edges),
        'no_question': len(missing),
      },
    }
    os.makedirs(P('data','graph'), exist_ok=True)
    with open(P('data','graph','graph.json'),'w',encoding='utf-8') as f:
        json.dump(G,f,ensure_ascii=False,separators=(',',':'))
    print(f"گراف: {len(nodes)} گره، {len(edges)} یال · {G['stats']['concepts']} مفهوم "
          f"({G['stats']['reviewed']} بازبینی‌شده)")
    if missing:
        print('بدون مسئلهٔ باز (' + str(len(missing)) + '):', '، '.join(missing[:12]))
    return G

if __name__ == '__main__':
    build()
