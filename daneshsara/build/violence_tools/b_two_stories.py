# -*- coding: utf-8 -*-
from _head import page
css = """
.step{border:1px solid var(--line);border-radius:var(--r-xl);background:var(--surface);padding:20px;max-width:780px;margin-bottom:16px}
.step h2{margin-bottom:6px}.step p.h{color:var(--ink-2);line-height:1.95;margin:0 0 12px}
textarea{width:100%;min-height:90px;font:inherit;padding:12px;border-radius:var(--r-md);border:1px solid var(--line-strong);background:var(--paper);color:var(--ink);line-height:1.9;box-sizing:border-box}
.q{margin:16px 0}.q b{display:block;margin-bottom:4px;font-size:.98rem}
.ends{display:flex;justify-content:space-between;font-size:var(--chip);color:var(--ink-3)}
.gap{display:grid;gap:18px;max-width:780px}
.g b{display:block;margin-bottom:6px}
.tr{position:relative;height:26px;border-radius:13px;background:var(--vz);direction:ltr}
.tr i{position:absolute;top:3px;width:20px;height:20px;border-radius:50%;margin-left:-10px}
.tr i.a{background:var(--vm)}.tr i.b{background:var(--vh)}
.tr span{position:absolute;top:11px;height:4px;background:var(--va);opacity:.7}
.key{font-size:var(--chip);color:var(--ink-2)}.key i{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;margin-inline:8px 4px}
.big{font-size:1.15rem;line-height:2;margin:var(--s4) 0}
ul.ask{line-height:2.1;padding-inline-start:1.2em;max-width:44em}
"""
QS = [("اثرش چقدر ماند؟", "همان لحظه تمام شد", "هنوز هست"),
      ("چقدر دلیل داشت؟", "بی‌دلیل بود", "کاملاً قابل‌فهم بود"),
      ("ماجرا بسته شده؟", "هنوز باز است", "کاملاً تمام شده"),
      ("چقدر بزرگ بود؟", "چیز کوچکی بود", "خیلی بزرگ بود")]
def sliders(p):
    return ''.join(f'<div class="q"><b>{q}</b><input type="range" id="{p}{i}" min="0" max="10" value="5"><div class="ends"><span>{b}</span><span>{a}</span></div></div>' for i, (q, a, b) in enumerate(QS))
body = f'''<h1>دو روایت از یک ماجرا</h1>
<p class="lead">پژوهش‌ها نشان می‌دهند همان آدم، وقتی ماجرایی را از جای کسی که آزار داده تعریف می‌کند، آن را کوچک، قابل‌فهم و تمام‌شده می‌بیند؛ و وقتی از جای کسی که آزار دیده، بزرگ، بی‌دلیل و ادامه‌دار. این ابزار همین شکاف را روی یک ماجرای خودت نشان می‌دهد.</p>
<div class="note w">هیچ‌چیز ذخیره یا فرستاده نمی‌شود؛ با بستن صفحه همه‌چیز پاک می‌شود. اگر ماجرا دربارهٔ خشونت جدی یا خطرِ ادامه‌دار است، این تمرین جای کمک حرفه‌ای را نمی‌گیرد، و قرار نیست کسی را به «دیدنِ طرف مقابل» وادار کند که از او می‌ترسد.</div>
<div class="step"><h2>۱. ماجرایی که در آن تو کسی را رنجاندی</h2><p class="h">یک ماجرای واقعی و نه خیلی سنگین انتخاب کن: حرفی که زدی، کاری که کردی، قولی که شکستی. اگر خواستی چند خط بنویس؛ لازم نیست.</p>
<textarea aria-label="یادداشت اختیاری" placeholder="اختیاری"></textarea>
<p class="h" style="margin-top:14px"><b>از جای خودت جواب بده:</b></p>{sliders("a")}</div>
<div class="step"><h2>۲. حالا همان ماجرا، از جای او</h2><p class="h">چشم‌هایت را یک لحظه ببند و جای او بنشین: همان روز، همان جمله، و روزهای بعدش. اگر او این چهار پرسش را جواب می‌داد، چه می‌گفت؟ حدس بزن؛ حدسِ صادقانه.</p>{sliders("b")}
<button class="pb go" id="go">شکاف را نشان بده</button></div>
<section id="out" class="off"><h2>شکاف</h2>
<p class="key"><i style="background:var(--vm)"></i>روایت من<i style="background:var(--vh)"></i>روایتی که برای او حدس زدم</p>
<div class="gap" id="gap"></div><p class="big" id="say"></p>
<h2>سه پرسش که می‌شود از خودِ او پرسید</h2>
<ul class="ask"><li>«آن روز برای تو چطور بود؟» و بعد فقط گوش‌دادن، بدون توضیح‌دادن.</li><li>«چیزی از آن ماجرا هنوز با تو هست؟»</li><li>«چه چیزی کمک می‌کرد، یا هنوز کمک می‌کند؟»</li></ul>
<p class="note g">حدس تو دربارهٔ روایت او هنوز روایت توست. شکاف واقعی را فقط خودش می‌تواند بگوید، و معمولاً از حدس ما بزرگ‌تر است. · منبع: Baumeister, Stillwell & Wotman (1990), Journal of Personality and Social Psychology · <a href="../entries.html#violence-unseen-by-doer">مدخل: آیا آدم‌هایی هستند که نفهمند دارند خشونت می‌کنند؟</a></p>
<button class="pb" id="flip">برعکسش: ماجرایی که در آن من رنجیدم</button>
<p class="note g off" id="fl" style="margin-top:12px">همین چهار لغزنده را برای ماجرایی پر کن که در آن تو رنجیدی، و بعد از جای کسی که رنجاند. معمولاً همین‌جا می‌بینیم او هم به احتمال زیاد ماجرا را «کوچک و تمام‌شده» به یاد دارد؛ نه لزوماً از بدجنسی، بلکه چون از آن صندلی همین‌طور دیده می‌شود. فهمیدنِ این، کار او را درست نمی‌کند؛ فقط توضیح می‌دهد چرا «خودش باید بفهمد» معمولاً جواب نمی‌دهد و باید گفت.</p></section>
'''
js = r'''
const Q=%s;
$("go").addEventListener("click",()=>{let big=0,worst=0,wi=0;
$("gap").innerHTML=Q.map((q,i)=>{const a=+$("a"+i).value,b=+$("b"+i).value,d=Math.abs(a-b);big+=d;if(d>worst){worst=d;wi=i}
const l=Math.min(a,b)*10,w=d*10;return '<div class="g"><b>'+q[0]+'</b><div class="tr"><span style="left:'+l+'%%;width:'+w+'%%"></span><i class="a" style="left:'+a*10+'%%"></i><i class="b" style="left:'+b*10+'%%"></i></div><div class="ends"><span>'+q[1]+'</span><span>'+q[2]+'</span></div></div>'}).join("");
$("say").textContent=big<=4?"دو روایتت نزدیک هم‌اند. یا واقعاً او را خوب می‌بینی، یا حدست برای او هنوز از صندلی خودت است. تنها راه دانستنش پرسیدن است.":"بزرگ‌ترین فاصله در «"+Q[wi][0].replace("؟","")+"» است. همین یک خط معمولاً جایی است که دو نفر بر سرش حرف هم را نمی‌فهمند: یکی می‌گوید «گذشت» و دیگری هنوز در آن است.";
$("out").classList.remove("off");$("out").scrollIntoView({behavior:"smooth"})});
$("flip").addEventListener("click",()=>$("fl").classList.remove("off"));
''' % __import__('json').dumps([[q, b, a] for q, a, b in QS], ensure_ascii=False)
page('violence-two-stories', 'دو روایت از یک ماجرا', 'یک ماجرا را یک بار از جای کسی که رنجاند و یک بار از جای کسی که رنجید ببین. شکاف میان دو روایت، بر پایهٔ پژوهش بامایستر.', css, body, js)
