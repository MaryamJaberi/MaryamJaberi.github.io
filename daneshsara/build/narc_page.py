import json
# -*- coding: utf-8 -*-
"""صفحهٔ «پروندهٔ خودشیفتگی و کنترل»: python3 build/narc_page.py → psy/narcissism.html"""
import os, json, glob, html
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
C = {}
for p in glob.glob(f'{R}/data/psy/concepts/*.json'):
    c = json.load(open(p, encoding='utf-8')); C[c['id'].split(':')[1]] = c
SRC = json.load(open(f'{R}/core/sources.json', encoding='utf-8'))

GROUPS = [
 ("خودِ پدیده", "خودشیفتگی چیست، چه نیست، و چرا برچسب کمکی نمی‌کند.", "#4867a8",
  ["narcissism", "npd", "vulnerable-narcissism", "healthy-narcissism", "drive-not-control", "narcissism-culture", "collective-narcissism", "labels-harm"]),
 ("رفتارهای کنترل‌گرانه", "نُه دسته رفتار که می‌شود دید و شمرد، به‌جای حدس‌زدن دربارهٔ درون آدم‌ها.", "#8a4a6b",
  ["control-behaviors", "psychological-control", "coercive-control", "gaslighting", "darvo", "gottman-horsemen", "defensive-reactions", "public-private"]),
 ("نقش‌هایی که بازی می‌کنیم", "مثلث قربانی، ظالم و ناجی — و راه بیرون آمدن از آن.", "#2f7f8a",
  ["karpman-triangle", "rescuing", "victim-mindset", "agency"]),
 ("ریشه‌ها: کودکی و خانواده", "از کجا می‌آید، و آنچه دربارهٔ «بچه‌های والدین خودشیفته» واقعاً می‌دانیم.", "#b0652a",
  ["narcissism-origins", "children-of-narcissists", "conditional-regard", "breaking-cycle"]),
 ("قوس رابطه", "چطور شروع می‌شود، چه چیزی ادامه‌اش می‌دهد، و چطور تمام می‌شود.", "#9a3b3b",
  ["relationship-arc", "love-bombing", "intermittent-bond", "leaving"]),
 ("در هر نقشی که زندگی می‌دهد", "کار، خانواده، دوستی، گروه و فضای مجازی.", "#7a5ea8",
  ["control-in-couple", "control-in-parenting", "control-at-work", "control-in-family", "control-in-helping", "control-online"]),
 ("اثر، و بیرون آمدن", "آنچه بر تن و روان می‌گذرد، و آنچه واقعاً کمک می‌کند.", "#2f6b4f",
  ["victim-toll", "cptsd", "self-trust", "self-silencing", "boundaries", "assertiveness", "around-them", "recovery", "change-possible"]),
 ("جامعه و فرهنگ", "آیا این قرن خودشیفته‌تر شده، شبکه‌های اجتماعی چه کرده‌اند، و فرهنگ کجای این ماجراست.", "#38756b",
  ["narcissism-epidemic", "social-media-narcissism", "honour-culture", "culture-and-self", "cross-culture-measure", "front-and-back", "authoritarian-character", "measuring-control"]),
 ("ژن، مغز و تغییر", "ارثی بودن یعنی ثابت بودن؟ و دربارهٔ «مغزِ آدم خودشیفته» واقعاً چه می‌دانیم.", "#6b6b2f",
  ["genes-and-change", "gene-environment-myth", "neuroticism", "brain-claims"]),
 ("فلسفه: دقیقاً چه چیزی این‌جا غلط است؟", "کانت، هگل و هونت، فریکر، برلین، فرانکفورت، مرداک و سارتر — هفت صورت‌بندی از یک مسئله.", "#7a3b5e",
  ["means-and-ends", "recognition", "epistemic-injustice", "two-liberties", "freedom-of-will", "attention", "bad-faith", "analogies"]),
]
TOOLS = [
 ("control-check", "آیا در این رابطه کنترل هست؟", "بیست‌وپنج جمله، از دو طرف: «با من چه می‌شود» و «من چه می‌کنم». نتیجه نُه الگوی رفتاری است، نه برچسب."),
 ("triangle", "مثلث قربانی، ظالم، ناجی", "سه گوشه، سود پنهان هرکدام، و شش گام برای بیرون آوردن یک موقعیت واقعی خودتان."),
 ("sentences", "جمله‌ساز: به‌جای این، آن", "پنجاه‌وچند جملهٔ آشنا، با توضیح اینکه چه می‌کند و چه جایگزینی دارد. جملهٔ خودتان را هم می‌شود آزمود."),
 ("arc", "قوس رابطه", "هفت مرحله در پنج نقش: زوج، خانواده، کار، گروه و آنلاین — با عددهایی که واقعاً وجود دارند."),
 ("toll", "آنچه بر تن و روان می‌گذرد", "نقشهٔ تن و روان: چه چیزی تغییر می‌کند، با چه مقدار شواهد، و چه چیزی کمک می‌کند."),
 ("roles", "آینهٔ نقش‌ها: چطور آن آدم نباشم", "شش نقشی که زندگی می‌دهد — والد، شریک، رئیس، دوست، کمک‌کننده، فرزند بزرگسال — با تله‌های هر کدام و یک آزمایش کوچک برای همین هفته."),
 ("week", "هفت روز، هفت کار کوچک", "پنج وضعیت، و برای هر کدام هفت کارِ یک‌شبه با دلیلش. کوچک، چون در پژوهش چالشِ تمام‌شده تغییر آورد و چالشِ نیمه‌تمام پس‌رفت."),
 ("say", "چه بگویم؟ جمله‌های لحظهٔ سخت", "دوازده موقعیت: آنچه معمولاً می‌گوییم و چرا جواب نمی‌دهد، جایگزین‌ها در سه شدت، و قاعدهٔ پشت هر کدام."),
 ("analogies", "این مثل چیست؟ شش آنالوژی", "از هزینهٔ تعویض در اقتصاد تا تک‌کشتی در کشاورزی: شش قیاس ساختاری با جدول نگاشت، نقطهٔ شکست و یک پیش‌بینی آزمودنی."),
]
gaps = []
for g in GROUPS:
    for s in g[3]:
        c = C.get(s)
        if not c: continue
        for pt in c.get('points', []):
            for f in pt.get('flags', []):
                if f in ('unreplicated', 'contested'):
                    gaps.append((c['title']['fa'], s, f, pt['text']['fa'][:150]))
nsrc = len({s for s in C if False}) 
allsrc = sorted({x for g in GROUPS for s in g[3] if s in C for x in C[s].get('sources', [])})
tiers = {}
for s in allsrc:
    t = SRC.get(s, {}).get('tier', 0); tiers[t] = tiers.get(t, 0) + 1
n_entries = sum(1 for g in GROUPS for s in g[3] if s in C)

def card(slug):
    c = C.get(slug)
    if not c: return ''
    n = len(c.get('points', []))
    return (f'<a class="ent" href="entries.html#{slug}"><b>{E(c["title"]["fa"])}</b>'
            f'<span>{E(c["summary"]["fa"][:135])}…</span>'
            f'<i>{fa(n)} گزاره · {fa(len(c.get("sources", [])))} منبع</i></a>')

groups_html = ''.join(
 f'<section class="grp" style="--k:{g[2]}" id="g{i+1}"><header><h2>{E(g[0])}</h2><p>{E(g[1])}</p></header>'
 f'<div class="ents">{"".join(card(s) for s in g[3])}</div></section>' for i, g in enumerate(GROUPS))
tools_html = ''.join(f'<a class="tool" href="tools/{t[0]}.html"><b>{E(t[1])}</b><span>{E(t[2])}</span></a>' for t in TOOLS)
tools_html += ('<a class="tool stories" href="stories/narcissism-control.html">'
  '<b>بیست‌وهشت داستان مستند</b><span>پرونده‌های دادگاهی، گزارش‌های رسمی، ارزیابی‌های پژوهشی و خاطرات — '
  'از ایران و افغانستان تا بریتانیا و آمریکا، هر کدام با درجهٔ منبع و پیوند قابل کلیک.</span></a>')
map_html = ''.join(f'<a class="m" href="#g{i+1}" style="--k:{g[2]}"><b>{E(g[0])}</b><i>{fa(len(g[3]))} مدخل</i></a>' for i, g in enumerate(GROUPS))
gaps_html = ''.join(f'<li><a href="entries.html#{s}">{E(t)}</a> — {E(txt)}…</li>' for t, s, f, txt in gaps[:14])

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from narc_questions import STATIONS
nq = sum(len(st[3]) for st in STATIONS)

def qlinks(slugs):
    out = []
    for sl in slugs:
        c = C.get(sl)
        if c: out.append(f'<a href="entries.html#{sl}">{E(c["title"]["fa"])}</a>')
    return ''.join(out)

qi = 0
st_html = []
for si, st in enumerate(STATIONS):
    qs = []
    for q in st[3]:
        qi += 1
        qs.append(
         f'<details class="q"><summary><span class="n">{fa(qi)}</span><b>{E(q[0])}</b></summary>'
         f'<div class="qb"><p class="ans">{q[1]}<span class="qc" data-s="{",".join(q[4])}"></span></p>'
         f'<div class="today"><b>همین امروز</b>{E(q[2])}</div>'
         f'<div class="qlinks">{qlinks(q[3])}</div></div></details>')
    st_html.append(
     f'<section class="st" id="s{si+1}" style="--k:{st[2]}">'
     f'<header><span class="sn">{E(st[0])}</span><h2>{E(st[1])}</h2></header>'
     f'{"".join(qs)}</section>')
questions_html = ''.join(st_html)
qkeys = []
for st in STATIONS:
    for q in st[3]:
        for k in q[4]:
            if k not in qkeys: qkeys.append(k)
spine_html = ''.join(
 f'<a class="sp" href="#s{i+1}" style="--k:{st[2]}"><i>{E(st[0])}</i><b>{E(st[1])}</b>'
 f'<span>{fa(len(st[3]))} پرسش</span></a>' for i, st in enumerate(STATIONS))

TPL = open(f'{os.path.dirname(os.path.abspath(__file__))}/narc_page.tpl.html', encoding='utf-8').read()
out = (TPL.replace('__MAP__', map_html).replace('__GROUPS__', groups_html)
          .replace('__TOOLS__', tools_html).replace('__GAPS__', gaps_html)
          .replace('__N__', fa(n_entries)).replace('__NSRC__', fa(len(allsrc)))
          .replace('__T1__', fa(tiers.get(1, 0))).replace('__T2__', fa(tiers.get(2, 0)))
          .replace('__T34__', fa(tiers.get(3, 0) + tiers.get(4, 0)))
          .replace('__QUESTIONS__', questions_html).replace('__SPINE__', spine_html)
          .replace('__NQ__', fa(nq)).replace('__NTOOLS__', fa(len(TOOLS)))
          .replace('__QKEYS__', json.dumps(qkeys, ensure_ascii=False)))
open(f'{R}/psy/narcissism.html', 'w', encoding='utf-8').write(out)
print('narcissism.html', nq, 'questions,', n_entries, 'entries', len(allsrc), 'sources', len(gaps), 'flagged points')
