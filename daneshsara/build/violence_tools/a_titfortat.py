# -*- coding: utf-8 -*-
from _head import page
css = """
.grid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px}
@media (max-width:820px){.grid2{grid-template-columns:1fr}}
.strip{display:grid;grid-template-columns:repeat(40,1fr);gap:2px;direction:ltr;margin:4px 0}
.strip i{aspect-ratio:1;border-radius:3px;background:var(--vr)}.strip i.d{background:var(--vh)}.strip i.x{outline:2px solid var(--va);outline-offset:-1px}
.who{font-size:var(--small);color:var(--ink-2);display:flex;justify-content:space-between;margin-top:10px}
.who b{color:var(--ink)}
.sc{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}
.sc div{border:1px solid var(--line);border-radius:var(--r-lg);padding:12px;background:var(--surface)}
.sc b{display:block;font-size:1.9rem;font-variant-numeric:tabular-nums;color:var(--c);line-height:1.2}.sc span{font-size:var(--chip);color:var(--ink-2)}
.say{line-height:1.95;color:var(--ink-2);min-height:3.6em}
table.tb{border-collapse:collapse;width:100%;font-size:var(--small)}table.tb td,table.tb th{padding:8px 6px;border-bottom:1px solid var(--line);text-align:start}
table.tb td:last-child{font-weight:800;font-variant-numeric:tabular-nums}
.bar2{display:block;height:10px;border-radius:5px;background:var(--c)}
label.sl{display:grid;gap:4px;font-size:var(--small);color:var(--ink-2);margin:12px 0}label.sl b{color:var(--ink)}label.sl output{color:var(--c);font-weight:800}
.pay{display:grid;grid-template-columns:auto 1fr 1fr;gap:6px;max-width:420px;font-size:var(--small);margin:8px 0}
.pay div{border:1px solid var(--line);border-radius:var(--r-md);padding:8px;text-align:center;background:var(--surface)}.pay .h{border:0;background:none;color:var(--ink-3)}
.key{font-size:var(--chip);color:var(--ink-2)}.key i{display:inline-block;width:11px;height:11px;border-radius:3px;vertical-align:-1px;margin-inline:8px 4px}
"""
body = '''<h1>تلافی یا بخشش؟</h1>
<p class="lead">دو نفر، بارها و بارها. هر بار هر کدام می‌تواند <b>بسازد</b> یا <b>بزند</b>. اگر هر دو بسازند هر دو خوب می‌برند؛ اگر یکی بزند و دیگری بسازد، زننده بیشتر می‌برد؛ اگر هر دو بزنند هر دو کم می‌برند. کدام شیوه در درازمدت بهتر است؟</p>
<div class="note r"><b>این بازی دربارهٔ دو طرفِ هم‌زور است،</b> مثل دو همسایه، دو همکار، دو گروه. دربارهٔ رابطه‌ای که در آن یکی بر دیگری قدرت دارد و او را می‌ترساند نیست. «بخشش» در این بازی به معنای ماندن کنار کسی که آزار می‌دهد نیست؛ آن‌جا موضوع ایمنی است.</div>
<div class="pay"><div class="h"></div><div class="h">او می‌سازد</div><div class="h">او می‌زند</div><div class="h">من می‌سازم</div><div>هر دو ۳</div><div>من ۰، او ۵</div><div class="h">من می‌زنم</div><div>من ۵، او ۰</div><div>هر دو ۱</div></div>
<section><h2>۱. دو شیوه را روبه‌روی هم بگذار</h2>
<div class="grid2"><div>
<p class="key" style="margin:0 0 6px">شیوهٔ من</p><div class="row" id="pa"></div>
<p class="key" style="margin:12px 0 6px">شیوهٔ او</p><div class="row" id="pb"></div>
<label class="sl"><b>سوءتفاهم: <output id="on"></output>٪</b><input type="range" id="noise" min="0" max="15" step="1" value="0">گاهی کسی می‌خواهد بسازد و کارش ناخواسته ضربه از آب درمی‌آید، یا چنین فهمیده می‌شود. در زندگی واقعی این صفر نیست.</label>
</div><div>
<div class="who"><b>من</b><span>هر خانه یک نوبت، از چپ به راست</span></div><div class="strip" id="sa"></div>
<div class="who"><b>او</b><span></span></div><div class="strip" id="sb"></div>
<p class="key"><i style="background:var(--vr)"></i>ساخت<i style="background:var(--vh)"></i>زد<i style="outline:2px solid var(--va);background:none"></i>سوءتفاهم</p>
<div class="sc"><div><b id="ta"></b><span>امتیاز من در ۴۰ نوبت</span></div><div><b id="tb2"></b><span>امتیاز او</span></div></div>
<p class="say" id="say"></p></div></div></section>
<section><h2>۲. اگر همه مثل هم بودند</h2>
<p class="lead">جامعه‌ای را تصور کن که همه یک شیوه دارند. با همان درصد سوءتفاهم بالا، میانگین امتیاز هر نفر در هر نوبت (بهترینِ ممکن ۳ است):</p>
<table class="tb" id="self"></table></section>
<section><h2>۳. همه با همه</h2>
<p class="lead">حالا شیوه‌ها قاطی‌اند و هر کدام با همه (و با خودش) بازی می‌کند. چه کسانی در این جمع باشند؟</p>
<div class="row" id="pop"></div>
<table class="tb" id="tour" style="margin-top:12px"></table>
<p class="say" id="say2"></p></section>
<section><h2>چه چیزی را ببینی</h2>
<p class="lead">۱. سوءتفاهم را روی صفر بگذار: هر جمعی که «همیشه بزن» در آن نباشد، به بهترین نتیجه می‌رسد. مشکل از جایی شروع می‌شود که آدم‌ها گاهی اشتباه می‌کنند.</p>
<p class="lead">۲. سوءتفاهم را روی ۵ درصد بگذار و بخش ۲ را ببین. جامعهٔ «کینه» تقریباً همه‌چیز را از دست می‌دهد: یک اشتباه، و تا ابد زدن. جامعهٔ «یکی به یکی» در زنجیرهٔ تلافی گیر می‌کند. جامعهٔ «یکی به یکی، با بخشش» نزدیکِ بهترین می‌ماند، چون گاهی یک ضربه را بی‌جواب می‌گذارد.</p>
<p class="lead">۳. حالا بخش ۳، و این قسمتِ ناخوشایند ماجراست: تا وقتی «همیشه بساز» در جمع هست، «کینه» و «همیشه بزن» بالا می‌آیند، چون از او سواری می‌گیرند. او را از جمع بردار و دوباره ببین. بخششِ بی‌حساب، ناخواسته به زننده‌ها سود می‌رساند؛ بخششی کار می‌کند که مرز هم دارد.</p>
<p class="note g">منبع: مسابقه‌های رابرت اکسلرود (The Evolution of Cooperation، ۱۹۸۴) و کارهای بعدی دربارهٔ سوءتفاهم و «یکی به یکیِ بخشنده» (Nowak & Sigmund، ۱۹۹۲). عددهای این صفحه را همین شبیه‌ساز می‌سازد، نه آن پژوهش‌ها؛ با امتیازهای دیگر نتیجه‌ها جابه‌جا می‌شوند. <a href="../entries.html#violence-epidemic">مدخل: سرایت و زنجیرهٔ تلافی</a></p></section>
'''
js = r'''
const ST={ac:["همیشه بساز",(m,o)=>0],tft:["یکی به یکی",(m,o)=>o.length?o[o.length-1]:0],gtft:["یکی به یکی، با بخشش",(m,o,r)=>o.length&&o[o.length-1]?(r()<.33?0:1):0],grim:["کینه: یک بار بزنی، تا ابد می‌زنم",(m,o)=>o.includes(1)?1:0],ad:["همیشه بزن",(m,o)=>1]};
const K=Object.keys(ST);let A="tft",B="tft";const POP=new Set(K);
function rng(s){return()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}}
function play(a,b,n,noise,seed){const r=rng(seed),ha=[],hb=[],sa=[],sb=[],ea=[],eb=[];let pa=0,pb=0;
for(let i=0;i<n;i++){let x=ST[a][1](ha,sb,r),y=ST[b][1](hb,sa,r);ha.push(x);hb.push(y);
let fx=r()<noise,fy=r()<noise;const seenx=fx?1-x:x,seeny=fy?1-y:y;sa.push(seenx);sb.push(seeny);ea.push(fx);eb.push(fy);
pa+=seenx?(seeny?1:5):(seeny?0:3);pb+=seeny?(seenx?1:5):(seenx?0:3)}
return{sa,sb,ea,eb,pa,pb}}
function btns(id,cur,set){$(id).innerHTML=K.map(k=>'<button class="pb" data-k="'+k+'" aria-pressed="'+(k===cur)+'">'+ST[k][0]+'</button>').join("");
$(id).onclick=e=>{const b=e.target.closest("button");if(!b)return;set(b.dataset.k);draw()}}
function draw(){btns("pa",A,k=>A=k);btns("pb",B,k=>B=k);const nz=+$("noise").value/100;$("on").textContent=fa($("noise").value);
const g=play(A,B,40,nz,12345);const strip=(s,e)=>s.map((v,i)=>'<i class="'+(v?"d":"")+(e[i]?" x":"")+'"></i>').join("");
$("sa").innerHTML=strip(g.sa,g.ea);$("sb").innerHTML=strip(g.sb,g.eb);$("ta").textContent=fa(g.pa);$("tb2").textContent=fa(g.pb);
const hits=g.sa.filter(Boolean).length+g.sb.filter(Boolean).length;
$("say").textContent=hits===0?"چهل نوبت ساختن. بیشترین چیزی که دو نفر با هم می‌توانند ببرند: ۱۲۰.":hits>60?"تقریباً همه‌اش زدن. هر دو کمتر از یک‌سومِ آنچه می‌شد بردند.":nz>0&&hits>6?"به خانه‌های نارنجی نگاه کن: یک سوءتفاهم، و بعد زنجیرهٔ تلافی.":"چند ضربه، و بعد برگشتن به ساختن.";
const avg=(a,pop)=>{let t=0,c=0;pop.forEach((b,j)=>{for(let s=1;s<=6;s++){const q=play(a,b,200,nz,s*977+j*31);t+=q.pa;c+=200}});return t/c};
const row=(r,i)=>'<tr><td>'+fa(i+1)+'</td><td>'+ST[r[0]][0]+'</td><td style="width:40%"><span class="bar2" style="width:'+(r[1]/3*100).toFixed(0)+'%"></span></td><td>'+fa(r[1].toFixed(2))+'</td></tr>';
$("self").innerHTML=K.map(a=>[a,avg(a,[a])]).sort((x,y)=>y[1]-x[1]).map(row).join("");
$("pop").innerHTML=K.map(k=>'<button class="pb" data-k="'+k+'" aria-pressed="'+POP.has(k)+'">'+ST[k][0]+'</button>').join("");
const pop=K.filter(k=>POP.has(k));const res=pop.map(a=>[a,avg(a,pop)]).sort((x,y)=>y[1]-x[1]);
$("tour").innerHTML=res.map(row).join("");
$("say2").textContent="در این جمع و با "+fa($("noise").value)+" درصد سوءتفاهم، بالاترین میانگین را «"+ST[res[0][0]][0]+"» گرفت. آدم‌های جمع را عوض کن و ببین رتبه‌ها چطور جابه‌جا می‌شوند."}
$("pop").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;const k=b.dataset.k;if(POP.has(k)){if(POP.size>2)POP.delete(k)}else POP.add(k);draw()});
$("noise").addEventListener("input",draw);draw();
'''
page('violence-titfortat', 'تلافی یا بخشش؟ بازی تکرارشونده', 'شبیه‌ساز دوراهی زندانیِ تکرارشونده: پنج شیوه از «همیشه بساز» تا «کینه»، با سوءتفاهم. چرا تلافیِ بی‌بخشش هر دو طرف را می‌سوزاند.', css, body, js)
