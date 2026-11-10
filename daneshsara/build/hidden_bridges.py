# -*- coding: utf-8 -*-
"""«پل‌های پنهان» — cross-wiki link suggestions by Swanson's ABC logic on our own graph.
A (wiki X) —B— C (wiki Y): A and C are not linked, but share intermediaries B (an entry both touch, or a person both name).
Score = Adamic–Adar: sum over shared B of 1/ln(degree B), so a specific bridge counts more than a hub.
The page reports a hold-out test of the method on our own links, so nobody mistakes a suggestion for a finding.
python3 build/hidden_bridges.py  → atlas/hidden-bridges.html"""
import json, glob, os, math, random, collections, html
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..'); os.chdir(R)
fa = lambda n: str(n).translate(str.maketrans('0123456789.', '۰۱۲۳۴۵۶۷۸۹٫'))
C = {}
for f in glob.glob('data/*/concepts/*.json'):
    d = json.load(open(f, encoding='utf-8')); C[d['id']] = d
reg = json.load(open('core/registry.json', encoding='utf-8'))['entries']
people = json.load(open('core/people.json', encoding='utf-8'))
wk = lambda i: i.split(':')[0]
con = sorted(i for i, d in C.items() if d['kind'] == 'concept' and i in reg)
conset = set(con)
def graph(skip=frozenset()):
    nb = collections.defaultdict(set)
    for i in con:
        for l in C[i].get('links', []):
            j = l['to']
            if j in conset and j != i and frozenset((i, j)) not in skip: nb[i].add(j); nb[j].add(i)
        for p in C[i].get('people', []): nb[i].add('P|' + p); nb['P|' + p].add(i)
    return nb
def scores(nb, pairs=None):
    """Adamic–Adar over shared intermediaries, cross-wiki, not already adjacent."""
    out = collections.defaultdict(float); via = collections.defaultdict(list)
    for b, ns in nb.items():
        ns = [x for x in ns if x in conset]
        if len(ns) < 2 or len(ns) > 60: continue          # a hub that touches everything explains nothing
        w = 1 / math.log(len(nb[b]) + 1)
        for x in range(len(ns)):
            for y in range(x + 1, len(ns)):
                a, c = ns[x], ns[y]
                if wk(a) == wk(c) or c in nb[a]: continue
                k = (a, c) if a < c else (c, a)
                if pairs is not None and k not in pairs: continue
                out[k] += w; via[k].append(b)
    return out, via
# ---- hold-out test: hide 15% of the cross-wiki links we already have and see whether the method scores them above random non-links
random.seed(7)
full = graph()
cross = sorted({tuple(sorted((a, b))) for a in con for b in full[a] if b in conset and wk(a) != wk(b)})
hid = random.sample(cross, max(1, len(cross) * 15 // 100))
nb_t = graph(frozenset(frozenset(p) for p in hid))
neg = set()
while len(neg) < len(hid):
    a, c = random.sample(con, 2)
    if wk(a) != wk(c) and c not in full[a]: neg.add(tuple(sorted((a, c))))
neg = sorted(neg)
sc_t, _ = scores(nb_t, set(hid) | set(neg))
ph = [sc_t.get(p, 0) for p in hid]; pn = [sc_t.get(p, 0) for p in neg]
auc = sum((1 if x > y else .5 if x == y else 0) for x in ph for y in pn) / (len(ph) * len(pn))
found = sum(1 for x in ph if x > 0) / len(ph); false = sum(1 for x in pn if x > 0) / len(pn)
# ---- suggestions on the full graph
sc, via = scores(full)
top = sorted(sc.items(), key=lambda kv: -kv[1])
keep = [(k, s) for k, s in top if len(via[k]) >= 2][:300]
idx = {}; nodes = []
def nid(i):
    if i not in idx:
        idx[i] = len(nodes)
        if i.startswith('P|'):
            p = people.get(i[2:], {}); nodes.append({'t': (p.get('name') or {}).get('fa') or i[2:], 'w': 'person'})
        else: nodes.append({'t': C[i]['title']['fa'], 'w': wk(i), 'u': '../' + reg[i]['url']})
    return idx[i]
pairs = [[nid(a), nid(c), round(s, 2), [nid(b) for b in sorted(via[(a, c)], key=lambda b: len(full[b]))[:6]]] for (a, c), s in keep]
per = collections.defaultdict(list)
for (a, c), s in top:
    if len(per[a]) < 4: per[a].append((c, s))
    if len(per[c]) < 4: per[c].append((a, s))
openx = {nid(a): [[nid(c), round(s, 2), [nid(b) for b in sorted(via[tuple(sorted((a, c)))], key=lambda b: len(full[b]))[:4]]] for c, s in v] for a, v in per.items()}
wp = collections.Counter(tuple(sorted((nodes[p[0]]['w'], nodes[p[1]]['w']))) for p in pairs)
DATA = {'nodes': nodes, 'pairs': pairs, 'open': openx}
WN = {'psy': 'روان', 'soc': 'جامعه', 'phil': 'فلسفه', 'tabar': 'تبار', 'tarikh': 'تاریخ', 'person': 'چهره'}
WV = {'psy': '--fam-psy', 'soc': '--fam-soc', 'phil': '--fam-hum', 'tabar': '--fam-bio', 'tarikh': '--fam-hist', 'person': '--ink-3'}
TPL = '''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>پل‌های پنهان | اطلس‌ها | دانش‌سرا</title>
<meta name="description" content="جفت مدخل‌هایی از دو رشتهٔ جدا که به هم پیوند ندارند ولی از راه چند مدخل یا چهرهٔ مشترک به هم می‌رسند. پیشنهاد ماشین است، نه یافته.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
h1{font-size:var(--h1);margin:var(--s8) 0 var(--s3);line-height:var(--lh-tight);text-wrap:balance}
p.lead{color:var(--ink-2);max-width:47em;line-height:2;margin:0 0 var(--s4);font-size:1.05rem}
section{padding-block:var(--s5);border-top:1px solid var(--line)}
h2{font-size:var(--h3);margin:0 0 var(--s2)}
p.sub{color:var(--ink-3);font-size:var(--small);line-height:1.9;margin:0 0 var(--s4);max-width:50em}
.test{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:var(--s3);max-width:60em;margin-bottom:var(--s3)}
.test div{padding:var(--s3) var(--s4);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface)}
.test b{display:block;font-size:1.6rem;line-height:1.2}.test span{font-size:var(--chip);color:var(--ink-3);line-height:1.7;display:block}
.meter{height:10px;border-radius:5px;background:var(--surface-subtle);position:relative;margin-top:8px;direction:ltr}
.meter i{position:absolute;inset:0 auto 0 0;background:var(--primary);border-radius:5px}.meter u{position:absolute;top:-3px;bottom:-3px;left:50%;width:2px;background:var(--ink-3)}
.warn{padding:var(--s3) var(--s4);border-radius:var(--r-md);font-size:var(--small);line-height:1.9;color:var(--ink-2);max-width:60em;background:color-mix(in srgb,var(--warn) 9%,var(--paper));border:1px solid color-mix(in srgb,var(--warn) 40%,var(--line))}
.ctl{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:var(--s4)}
.ctl input{font:inherit;flex:1 1 240px;max-width:420px;padding:9px 14px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:var(--surface);color:var(--ink)}
.ctl button{font:inherit;font-size:var(--small);padding:6px 14px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:none;color:var(--ink-2);cursor:pointer}
.ctl button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.list{display:grid;gap:10px;max-width:64em}
.br{border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);padding:var(--s3) var(--s4);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr) minmax(0,1fr);gap:10px;align-items:center}
.end{display:grid;gap:4px;min-width:0}
.end a{font-weight:650;color:var(--ink);text-decoration:none;line-height:1.7}.end a:hover{text-decoration:underline}
.end small,.mid small{font-size:var(--chip);color:var(--ink-3)}
.end small i{font-style:normal;display:inline-block;width:9px;height:9px;border-radius:50%;margin-inline-end:6px;background:var(--w)}
.end.c{text-align:end}
.mid{display:grid;gap:5px;justify-items:center;border-inline:1px dashed var(--line-strong);padding-inline:8px;min-width:0}
.mid>*{max-width:100%;min-width:0}
.mid .b{display:flex;flex-wrap:wrap;gap:4px;justify-content:center;width:100%}
.mid .b>*{display:block;box-sizing:border-box}
.mid .b a,.mid .b span{font-size:var(--chip);padding:1px 9px;border-radius:var(--r-full);border:1px solid color-mix(in srgb,var(--w) 50%,var(--line));color:var(--ink-2);text-decoration:none;background:color-mix(in srgb,var(--w) 8%,var(--paper));max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sc{display:flex;gap:6px;align-items:center;font-size:var(--chip);color:var(--ink-3)}
.sc i{display:block;height:5px;border-radius:3px;background:var(--primary)}
@media (max-width:640px){.br{grid-template-columns:minmax(0,1fr)}.mid{border-inline:0;border-block:1px dashed var(--line-strong);padding:8px 0}.end.c{text-align:start}}
.more{margin-top:var(--s4)}
.empty{color:var(--ink-3);font-size:var(--small)}
ol.how{max-width:50em;padding-inline-start:1.4em;display:grid;gap:8px;color:var(--ink-2);line-height:1.95;font-size:var(--small)}
footer.f{border-top:1px solid var(--line);padding-block:var(--s5);font-size:var(--small);color:var(--ink-3)}footer.f a{color:var(--ink-2);margin-inline-end:var(--s4)}
</style>
</head>
<body>
<main class="wrap">
<h1>پل‌های پنهان</h1>
<p class="lead">دو مدخل از دو رشتهٔ جدا که هیچ پیوندی به هم ندارند، ولی هر دو به چند مدخل یا چهرهٔ یکسان می‌رسند. این صفحه چنین جفت‌هایی را از میان __NCON__ مدخل پیدا می‌کند تا یک آدم نگاهشان کند: شاید این‌جا حرف مشترکی هست که هنوز کسی ننوشته.</p>
<p class="warn"><b>این‌ها پیشنهاد ماشین‌اند، نه یافته.</b> «از یک راه به هم می‌رسند» به معنای «به هم مربوط‌اند» نیست. هیچ جفتی از این صفحه خودکار به ویکی‌ها اضافه نمی‌شود.</p>

<section id="test">
<h2>این روش چقدر می‌ارزد؟ یک آزمون روی داده‌های خودمان</h2>
<p class="sub">__NHID__ پیوند میان‌رشته‌ایِ موجود را پنهان کردیم (۱۵ درصد از __NCROSS__)، روش را روی باقی اجرا کردیم و دیدیم آیا به پیوندهای پنهان‌شده نمرهٔ بالاتری می‌دهد تا به همان تعداد جفتِ تصادفیِ بی‌پیوند.</p>
<div class="test">
<div><b>__AUC__</b><span>احتمال این‌که یک پیوند واقعیِ پنهان‌شده نمره‌ای بالاتر از یک جفت تصادفی بگیرد. خط وسط یعنی شیر یا خط.</span><div class="meter"><i style="width:__AUCW__%"></i><u></u></div></div>
<div><b>__FOUND__٪</b><span>از پیوندهای پنهان‌شده اصلاً راه دوگامی داشتند. بقیه را این روش هرگز نمی‌تواند ببیند.</span></div>
<div><b>__FALSE__٪</b><span>از جفت‌های تصادفی هم راه دوگامی داشتند، یعنی هشدار نادرست.</span></div>
</div>
<p class="sub">خوانش: روش از تصادف بهتر است، ولی بیشتر پیوندهای واقعی را نمی‌بیند. و چون آزمون با پیوندهایی است که خود ما نوشته‌ایم، فقط می‌گوید روش سلیقهٔ پیوندنویسی ما را تا چه حد بازمی‌سازد، نه این‌که پیشنهادهایش از نظر علمی درست‌اند.</p>
</section>

<section id="find">
<h2>از یک مدخل شروع کنید</h2>
<p class="sub">نام مدخلی را بنویسید تا ببینید در رشته‌های دیگر به چه چیزهایی نزدیک است بی‌آن‌که پیوندی داشته باشد.</p>
<div class="ctl"><input id="q" type="search" placeholder="مثلاً: دلبستگی، مشروعیت، انتخاب طبیعی" aria-label="جست‌وجوی مدخل" autocomplete="off"></div>
<div class="list" id="openlist"><p class="empty">هنوز چیزی ننوشته‌اید.</p></div>
</section>

<section id="top">
<h2>قوی‌ترین پل‌های ننوشته</h2>
<p class="sub">__NPAIR__ جفت با بیشترین نمره که دست‌کم دو واسطهٔ مشترک دارند. نوار، نمره را نسبت به بالاترین نمره نشان می‌دهد؛ واسطه‌های خاص وزن بیشتری دارند تا مدخل‌های پرپیوند.</p>
<div class="ctl" id="wf"></div>
<div class="list" id="toplist"></div>
<div class="more"><button class="ctl-more" id="more" style="font:inherit;padding:8px 20px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:none;color:var(--ink-2);cursor:pointer">بیشتر نشان بده</button></div>
</section>

<section id="how">
<h2>روش</h2>
<ol class="how">
<li>شبکه از پیوندهایی ساخته می‌شود که در مدخل‌ها نوشته‌ایم، به‌علاوهٔ چهره‌هایی که هر مدخل نام می‌برد. رشته‌ها و ریشه‌ها واسطه حساب نمی‌شوند، و واسطه‌ای که به بیش از شصت مدخل وصل است کنار گذاشته می‌شود، چون چیزی را توضیح نمی‌دهد.</li>
<li>برای هر دو مدخل از دو ویکیِ متفاوت که پیوند مستقیم ندارند، واسطه‌های مشترک شمرده می‌شود. هر واسطه به اندازهٔ یک تقسیم بر لگاریتمِ شمار پیوندهایش وزن می‌گیرد (سنجهٔ آدامیک و آدار در پیش‌بینی پیوند).</li>
<li>الگو از «کشف مبتنی بر متون» دان سوانسون می‌آید: اگر الف به ب و ب به ج وصل است و الف و ج در دو ادبیات جدا مانده‌اند، شاید پیوندی ننوشته میانشان باشد. مرورهای این حوزه هشدار می‌دهند که چنین روش‌هایی خروجیِ زیاد و سخت‌تفسیر می‌دهند و هم‌رخدادی دلیل ربط نیست؛ برای همین آزمون بالا را کنار نتیجه گذاشته‌ایم.</li>
</ol>
<p class="sub" style="margin-top:var(--s3)">منبع روش: Swanson, D. R. (1986). Undiscovered public knowledge. <i>The Library Quarterly</i>, 56(2)؛ Adamic, L. A., & Adar, E. (2003). Friends and neighbors on the Web. <i>Social Networks</i>, 25(3)؛ Thilakaratne, M., Falkner, K., & Atapattu, T. (2019). A systematic review on literature-based discovery workflow. <i>PeerJ Computer Science</i>, 5, e235. دو منبع نخست از دانستهٔ ویراستار آمده‌اند؛ سومی خوانده شده است.</p>
</section>
</main>
<footer class="f"><div class="wrap"><a href="../">دانش‌سرا</a><a href="./">اطلس‌ها</a><a href="coverage.html">نقشهٔ پوشش</a><a href="sitemap.html">نقشهٔ سایت</a></div></footer>
<script>
(() => {
const D = __DATA__, WN = __WN__, WV = __WV__;
const fa = n => String(n).replace(/\\d/g, d => "۰۱۲۳۴۵۶۷۸۹"[d]).replace(".", "٫");
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const $ = id => document.getElementById(id), N = D.nodes, max = D.pairs.length ? D.pairs[0][2] : 1;
const end = (i, cls) => `<div class="end ${cls}" style="--w:var(${WV[N[i].w]})"><a href="${N[i].u}">${esc(N[i].t)}</a><small><i></i>ویکی ${WN[N[i].w]}</small></div>`;
const chip = i => N[i].u ? `<a href="${N[i].u}" style="--w:var(${WV[N[i].w]})" title="${esc(N[i].t)}">${esc(N[i].t)}</a>` : `<span style="--w:var(${WV[N[i].w]})" title="${esc(N[i].t)}">${esc(N[i].t)}</span>`;
const card = (a, c, s, bs) => `<div class="br">${end(a, "a")}<div class="mid"><small>از راهِ</small><div class="b">${bs.map(chip).join("")}</div><div class="sc"><i style="width:${Math.max(8, s / max * 70)}px"></i>${fa(s.toFixed(2))}</div></div>${end(c, "c")}</div>`;
let shown = 20, filt = "";
const pairKey = p => [N[p[0]].w, N[p[1]].w].sort().join("+");
function top() {
  const L = D.pairs.filter(p => !filt || pairKey(p) === filt);
  $("toplist").innerHTML = L.slice(0, shown).map(p => card(p[0], p[1], p[2], p[3])).join("") || `<p class="empty">جفتی نیست.</p>`;
  $("more").hidden = shown >= L.length;
}
const keys = [...new Set(D.pairs.map(pairKey))].map(k => [k, D.pairs.filter(p => pairKey(p) === k).length]).sort((a, b) => b[1] - a[1]);
$("wf").innerHTML = `<button data-k="" aria-pressed="true">همه (${fa(D.pairs.length)})</button>` + keys.map(([k, n]) => `<button data-k="${k}" aria-pressed="false">${k.split("+").map(w => WN[w]).join(" و ")} (${fa(n)})</button>`).join("");
$("wf").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; filt = b.dataset.k; shown = 20; $("wf").querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); top(); });
$("more").addEventListener("click", () => { shown += 20; top(); });
top();
const norm = s => s.replace(/[ي]/g, "ی").replace(/[ك]/g, "ک").replace(/[\\u200c\\s]+/g, " ").trim();
$("q").addEventListener("input", e => {
  const q = norm(e.target.value);
  if (q.length < 2) { $("openlist").innerHTML = `<p class="empty">هنوز چیزی ننوشته‌اید.</p>`; return; }
  const hits = Object.keys(D.open).map(Number).filter(i => norm(N[i].t).includes(q)).slice(0, 6);
  $("openlist").innerHTML = hits.map(a => D.open[a].map(([c, s, bs]) => card(a, c, s, bs)).join("")).join("") || `<p class="empty">برای این نام پلی پیدا نشد. یا مدخلی با این نام نیست، یا هیچ راه دوگامی به رشتهٔ دیگری ندارد.</p>`;
});
})();
</script>
</body>
</html>
'''
page = (TPL.replace('__NCON__', fa(len(con))).replace('__NHID__', fa(len(hid))).replace('__NCROSS__', fa(len(cross)))
        .replace('__AUC__', fa(f'{auc:.2f}')).replace('__AUCW__', f'{auc * 100:.0f}').replace('__FOUND__', fa(round(found * 100))).replace('__FALSE__', fa(round(false * 100)))
        .replace('__NPAIR__', fa(len(pairs))).replace('__DATA__', json.dumps(DATA, ensure_ascii=False, separators=(',', ':')))
        .replace('__WN__', json.dumps(WN, ensure_ascii=False)).replace('__WV__', json.dumps(WV)))
open('atlas/hidden-bridges.html', 'w', encoding='utf-8').write(page)
print(f'hidden bridges: {len(pairs)} pairs, {len(openx)} start points | hold-out n={len(hid)} AUC={auc:.3f} found={found:.2f} false={false:.2f} | {dict(wp)} | {len(page)//1024} KB')
for (a, c), s in keep[:8]: print(f'  {s:.2f} {C[a]["title"]["fa"][:38]} ~ {C[c]["title"]["fa"][:38]} via {len(via[(a,c)])}')
