(function(){
"use strict";
const W=window.WIKI, V=window.VIDEOS||[], R=window.REFS||{};
const view=document.getElementById('view');
const A={}, P={}, D={};
W.articles.forEach(a=>A[a.id]=a); W.people.forEach(p=>P[p.id]=p); W.domains.forEach(d=>D[d.id]=d);
const VT={}; V.forEach(v=>VT[v.id]=v);
const FA=n=>String(n).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d]);
const fmt=n=>FA(Math.round(n).toLocaleString('en-US').replace(/,/g,'٬'));
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const hms=s=>{const h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;return FA(h?`${h}:${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`:`${m}:${String(x).padStart(2,'0')}`)};
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
let tip=document.createElement('div');tip.className='tip';document.body.appendChild(tip);
function showTip(e,html){tip.innerHTML=html;tip.style.opacity=1;const x=Math.min(e.clientX+12,innerWidth-290);tip.style.left=x+'px';tip.style.top=(e.clientY+14)+'px'}
function hideTip(){tip.style.opacity=0}
function href(id){return A[id]?'#/a/'+id:(P[id]?'#/p/'+id:null)}
function label(id){return A[id]?A[id].t:(P[id]?P[id].n:id)}
function linkify(t){return esc(t).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,id,lab)=>{const h=href(id);return h?`<a class="wl" href="${h}">${lab||label(id)}</a>`:(lab||id)}).replace(/\(؟\)/g,'<span class="chip" title="نیازمند تأیید منبع">؟</span>')}
function setNav(){document.querySelectorAll('#nav details[open]').forEach(d=>d.removeAttribute('open'));const h=location.hash||'#/';document.querySelectorAll('#nav a').forEach(a=>{const r=a.getAttribute('href');a.classList.toggle('on',r==='#/'?h==='#/'||h==='':h.startsWith(r))})}
function head(eyebrow,title,lede){return `<div class="eyebrow">${eyebrow}</div><h1>${title}</h1>${lede?`<p class="lede">${lede}</p>`:''}`}
const ERA_LINK=id=>`../index.html#era-${id}`;
const yrs=y=>y>=1e6?FA((y/1e6).toFixed(y>=1e7?0:1))+' میلیون سال پیش':y>=1e4?fmt(y/1000)+' هزار سال پیش':fmt(y)+' سال پیش';

/* ============ HOME ============ */
function home(){
  const nA=W.articles.length,nP=W.people.length,nG=allGaps().length;
  const tools=[["#/lithics","جعبه‌ابزار سنگی","پنج سنت ابزارسازی از الدوانی تا ریزسنگ‌ها: چه کسی، چطور، و در کدام غار ایران."],["#/gen","نسل‌ها","فاصلهٔ تو تا هر رویداد، نه به سال، که به نسل: مادرِ مادرِ مادر…"],["#/genes","ژن‌های باستانی درون تو","چند درصد ژنوم هر گروه انسانی از نئاندرتال‌ها و دنیسووایی‌هاست، و چه ژن‌هایی از آن‌ها مانده."],["#/mtree","درخت مادری","درخت هاپلوگروه‌های میتوکندری از آفریقا تا آمریکا؛ هر شاخه نمونه‌های باستانی‌اش را روی نقشه نشان می‌دهد."],["#/graph","شبکهٔ دانش","همهٔ مقاله‌ها و دانشمندان و پیوندهایشان؛ با نمای درخت شعاعی."],["#/coexist","هم‌روزگاری","کدام انسان‌ها هم‌زمان روی زمین بودند؟ نوار زمان را بکش."],["#/migrate","نقشهٔ مهاجرت","از آفریقا تا آمریکا؛ گام‌به‌گام در زمان."],["#/brain","اندازهٔ مغز","حجم مغز هر گونهٔ انسان در طول ۷ میلیون سال، و مقایسهٔ دوبه‌دوی گونه‌ها."],["#/iran","ایران پارینه‌سنگی","محوطه‌های ایران روی نقشه و در یک نمودار زمانی: نئاندرتال‌ها و انسان خردمند در زاگرس."],["#/sites","محوطه‌های پارینه‌سنگی","۷۷۱ محوطه از آفریقا تا آسیای مرکزی در پایگاه ROAD؛ از ۳٫۵ میلیون سال پیش تا نوسنگی."],["#/c14","نقشهٔ رادیوکربن","۱۱۴۸ محوطهٔ تاریخ‌گذاری‌شدهٔ جنوب‌غرب آسیا، از یخبندان تا عصر مفرغ."],["#/dna","نقشهٔ DNA باستانی","۱۷ هزار ژنوم باستانی؛ و ۱۴۹ نمونهٔ ایران."],["#/clocks","کدام ساعت؟","روش‌های سن‌یابی برای هر سن و ماده، شبیه‌ساز کربن-۱۴، و خواندن لایه‌های یک غار."],["#/dom","اهلی‌سازی","سگ، بز، گندم، گاو و… کجا و کی اهلی شدند."],["#/clock","ساعت زمین","اگر تاریخ زمین یک شبانه‌روز بود، انسان کی رسید؟"],["#/quiz","افسانه یا واقعیت","ده جمله دربارهٔ فرگشت؛ درست یا نادرست؟"]];
  const bands=W.domains.map(d=>{const arts=W.articles.filter(a=>a.d===d.id);return `<div class="band"><div><h3><span class="dot" style="background:${d.color}"></span>${d.name}</h3><p>${d.desc}</p></div><div class="rows">${arts.map(a=>`<a href="#/a/${a.id}">${a.t}<span class="k">${a.k}</span></a>`).join('')}</div></div>`}).join('');
  view.innerHTML=`<section class="hero"><div>${head('ویکی فارسی تبارشناسی انسان','ویکی تبار','از نیای مشترک ما و شامپانزه تا نخستین روستاهای زاگرس. مقاله‌ها موضوعی‌اند و هر کدام به لحظهٔ دقیق ویدیوهای خداحافظ آفریقا و پادکست رخ لینک می‌شوند.')}
   <div class="stats"><span><b>${FA(nA)}</b> مقاله</span><span><b>${FA(nP)}</b> دانشمند و نویسنده</span><span><b>${FA(V.length)}</b> ویدیو با متن کامل</span><span><b>${FA(nG)}</b> جای خالی</span></div>
   <div class="ctrl" style="margin-top:16px"><a class="btn" href="#/a/hominins">از اینجا شروع کن: انسان‌تباران</a><a class="btn" href="archive.html">آرشیو متن ویدیوها</a></div></div>
   <div id="heroTree"></div></section>
   <section class="sec"><header><h2>مسیرهای خواندن</h2><p>اگر نمی‌دانی از کجا شروع کنی، یکی از این‌ها را دنبال کن.</p></header><div class="paths">${(W.paths||[]).map(pathCard).join('')}</div></section>
   <section class="sec"><header><h2>ابزارها</h2><p>هر ابزار از داده‌های واقعی یا مقاله‌های همین ویکی ساخته شده است.</p></header><div class="tools">${tools.map(t=>`<a class="tool" href="${t[0]}"><b>${t[1]}</b><span>${t[2]}</span></a>`).join('')}</div></section>
   <section class="sec"><header><h2>شش قلمرو</h2><p>هر مقاله در یک قلمرو است و به مقاله‌های قلمروهای دیگر پیوند دارد.</p></header>${bands}</section>`;
  heroTree(document.getElementById('heroTree'));
}
const GC={early:'#b0652a',aus:'#7a7a2a',homo:'#4867a8',sap:'#a8404f'};
const GN={early:'نخستین انسان‌تباران',aus:'استرالوپیتکوس‌ها',homo:'سردهٔ انسان',sap:'انسان خردمند'};
function grpOf(a){return a.id==='homo-sapiens'?'sap':/^homo|dmanisi|naledi|floresiensis|neanderthal|denisovan/.test(a.id)?'homo':/australo|paranthropus|kenyan/.test(a.id)?'aus':'early'}
function heroTree(el){
  const sp=W.articles.filter(a=>a.from!=null&&a.k==='گونه').sort((a,b)=>b.from-a.from);
  // drawn at the box's real width so names stay ~12px on phones (a fixed 620-wide drawing shrank them to ~6px)
  const w=Math.max(300,Math.min(760,el.clientWidth||620)),rh=w<480?19:17,top=26,h=top+sp.length*rh+40,lab=w<480?128:150,pad=14;
  const x=d3.scaleLog().domain([8e6,1e4]).range([w-lab,pad]);
  let s=`<svg class="bush" viewBox="0 0 ${w} ${h}" role="img" aria-label="بوتهٔ انسان‌تباران">`;
  [[7e6,'۷ میلیون'],[1e6,'۱ میلیون'],[1e5,'۱۰۰ هزار'],[1e4,w<480?'۱۰ هزار':'۱۰ هزار سال پیش']].forEach(([v,l])=>s+=`<line x1="${x(v)}" x2="${x(v)}" y1="${top-8}" y2="${h-30}" class="bgrid"/><text class="svgmuted" x="${x(v)}" y="${h-12}" font-size="10.5" direction="rtl" text-anchor="${v===1e4?'end':'middle'}">${l}</text>`);
  sp.forEach((a,i)=>{const g=grpOf(a),y=top+i*rh,x1=x(a.from*1e6),x2=x(Math.max(a.to*1e6,1.1e4)),c=GC[g];
    s+=`<a href="#/a/${a.id}" class="bl"><title>${a.t}</title><rect x="${x2}" y="${y-5}" width="${Math.max(6,x1-x2)}" height="10" rx="5" fill="${c}" style="--d:${i*40}ms"/><text class="svgtext" x="${w-pad}" y="${y+4}" font-size="11.5" text-anchor="start" direction="rtl">${a.t.replace(/ \(.*\)/,'')}</text></a>`});
  const xs=x(3e5);s+=`<text x="${xs}" y="${top-12}" font-size="10.5" class="svgmuted" text-anchor="middle">ما از اینجا ↓</text>`;
  s+=`</svg><div class="legend" style="justify-content:center">${Object.keys(GC).map(k=>`<span><span class="dot" style="background:${GC[k]}"></span>${GN[k]}</span>`).join('')}</div>`;
  el.innerHTML=s;
}

/* ============ ARTICLE ============ */
function passport(a){
  if(a.from==null||a.k!=='گونه'&&a.k!=='محوطه'&&a.k!=='رویداد'&&a.k!=='مفهوم'||a.from>10)return '';
  const w=620,x=d3.scaleLog().domain([8e6,1e4]).range([w-14,14]);const x1=x(a.from*1e6),x2=x(Math.max((a.to||0)*1e6,1.1e4));
  const c=a.k==='گونه'?GC[grpOf(a)]:D[a.d].color;
  const peers=W.articles.filter(b=>b.k==='گونه'&&b.from!=null&&b.id!==a.id);
  let s=`<figure class="pass"><svg viewBox="0 0 ${w} 74" role="img" aria-label="جای این موضوع در ۷ میلیون سال">`;
  peers.forEach(b=>{s+=`<rect x="${x(Math.max((b.to||0)*1e6,1.1e4))}" y="22" width="${Math.max(3,x(b.from*1e6)-x(Math.max((b.to||0)*1e6,1.1e4)))}" height="6" rx="3" class="ghost"/>`});
  s+=`<rect x="${x2}" y="16" width="${Math.max(8,x1-x2)}" height="18" rx="9" fill="${c}"/>`;
  [[7e6,'۷ میلیون'],[1e6,'۱ میلیون'],[1e5,'۱۰۰ هزار'],[1e4,'امروز']].forEach(([v,l])=>s+=`<text x="${x(v)}" y="58" font-size="11" class="svgmuted" text-anchor="middle">${l}</text>`);
  s+=`</svg>`;
  if(a.brain){const m=(a.brain[0]+a.brain[1])/2;s+=`<figcaption><svg viewBox="0 0 60 60" width="46" height="46" aria-hidden="true"><circle cx="30" cy="30" r="28" class="ghostc"/><circle cx="30" cy="30" r="${(Math.sqrt(m/1350)*28).toFixed(1)}" fill="${c}"/></svg><span>مغز ${FA(a.brain[0])}–${FA(a.brain[1])} سی‌سی؛ حدود ${FA(Math.round(m/1350*100))}٪ انسان امروز (دایرهٔ کم‌رنگ). <a href="#/brain">مقایسه ←</a></span></figcaption>`}
  else s+=`<figcaption><span>نوار پررنگ: ${a.to?`${yrs(a.from*1e6)} تا ${yrs(a.to*1e6)}`:`از ${yrs(a.from*1e6)}`}؛ نوارهای کم‌رنگ: گونه‌های دیگر انسان.</span></figcaption>`;
  return s+`</figure>`;
}
function drawMini(){document.querySelectorAll('.minimap').forEach(el=>{const lon=+el.dataset.lon,lat=+el.dataset.lat,w=320,h=200;
  const svg=d3.select(el).append('svg').attr('viewBox',`0 0 ${w} ${h}`);const proj=d3.geoNaturalEarth1?d3.geoNaturalEarth1():d3.geoMercator();
  proj.rotate([-lon,0]).fitExtent([[4,4],[w-4,h-4]],{type:'MultiPoint',coordinates:[[lon-60,Math.max(-60,lat-38)],[lon+60,Math.min(75,lat+38)]]});baseMap(svg,proj,w,h);
  const p=proj([lon,lat]);svg.append('circle').attr('cx',p[0]).attr('cy',p[1]).attr('r',14).attr('fill',el.dataset.c).attr('opacity',.18).attr('class','pulse');
  svg.append('circle').attr('cx',p[0]).attr('cy',p[1]).attr('r',5).attr('fill',el.dataset.c).attr('stroke',css('--card')).attr('stroke-width',2)})}
function pathNav(id,bottom){
  const ps=(W.paths||[]).filter(p=>p.steps.includes(id));if(!ps.length)return '';
  return ps.map(p=>{const i=p.steps.indexOf(id),prev=p.steps[i-1],next=p.steps[i+1];
    return `<nav class="pnav${bottom?' bottom':''}" style="--pc:${p.c}" aria-label="مسیر ${esc(p.t)}"><a class="pt" href="#/path/${p.id}">مسیر: ${esc(p.t)} · ${FA(i+1)} از ${FA(p.steps.length)}</a>
    <span class="pdots">${p.steps.map((s,k)=>`<a href="#/a/${s}" title="${esc(label(s))}" class="${k===i?'on':''}"></a>`).join('')}</span>
    <span class="pnx">${prev?`<a href="#/a/${prev}">→ ${esc(label(prev))}</a>`:''}${next?`<a href="#/a/${next}">${esc(label(next))} ←</a>`:''}</span></nav>`}).join('');
}
function pathPage(id){
  const ps=W.paths||[];const p=ps.find(x=>x.id===id);
  if(!p){view.innerHTML=head('','مسیرهای خواندن','هر مسیر چند مقاله را به ترتیبی می‌چیند که داستانی کامل بسازند. از هر جا خواستی شروع کن.')+`<div class="paths">${ps.map(pathCard).join('')}</div>`;return}
  view.innerHTML=head('مسیر خواندن',esc(p.t),esc(p.d))+`<ol class="trail" style="--pc:${p.c}">${p.steps.map((s,k)=>{const a=A[s];return a?`<li><a href="#/a/${s}"><span class="n">${FA(k+1)}</span><b>${a.t}</b><span>${esc(a.sum)}</span></a></li>`:''}).join('')}</ol>`;
}
function pathCard(p){return `<a class="pathc" href="#/path/${p.id}" style="--pc:${p.c}"><b>${esc(p.t)}</b><span>${esc(p.d)}</span><span class="pdots">${p.steps.map(()=>'<i></i>').join('')}</span><small>${FA(p.steps.length)} ایستگاه</small></a>`}

function srcBox(id){const bs=W.books.filter(b=>(b.on||[]).includes(id));return bs.length?`<div class="box"><h4>منابع در کتابخانه</h4><ul class="srcl">${bs.map(b=>`<li><b>${esc(b.t)}</b><br><small>${esc(b.a||'')}</small> <span class="${b.have?'have':'need'}">${b.have?'دارم':'لازم'}</span></li>`).join('')}</ul></div>`:''}
function article(id){
  const a=A[id]; if(!a) return notFound();
  const d=D[a.d], refs=R[id]||[];
  const people=W.people.filter(p=>(p.rel||[]).includes(id));
  const backs=W.articles.filter(x=>x.id!==id&&((x.rel||[]).includes(id)||x.body.join(' ').includes('[['+id)));
  view.innerHTML=`<div class="eyebrow"><a href="#/" style="color:inherit">ویکی تبار</a> › <span class="dot" style="background:${d.color}"></span>${d.name}</div>
  <h1>${a.t}</h1><p class="lede"><span class="latin">${esc(a.en)}</span> · <span class="chip">${a.k}</span></p>
  ${pathNav(id)}<div class="art" style="margin-top:18px"><div class="body">${passport(a)}<p><b>${linkify(a.sum)}</b></p>${a.body.map(p=>`<p>${linkify(p)}</p>`).join('')}
   <section class="sec" style="margin-top:28px"><header><h3>در ویدیوها</h3><p>بندهایی از متن ویدیوها که این موضوع در آن‌ها آمده؛ روی زمان بزن تا از همان لحظه پخش شود.</p></header>
   ${refs.length?`<ul class="refs">${refs.map(r=>`<li><a class="ts" href="https://youtu.be/${r[0]}?t=${r[1]}" target="_blank" rel="noopener">${hms(r[1])}</a>…${esc(r[2])}…<span class="vt">${esc((VT[r[0]]||{}).t||'')}</span></li>`).join('')}</ul>`:'<p class="gap">هنوز بندی از ویدیوها برای این موضوع پیدا نشده. اگر ویدیو یا متنی دربارهٔ آن داری بفرست.</p>'}
   </section></div>
   <aside class="side">
    ${a.loc?`<div class="box"><h4>کجا</h4><div class="minimap" data-lon="${a.loc[0]}" data-lat="${a.loc[1]}" data-c="${d.color}"></div></div>`:''}
    ${a.facts&&a.facts.length?`<div class="box"><h4>واقعیت‌ها</h4><dl class="facts">${a.facts.map(f=>`<div><dt>${f[0]}</dt><dd>${linkify(f[1])}</dd></div>`).join('')}</dl></div>`:''}
    ${a.era||a.from!=null?`<div class="box"><h4>در اطلس زمین</h4><a class="btn" href="${ERA_LINK(a.era||eraFor(a))}">نمایش روی نوار زمان ↗</a></div>`:''}
    ${(a.rel||[]).length?`<div class="box"><h4>مرتبط</h4><div class="rows">${a.rel.map(r=>href(r)?`<a href="${href(r)}">${label(r)}</a>`:'').join('')}</div></div>`:''}
    ${backs.length?`<div class="box"><h4>به اینجا پیوند داده‌اند</h4><div class="rows">${backs.map(x=>`<a href="#/a/${x.id}">${x.t}</a>`).join('')}</div></div>`:''}
    ${people.length?`<div class="box"><h4>آدم‌ها</h4><div class="rows">${people.map(p=>`<a href="#/p/${p.id}">${p.n}</a>`).join('')}</div></div>`:''}
    ${srcBox(id)}
    ${(a.gaps||[]).length?`<div class="gap"><h4>جای خالی — اگر پیدا کردی بفرست</h4><ul>${a.gaps.map(g=>`<li>${esc(g)}</li>`).join('')}</ul></div>`:''}
   </aside></div>${pathNav(id,true)}`;
  drawMini();
}
function eraFor(a){const y=(a.from||0)*1e6; if(y>=4e6)return 'hominins-split'; if(y>=2.5e6)return 'australopiths'; if(y>=1e6)return 'erectus-out'; if(y>=2e5)return 'neanderthal-world'; return 'sapiens-spread'}
function person(id){
  const p=P[id]; if(!p) return notFound();
  view.innerHTML=`<div class="eyebrow"><a href="#/people" style="color:inherit">دانشمندان و نویسندگان</a></div><h1>${p.n}</h1><p class="lede"><span class="latin">${esc(p.en)}</span> · ${p.y}</p>
  <div class="art" style="margin-top:18px"><div class="body"><p><b>${esc(p.role)}</b></p><p>${linkify(p.sum)}</p></div>
  <aside class="side">${(p.rel||[]).length?`<div class="box"><h4>در ویکی</h4><div class="rows">${p.rel.map(r=>`<a href="${href(r)}">${label(r)}</a>`).join('')}</div></div>`:''}
  ${(()=>{const bs=W.books.filter(b=>b.by===id);return bs.length?`<div class="box"><h4>آثار در کتابخانه</h4><ul class="srcl">${bs.map(b=>`<li>${esc(b.t)} <span class="${b.have?'have':'need'}">${b.have?'دارم':'لازم'}</span></li>`).join('')}</ul></div>`:''})()}
  ${(p.gaps||[]).length?`<div class="gap"><h4>جای خالی</h4><ul>${p.gaps.map(g=>`<li>${esc(g)}</li>`).join('')}</ul></div>`:''}</aside></div>`;
}
function notFound(){view.innerHTML=head('','این صفحه پیدا نشد','<a href="#/">بازگشت به خانه</a>')}

/* ============ GRAPH ============ */
function graph(){
  view.innerHTML=head('ابزار','شبکهٔ دانش','هر دایره یک مقاله یا یک دانشمند است و رنگش قلمرو را نشان می‌دهد. اندازهٔ هر دایره، شمار پیوندهای آن است. نشانگر را روی یک گره ببر تا همسایه‌هایش روشن شوند؛ بزن تا مقاله باز شود. با چرخ موس یا دو انگشت بزرگ کن تا نام‌های بیشتری پیدا شوند.')+
  `<div class="ctrl"><button id="gNet" class="on">شبکه</button><button id="gRad">درخت شعاعی</button><span class="legend">${W.domains.map(d=>`<span><span class="dot" style="background:${d.color}"></span>${d.name}</span>`).join('')}<span><span class="dot" style="background:var(--muted)"></span>دانشمندان</span></span></div><div class="stage" id="gStage"></div>`;
  const st=document.getElementById('gStage');
  const draw=m=>{st.innerHTML='';m==='net'?drawNet(st):drawRadial(st)};
  document.getElementById('gNet').onclick=e=>{e.target.classList.add('on');document.getElementById('gRad').classList.remove('on');draw('net')};
  document.getElementById('gRad').onclick=e=>{e.target.classList.add('on');document.getElementById('gNet').classList.remove('on');draw('rad')};
  draw('net');
}
function drawNet(st){
  // whole network first; names only where they fit (most-linked first); hover lights a node's links; wheel / pinch / drag to wander
  const w=1000,h=680;
  const nodes=[...W.domains.map(d=>({id:'d:'+d.id,t:d.name.split(':')[0],c:d.color,r:16,kind:'d'})),...W.articles.map(a=>({id:a.id,t:a.t,c:D[a.d].color,r:7,kind:'a'})),...W.people.map(p=>({id:p.id,t:p.n,c:css('--muted'),r:6,kind:'p'}))];
  const ids=new Set(nodes.map(n=>n.id)); const L=[]; const add=(s,t)=>{if(ids.has(s)&&ids.has(t)&&s!==t)L.push({source:s,target:t})};
  W.articles.forEach(a=>{add(a.id,'d:'+a.d);(a.rel||[]).forEach(r=>add(a.id,r))}); W.people.forEach(p=>(p.rel||[]).forEach(r=>add(p.id,r)));
  const deg=new Map(); L.forEach(l=>{deg.set(l.source,(deg.get(l.source)||0)+1);deg.set(l.target,(deg.get(l.target)||0)+1)});
  const nbr=new Map(nodes.map(n=>[n.id,new Set([n.id])])); L.forEach(l=>{nbr.get(l.source).add(l.target);nbr.get(l.target).add(l.source)});
  nodes.forEach(n=>{n.deg=deg.get(n.id)||0; if(n.kind!=='d') n.r=4+Math.min(8,Math.sqrt(n.deg)*1.6)});
  const sim=d3.forceSimulation(nodes).force('link',d3.forceLink(L).id(d=>d.id).distance(l=>l.target.kind==='d'||l.source.kind==='d'?80:50).strength(.4))
   .force('charge',d3.forceManyBody().strength(-150)).force('center',d3.forceCenter(w/2,h/2)).force('collide',d3.forceCollide(d=>d.r+4)).force('x',d3.forceX(w/2).strength(.05)).force('y',d3.forceY(h/2).strength(.09)).stop();
  for(let i=0;i<360;i++) sim.tick();
  {const xs=nodes.map(n=>n.x),ys=nodes.map(n=>n.y),x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys),sc=Math.min((w-80)/(x1-x0||1),(h-90)/(y1-y0||1));nodes.forEach(n=>{n.x=40+(n.x-x0)*sc;n.y=55+(n.y-y0)*sc})}
  st.insertAdjacentHTML('beforeend','<div class="gctl"><button type="button" data-z="in" aria-label="بزرگ‌تر">+</button><button type="button" data-z="out" aria-label="کوچک‌تر">−</button><button type="button" data-z="fit">نمای کل</button></div>');
  const svg=d3.select(st).append('svg').attr('viewBox',`0 0 ${w} ${h}`).attr('class','gnet');
  const g=svg.append('g');
  const link=g.append('g').selectAll('line').data(L).join('line').attr('stroke',css('--rule')).attr('vector-effect','non-scaling-stroke')
   .attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
  const node=g.append('g').selectAll('a').data(nodes).join('a').attr('href',d=>d.kind==='d'?null:href(d.id)).attr('class',d=>'gn k-'+d.kind).attr('transform',d=>`translate(${d.x},${d.y})`);
  node.append('title').text(d=>d.t+(d.deg?` · ${FA(d.deg)} پیوند`:''));
  const circ=node.append('circle').attr('r',d=>d.r).attr('fill',d=>d.c).attr('stroke',css('--card')).attr('stroke-width',1.5).attr('vector-effect','non-scaling-stroke');
  const lab=g.append('g').attr('class','glabels').selectAll('text').data(nodes).join('text').attr('x',d=>d.x).attr('y',d=>d.y).attr('text-anchor','middle').attr('class',d=>d.kind==='d'?'svgtext':'svgmuted').attr('font-weight',d=>d.kind==='d'?700:500)
   .style('paint-order','stroke').style('stroke',css('--card')).style('stroke-linejoin','round').text(d=>d.t);
  let k=1;
  const order=[...nodes].sort((a,b)=>(b.kind==='d')-(a.kind==='d')||b.deg-a.deg);
  const declutter=()=>{
    const box=st.getBoundingClientRect(); const taken=[];
    const el=new Map(); lab.each(function(d){el.set(d.id,this)});
    for(const d of order){const t=el.get(d.id); t.style.visibility='visible'; const r=t.getBoundingClientRect();
      const out=r.right<box.left||r.left>box.right||r.bottom<box.top||r.top>box.bottom;
      const hit=taken.some(o=>r.left<o.right+2&&r.right>o.left-2&&r.top<o.bottom&&r.bottom>o.top);
      if(out||hit) t.style.visibility='hidden'; else taken.push(r)}
  };
  const size=()=>{
    lab.attr('font-size',d=>(d.kind==='d'?15:11)/k).attr('dy',d=>-(d.r/Math.sqrt(k))-4/k).style('stroke-width',(3.5/k)+'px');
    circ.attr('r',d=>d.r/Math.sqrt(k));
  };
  let pend=0; const later=()=>{cancelAnimationFrame(pend);pend=requestAnimationFrame(declutter)};
  const zoom=d3.zoom().scaleExtent([1,8]).translateExtent([[0,0],[w,h]]).on('zoom',e=>{g.attr('transform',e.transform);k=e.transform.k;size();later()});
  svg.call(zoom).on('dblclick.zoom',null);
  st.querySelector('.gctl').onclick=e=>{const z=e.target.closest('[data-z]');if(!z)return;const v=z.dataset.z;
    if(v==='fit')svg.transition().duration(350).call(zoom.transform,d3.zoomIdentity);else svg.transition().duration(250).call(zoom.scaleBy,v==='in'?1.6:1/1.6)};
  node.on('mouseenter',(e,d)=>{const near=nbr.get(d.id);svg.classed('focus',true);node.classed('near',n=>near.has(n.id));link.classed('hot',l=>l.source.id===d.id||l.target.id===d.id);
      lab.filter(n=>near.has(n.id)).each(function(){this.style.visibility='visible'});lab.classed('far',n=>!near.has(n.id))})
   .on('mouseleave',()=>{svg.classed('focus',false);node.classed('near',false);lab.classed('far',false);link.classed('hot',false);declutter()});
  size(); declutter(); if(document.fonts) document.fonts.ready.then(declutter);
}
function drawRadial(st){
  const data={name:'تبار',children:[...W.domains.map(d=>({name:d.name.split(':')[0],c:d.color,children:W.articles.filter(a=>a.d===d.id).map(a=>({name:a.t,id:a.id,c:d.color}))})),{name:'دانشمندان',c:css('--muted'),children:W.people.map(p=>({name:p.n,id:p.id,c:css('--muted')}))}]};
  const R0=330,w=900;const root=d3.tree().size([2*Math.PI,R0-110]).separation((a,b)=>(a.parent==b.parent?1:2)/a.depth)(d3.hierarchy(data));
  const svg=d3.select(st).append('svg').attr('viewBox',`${-w/2} ${-w/2} ${w} ${w}`);
  svg.append('g').attr('fill','none').attr('stroke',css('--rule')).selectAll('path').data(root.links()).join('path').attr('d',d3.linkRadial().angle(d=>d.x).radius(d=>d.y));
  const n=svg.append('g').selectAll('g').data(root.descendants()).join('g').attr('transform',d=>`rotate(${d.x*180/Math.PI-90}) translate(${d.y},0)`).style('cursor',d=>d.data.id?'pointer':'default').on('click',(e,d)=>{if(d.data.id)location.hash=href(d.data.id)});
  n.append('circle').attr('r',d=>d.depth===0?6:d.depth===1?5:3.2).attr('fill',d=>d.data.c||css('--ink'));
  n.append('text').attr('class',d=>d.depth===1?'svgtext':'svgmuted').attr('font-size',d=>d.depth===1?12:9.5).attr('font-weight',d=>d.depth===1?700:400)
   .attr('dy','.32em').attr('x',d=>d.x<Math.PI===!d.children?7:-7).attr('text-anchor',d=>d.x<Math.PI===!d.children?'start':'end').attr('transform',d=>d.x>=Math.PI?'rotate(180)':null).text(d=>d.depth?d.data.name:'')
   .style('paint-order','stroke').style('stroke',css('--card')).style('stroke-width','3px');
}

/* ============ COEXIST ============ */
function coexist(){
  view.innerHTML=head('ابزار','هم‌روزگاری','کدام انسان‌ها هم‌زمان روی زمین بودند؟ نوار را بکش؛ گونه‌هایی که در آن لحظه زنده بودند پررنگ می‌شوند. محور زمان لگاریتمی است تا هم میلیون‌ها سال و هم هزاره‌های اخیر دیده شوند.')+
  `<div class="stage"><div id="cx"></div><div class="ctrl"><span>زمان:</span><input type="range" id="cxr" min="0" max="1000" value="930"><span class="read" id="cxv"></span></div><p id="cxl" style="margin:.4rem 0 0"></p></div>`;
  const sp=W.articles.filter(a=>a.from!=null&&a.k==='گونه').sort((a,b)=>b.from-a.from);
  const w=1000,rowH=34,h=sp.length*rowH+60,left=20,right=180;
  const x=d3.scaleLog().domain([7.5e6,2e4]).range([w-right,left]);
  const svg=d3.select('#cx').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  const ticks=[7e6,5e6,3e6,2e6,1e6,5e5,3e5,2e5,1e5,5e4,3e4];
  svg.append('g').selectAll('line').data(ticks).join('line').attr('x1',x).attr('x2',x).attr('y1',10).attr('y2',h-30).attr('stroke',css('--rule'));
  svg.append('g').selectAll('text').data(ticks).join('text').attr('class','svgmuted').attr('font-size',10.5).attr('x',x).attr('y',h-12).attr('text-anchor','middle').text(t=>t>=1e6?FA(t/1e6)+' م':FA(t/1e3)+' هـ');
  const g=svg.append('g').selectAll('g').data(sp).join('a').attr('href',d=>'#/a/'+d.id);
  g.append('rect').attr('x',d=>x(Math.max(d.to*1e6,2e4))).attr('width',d=>Math.max(6,x(d.from*1e6)-x(Math.max(d.to*1e6,2e4)))).attr('y',(d,i)=>14+i*rowH).attr('height',rowH-12).attr('rx',8).attr('fill',d=>D[d.d].color).attr('class','bar');
  g.append('text').attr('class','svgtext').attr('font-size',12.5).attr('direction','rtl').attr('text-anchor','start').attr('x',w-8).attr('y',(d,i)=>14+i*rowH+(rowH-12)/2+4).text(d=>d.t);
  const cur=svg.append('line').attr('y1',6).attr('y2',h-28).attr('stroke',css('--ink')).attr('stroke-width',2);
  const r=document.getElementById('cxr');
  const upd=()=>{const t=Math.exp(Math.log(7.5e6)+(Math.log(2e4)-Math.log(7.5e6))*r.value/1000);cur.attr('x1',x(t)).attr('x2',x(t));
    const alive=sp.filter(s=>s.from*1e6>=t&&Math.max(s.to*1e6,0)<=t);
    svg.selectAll('.bar').attr('opacity',d=>alive.includes(d)?1:.25);
    document.getElementById('cxv').textContent=yrs(t);
    document.getElementById('cxl').innerHTML=alive.length?`<b>${FA(alive.length)} گونه</b> در این زمان: `+alive.map(a=>`<a href="#/a/${a.id}">${a.t}</a>`).join('، '):'در این لحظه هیچ‌کدام از گونه‌های این فهرست ثبت نشده‌اند.'};
  r.oninput=upd;upd();
}

/* ============ MAP helpers ============ */
function baseMap(svg,proj,w,h){
  const path=d3.geoPath(proj);
  svg.append('rect').attr('width',w).attr('height',h).attr('fill',css('--sea')).attr('rx',8);
  svg.append('path').datum(d3.geoGraticule10()).attr('d',path).attr('fill','none').attr('stroke',css('--landline')).attr('stroke-opacity',.25).attr('stroke-width',.5);
  svg.append('g').selectAll('path').data(window.LAND.features).join('path').attr('d',path).attr('fill',css('--land')).attr('stroke',css('--landline')).attr('stroke-width',.5);
  return path;
}
function playBtn(btn,input,step,ms){let t=null;btn.onclick=()=>{if(t){clearInterval(t);t=null;btn.textContent='پخش';return}btn.textContent='توقف';t=setInterval(()=>{let v=+input.value+step;if(v>+input.max||v<+input.min){clearInterval(t);t=null;btn.textContent='پخش';return}input.value=v;input.oninput()},ms)};return()=>{if(t)clearInterval(t)}}
let cleanup=null;

/* ============ MIGRATE ============ */
const ROUTES=[
 {g:"erectus",c:"#b0652a",n:"انسان راست‌قامت",pts:[[36,1,1900,"شرق آفریقا"],[44.35,41.33,1800,"دمانیسی"],[110.4,-7.4,1500,"جاوه"],[115.9,39.7,770,"ژوکودیان (انسان پکن)"]]},
 {g:"sapiens",c:"#4867a8",n:"انسان خردمند (نخستین گام‌ها)",pts:[[-8.87,31.85,300,"جبل ایرهود"],[36,5,233,"اومو کیبیش"],[35,32.7,185,"میسلیا"],[35.03,32.67,110,"اسخول و قفزه"]]},
 {g:"ooa",c:"#a8404f",n:"خروج اصلی از آفریقا",pts:[[39,9,70,"شاخ آفریقا"],[43.4,12.6,65,"باب‌المندب"],[50,22,60,"عربستان"],[53,33,55,"فلات ایران (پایگاه؟)"],[25.2,43.1,45,"بالکان (باچو کیرو)"],[2,47,42,"اروپای غربی"]]},
 {g:"east",c:"#3f7f6e",n:"به شرق و استرالیا",pts:[[53,33,55,"فلات ایران"],[78,22,52,"هند"],[102,14,50,"جنوب‌شرق آسیا"],[133,-12.5,48,"ساحول (استرالیا)"]]},
 {g:"north",c:"#7a7a2a",n:"به شمال‌شرق و آمریکا",pts:[[102,14,50,"جنوب‌شرق آسیا"],[115.9,39.7,40,"تیان‌یوان"],[130,62,30,"سیبری"],[172,64,25,"برینگیا"],[-106.3,32.8,23,"وایت‌سندز"],[-73,-41.5,14.5,"مونته‌ورده"]]}
];
function migrate(){
  view.innerHTML=head('ابزار','نقشهٔ مهاجرت','نوار زمان را به سوی امروز بکش یا «پخش» را بزن. هر مسیر وقتی آشکار می‌شود که زمانش برسد. سایهٔ قهوه‌ای گسترهٔ تقریبی نئاندرتال‌هاست. خط ساحل امروز است، نه یخبندان.')+
  `<div class="split"><div class="stage"><div id="mg"></div><div class="ctrl"><button id="mgp">پخش</button><input type="range" id="mgr" min="0" max="1000" value="150"><span class="read" id="mgv"></span></div><div class="legend">${ROUTES.map(r=>`<span><span class="dot" style="background:${r.c}"></span>${r.n}</span>`).join('')}</div></div>
  <div class="box list" id="mgl"></div></div>`;
  const w=1000,h=520; const svg=d3.select('#mg').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  const proj=d3.geoEqualEarth().rotate([-40,0]).fitExtent([[6,6],[w-6,h-6]],{type:"Sphere"}); baseMap(svg,proj,w,h);
  const nea=svg.append('ellipse').attr('cx',proj([25,45])[0]).attr('cy',proj([25,45])[1]).attr('rx',150).attr('ry',55).attr('fill','#b0652a').attr('fill-opacity',.18).attr('stroke','#b0652a').attr('stroke-dasharray','4 4');
  const nea2=svg.append('text').attr('class','svgmuted').attr('font-size',11).attr('x',proj([20,52])[0]).attr('y',proj([20,52])[1]).text('نئاندرتال‌ها');
  const lay=svg.append('g');
  const segs=[];ROUTES.forEach(r=>r.pts.forEach((p,i)=>{if(i)segs.push({r,a:r.pts[i-1],b:p})}));
  const line=lay.selectAll('path').data(segs).join('path').attr('fill','none').attr('stroke',d=>d.r.c).attr('stroke-width',2.5).attr('stroke-linecap','round')
   .attr('d',d=>d3.geoPath(proj)({type:'LineString',coordinates:[[d.a[0],d.a[1]],[d.b[0],d.b[1]]]}));
  const pts=[];ROUTES.forEach(r=>r.pts.forEach(p=>pts.push({r,p})));
  const dots=lay.selectAll('g').data(pts).join('g').attr('transform',d=>`translate(${proj([d.p[0],d.p[1]])})`).on('mousemove',(e,d)=>showTip(e,`${d.p[3]}<br>${fmt(d.p[2])} هزار سال پیش`)).on('mouseleave',hideTip);
  dots.append('circle').attr('r',4.5).attr('fill',d=>d.r.c).attr('stroke',css('--card'));
  const sc=d3.scaleLog().domain([2000,12]).range([0,1000]);
  const r=document.getElementById('mgr');
  r.oninput=()=>{const ka=sc.invert(+r.value);document.getElementById('mgv').textContent=yrs(ka*1000);
    line.attr('opacity',d=>d.b[2]>=ka?1:0).each(function(d){const L=this.getTotalLength();d3.select(this).attr('stroke-dasharray',L).attr('stroke-dashoffset',d.b[2]>=ka?0:L)});
    dots.attr('opacity',d=>d.p[2]>=ka?1:0);
    const on=ka<=400&&ka>=40;nea.attr('opacity',on?1:0);nea2.attr('opacity',on?1:0);
    const seen=pts.filter(d=>d.p[2]>=ka).sort((a,b)=>b.p[2]-a.p[2]);
    document.getElementById('mgl').innerHTML=`<table><tr><th>هزار سال پیش</th><th>کجا</th></tr>${seen.map(d=>`<tr><td class="num">${fmt(d.p[2])}</td><td><span class="dot" style="background:${d.r.c}"></span>${d.p[3]}</td></tr>`).join('')}</table>`};
  r.oninput(); cleanup=playBtn(document.getElementById('mgp'),r,8,90);
}

/* ============ C14 ============ */
function c14(){
  view.innerHTML=head('ابزار و داده','نقشهٔ رادیوکربن','هر نقطه یک محوطهٔ باستانی در جنوب‌غرب آسیاست که در پایگاه p3k14c تاریخ رادیوکربن دارد. نوار را بکش: محوطه‌هایی که در آن زمان سکونت داشتند روشن می‌شوند. محوطه‌های ایران با حلقه مشخص‌اند. اعداد «سال پیش از حال» کالیبره‌نشده‌اند.')+
  `<div class="split"><div class="stage"><div id="cm"></div><div class="ctrl"><button id="cmp">پخش</button><input type="range" id="cmr" min="3000" max="16000" step="100" value="7000"><span class="read" id="cmv"></span><label><input type="checkbox" id="cmi"> فقط ایران</label></div></div><div class="box list" id="cml"></div></div>`;
  const data=(window.P3K||[]).map(r=>({n:r[0],c:r[1],lat:r[2],lon:r[3],old:r[4],young:r[5],k:r[6]}));
  const w=1000,h=760;const svg=d3.select('#cm').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  const proj=d3.geoMercator().fitExtent([[0,0],[w,h]],{type:'MultiPoint',coordinates:[[25,12],[75,48]]});baseMap(svg,proj,w,h);
  const g=svg.append('g').selectAll('circle').data(data).join('circle').attr('cx',d=>proj([d.lon,d.lat])[0]).attr('cy',d=>proj([d.lon,d.lat])[1])
    .attr('r',d=>2.5+Math.min(6,Math.sqrt(d.k))).attr('stroke',d=>d.c==='Iran'?css('--ink'):'none').attr('stroke-width',1.2)
    .on('mousemove',(e,d)=>showTip(e,`<b>${esc(d.n)}</b> (${esc(d.c)})<br>${fmt(d.old)} تا ${fmt(d.young)} سال پیش · ${FA(d.k)} تاریخ`)).on('mouseleave',hideTip);
  const r=document.getElementById('cmr'),ir=document.getElementById('cmi');
  r.oninput=ir.onchange=()=>{const t=16000-(+r.value-3000);document.getElementById('cmv').textContent=fmt(t)+' سال پیش';
   const act=d=>d.old>=t-400&&d.young<=t+400&&(!ir.checked||d.c==='Iran');
   g.attr('fill',d=>act(d)?'#a8404f':css('--muted')).attr('fill-opacity',d=>act(d)?.85:(ir.checked&&d.c!=='Iran'?0:.12));
   const on=data.filter(act).sort((a,b)=>b.k-a.k);
   document.getElementById('cml').innerHTML=`<p style="margin:0 0 6px"><b>${FA(on.length)}</b> محوطه در حدود ${fmt(t)} سال پیش</p><table><tr><th>محوطه</th><th>کشور</th><th>بازه</th></tr>${on.slice(0,80).map(d=>`<tr><td class="latin">${esc(d.n)}</td><td class="latin">${esc(d.c)}</td><td class="num">${fmt(d.old/1000)}–${fmt(d.young/1000)} هـ</td></tr>`).join('')}</table>`};
  r.oninput(); cleanup=playBtn(document.getElementById('cmp'),r,100,120);
}


/* ============ ROAD SITES ============ */
function sites(){
  const PN=['پارینه‌سنگی قدیم','پارینه‌سنگی میانه','پارینه‌سنگی جدید','فراپارینه‌سنگی','نوسنگی و پس از آن'];
  const PC=['#b0652a','#3f7f6e','#4867a8','#a8404f','#7a7a2a'];
  view.innerHTML=head('ابزار و داده','محوطه‌های پارینه‌سنگی',`هر نقطه محوطه‌ای است در پایگاه ROAD (دانشگاه توبینگن): غار، پناهگاه صخره‌ای یا محوطهٔ باز با ابزار سنگی، استخوان جانوران یا بقایای انسان. رنگ، کهن‌ترین دورهٔ فرهنگی محوطه است. نوار را بکش تا ببینی در هر زمان کجاها زیسته‌گاه بوده؛ مقیاس زمان لگاریتمی است.`)+
  `<div class="split"><div class="stage"><div id="sm"></div><div class="ctrl"><button id="smp">پخش</button><input type="range" id="smr" min="0" max="1000" value="250"><span class="read" id="smv"></span></div>
  <div class="ctrl" style="flex-wrap:wrap"><label><input type="checkbox" id="smh"> فقط با بقایای انسان</label><label><input type="checkbox" id="sms"> فقط با اشیای نمادین</label><label><input type="checkbox" id="sma"> همهٔ زمان‌ها</label>
  <select id="smc" aria-label="کشور"><option value="">همهٔ کشورها</option></select></div>
  <div class="legend">${PN.map((n,i)=>`<span><span class="dot" style="background:${PC[i]}"></span>${n}</span>`).join('')}<span><span class="dot" style="background:var(--muted)"></span>دوره نامعلوم</span></div></div>
  <div class="box list" id="sml"></div></div>
  <section class="sec"><header><h2>محوطه‌ها بر پایهٔ کشور</h2><p>شمار محوطه‌های این خروجی ROAD؛ رنگ‌ها سهم هر دوره است.</p></header><div id="smbar"></div></section>`;
  const rows=(window.ROAD||[]).map(r=>({n:r[0],c:r[1],lat:r[2],lon:r[3],ty:r[4],p:r[5],a0:r[6],a1:r[7],h:r[8],s:r[9]}));
  const cs=[...new Set(rows.map(d=>d.c))].sort();const sel=document.getElementById('smc');sel.innerHTML+=cs.map(c=>`<option>${esc(c)}</option>`).join('');
  const col=d=>d.p.length?PC[d.p[0]]:css('--muted');
  const w=1000,h=820;const svg=d3.select('#sm').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  const proj=d3.geoMercator().fitExtent([[0,0],[w,h]],{type:'MultiPoint',coordinates:[[-18,-36],[76,46]]});baseMap(svg,proj,w,h);
  const g=svg.append('g').selectAll('circle').data(rows).join('circle').attr('cx',d=>proj([d.lon,d.lat])[0]).attr('cy',d=>proj([d.lon,d.lat])[1])
    .attr('r',d=>d.h?4.6:3.2).attr('fill',col).attr('stroke',d=>d.h?css('--ink'):'none').attr('stroke-width',1)
    .on('mousemove',(e,d)=>showTip(e,`<b class="latin">${esc(d.n)}</b><br>${esc(d.c)} · <span class="latin">${esc(d.ty)}</span><br>${d.a1?`${fmt(d.a0)} تا ${fmt(d.a1)} سال پیش`:'قدمت نامعلوم'}<br>${d.p.map(i=>PN[i]).join('، ')||'دوره نامعلوم'}${d.h?'<br>بقایای انسان':''}${d.s?'<br>اشیای نمادین':''}`)).on('mouseleave',hideTip);
  const sc=d3.scaleLog().domain([3500000,8000]).range([0,1000]);
  const r=document.getElementById('smr'),hh=document.getElementById('smh'),ss=document.getElementById('sms'),aa=document.getElementById('sma');
  const upd=()=>{const t=sc.invert(+r.value);document.getElementById('smv').textContent=aa.checked?'همهٔ زمان‌ها':(t>=1e6?FA((t/1e6).toFixed(2))+' میلیون سال پیش':fmt(t)+' سال پیش');
    const okF=d=>(!hh.checked||d.h)&&(!ss.checked||d.s)&&(!sel.value||d.c===sel.value);
    const okT=d=>aa.checked||(d.a1&&d.a1>=t*0.85&&d.a0<=t*1.15);
    g.attr('opacity',d=>okF(d)&&okT(d)?.9:(okF(d)?.07:0));
    const on=rows.filter(d=>okF(d)&&okT(d)).sort((a,b)=>(b.a1||0)-(a.a1||0));
    document.getElementById('sml').innerHTML=`<p style="margin:0 0 6px"><b>${FA(on.length)}</b> محوطه</p><table><tr><th>محوطه</th><th>کشور</th><th>کهن‌ترین</th></tr>${on.slice(0,120).map(d=>`<tr><td class="latin">${esc(d.n)}${d.h?' ●':''}</td><td class="latin">${esc(d.c)}</td><td class="num">${d.a1?(d.a1>=1e6?FA((d.a1/1e6).toFixed(1))+' م':fmt(d.a1/1000)+' هـ'):'—'}</td></tr>`).join('')}</table>`};
  r.oninput=upd;hh.onchange=ss.onchange=aa.onchange=sel.onchange=upd;upd();cleanup=playBtn(document.getElementById('smp'),r,8,90);
  // stacked bars by country
  const byC=d3.rollups(rows,v=>PN.map((_,i)=>v.filter(d=>d.p[0]===i).length).concat([v.filter(d=>!d.p.length).length]),d=>d.c).sort((a,b)=>d3.sum(b[1])-d3.sum(a[1]));
  const bw=1000,bh=byC.length*22+20,x=d3.scaleLinear().domain([0,d3.max(byC,d=>d3.sum(d[1]))]).range([0,700]);
  const bs=d3.select('#smbar').append('svg').attr('viewBox',`0 0 ${bw} ${bh}`);
  byC.forEach(([c,v],i)=>{let acc=0;v.forEach((n,j)=>{if(!n)return;bs.append('rect').attr('x',bw-200-x(acc+n)).attr('y',i*22+4).attr('width',x(n)).attr('height',16).attr('fill',j<5?PC[j]:css('--muted')).attr('rx',2);acc+=n});
    bs.append('text').attr('x',bw-190).attr('y',i*22+16).attr('class','svgmuted latin').attr('font-size',12).attr('text-anchor','start').attr('direction','ltr').text(c);
    bs.append('text').attr('x',bw-206-x(acc)).attr('y',i*22+16).attr('class','svgmuted').attr('font-size',11).attr('text-anchor','end').text(FA(acc))});
}


/* ============ IRAN ============ */
function iran(){
  const WC={ne:'#b0652a',sa:'#4867a8',er:'#7a7a2a'},WN={ne:'نئاندرتال',sa:'انسان خردمند',er:'انسان راست‌قامت یا پیشین'};
  const sites=W.articles.filter(a=>a.loc&&a.k==='محوطه'&&a.loc[0]>42&&a.loc[0]<63&&a.loc[1]>24&&a.loc[1]<41);
  view.innerHTML=head('ابزار','ایران پارینه‌سنگی',`محوطه‌های پیش‌ازتاریخ ایران و زاگرس که در این ویکی مقاله دارند. رنگ نشان می‌دهد چه انسانی آنجا زیسته؛ دو رنگ یعنی هر دو. نقطه‌های کم‌رنگ محوطه‌های دیگر پایگاه ROAD‌اند. روی هر محوطه بزن تا مقاله‌اش باز شود.`)+
  `<div class="split"><div class="stage"><div id="ir"></div><div class="legend">${Object.keys(WN).map(k=>`<span><span class="dot" style="background:${WC[k]}"></span>${WN[k]}</span>`).join('')}<span><span class="dot" style="background:var(--muted)"></span>نامعلوم / روستا</span></div></div>
  <div class="box list" id="irl"></div></div>
  <section class="sec"><header><h2>چه کسی، کی، کجا</h2><p>هر نوار بازهٔ سکونت یک محوطه است (مقیاس لگاریتمی). نوارهای دورنگ یعنی هم نئاندرتال و هم خردمند. خط‌چین حدود ۴۵ تا ۴۰ هزار سال پیش، زمان هم‌زیستی احتمالی دو گونه در زاگرس است.</p></header><div class="stage" id="irg"></div></section>`;
  const col=a=>{const w=(a.who||'').split(' ').filter(Boolean);return w.length?WC[w[0]]:css('--muted')};
  const w=1000,h=760;const svg=d3.select('#ir').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  const proj=d3.geoMercator().fitExtent([[10,10],[w-10,h-10]],{type:'MultiPoint',coordinates:[[43,25],[62,40]]});baseMap(svg,proj,w,h);
  const road=(window.ROAD||[]).filter(r=>r[3]>42&&r[3]<63&&r[2]>24&&r[2]<41);
  svg.append('g').selectAll('circle').data(road).join('circle').attr('cx',r=>proj([r[3],r[2]])[0]).attr('cy',r=>proj([r[3],r[2]])[1]).attr('r',3).attr('fill',css('--muted')).attr('opacity',.35)
    .on('mousemove',(e,r)=>showTip(e,`<b class="latin">${esc(r[0])}</b> · ROAD`)).on('mouseleave',hideTip);
  const g=svg.append('g').selectAll('g').data(sites).join('g').attr('transform',a=>`translate(${proj(a.loc)})`).style('cursor','pointer').on('click',(e,a)=>location.hash='#/a/'+a.id)
    .on('mousemove',(e,a)=>showTip(e,`<b>${a.t}</b><br>${esc(a.sum).slice(0,140)}…`)).on('mouseleave',hideTip);
  g.append('circle').attr('r',7).attr('fill',col).attr('stroke',css('--card')).attr('stroke-width',1.5);
  g.filter(a=>(a.who||'').includes(' ')).append('path').attr('d',d3.arc()({innerRadius:0,outerRadius:7,startAngle:0,endAngle:Math.PI})).attr('fill',a=>WC[(a.who||'').split(' ')[1]]);
  // readable names: bigger, with a halo; each tries left, right, above, below of its dot and never covers another name or dot
  const nm=a=>a.t.replace(/^(غار|پناهگاه صخره‌ای|اشکفت) /,'');
  const boxes=sites.map(a=>{const p=proj(a.loc);return [p[0]-8,p[1]-8,p[0]+8,p[1]+8]});
  sites.forEach(a=>{const [px,py]=proj(a.loc),wd=nm(a).length*9+6;a._lab=null;
    for(const [dx,dy,an] of [[-11,6,'end'],[11,6,'start'],[0,-12,'middle'],[0,24,'middle']]){const l=an==='end'?px+dx-wd:an==='start'?px+dx:px-wd/2;const bx=[l,py+dy-15,l+wd,py+dy+3];
      if(!boxes.some(b=>bx[0]<b[2]&&bx[2]>b[0]&&bx[1]<b[3]&&bx[3]>b[1])&&bx[0]>4&&bx[2]<w-4){boxes.push(bx);a._lab=[dx,dy,an];break}}});
  g.filter(a=>a._lab).append('text').attr('x',a=>a._lab[0]).attr('y',a=>a._lab[1]).attr('text-anchor',a=>a._lab[2]).attr('direction','ltr').attr('font-size',16).attr('font-weight',600).attr('fill',css('--ink'))
    .style('paint-order','stroke').style('stroke',css('--card')).style('stroke-width','4px').style('stroke-linejoin','round').text(nm);
  document.getElementById('irl').innerHTML=`<p style="margin:0 0 6px"><b>${FA(sites.length)}</b> محوطه با مقاله</p><table><tr><th>محوطه</th><th>انسان</th></tr>${sites.map(a=>`<tr><td><a href="#/a/${a.id}">${a.t}</a></td><td>${(a.who||'').split(' ').filter(Boolean).map(k=>`<span class="dot" style="background:${WC[k]}"></span>`).join(' ')||'—'}</td></tr>`).join('')}</table>`;
  // gantt
  const rows=W.articles.filter(a=>a.span&&(a.d==='iran'||a.loc&&a.loc[0]>42&&a.loc[0]<63)).sort((a,b)=>b.span[0]-a.span[0]);
  const gw=1000,rh=26,gh=rows.length*rh+50,L=220;const x=d3.scaleLog().domain([140000,6000]).range([gw-L,20]);
  const gs=d3.select('#irg').append('svg').attr('viewBox',`0 0 ${gw} ${gh}`);
  [100000,50000,20000,10000].forEach(t=>{gs.append('line').attr('x1',x(t)).attr('x2',x(t)).attr('y1',10).attr('y2',gh-30).attr('stroke',css('--rule'));gs.append('text').attr('x',x(t)).attr('y',gh-12).attr('text-anchor','middle').attr('font-size',11).attr('class','svgmuted').text(fmt(t/1000)+' هزار سال پیش')});
  gs.append('rect').attr('x',Math.min(x(45000),x(40000))).attr('width',Math.abs(x(40000)-x(45000))).attr('y',10).attr('height',gh-40).attr('fill',css('--wash')).attr('stroke',css('--muted')).attr('stroke-dasharray','3 3');
  rows.forEach((a,i)=>{const y=14+i*rh,x0=x(Math.min(a.span[0],140000)),x1=x(Math.max(a.span[1],6000)),ws=(a.who||'').split(' ').filter(Boolean);
    const gg=gs.append('g').style('cursor','pointer').on('click',()=>location.hash='#/a/'+a.id).on('mousemove',e=>showTip(e,`<b>${a.t}</b><br>${fmt(a.span[0])} تا ${fmt(a.span[1])} سال پیش`)).on('mouseleave',hideTip);
    const bx=x1,bw=Math.max(4,x0-x1);
    if(ws.length>1){gg.append('rect').attr('x',bx).attr('y',y).attr('width',bw).attr('height',(rh-8)/2).attr('fill',WC[ws[0]]);gg.append('rect').attr('x',bx).attr('y',y+(rh-8)/2).attr('width',bw).attr('height',(rh-8)/2).attr('fill',WC[ws[1]])}
    else gg.append('rect').attr('x',bx).attr('y',y).attr('width',bw).attr('height',rh-8).attr('rx',3).attr('fill',ws.length?WC[ws[0]]:css('--muted'));
    gg.append('text').attr('x',gw-10).attr('y',y+13).attr('font-size',13).attr('fill',css('--ink')).attr('text-anchor','start').attr('direction','rtl').text(a.t)});
}
/* ============ NEWS ============ */
function news(){
  const vs=W.versions||[];
  view.innerHTML=head('','تازه‌ها','ویکی تکه‌تکه ساخته می‌شود. هر نسخه را ببین و بگو با فکرت جور است یا نه.')+vs.map(v=>`<section class="sec"><header><h2>نسخهٔ ${v.v} · ${esc(v.t)}</h2><p>${esc(v.d)}</p></header><ul class="nl">${v.items.map(i=>`<li>${esc(i)}</li>`).join('')}</ul>${v.ask?`<div class="gap" style="margin-top:12px"><h4>برای بررسی با هم</h4><ul>${v.ask.map(i=>`<li>${esc(i)}</li>`).join('')}</ul></div>`:''}</section>`).join('');
}


/* ============ BRAIN ============ */
function brain(){
  const sp=W.articles.filter(a=>a.brain&&a.from!=null).sort((a,b)=>b.from-a.from);
  view.innerHTML=head('ابزار','اندازهٔ مغز',`حجم مغز هر گونه (سی‌سی) در برابر زمانی که می‌زیست. خط افقی بازهٔ زمانی گونه است و خط عمودی بازهٔ حجم مغز در نمونه‌های شناخته‌شده. محور زمان لگاریتمی است. عددها تقریبی‌اند.`)+
  `<div class="stage"><div id="bz"></div><div class="legend"><span><span class="dot" style="background:#b0652a"></span>نخستین انسان‌تباران</span><span><span class="dot" style="background:#7a7a2a"></span>استرالوپیتکوس‌ها و خویشاوندان</span><span><span class="dot" style="background:#4867a8"></span>سردهٔ انسان (هومو)</span><span><span class="dot" style="background:#a8404f"></span>انسان خردمند</span></div></div>
  <section class="sec"><header><h2>مقایسهٔ دو گونه</h2><p>دو گونه را انتخاب کن. اندازهٔ دایره‌ها به نسبت حجم مغز است.</p></header>
  <div class="ctrl" style="flex-wrap:wrap"><select id="bza" aria-label="گونهٔ اول"></select><span>با</span><select id="bzb" aria-label="گونهٔ دوم"></select></div><div id="bzc" class="cmp"></div></section>`;
  const w=1000,h=560,L=60,R=40,T=20,B=50;
  const x=d3.scaleLog().domain([8e6,2e4]).range([w-R,L]),y=d3.scaleLinear().domain([250,1800]).range([h-B,T]);
  const svg=d3.select('#bz').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  [7e6,3e6,1e6,3e5,1e5,3e4].forEach(v=>{svg.append('line').attr('x1',x(v)).attr('x2',x(v)).attr('y1',T).attr('y2',h-B).attr('stroke',css('--rule'));svg.append('text').attr('x',x(v)).attr('y',h-B+20).attr('text-anchor','middle').attr('font-size',11).attr('class','svgmuted').text(v>=1e6?FA(v/1e6)+' میلیون':FA(v/1e3)+' هزار')});
  [400,800,1200,1600].forEach(v=>{svg.append('line').attr('x1',L).attr('x2',w-R).attr('y1',y(v)).attr('y2',y(v)).attr('stroke',css('--rule'));svg.append('text').attr('x',L-8).attr('y',y(v)+4).attr('text-anchor','end').attr('font-size',11).attr('class','svgmuted').attr('direction','ltr').text(FA(v))});
  svg.append('text').attr('x',w/2).attr('y',h-6).attr('text-anchor','middle').attr('font-size',12).attr('class','svgmuted').text('سال پیش ←');
  [[400,'شامپانزهٔ امروز ≈ ۴۰۰'],[1350,'میانگین انسان امروز ≈ ۱۳۵۰']].forEach(([v,l])=>{svg.append('line').attr('x1',L).attr('x2',w-R).attr('y1',y(v)).attr('y2',y(v)).attr('stroke',css('--muted')).attr('stroke-dasharray','5 4');svg.append('text').attr('x',L+4).attr('y',y(v)-6).attr('text-anchor','end').attr('font-size',11.5).attr('class','svgmuted').text(l)});
  const g=svg.append('g').selectAll('a').data(sp).join('a').attr('href',a=>'#/a/'+a.id).on('mousemove',(e,a)=>showTip(e,`<b>${a.t}</b><br>${FA(a.brain[0])} تا ${FA(a.brain[1])} سی‌سی<br>${yrs(a.from*1e6)} تا ${a.to?yrs(a.to*1e6):'امروز'}`)).on('mouseleave',hideTip);
  const GC={early:'#b0652a',aus:'#7a7a2a',homo:'#4867a8',sap:'#a8404f'},grp=a=>a.id==='homo-sapiens'?'sap':/^homo|dmanisi|naledi|floresiensis|neanderthal|denisovan/.test(a.id)?'homo':/australo|paranthropus|kenyan/.test(a.id)?'aus':'early';
  const mid=a=>Math.sqrt(a.from*1e6*Math.max(a.to*1e6,2e4)),c=a=>GC[grp(a)];
  g.append('line').attr('x1',a=>x(a.from*1e6)).attr('x2',a=>x(Math.max(a.to*1e6,2e4))).attr('y1',a=>y((a.brain[0]+a.brain[1])/2)).attr('y2',a=>y((a.brain[0]+a.brain[1])/2)).attr('stroke',c).attr('stroke-width',2).attr('opacity',.5);
  g.append('rect').attr('x',a=>x(mid(a))-5).attr('width',10).attr('y',a=>y(a.brain[1])).attr('height',a=>Math.max(4,y(a.brain[0])-y(a.brain[1]))).attr('rx',5).attr('fill',c);
  // names never cover a bar or another name: bars are obstacles first, then each name tries above, below, right, left
  const lab=a=>a.t.replace(/ \(.*\)/,'');
  const boxes=sp.map(a=>[x(mid(a))-6,y(a.brain[1])-1,x(mid(a))+6,y(a.brain[0])+1]);
  sp.slice().sort((p,q)=>(q.brain[1]-q.brain[0])-(p.brain[1]-p.brain[0])).forEach(a=>{const cx=x(mid(a)),wd=lab(a).length*7.2+8,top=y(a.brain[1]),bot=y(a.brain[0]),cy=(top+bot)/2+4;
    const tries=[[cx,top-8,'middle'],[cx,bot+17,'middle'],[cx+10,cy,'start'],[cx-10,cy,'end'],[cx,top-24,'middle'],[cx,bot+33,'middle']];
    for(const [xx,yy,an] of tries){const l=an==='middle'?xx-wd/2:an==='start'?xx:xx-wd;const bx=[l,yy-13,l+wd,yy+3];
      if(!boxes.some(b=>bx[0]<b[2]&&bx[2]>b[0]&&bx[1]<b[3]&&bx[3]>b[1])&&bx[0]>L&&bx[2]<w-4){boxes.push(bx);a._lx=xx;a._ly=yy;a._la=an;return}}a._ly=null});
  g.filter(a=>a._ly!=null).append('text').attr('x',a=>a._lx).attr('y',a=>a._ly).attr('direction','ltr').attr('text-anchor',a=>a._la).attr('font-size',12).attr('fill',css('--ink')).style('paint-order','stroke').style('stroke',css('--card')).style('stroke-width','3px').text(lab);
  const A=document.getElementById('bza'),Bs=document.getElementById('bzb');
  const opts=sp.map(a=>`<option value="${a.id}">${a.t}</option>`).join('');A.innerHTML=opts;Bs.innerHTML=opts;A.value='homo-erectus';Bs.value='homo-sapiens';
  const card=a=>{const m=(a.brain[0]+a.brain[1])/2;return `<div class="box"><svg viewBox="0 0 120 120" width="120" height="120" aria-hidden="true"><circle cx="60" cy="60" r="${(Math.sqrt(m/1750)*56).toFixed(1)}" fill="${c(a)}" opacity=".85"/></svg>
    <h3><a href="#/a/${a.id}">${a.t}</a></h3><p class="latin">${esc(a.en)}</p><dl class="facts"><dt>مغز</dt><dd>${FA(a.brain[0])} تا ${FA(a.brain[1])} سی‌سی</dd><dt>زمان</dt><dd>${yrs(a.from*1e6)} تا ${a.to?yrs(a.to*1e6):'امروز'}</dd><dt>نسبت به ما</dt><dd>حدود ${FA(Math.round(m/1350*100))}٪ انسان امروز</dd></dl><p>${esc(a.sum)}</p></div>`};
  const upd=()=>{const a=sp.find(s=>s.id===A.value),b=sp.find(s=>s.id===Bs.value);document.getElementById('bzc').innerHTML=card(a)+card(b)};
  A.onchange=Bs.onchange=upd;upd();
}

/* ============ DNA ============ */
function dna(sub){
  const MT=sub&&sub.startsWith('mt-')?decodeURIComponent(sub.slice(3)).split(','):null;
  view.innerHTML=head('ابزار و داده','نقشهٔ DNA باستانی','هر نقطه یک انسان باستانی است که ژنومش خوانده شده (پایگاه AADR نسخهٔ ۶۶). رنگ‌ها هاپلوگروه کروموزوم Y (تبار پدری) را نشان می‌دهند؛ زنان و نمونه‌های بی‌داده خاکستری‌اند. نوار زمان را بکش.')+
  `<div class="stage"><div id="dm"></div><div class="ctrl"><button id="dmp">پخش</button><input type="range" id="dmr" min="0" max="1000" value="600"><span class="read" id="dmv"></span></div><div class="legend" id="dmlg"></div></div>
  <section class="sec"><header><h2>نمونه‌های باستانی ایران</h2><p>۱۴۹ نفر؛ مرتب بر اساس قدمت.</p></header><div class="box list" id="dml"></div></section>`;
  const rows=(window.AADR||[]).map(r=>({lat:r[0],lon:r[1],bp:r[2],c:r[3],g:r[4],y:r[5],mt:r[6]}));
  const Y=['R','J','G','E','I','H','L','N','Q','C','T','O'];const col=d3.scaleOrdinal(Y,['#a8404f','#b0652a','#3f7f6e','#7a7a2a','#4867a8','#6b4f8f','#c48a2a','#2f8a8a','#8a5a3a','#5a6aa8','#a86a8a','#4a8a4a']);
  const mtHit=d=>MT&&d.mt&&MT.some(p=>d.mt.startsWith(p)&&!(p==='L'&&false));
  const yc=d=>{if(MT)return mtHit(d)?css('--accent'):css('--muted');const k=(d.y||'')[0];return Y.includes(k)?col(k):css('--muted')};
  if(MT){document.querySelector('#view .lede').innerHTML=`نمونه‌هایی که هاپلوگروه مادری‌شان از شاخهٔ <b class="latin">${esc(MT.join(' / '))}</b> است پررنگ‌اند (${FA(rows.filter(mtHit).length)} نفر). <a href="#/mtree">بازگشت به درخت مادری</a> · <a href="#/dna">همهٔ نمونه‌ها</a>`}
  if(!MT)document.getElementById('dmlg').innerHTML=Y.map(k=>`<span><span class="dot" style="background:${col(k)}"></span><span class="latin">${k}</span></span>`).join('');
  const w=1000,h=560;const svg=d3.select('#dm').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  const proj=d3.geoMercator().fitExtent([[0,0],[w,h]],{type:'MultiPoint',coordinates:[[-18,-35],[120,62]]});baseMap(svg,proj,w,h);
  const c=svg.append('g').selectAll('circle').data(rows).join('circle').attr('cx',d=>proj([d.lon,d.lat])[0]).attr('cy',d=>proj([d.lon,d.lat])[1]).attr('r',2.6).attr('fill',yc)
    .on('mousemove',(e,d)=>showTip(e,`<span class="latin">${esc(d.g)}</span><br>${esc(d.c)} · ${fmt(d.bp)} سال پیش<br>Y: <span class="latin">${esc(d.y||'—')}</span> · mt: <span class="latin">${esc(d.mt||'—')}</span>`)).on('mouseleave',hideTip);
  const sc=d3.scaleLog().domain([45000,300]).range([0,1000]);const r=document.getElementById('dmr');
  r.oninput=()=>{const t=sc.invert(+r.value),win=Math.max(300,t*.12);document.getElementById('dmv').textContent=fmt(t)+' سال پیش';
    c.attr('opacity',d=>MT?(mtHit(d)?(Math.abs(d.bp-t)<=win?1:.35):(Math.abs(d.bp-t)<=win?.25:0)):(Math.abs(d.bp-t)<=win?.9:0)).attr('r',d=>MT&&mtHit(d)?3.6:2.6)};
  r.oninput(); cleanup=playBtn(document.getElementById('dmp'),r,6,80);
  const ir=rows.filter(d=>d.c==='Iran').sort((a,b)=>b.bp-a.bp);
  document.getElementById('dml').innerHTML=`<table><tr><th>سال پیش</th><th>گروه</th><th>Y</th><th>mtDNA</th></tr>${ir.map(d=>`<tr><td class="num">${fmt(d.bp)}</td><td class="latin">${esc(d.g)}</td><td class="latin">${esc(d.y)}</td><td class="latin">${esc(d.mt)}</td></tr>`).join('')}</table>`;
}


/* ============ ARCHAIC GENES ============ */
const ARCH=[
 ["آفریقای غربی (یوروبا)",0.3,0,"تقریباً بی‌DNA باستانیِ اوراسیایی؛ همین مقدار کم هم با بازگشت مردمانی از اوراسیا به آفریقا آمده."],
 ["اروپا",1.8,0.05,"حدود ۲٪ نئاندرتالی، مثل بیشتر غیرآفریقایی‌ها."],
 ["ایران و جنوب‌غرب آسیا",1.6,0.05,"کمی کمتر از اروپا و شرق آسیا؛ شاید به خاطر سهم «اوراسیایی‌های پایه» (؟)."],
 ["جنوب آسیا",1.9,0.1,"نئاندرتالی مثل بقیه و ردی کم از دنیسووایی‌ها."],
 ["شرق آسیا",2.2,0.2,"کمی بیشتر نئاندرتالی؛ و تکه‌هایی از یک گروه دنیسووایی دیگر."],
 ["بومیان آمریکا",2.0,0.1,"نوادگان مردمانی از شرق سیبری؛ الگویی شبیه شرق آسیا."],
 ["پاپوآ گینهٔ نو",2.0,4,"بیشترین سهم دنیسووایی در جهان، همراه با آیتاهای فیلیپین."],
 ["آیتا (فیلیپین)",2.0,5,"سهم دنیسووایی بسیار بالا (برآورد ۲۰۲۱) (؟)."]];
const TRAITS=[
 ["EPAS1","دنیسووایی","زیستن در ارتفاع زیاد بدون غلیظ شدن خطرناک خون","تبتی‌ها"],
 ["OAS1","نئاندرتالی","نسخه‌ای که خطر کووید شدید را کمتر می‌کند","اروپا و آسیا"],
 ["ناحیه‌ای روی کروموزوم ۳","نئاندرتالی","نسخه‌ای که خطر کووید شدید را بیشتر می‌کند","به‌ویژه جنوب آسیا"],
 ["TLR1، TLR6، TLR10","نئاندرتالی","گیرنده‌های ایمنی ذاتی؛ پاسخ سریع‌تر به میکروب‌ها و شاید آلرژی بیشتر","سراسر اوراسیا"],
 ["ژن‌های کراتین (مثل BNC2)","نئاندرتالی","پوست و مو؛ شاید سازگاری با نور کم شمال","اروپا و آسیا"],
 ["TBX15 / WARS2","دنیسووایی","پراکندگی چربی بدن و سازگاری با سرما","گرینلندی‌ها و بومیان آمریکا"]];
function genes(){
  view.innerHTML=head('ابزار','ژن‌های باستانی درون تو','هر انسانِ امروز ژنومی دارد که تکه‌هایی از آن از انسان‌های دیگر آمده؛ یادگار آمیزش‌های ده‌ها هزار سال پیش. یک گروه را انتخاب کن تا ببینی از هر ۱۰۰ تکهٔ ژنومش چندتا از نئاندرتال‌ها و دنیسووایی‌هاست. عددها گرد و تقریبی‌اند.')+
  `<div class="gsplit"><div class="box"><div class="gpick" id="gp"></div></div><div class="box gview"><h3 id="gt"></h3><div id="gw" class="waffle" aria-hidden="true"></div><p id="gd" class="lede" style="margin-top:10px"></p>
  <div class="legend"><span><span class="dot" style="background:var(--wash);outline:1px solid var(--rule)"></span>انسان خردمند</span><span><span class="dot" style="background:#b0652a"></span>نئاندرتال</span><span><span class="dot" style="background:#4867a8"></span>دنیسووایی</span></div></div></div>
  <section class="sec"><header><h2>همه کنار هم</h2><p>سهم DNA باستانی، به درصد. مقیاس تا ۸٪ است.</p></header><div class="stage" id="gb"></div></section>
  <section class="sec"><header><h2>ژن‌هایی که از آن‌ها مانده</h2><p>چند نمونهٔ شناخته‌شده. بیشتر ژن‌های به‌ارث‌رسیده اثر کوچکی دارند و بسیاری‌شان در طول زمان حذف شده‌اند.</p></header>
  <div class="traits">${TRAITS.map(r=>`<div class="trait ${r[1]==='دنیسووایی'?'den':'nea'}"><b class="latin">${esc(r[0])}</b><span class="chip">${r[1]}</span><p>${esc(r[2])}</p><small>${esc(r[3])}</small></div>`).join('')}</div></section>
  <p class="eyebrow" style="margin-top:20px">بیشتر بخوان: <a href="#/a/interbreeding">آمیزش با خویشاوندان</a> · <a href="#/a/denisovan-genes">ژن‌های دنیسووایی</a> · <a href="#/a/basal-eurasian">اوراسیایی‌های پایه</a>. منبع عددها: مقاله‌های مروری ژنتیک باستانی؛ برای ایران با احتیاط.</p>`;
  const gp=document.getElementById('gp');gp.innerHTML=ARCH.map((r,i)=>`<button type="button" data-i="${i}">${r[0]}</button>`).join('');
  const show=i=>{const r=ARCH[i];gp.querySelectorAll('button').forEach(b=>b.classList.toggle('on',+b.dataset.i===i));
    document.getElementById('gt').textContent=r[0];
    // 100 cells x 4 sub-quarters = 400 quarter cells so 0.25% resolution
    const nN=Math.round(r[1]*4),nD=Math.round(r[2]*4);let cells='';
    for(let k=0;k<100;k++){let q='';for(let s=0;s<4;s++){const idx=k*4+s;q+=`<i class="${idx<nN?'n':idx<nN+nD?'d':''}"></i>`}cells+=`<span>${q}</span>`}
    document.getElementById('gw').innerHTML=cells;
    document.getElementById('gd').innerHTML=`نئاندرتالی حدود <b>${FA(r[1])}٪</b> · دنیسووایی حدود <b>${FA(r[2])}٪</b><br>${linkify(r[3])}`};
  gp.onclick=e=>{const b=e.target.closest('button');if(b)show(+b.dataset.i)};show(2);
  const w=1000,rh=34,h=ARCH.length*rh+40,L=230,x=d3.scaleLinear().domain([0,8]).range([0,w-L-40]);
  const svg=d3.select('#gb').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  [0,2,4,6,8].forEach(v=>{svg.append('line').attr('x1',w-L-x(v)).attr('x2',w-L-x(v)).attr('y1',4).attr('y2',h-26).attr('stroke',css('--rule'));svg.append('text').attr('x',w-L-x(v)).attr('y',h-8).attr('text-anchor','middle').attr('font-size',11).attr('class','svgmuted').text(FA(v)+'٪')});
  ARCH.forEach((r,i)=>{const y=10+i*rh;svg.append('rect').attr('x',w-L-x(r[1])).attr('y',y).attr('width',x(r[1])).attr('height',rh-14).attr('rx',4).attr('fill','#b0652a');
    svg.append('rect').attr('x',w-L-x(r[1]+r[2])).attr('y',y).attr('width',x(r[2])).attr('height',rh-14).attr('rx',4).attr('fill','#4867a8');
    svg.append('text').attr('x',w-10).attr('y',y+14).attr('font-size',13).attr('fill',css('--ink')).attr('text-anchor','start').attr('direction','rtl').text(r[0])});
}

/* ============ MOTHER TREE (mtDNA) ============ */
const MTREE={n:"L",r:"af",k:"حدود ۲۰۰–۱۵۰ هزار",d:"ریشه: «حوای میتوکندریایی» در آفریقا",c:[
 {n:"L0",r:"af",d:"کهن‌ترین شاخه؛ امروز بیشتر در خوی‌سان‌های جنوب آفریقا"},
 {n:"L1",r:"af",d:"آفریقای مرکزی و غربی"},{n:"L2",r:"af",d:"فراوان‌ترین در آفریقای غربی"},
 {n:"L3",r:"af",k:"حدود ۷۰ هزار",d:"شاخهٔ شرق آفریقا که دو شاخهٔ خروج را داد",c:[
  {n:"M",r:"as",k:"حدود ۶۰ هزار",d:"شاخهٔ آسیایی خروج",c:[{n:"D",r:"as",d:"شرق آسیا؛ و آمریکا"},{n:"C",r:"as",d:"سیبری؛ و آمریکا"},{n:"G",r:"as",d:"شمال‌شرق آسیا"},{n:"Q",r:"oc",d:"پاپوآ و ملانزی"}]},
  {n:"N",r:"me",k:"حدود ۶۰ هزار",d:"شاخهٔ دیگر خروج؛ از جنوب‌غرب آسیا پخش شد",c:[
   {n:"A",r:"as",d:"شرق آسیا؛ و آمریکا"},{n:"X",r:"me",d:"پراکنده از خاورمیانه تا آمریکای شمالی"},{n:"W",r:"me",d:"جنوب‌غرب و جنوب آسیا"},{n:"I",r:"me",d:"خاورمیانه و اروپا"},{n:"S",r:"oc",d:"استرالیا"},
   {n:"R",r:"me",k:"حدود ۵۵ هزار",d:"بزرگ‌ترین شاخهٔ N",c:[
    {n:"B",r:"as",d:"شرق آسیا، اقیانوسیه و آمریکا"},{n:"F",r:"as",d:"جنوب‌شرق آسیا"},{n:"P",r:"oc",d:"اقیانوسیه"},
    {n:"U",r:"eu",d:"کهن‌ترین شاخهٔ اروپایی‌ها؛ U5 در شکارگران اروپا",c:[{n:"K",r:"me",d:"خاورمیانه و اروپا؛ فراوان در کشاورزان نوسنگی"}]},
    {n:"JT",r:"me",d:"جنوب‌غرب آسیا",c:[{n:"J",r:"me",d:"نوسنگی خاورمیانه و اروپا"},{n:"T",r:"me",d:"با کشاورزان نخستین پخش شد"}]},
    {n:"HV",r:"me",d:"احتمالاً در جنوب‌غرب آسیا پدید آمد",c:[{n:"H",r:"eu",d:"فراوان‌ترین هاپلوگروه مادری اروپا امروز"},{n:"V",r:"eu",d:"اروپا"}]}]}]}]},
 {n:"L4–L6",r:"af",d:"شاخه‌های کوچک‌تر شرق آفریقا"}]};
const RC={af:'#b0652a',me:'#a8404f',eu:'#4867a8',as:'#7a7a2a',oc:'#3f7f6e'},RN={af:'آفریقا',me:'جنوب‌غرب آسیا',eu:'اروپا',as:'آسیا و آمریکا',oc:'اقیانوسیه'};
function mtree(){
  view.innerHTML=head('ابزار','درخت مادری','DNA میتوکندری فقط از مادر می‌رسد؛ پس درخت آن، درخت مادران مادرانِ ماست. هر شاخه یک هاپلوگروه است و رنگش جایی را نشان می‌دهد که امروز بیشتر دیده می‌شود. روی هر شاخه بزن تا نمونه‌های باستانی‌اش را روی نقشه ببینی. سن‌ها تقریبی‌اند.')+
  `<div class="stage"><div id="mt"></div><div class="legend">${Object.keys(RC).map(k=>`<span><span class="dot" style="background:${RC[k]}"></span>${RN[k]}</span>`).join('')}</div></div><div class="box" id="mti" style="margin-top:12px"></div>`;
  const root=d3.hierarchy(MTREE,d=>d.c);const w=1000,h=640;
  d3.tree().size([2*Math.PI*0.86,280]).separation((a,b)=>(a.parent===b.parent?1:1.4)/a.depth)(root);
  const svg=d3.select('#mt').append('svg').attr('viewBox',`${-w/2} ${-h/2} ${w} ${h}`);
  const rot=-Math.PI*0.86;const NA=v=>((v%(2*Math.PI))+2*Math.PI)%(2*Math.PI);
  svg.append('g').selectAll('path').data(root.links()).join('path').attr('fill','none').attr('stroke',d=>RC[d.target.data.r]).attr('stroke-opacity',.6).attr('stroke-width',d=>3.4-d.target.depth*.55)
    .attr('d',d3.linkRadial().angle(d=>d.x+rot).radius(d=>d.y));
  const leaves=d=>{const s=[];d.each(n=>s.push(n.data.n.replace('L4–L6','L4,L5,L6')));return s.join(',').split(',')};
  const n=svg.append('g').selectAll('g').data(root.descendants()).join('a').attr('href',d=>'#/dna/mt-'+encodeURIComponent(leaves(d).filter(x=>x!=='JT'&&x!=='HV'||true).join(',')))
    .attr('transform',d=>`rotate(${(d.x+rot)*180/Math.PI-90}) translate(${d.y},0)`)
    .on('mouseenter',(e,d)=>{document.getElementById('mti').innerHTML=`<b class="latin">${d.data.n}</b> · ${RN[d.data.r]}${d.data.k?` · ${d.data.k} سال پیش`:''}<br>${d.data.d}`});
  n.append('circle').attr('r',d=>d.children?6:5).attr('fill',d=>RC[d.data.r]).attr('stroke',css('--card')).attr('stroke-width',2);
  n.append('text').attr('dy','0.32em').attr('x',d=>(NA(d.x+rot)<Math.PI)===!d.children?10:-10).attr('text-anchor',d=>(NA(d.x+rot)<Math.PI)===!d.children?'start':'end')
    .attr('transform',d=>NA(d.x+rot)>=Math.PI?'rotate(180)':null).attr('font-size',13).attr('class','latin').attr('fill',css('--ink')).attr('direction','ltr').text(d=>d.data.n);
  {const bb=svg.node().getBBox(),p=24;svg.attr('viewBox',`${bb.x-p} ${bb.y-p} ${bb.width+2*p} ${bb.height+2*p}`).style('max-height','78vh').style('display','block').style('margin','auto')}
  document.getElementById('mti').innerHTML='روی یک شاخه برو تا توضیحش را ببینی؛ کلیک کن تا نمونه‌های باستانی‌اش روی نقشه بیایند. نگاه کنید به <a href="#/a/mito-eve">حوای میتوکندریایی</a> و <a href="#/a/haplogroups">هاپلوگروه‌ها</a>.';
}

/* ============ WHICH CLOCK? (dating) ============ */
const METH=[
 ['dendro','حلقهٔ درخت','چوب',1,12500,'#6f8a3a',['wood']],
 ['radiocarbon','رادیوکربن','استخوان، زغال، چوب، دانه',100,55000,'#b0652a',['bone','wood']],
 ['luminescence','لومینسانس (OSL/TL)','رسوب، سنگ‌چخماق سوخته، سفال',100,5e5,'#c99a2e',['sed','burnt']],
 ['uranium-series','اورانیوم-توریم','چکنده و پوستهٔ آهکی غار، دندان',1000,5e5,'#3f7f6e',['cave','tooth']],
 ['esr','ESR','مینای دندان',1000,2e6,'#4867a8',['tooth']],
 ['paleomagnetism','دیرینه‌مغناطیس','رسوب و گدازه؛ فقط همراه روش دیگر',1e4,1e8,'#6b4f8f',['sed','volc']],
 ['argon-argon','آرگون-آرگون','سنگ و خاکستر آتشفشانی',2e4,1e8,'#a8404f',['volc']]];
const IDM=[['ancient-dna','DNA باستانی','استخوان، دندان، خاک غار',0,2e6,['bone','tooth','sed']],['paleoproteomics','پروتئین باستانی','استخوان، مینای دندان',0,2e6,['bone','tooth']]];
const MATS=[['all','همه'],['bone','استخوان و زغال'],['tooth','دندان'],['sed','رسوب و خاک'],['cave','سنگ غار'],['volc','آتشفشانی'],['wood','چوب'],['burnt','سنگ و سفال سوخته']];
const STRATA=[
 {n:'خاک امروز',c:'#8a7a5c',h:40,t:'امروز',d:'خاک و فضولات دام؛ شبانان زاگرس هنوز گله را در غارها پناه می‌دهند. همین می‌تواند لایه‌های زیرین را به هم بریزد.',m:'رادیوکربن (اگر لازم باشد)'},
 {n:'سفال و استخوان بز اهلی',c:'#b38a5a',h:58,t:'حدود ۸ تا ۶ هزار سال پیش',a:'neolithic',d:'تکه‌های سفال، دانهٔ سوخته و استخوان بزهایی که بیشترشان نرهای جوان‌اند: نشان گله‌داری. اینجا شبانان نوسنگی گاه‌به‌گاه می‌ماندند.',m:'رادیوکربن روی دانه یا استخوان'},
 {n:'میکرولیت و حلزون',c:'#a39468',h:62,t:'حدود ۲۰ تا ۱۲ هزار سال پیش',a:'zarzian',d:'ابزارهای سنگی بسیار کوچک و انبوه پوستهٔ حلزون خوراکی: فرهنگ زرزی و «سفرهٔ گسترده» پیش از کشاورزی.',m:'رادیوکربن روی زغال اجاق'},
 {n:'تیغه‌های کوچک',c:'#8f7c55',h:64,t:'حدود ۴۲ تا ۲۵ هزار سال پیش',a:'baradostian',d:'تیغه‌ها و ریزتیغه‌های بردوستی؛ از نخستین نشانه‌های انسان خردمند در زاگرس.',m:'رادیوکربن در مرز توانش؛ OSL روی رسوب'},
 {n:'سنگ‌ریزهٔ ریزش سقف',c:'#9d9a90',h:34,t:'گسستگی',d:'لایه‌ای بی‌آثار از سنگ‌هایی که از سقف ریخته‌اند. یعنی غار مدتی خالی بوده است؛ شاید هزاران سال. «نبودن» هم داده است.',m:'لایه‌نگاری: فاصلهٔ زمانی را باید از لایه‌های بالا و پایین حدس زد'},
 {n:'ابزار موستری و استخوان سوخته',c:'#6f5d42',h:76,t:'حدود ۱۰۰ تا ۴۵ هزار سال پیش',a:'neanderthal',d:'ابزارهای موستری، اجاق و استخوان سوختهٔ بز و گوزن. سازندگانشان به احتمال زیاد نئاندرتال‌ها بودند.',m:'OSL روی رسوب، اورانیوم-توریم روی پوستهٔ آهکی، ESR روی دندان جانوران'},
 {n:'سنگ بستر',c:'#57524a',h:46,t:'میلیون‌ها سال',d:'آهک کوه که غار در آن کنده شده. اینجا داستان زمین‌شناسی است، نه انسان.',m:'—'}];
function clocks(){
  view.innerHTML=head('ابزار','کدام ساعت؟','هیچ ساعتی برای همه چیز کار نمی‌کند. سن و ماده را انتخاب کن تا ببینی کدام روش به کار می‌آید؛ بعد کربن-۱۴ را ببین که می‌پاشد، و لایه‌های یک غار را بخوان.')+
  `<section class="sec"><header><h2>۱. چند سال، از چه چیز؟</h2><p>مقیاس لگاریتمی است: هر خانه ده برابر خانهٔ قبلی.</p></header>
   <div class="split"><div class="stage"><div class="chips" id="cmat">${MATS.map(([k,l])=>`<button data-m="${k}" class="${k==='all'?'on':''}">${l}</button>`).join('')}</div><div id="cchart"></div>
    <div class="ctrl"><label for="cage">سن</label><input type="range" id="cage" min="1" max="8" step="0.01" value="4.6"><span class="read" id="cagev"></span></div></div>
    <div class="box" id="cres"></div></div></section>
  <section class="sec"><header><h2>۲. ساعت کربن-۱۴</h2><p>نیمه‌عمر حدود ۵۷۳۰ سال. نوار را بکش.</p></header>
   <div class="split"><div class="stage"><div id="c14c"></div><div class="ctrl"><button id="c14p">پخش</button><input type="range" id="c14r" min="0" max="60000" step="100" value="0"><span class="read" id="c14v"></span></div></div>
    <div class="box"><div class="atoms" id="atoms"></div><p id="c14t" class="small"></p></div></div></section>
  <section class="sec"><header><h2>۳. لایه‌های یک غار را بخوان</h2><p>برش آموزشی از یک غار خیالی در زاگرس، بر پایهٔ توالی رایج منطقه. روی هر لایه بزن.</p></header>
   <div class="split"><div class="stage"><div id="strata"></div></div><div class="box" id="stinfo"></div></div></section>
  <p class="small">بیشتر بخوان: <a href="#/a/dating-methods">نمای کلی سن‌یابی</a> · <a href="#/path/clocks">مسیر «ساعت‌های گذشته»</a></p>`;
  /* --- 1. range chart --- */
  let mat='all';const w=1000,rowH=34,top=34,all=METH.concat(IDM.map(r=>[r[0],r[1],r[2],1,r[4],'#9a9389',r[5],1]));const h=top+all.length*rowH+56;
  const x=d3.scaleLog().domain([10,1e8]).range([w-40,250]);
  const svg=d3.select('#cchart').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  [[10,'۱۰ سال'],[100,'۱۰۰'],[1e3,'هزار'],[1e4,'۱۰ هزار'],[1e5,'۱۰۰ هزار'],[1e6,'میلیون'],[1e7,'۱۰ میلیون'],[1e8,'۱۰۰ میلیون']].forEach(([v,l])=>{svg.append('line').attr('x1',x(v)).attr('x2',x(v)).attr('y1',top-10).attr('y2',h-30).attr('stroke',css('--rule')).attr('stroke-dasharray','2 4');svg.append('text').attr('class','svgmuted').attr('x',x(v)).attr('y',h-10).attr('font-size',15).attr('text-anchor','middle').text(l)});
  svg.append('text').attr('class','svgmuted').attr('x',w-20).attr('y',18).attr('font-size',14).attr('text-anchor','start').text('امروز ←  گذشته');
  const sepY=top+METH.length*rowH;svg.append('text').attr('class','svgmuted').attr('x',240).attr('y',sepY+18).attr('font-size',13).attr('text-anchor','start').text('نه ساعت، بلکه «چه کسی؟»');
  const rows=svg.selectAll('g.r').data(all).join('g').attr('class','r').attr('transform',(d,i)=>`translate(0,${top+i*rowH+(i>=METH.length?30:0)})`).style('cursor','pointer').on('click',(e,d)=>location.hash='#/a/'+d[0]);
  rows.append('rect').attr('x',d=>x(Math.min(d[4],1e8))).attr('width',d=>x(Math.max(d[3],10))-x(Math.min(d[4],1e8))).attr('y',4).attr('height',rowH-12).attr('rx',(rowH-12)/2).attr('fill',d=>d[5]);
  rows.append('text').attr('class','svgtext').attr('x',240).attr('y',rowH/2+3).attr('font-size',16).attr('text-anchor','start').text(d=>d[1]);
  const line=svg.append('line').attr('y1',top-6).attr('y2',h-30).attr('stroke',css('--ink')).attr('stroke-width',2);
  const cr=document.getElementById('cage');
  const upd=()=>{const age=Math.pow(10,+cr.value);document.getElementById('cagev').textContent=yrs(age);line.attr('x1',x(age)).attr('x2',x(age));
   const ok=d=>age>=d[3]&&age<=d[4]&&(mat==='all'||d[6].includes(mat));rows.attr('opacity',d=>ok(d)?1:.18);
   const m=METH.filter(ok),id=IDM.filter(d=>age<=d[4]&&(mat==='all'||d[5].includes(mat)));
   document.getElementById('cres').innerHTML=`<h3>${yrs(age)}${mat!=='all'?' · '+MATS.find(q=>q[0]===mat)[1]:''}</h3>`+(m.length?`<ul class="meth">${m.map(d=>`<li><span class="dot" style="background:${d[5]}"></span><a href="#/a/${d[0]}">${d[1]}</a><small>${d[2]}</small></li>`).join('')}</ul>`:`<p>هیچ ساعت مطلقی برای این ترکیب نیست. اینجا فقط <a href="#/a/stratigraphy">لایه‌نگاری</a> کمک می‌کند: از لایه‌های بالا و پایین سن را حدس بزن.</p>`)+
    (id.length?`<p class="small">برای شناختن صاحب استخوان یا لایه: ${id.map(d=>`<a href="#/a/${d[0]}">${d[1]}</a>`).join(' و ')}${age>1e5?' (در این سن فقط اگر سرما آن را نگه داشته باشد)':''}.</p>`:'')+
    (age>5e4&&age<3e5?`<p class="small note">این بازه همان «شکاف» معروف است: پس از پایان رادیوکربن، روش‌ها کم‌دقت‌ترند. خروج از آفریقا و پایان نئاندرتال‌ها همین‌جاست.</p>`:'')};
  cr.oninput=upd;document.querySelectorAll('#cmat button').forEach(b=>b.onclick=()=>{mat=b.dataset.m;document.querySelectorAll('#cmat button').forEach(q=>q.classList.toggle('on',q===b));upd()});upd();
  /* --- 2. C14 decay --- */
  const cw=1000,ch=360,px=d3.scaleLinear().domain([0,60000]).range([cw-30,70]),py=d3.scaleLinear().domain([0,1]).range([ch-40,20]);
  const s2=d3.select('#c14c').append('svg').attr('viewBox',`0 0 ${cw} ${ch}`);const HL=5730,rem=t=>Math.pow(.5,t/HL);
  for(let k=1;k<=10;k++){const t=k*HL;if(t>60000)break;s2.append('line').attr('x1',px(t)).attr('x2',px(t)).attr('y1',py(rem(t))).attr('y2',ch-40).attr('stroke',css('--rule')).attr('stroke-dasharray','2 3');s2.append('text').attr('class','svgmuted').attr('x',px(t)).attr('y',ch-18).attr('font-size',14).attr('text-anchor','middle').text(FA(Math.round(t/1000))+' هزار')}
  [1,.5,.25].forEach(v=>s2.append('text').attr('class','svgmuted').attr('x',60).attr('y',py(v)+5).attr('font-size',14).attr('text-anchor','start').text(FA(v*100)+'٪'));
  s2.append('rect').attr('x',70).attr('width',px(50000)-70).attr('y',20).attr('height',ch-60).attr('fill',css('--wash')).attr('opacity',.8);
  s2.append('text').attr('class','svgmuted').attr('x',(70+px(50000))/2).attr('y',50).attr('font-size',14).attr('text-anchor','middle').text('بیرون از توان روش');
  s2.append('path').attr('fill','none').attr('stroke','#b0652a').attr('stroke-width',3).attr('d',d3.line().x(t=>px(t)).y(t=>py(rem(t)))(d3.range(0,60001,250)));
  const dot=s2.append('circle').attr('r',9).attr('fill','#b0652a').attr('stroke',css('--card')).attr('stroke-width',3);
  const rk=d3.shuffle(d3.range(100));document.getElementById('atoms').innerHTML=rk.map(()=>'<i></i>').join('');const at=[...document.querySelectorAll('#atoms i')];
  const r2=document.getElementById('c14r');r2.oninput=()=>{const t=+r2.value,f=rem(t),n=Math.round(f*100);dot.attr('cx',px(t)).attr('cy',py(f));
   document.getElementById('c14v').textContent=t?fmt(t)+' سال پس از مرگ':'لحظهٔ مرگ';at.forEach((e,i)=>e.classList.toggle('gone',rk[i]>=f*100));
   document.getElementById('c14t').innerHTML=`از هر ۱۰۰ اتم کربن-۱۴، <b>${FA(n<1&&f>0?'کمتر از ۱':n)}</b> مانده است (${FA((f*100).toFixed(f<.01?2:1))}٪).`+(t>50000?' <b>دیگر با رادیوکربن نمی‌شود تاریخ گذاشت.</b> نگاه کنید به <a href="#/a/luminescence">لومینسانس</a>.':t>=HL?` ${FA((t/HL).toFixed(1))} نیمه‌عمر گذشته.`:' گیاه یا جانور زنده کربن-۱۴ را هم‌تراز جو نگه می‌دارد؛ با مرگ، ساعت راه می‌افتد.')};
  r2.oninput();cleanup=playBtn(document.getElementById('c14p'),r2,300,60);
  /* --- 3. strata --- */
  const sw=1000,tot=STRATA.reduce((s,l)=>s+l.h,0),sh=tot*1.6+40;const s3=d3.select('#strata').append('svg').attr('viewBox',`0 0 ${sw} ${sh}`);
  let y0=20;const wav=(y,seed)=>d3.range(0,sw+1,50).map(xx=>[xx,y+Math.sin(xx/90+seed)*5]);
  const lay=STRATA.map((l,i)=>{const a=wav(y0,i*1.7),b=wav(y0+l.h*1.6,i*1.7+1.7);y0+=l.h*1.6;return {l,i,a,b}});
  s3.append('g').selectAll('path').data(lay).join('path').attr('d',d=>'M'+d.a.map(p=>p.join(',')).join('L')+'L'+d.b.slice().reverse().map(p=>p.join(',')).join('L')+'Z').attr('fill',d=>d.l.c).attr('stroke',css('--card')).attr('stroke-width',2).attr('class','layer').style('cursor','pointer').on('click',(e,d)=>pick(d.i));
  const rnd=d3.randomLcg(7);lay.forEach(d=>{if(d.i===STRATA.length-1)return;for(let k=0;k<d.l.h/2.2;k++){s3.append('circle').attr('cx',rnd()*sw).attr('cy',(d.a[0][1]+8)+rnd()*(d.l.h*1.6-16)).attr('r',1+rnd()*2.4).attr('fill','#000').attr('opacity',.13).style('pointer-events','none')}});
  const pt=lay[1],pb=lay[2];const pit=`M240,${pt.a[5][1]+20} C250,${pb.b[5][1]-10} 360,${pb.b[5][1]-10} 370,${pt.a[7][1]+20}Z`;
  s3.append('path').attr('d',pit).attr('fill','#c2a06d').attr('stroke','#5b4a33').attr('stroke-dasharray','5 4').attr('stroke-width',2).style('cursor','pointer').on('click',()=>pick('pit'));
  lay.forEach(d=>s3.append('text').attr('x',sw-24).attr('y',(d.a[0][1]+d.b[0][1])/2+8).attr('text-anchor','start').attr('font-size',26).attr('fill','#fff').style('paint-order','stroke').style('stroke','rgba(0,0,0,.35)').style('stroke-width','3px').style('pointer-events','none').text(FA(d.i+1)+'. '+d.l.n));
  s3.append('text').attr('x',305).attr('y',pb.a[6][1]+14).attr('text-anchor','middle').attr('font-size',22).attr('fill','#3b2f20').style('pointer-events','none').text('گودال');
  function pick(i){s3.selectAll('.layer').attr('opacity',d=>i==='pit'||d.i===i?1:.55);const L=i==='pit'?{n:'گودال',t:'نوسنگی (جوان‌تر از لایهٔ دور و برش)',d:'گودالی که مردم نوسنگی کنده‌اند و تا لایهٔ زرزی پایین رفته است. هرچه درون آن است جوان‌تر از لایهٔ پیرامونش است. اگر باستان‌شناس آن را نبیند، تکه‌ای سفال را به اشتباه ۱۵ هزار ساله می‌پندارد. قانون «پایینی پیرتر است» فقط در لایه‌های دست‌نخورده درست است.',m:'لایه‌نگاری دقیق، و رادیوکربن روی خود محتویات گودال'}:STRATA[i];
   document.getElementById('stinfo').innerHTML=`<h3>${L.n}</h3><p class="read">${L.t}</p><p>${L.d}</p><p class="small"><b>ساعت مناسب:</b> ${L.m}</p>${L.a?`<p class="small"><a href="#/a/${L.a}">${label(L.a)} ←</a></p>`:''}<p class="small muted">برش آموزشی است، نه یک غار واقعی.</p>`}
  pick(2);
}

/* ============ SEARCH ============ */
const norm=s=>String(s||'').toLowerCase()
  .replace(/[\u064A\u0649]/g,'ی').replace(/\u0643/g,'ک').replace(/[\u200c\u200d\u200e\u200f]/g,' ')
  .replace(/[\u064B-\u0652\u0640]/g,'').replace(/[أإآٱ]/g,'ا').replace(/[ۀة]/g,'ه')
  .replace(/[^\p{L}\p{N}]+/gu,' ').trim();
let IDX=null;
function buildIdx(){
  if(IDX)return IDX; IDX=[];
  W.articles.forEach(a=>IDX.push({u:'#/a/'+a.id,k:a.k,e:(D[a.d]||{}).name||'',t:a.t,s:a.sum,
    n1:norm(a.t+' '+(a.en||'')),n2:norm([a.sum,(a.kw||[]).join(' '),(a.facts||[]).map(f=>f.join(' ')).join(' ')].join(' ')),n3:norm(a.body.join(' '))}));
  W.people.forEach(p=>IDX.push({u:'#/p/'+p.id,k:'دانشمند',e:p.role||'',t:p.n,s:p.sum,
    n1:norm(p.n+' '+(p.en||'')),n2:norm([p.sum,p.role,p.y].join(' ')),n3:''}));
  (W.books||[]).forEach(b=>IDX.push({u:'#/library',k:'منبع',e:b.have?'در کتابخانه':'هنوز نداریم',t:b.t,s:b.a||'',
    n1:norm(b.t),n2:norm((b.a||'')+' '+(b.note||'')),n3:''}));
  const cnt={}; V.forEach(v=>{cnt[v.s]=(cnt[v.s]||0)+1;IDX.push({u:'archive.html#'+v.s+'-'+cnt[v.s],k:'ویدیو',e:v.src||'',t:v.t,s:'متن کامل در آرشیو',
    n1:norm(v.t),n2:norm(v.src||''),n3:''})});
  return IDX;
}
function hilite(txt,toks){let s=esc(txt);toks.forEach(t=>{if(t.length<2)return;
  try{s=s.replace(new RegExp('('+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/[یيى]/g,'[یيى]').replace(/[کك]/g,'[کك]')+')','gi'),'<mark>$1</mark>')}catch(e){}});return s}
function searchRun(q,el){
  const toks=norm(q).split(' ').filter(Boolean);
  if(!toks.length){el.innerHTML='<p class="lede">یک واژه بنویس: نام گونه، محوطه، دانشمند، یا هر چیزی که در متن مقاله‌ها باشد.</p>';return}
  const raw=q.trim().split(/\s+/);
  const res=[];
  for(const it of buildIdx()){let sc=0,ok=true;
    for(const t of toks){let s=0;
      if(it.n1.startsWith(t))s=120;else if(new RegExp('(^| )'+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).test(it.n1))s=90;else if(it.n1.includes(t))s=60;
      else if(it.n2.includes(t))s=26;else if(it.n3&&it.n3.includes(t))s=9;
      if(!s){ok=false;break} sc+=s}
    if(ok)res.push([sc,it])}
  res.sort((a,b)=>b[0]-a[0]||a[1].t.length-b[1].t.length);
  if(!res.length){el.innerHTML=`<p class="lede">چیزی پیدا نشد. شاید واژهٔ دیگری؟ یا اگر فکر می‌کنی این موضوع باید در ویکی باشد، <a href="#/need">به فهرست کمبودها</a> نگاه کن.</p>`;return}
  el.innerHTML=`<p class="small">${FA(res.length)} نتیجه</p><div class="hits">`+res.slice(0,60).map(([sc,it])=>
    `<a class="hit" href="${it.u}"><div><b>${hilite(it.t,raw)}</b><span class="k">${esc(it.k)}</span></div><p>${hilite((it.s||'').slice(0,180),raw)}</p>${it.e?`<small>${esc(it.e)}</small>`:''}</a>`).join('')+'</div>'+
    (res.length>60?'<p class="small">فقط ۶۰ نتیجهٔ نخست نشان داده شد.</p>':'');
}
function searchPage(q0){
  const q=q0?decodeURIComponent(q0):'';
  view.innerHTML=head('','جست‌وجو','در عنوان و متن کامل همهٔ مقاله‌ها، دانشمندان، منابع و عنوان ویدیوها.')+
   `<div class="searchbox"><input id="bq" type="search" placeholder="مثلاً: نئاندرتال، زاگرس، بز، لوالوا" value="${esc(q)}" autocomplete="off"></div><div id="sr"></div>`;
  const inp=document.getElementById('bq'),out=document.getElementById('sr');
  let t=null; inp.oninput=()=>{clearTimeout(t);t=setTimeout(()=>searchRun(inp.value,out),120)};
  searchRun(q,out); inp.focus(); inp.setSelectionRange(q.length,q.length);
}

/* ============ GENERATIONS ============ */
const MILE=[
 [100,'صد سال پیش',null],
 [10000,'گله‌داری در گنج‌دره','ganj-dareh'],
 [11600,'ستون‌های گوبکلی‌تپه','gobekli-tepe'],
 [14000,'نخستین یکجانشینان ناتوفی','natufian'],
 [24000,'سردترین روز آخرین یخبندان','lgm'],
 [40000,'شکارگران برادوستی در زاگرس','baradostian'],
 [45000,'رسیدن انسان خردمند به اروپا','europe-arrival'],
 [55000,'آمیزش با نئاندرتال‌ها','interbreeding'],
 [60000,'خروج بزرگ از آفریقا','out-of-africa'],
 [65000,'رسیدن به استرالیا','australia'],
 [155000,'حوای میتوکندریایی','mito-eve'],
 [300000,'کهن‌ترین انسان خردمند','homo-sapiens'],
 [600000,'جدایی راه ما و نئاندرتال‌ها','neanderthal'],
 [1800000,'انسان راست‌قامت در دمانیسی','dmanisi'],
 [3200000,'لوسی','australopithecus'],
 [7000000,'نیای مشترک ما و شامپانزه','common-ancestor']];
function gen(){
  view.innerHTML=head('ابزار','نسل‌ها','تاریخ با «سال» دور به نظر می‌رسد. با «نسل» نزدیک‌تر است: مادرِ مادرِ مادر… هر پله یک نفر که واقعاً زندگی کرده است.')+
  `<section class="sec"><div class="split"><div class="stage"><div id="spiral"></div><p class="small" style="text-align:center;margin:0">از مرکز (تو) تا لبهٔ بیرونی (آن روز) — هر نقطه یک نسل</p>
     <div class="ctrl"><label for="gl">طول هر نسل</label><input type="range" id="gl" min="18" max="35" step="1" value="25"><span class="read" id="glv"></span></div></div>
    <div class="box"><div class="gpick" id="gpick">${MILE.map((m,i)=>`<button data-i="${i}" class="${i===8?'on':''}">${m[1]}</button>`).join('')}</div></div></div></section>
   <section class="sec"><div class="box" id="gout"></div></section>
   <section class="sec"><header><h2>همهٔ رویدادها</h2><p>شمار نسل‌ها با طول نسلی که انتخاب کرده‌ای.</p></header><div class="box list" style="max-height:none"><table id="gtab"></table></div></section>
   <p class="small">نسل یعنی فاصلهٔ میانگین میان تولد مادر و تولد فرزندش. برای جمعیت‌های انسانی معمولاً میان ۲۵ تا ۳۰ سال برآورد می‌شود؛ پس این عددها تقریبی‌اند و برای حس‌کردن فاصله‌اند، نه برای محاسبهٔ دقیق.</p>`;
  let sel=8;const gl=document.getElementById('gl');
  const svg=d3.select('#spiral').append('svg').attr('viewBox','-250 -250 500 500');
  const gdots=svg.append('g'),gtxt=svg.append('g');
  function draw(){
    const L=+gl.value;document.getElementById('glv').textContent=FA(L)+' سال';
    const m=MILE[sel],g=Math.round(m[0]/L);
    const n=Math.min(g,2600),per=g/n;
    const R=224,GA=Math.PI*(3-Math.sqrt(5));
    const pts=d3.range(n).map(i=>{const th=i*GA,r=R*Math.sqrt((i+0.5)/n);return[Math.cos(th)*r,Math.sin(th)*r]});
    const k=1,dr=Math.max(1.3,Math.min(7,0.78*R/Math.sqrt(n)));
    const col=d3.scaleSequential(t=>d3.interpolateRgb('#b0652a','#4867a8')(t)).domain([0,n]);
    gdots.selectAll('circle').data(pts).join(
      en=>en.append('circle').attr('r',0).call(s=>s.transition().duration(450).delay((d,i)=>i*0.22).attr('r',dr)),
      up=>up.call(s=>s.transition().duration(350).attr('r',dr)),
      ex=>ex.remove())
      .attr('cx',d=>d[0]*k).attr('cy',d=>d[1]*k).attr('fill',(d,i)=>col(i)).attr('opacity',.85);
    gtxt.selectAll('*').remove();
    gtxt.append('circle').attr('r',64).attr('fill',css('--paper')).attr('opacity',.92);
    gtxt.append('text').attr('class','svgtext').attr('text-anchor','middle').attr('y',-6).attr('font-size',30).attr('font-weight',700).text(fmt(g));
    gtxt.append('text').attr('class','svgmuted').attr('text-anchor','middle').attr('y',18).attr('font-size',15).text(per>1.05?`نسل · هر نقطه ${fmt(per)} نسل`:'نسل');
    const km=g*1.5/1000, laps=km/40075, mar=km/42.195;
    document.getElementById('gout').innerHTML=
     `<h3>${esc(m[1])}${m[2]?` <a class="small" href="#/a/${m[2]}">مقاله ←</a>`:''}</h3>
      <p class="read">${yrs(m[0])} · ${fmt(g)} نسل</p>
      <p>اگر هر نسل یک نفر باشد و همه دست در دست هم بدهند — تو، مادرت، مادرِ او و همین‌طور تا آن روز — زنجیره‌ای از ${fmt(g)} نفر می‌شود؛ حدود <b>${fmt(km)} کیلومتر</b>${laps>=1?` یعنی ${FA(laps.toFixed(laps<10?1:0))} بار دور زمین`:` یعنی ${FA(mar.toFixed(mar<10?1:0))} ماراتن`}.</p>
      <p class="small">اگر هر نسل را یک ثانیه بشماری، ${g*1<60?'':''}${fmt(g)} نسل ${g/3600>=24?FA((g/86400).toFixed(1))+' شبانه‌روز':g/60>=60?FA((g/3600).toFixed(1))+' ساعت':FA((g/60).toFixed(1))+' دقیقه'} طول می‌کشد.</p>`;
    document.getElementById('gtab').innerHTML=`<tr><th>رویداد</th><th>سال پیش</th><th>نسل</th></tr>`+MILE.map((x,i)=>
      `<tr${i===sel?' class="hi"':''}><td>${x[2]?`<a href="#/a/${x[2]}">${x[1]}</a>`:x[1]}</td><td class="num">${fmt(x[0])}</td><td class="num">${fmt(x[0]/L)}</td></tr>`).join('');
  }
  document.querySelectorAll('#gpick button').forEach(b=>b.onclick=()=>{sel=+b.dataset.i;document.querySelectorAll('#gpick button').forEach(q=>q.classList.toggle('on',q===b));draw()});
  gl.oninput=draw; draw();
}

/* ============ LITHICS ============ */
const SHP={
 chopper:{v:'0 0 112 128',d:'M20,52 C14,32 34,16 58,16 C84,16 98,34 98,58 C98,86 80,104 54,106 C38,107 26,100 20,90 L38,82 L24,74 L40,66 L24,58 Z',
  s:['M38,82 L62,74','M24,74 L52,66','M40,66 L64,58','M24,58 L48,50'],n:'چاپر (قلوه‌سنگ تراشیده)'},
 flake:{v:'0 0 112 128',d:'M34,24 C52,18 76,26 86,46 C96,68 88,94 68,104 C50,112 32,104 26,86 C20,66 22,30 34,24 Z',
  s:['M34,24 C44,48 50,76 60,102','M30,40 C46,52 58,70 66,92'],n:'تراشه'},
 handaxe:{v:'0 0 112 128',d:'M56,8 C70,32 84,56 84,80 C84,104 72,120 56,122 C40,120 28,104 28,80 C28,56 42,32 56,8 Z',
  s:['M30,72 L56,80','M32,94 L56,98','M82,72 L56,80','M80,94 L56,98','M42,40 L56,58','M70,40 L56,58','M34,56 L56,68','M78,56 L56,68'],n:'تبر دستی'},
 cleaver:{v:'0 0 112 128',d:'M34,18 C48,12 66,14 76,22 C84,40 86,70 84,96 L80,112 L34,112 L28,94 C24,66 26,34 34,18 Z',
  s:['M34,112 L44,92','M52,112 L56,92','M70,112 L68,92','M30,60 L54,66','M82,60 L58,66'],n:'ساطور آشولی'},
 lpoint:{v:'0 0 112 128',d:'M56,26 C76,44 94,72 98,90 C99,99 88,106 74,109 C64,111 48,111 38,109 C24,106 13,99 14,90 C18,72 36,44 56,26 Z',
  s:['M50,40 C44,62 40,84 38,104','M62,40 C68,62 74,84 76,104','M56,34 C56,62 56,84 56,106','M18,94 C40,100 72,100 94,94'],n:'نوک لوالوا',cm:'حدود ۷ سانتی‌متر'},
 scraper:{v:'0 0 112 128',d:'M26,46 C38,28 64,22 84,34 C88,42 82,46 86,52 C90,58 84,62 87,68 C90,74 83,77 85,83 C87,91 78,99 64,103 C46,108 28,98 23,82 C18,66 18,56 26,46 Z',
  s:['M84,34 L70,44','M86,52 L68,56','M85,83 L66,78','M87,68 L68,68','M30,54 C44,64 56,78 60,98'],n:'خراشندهٔ کناری (لبهٔ راست تیز شده)',cm:'حدود ۶ سانتی‌متر'},
 blade:{v:'0 0 112 128',d:'M56,8 C64,14 70,26 70,42 L70,108 C70,118 64,124 56,124 C48,124 42,118 42,108 L42,42 C42,26 48,14 56,8 Z',
  s:['M50,18 L50,118','M62,18 L62,118','M44,46 L68,46','M44,78 L68,78'],n:'تیغه'},
 burin:{v:'0 0 112 128',d:'M44,10 L70,20 C72,40 72,70 70,96 L62,122 L44,120 L40,96 C38,70 38,34 44,10 Z',
  s:['M56,16 L56,116','M44,10 L70,20','M48,44 L66,44','M48,80 L66,80'],n:'قلم (برای کار روی استخوان)'},
 trapeze:{v:'0 0 112 128',d:'M26,48 L86,48 L72,86 L40,86 Z',s:['M34,62 L78,62','M38,74 L74,74'],n:'ریزسنگ ذوزنقه‌ای'},
 hafted:{v:'0 0 112 128',haft:true,n:'ابزار مرکب: ریزسنگ‌ها روی دسته'}};
const LITH=[
 {id:'oldowan',t:'الدوانی',from:2.6e6,to:1.7e6,c:'#8a7a52',mk:'انسان ماهر (و شاید پیش از او)',tq:'ضربهٔ مستقیم با چکش سنگی؛ چند تراشه از لبهٔ یک قلوه‌سنگ.',sh:['chopper','flake'],
  ir:['kashafrud','ganj-par'],note:'ساده به نظر می‌آید، اما شناختن سنگ درست و زاویهٔ درست ضربه خودش دانشی است.'},
 {id:'acheulean',t:'آشولی',from:1.76e6,to:1.3e5,c:'#b0652a',mk:'انسان راست‌قامت و انسان هایدلبرگی',tq:'تراش دوسویه با چکش نرم (شاخ یا استخوان) برای رسیدن به تقارن.',sh:['handaxe','cleaver'],
  ir:['kashafrud','ganj-par'],note:'نخستین ابزاری که شکل نهایی‌اش پیش از ساخت در ذهن سازنده بود.'},
 {id:'mousterian',t:'موستری',from:1.6e5,to:4e4,c:'#3f7f6e',mk:'بیشتر نئاندرتال‌ها؛ در لوانت گاه انسان خردمند',tq:'روش لوالوا: آماده‌سازی سنگ‌مادر، سپس یک ضربه برای تراشهٔ از پیش طراحی‌شده.',sh:['lpoint','scraper'],
  ir:['bisotun','wezmeh','mirak','mar-tarik','kaldar'],note:'تفاوت ابزارها میان لایه‌ها، بحثی نیم‌قرنی ساخت: قوم متفاوت یا کار متفاوت؟'},
 {id:'blades',t:'تیغه‌ای (برادوستی)',sht:'تیغه‌ای',from:4.5e4,to:2e4,c:'#4867a8',mk:'انسان خردمند',tq:'سنگ‌مادر منشوری؛ ده‌ها تیغهٔ بلند پشت سر هم، و سپس ساخت ابزار روی آن‌ها.',sh:['blade','burin'],
  ir:['yafteh','kaldar','eshkaft-gavi','khorramabad'],note:'با همین قلم‌ها بود که کار روی استخوان، شاخ و سوزن ممکن شد.'},
 {id:'microlith',t:'ریزسنگی (زرزی و پس از آن)',sht:'ریزسنگی',from:2e4,to:8e3,c:'#7a7a2a',mk:'شکارگران فراپارینه‌سنگی و نخستین روستاییان',tq:'شکستن تیغه‌های کوچک و شکل‌دادن هندسی؛ سوارکردن چند تکه روی دستهٔ چوبی با قیر یا صمغ.',sh:['trapeze','hafted'],
  ir:['bawa-yawan','ganj-dareh','ali-kosh'],note:'ابزار از یک تکه به مجموعه‌ای از اجزای قابل‌تعویض تبدیل شد؛ پیکان و داس از همین‌جا آمدند.'}];
function stone(el,key,size){
  const S=SHP[key];const svg=d3.select(el).append('svg').attr('viewBox',S.v).attr('width',size).attr('height',size*128/112).attr('class','stonefig');
  const gid='sg'+Math.random().toString(36).slice(2,8);
  const lg=svg.append('defs').append('linearGradient').attr('id',gid).attr('x1',0).attr('y1',0).attr('x2',.6).attr('y2',1);
  lg.append('stop').attr('offset','0%').attr('stop-color','#cfc6b4');lg.append('stop').attr('offset','100%').attr('stop-color','#8e8475');
  if(S.haft){
    svg.append('path').attr('d','M12,112 C40,100 76,70 100,34').attr('stroke','#7b5a35').attr('stroke-width',13).attr('fill','none').attr('stroke-linecap','round');
    svg.append('path').attr('d','M12,112 C40,100 76,70 100,34').attr('stroke','#9b7445').attr('stroke-width',7).attr('fill','none').attr('stroke-linecap','round');
    [[34,96],[58,78],[82,56]].forEach(([x,y])=>{const g=svg.append('g').attr('transform',`translate(${x},${y}) rotate(-34)`);
      g.append('path').attr('d','M-13,-4 L13,-4 L7,12 L-7,12 Z').attr('fill',`url(#${gid})`).attr('stroke','#5f594e').attr('stroke-width',1.2)});
    return}
  svg.append('path').attr('d',S.d).attr('fill',`url(#${gid})`).attr('stroke','#5f594e').attr('stroke-width',1.6).attr('stroke-linejoin','round');
  (S.s||[]).forEach(p=>svg.append('path').attr('d',p).attr('fill','none').attr('stroke','#5f594e').attr('stroke-width',1).attr('opacity',.38));
}
function lithics(){
  view.innerHTML=head('ابزار','جعبه‌ابزار سنگی','سه میلیون سال فناوری در پنج سنت. روی خط زمان یکی را انتخاب کن: ببین چه کسی می‌ساخت، چطور، و در کدام غار ایران پیدا شده است.')+
  `<section class="sec"><div id="ltime"></div></section>
   <section class="sec"><div class="split"><div class="stage" id="lfig"></div><div class="box" id="linfo"></div></div></section>
   <p class="small">طرح‌ها شماتیک‌اند و برای نشان‌دادن ایدهٔ هر سنت کشیده شده‌اند، نه کپی از یک ابزار واقعی. مسیر خواندن: <a href="#/path/toolkit">ابزار در دست</a></p>`;
  const w=1000,h=170,x=d3.scaleLog().domain([3.2e6,6e3]).range([w-30,170]);
  const svg=d3.select('#ltime').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  [[3e6,'۳ میلیون'],[1e6,'۱ میلیون'],[1e5,'۱۰۰ هزار'],[1e4,'۱۰ هزار سال پیش']].forEach(([v,l])=>{
    svg.append('line').attr('x1',x(v)).attr('x2',x(v)).attr('y1',16).attr('y2',h-30).attr('stroke',css('--rule')).attr('stroke-dasharray','2 4');
    svg.append('text').attr('class','svgmuted').attr('x',x(v)).attr('y',h-10).attr('font-size',15).attr('text-anchor','middle').text(l)});
  const rows=svg.selectAll('g.li').data(LITH).join('g').attr('class','li').style('cursor','pointer')
    .attr('transform',(d,i)=>`translate(0,${20+i*26})`).on('click',(e,d)=>pick(d.id));
  rows.append('rect').attr('x',d=>x(d.to)).attr('width',d=>Math.max(8,x(d.from)-x(d.to))).attr('y',2).attr('height',18).attr('rx',9).attr('fill',d=>d.c);
  rows.append('text').attr('class','svgtext').attr('x',160).attr('y',15).attr('font-size',15).attr('text-anchor','start').text(d=>d.sht||d.t);
  function pick(id){
    const L=LITH.find(l=>l.id===id);rows.attr('opacity',d=>d.id===id?1:.3);
    const fig=document.getElementById('lfig');fig.innerHTML='<div class="figrow" id="fr"></div>';
    const fr=document.getElementById('fr');
    L.sh.forEach(k=>{const c=document.createElement('figure');fr.appendChild(c);const holder=document.createElement('div');c.appendChild(holder);
      stone(holder,k,210);const cap=document.createElement('figcaption');cap.innerHTML=esc(SHP[k].n)+'<span class="sbar"><i></i>'+(SHP[k].cm||'حدود ۸ سانتی‌متر')+'</span>';c.appendChild(cap)});
    document.getElementById('linfo').innerHTML=
     `<h3><span class="dot" style="background:${L.c}"></span>${L.t}</h3>
      <p class="read">${yrs(L.from)} تا ${yrs(L.to)}</p>
      <p>${esc(L.note)}</p>
      <p class="small"><b>سازنده:</b> ${esc(L.mk)}</p>
      <p class="small"><b>فن:</b> ${esc(L.tq)}</p>
      <p class="small"><b>در ایران:</b> ${L.ir.map(i=>A[i]?`<a href="#/a/${i}">${A[i].t}</a>`:i).join(' · ')}</p>
      <p><a class="btn" href="#/a/${L.id}">مقالهٔ کامل ←</a></p>`;
  }
  pick('mousterian');
}

/* ============ NEEDED SOURCES ============ */
function need(){
  const bs=W.books.filter(b=>!b.have).map(b=>({b,n:(b.on||[]).length})).sort((p,q)=>q.n-p.n);
  const thin=W.articles.filter(a=>a.body.join(' ').length<520).sort((p,q)=>p.body.join(' ').length-q.body.join(' ').length);
  const nosrc=W.articles.filter(a=>!W.books.some(b=>(b.on||[]).includes(a.id)));
  view.innerHTML=head('','منابعی که لازم است','اگر هر کدام از این‌ها را داری یا پیدا کردی، بفرست. فهرست بر پایهٔ اینکه هر منبع به چند مقاله کمک می‌کند مرتب شده است.')+
  `<section class="sec"><header><h2>کتاب‌ها و مقاله‌ها</h2><p>${FA(bs.length)} منبع</p></header><ol class="needl">${bs.map(({b,n})=>`<li><b>${esc(b.t)}</b><span>${esc(b.a||'')}</span><small>${n?`پشتوانهٔ ${FA(n)} مقاله: ${(b.on||[]).map(i=>`<a href="#/a/${i}">${label(i)}</a>`).join('، ')}`:''}${b.note?` · ${esc(b.note)}`:''}</small></li>`).join('')}</ol></section>
  <section class="sec"><header><h2>مقاله‌های کوتاه</h2><p>این‌ها بیشترین نیاز را به منبع تازه دارند.</p></header><div class="rows">${thin.map(a=>`<a href="#/a/${a.id}">${a.t}</a>`).join('')}</div></section>
  <section class="sec"><header><h2>مقاله‌های بی‌منبعِ کتابخانه‌ای</h2><p>${FA(nosrc.length)} مقاله هنوز هیچ کتاب یا مقاله‌ای در کتابخانه پشتشان نیست.</p></header><div class="rows">${nosrc.map(a=>`<a href="#/a/${a.id}">${a.t}</a>`).join('')}</div></section>
  <p class="eyebrow">فهرست کامل‌تر در <a href="#/gaps">جاهای خالی</a>.</p>`;
}

/* ============ DOMESTICATION ============ */
const DOM=[
 ["dog","سگ",15000,[50,48],"جانور","سرچشمه محل بحث؛ شواهد قطعی ~۱۵ هزار"],["goat","گوسفند",11000,[42,38],"جانور","آناتولی شرقی و زاگرس"],["goat","بز",10000,[47.6,34.3],"جانور","گنج‌دره، کرمانشاه"],
 ["wheat-barley","جو و گندم",11000,[46.4,33.2],"گیاه","چغاگلان و هلال حاصلخیز"],["cattle","گاو بی‌کوهان",10500,[38.5,37],"جانور","فرات علیا"],[null,"خوک",10500,[40,37.5],"جانور","آناتولی جنوب‌شرقی"],
 [null,"گربه",9500,[33,35],"جانور","گور مشترک انسان و گربه در قبرس"],[null,"برنج",9000,[120,30],"گیاه","درهٔ یانگ‌تسه"],[null,"ذرت",9000,[-100,18],"گیاه","جنوب مکزیک"],
 [null,"کدو و موز",8000,[143,-6],"گیاه","گینهٔ نو (موز و قلقاس)"],["cattle","گاو کوهان‌دار",8000,[68,27],"جانور","درهٔ سند"],[null,"سیب‌زمینی",8000,[-70,-15],"گیاه","آند"],
 [null,"اسب",5500,[69,53],"جانور","استپ؛ اسب امروزی ~۴٫۲ هزار"],[null,"شتر یک‌کوهانه",3000,[52,20],"جانور","جنوب عربستان"]];
function dom(){
  view.innerHTML=head('ابزار','اهلی‌سازی در جهان','کجا و کی؟ نوار را بکش تا گیاهان و جانوران به ترتیب اهلی شدن روی نقشه بیایند. زمان‌ها تقریبی‌اند و بر اساس قدیمی‌ترین شواهد پذیرفته‌شده.')+
  `<div class="split"><div class="stage"><div id="dmap"></div><div class="ctrl"><button id="dop">پخش</button><input type="range" id="dor" min="0" max="13000" step="100" value="13000"><span class="read" id="dov"></span></div><div class="legend"><span><span class="dot" style="background:#7a7a2a"></span>گیاه</span><span><span class="dot" style="background:#b0652a"></span>جانور</span></div></div><div class="box list" id="dol"></div></div>`;
  const w=1000,h=520;const svg=d3.select('#dmap').append('svg').attr('viewBox',`0 0 ${w} ${h}`);
  const proj=d3.geoEqualEarth().rotate([-20,0]).fitExtent([[6,6],[w-6,h-6]],{type:"Sphere"});baseMap(svg,proj,w,h);
  const g=svg.append('g').selectAll('g').data(DOM).join('g').attr('transform',d=>`translate(${proj(d[3])})`).style('cursor',d=>d[0]?'pointer':'default').on('click',(e,d)=>{if(d[0])location.hash='#/a/'+d[0]});
  g.append('circle').attr('r',7).attr('fill',d=>d[4]==='گیاه'?'#7a7a2a':'#b0652a').attr('stroke',css('--card')).attr('stroke-width',1.5);
  g.append('text').attr('class','svgtext').attr('font-size',12).attr('dy',-11).attr('text-anchor','middle').text(d=>d[1]).style('paint-order','stroke').style('stroke',css('--card')).style('stroke-width','3px');
  const r=document.getElementById('dor');
  r.oninput=()=>{const t=16000-(+r.value);document.getElementById('dov').textContent=fmt(t)+' سال پیش';g.attr('opacity',d=>d[2]>=t?1:0);
   const on=DOM.filter(d=>d[2]>=t).sort((a,b)=>b[2]-a[2]);document.getElementById('dol').innerHTML=`<table><tr><th>چه</th><th>کی</th><th>کجا</th></tr>${on.map(d=>`<tr><td>${d[0]?`<a href="#/a/${d[0]}">${d[1]}</a>`:d[1]}</td><td class="num">${fmt(d[2]/1000)} هـ</td><td>${d[5]}</td></tr>`).join('')}</table>`};
  r.value=0;r.oninput();cleanup=playBtn(document.getElementById('dop'),r,100,90);
}

/* ============ CLOCK ============ */
const CLK=[[4.54e9,"پیدایش زمین","earth-forms"],[3.5e9,"نخستین شواهد حیات","archean-life"],[2.4e9,"رویداد بزرگ اکسایش","great-oxidation"],[5.41e8,"انفجار کامبرین","cambrian"],[2.52e8,"بزرگ‌ترین انقراض","end-permian"],[6.6e7,"پایان دایناسورها","kpg"],[7e6,"جدایی شاخهٔ انسان و شامپانزه","common-ancestor"],[3.2e6,"لوسی","australopithecus"],[1.8e6,"انسان راست‌قامت در دمانیسی","dmanisi"],[3e5,"انسان خردمند","homo-sapiens"],[5e4,"خروج اصلی از آفریقا","out-of-africa"],[1.15e4,"آغاز کشاورزی","neolithic"],[5e3,"خط","present"]];
function clock(){
  view.innerHTML=head('ابزار','ساعت زمین','اگر ۴٫۵۴ میلیارد سال تاریخ زمین در یک شبانه‌روز (۲۴ ساعت) فشرده شود، هر رویداد کی رخ می‌دهد؟ تمام داستان انسان در کمتر از دو دقیقهٔ پایانی می‌گنجد.')+
  `<div class="split"><div class="stage"><div id="ck"></div></div><div class="box list"><table><tr><th>ساعت</th><th>رویداد</th></tr>${CLK.map(c=>`<tr><td class="num">${clk(c[0])}</td><td>${A[c[2]]?`<a href="#/a/${c[2]}">${c[1]}</a>`:`<a href="${ERA_LINK(c[2])}">${c[1]}</a>`}</td></tr>`).join('')}</table></div></div>`;
  const w=600,R=250;const svg=d3.select('#ck').append('svg').attr('viewBox',`${-w/2} ${-w/2} ${w} ${w}`);
  svg.append('circle').attr('r',R).attr('fill',css('--wash')).attr('stroke',css('--rule'));
  for(let i=0;i<24;i++){const a=i/24*2*Math.PI;svg.append('line').attr('x1',Math.sin(a)*(R-8)).attr('y1',-Math.cos(a)*(R-8)).attr('x2',Math.sin(a)*R).attr('y2',-Math.cos(a)*R).attr('stroke',css('--muted'));
    if(i%3===0)svg.append('text').attr('class','svgmuted').attr('font-size',13).attr('text-anchor','middle').attr('x',Math.sin(a)*(R-26)).attr('y',-Math.cos(a)*(R-26)+5).text(FA(i||24))}
  CLK.forEach((c,i)=>{const f=1-c[0]/4.54e9,a=f*2*Math.PI;const rr=R-40-(i%3)*34;
    svg.append('line').attr('x1',0).attr('y1',0).attr('x2',Math.sin(a)*rr).attr('y2',-Math.cos(a)*rr).attr('stroke',f>0.999?'#a8404f':css('--accent')).attr('stroke-opacity',.5);
    svg.append('circle').attr('cx',Math.sin(a)*rr).attr('cy',-Math.cos(a)*rr).attr('r',4).attr('fill',f>0.999?'#a8404f':css('--accent'))
     .on('mousemove',e=>showTip(e,`${c[1]}<br>ساعت ${clk(c[0])}`)).on('mouseleave',hideTip)});
  svg.append('circle').attr('r',5).attr('fill',css('--ink'));
}
function clk(y){const s=86400*(1-y/4.54e9);const h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=Math.floor(s%60);return FA(`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`)}

/* ============ QUIZ ============ */
const QZ=[
 ["انسان از شامپانزه فرگشت یافته است.",false,"ما و شامپانزه‌ها نیای مشترکی داریم که حدود ۶ تا ۷ میلیون سال پیش می‌زیست.","common-ancestor"],
 ["«نظریه» در علم یعنی حدس.",false,"نظریهٔ علمی چارچوبی آزموده و پرشاهد است که پیش‌بینی می‌کند.","only-theory"],
 ["جهش‌ها تصادفی‌اند، اما انتخاب طبیعی تصادفی نیست.",true,"انتخاب طبیعی مثل الکی است که تغییرهای تصادفی را بارها غربال می‌کند.","natural-selection"],
 ["مردم غیرآفریقایی امروز کمی DNA نئاندرتالی دارند.",true,"حدود ۱ تا ۲ درصد، از آمیزش حدود ۵۰ تا ۴۵ هزار سال پیش.","interbreeding"],
 ["نخستین ویژگی شاخهٔ انسان، مغز بزرگ بود.",false,"دوپایی میلیون‌ها سال پیش از مغز بزرگ آمد.","bipedalism"],
 ["تا حدود ۴۰ هزار سال پیش چند گونهٔ انسان هم‌زمان روی زمین زندگی می‌کردند.",true,"خردمند، نئاندرتال، دنیسووایی، فلورسی و… ابزار «هم‌روزگاری» را ببین.","hominins"],
 ["نخستین انسانی که از آفریقا بیرون رفت، انسان خردمند بود.",false,"انسان راست‌قامت حدود ۱٫۸ میلیون سال پیش در دمانیسی گرجستان بود.","homo-erectus"],
 ["سگ پیش از کشاورزی اهلی شد.",true,"سگ تنها جانوری است که در دوران شکارگری اهلی شد.","dog"],
 ["کهن‌ترین شواهد گله‌داری بز از زاگرس ایران است.",true,"گنج‌دره در کرمانشاه، حدود ۱۰ هزار سال پیش.","ganj-dareh"],
 ["رادیوکربن می‌تواند سن سنگوارهٔ لوسی را تعیین کند.",false,"رادیوکربن تنها تا حدود ۵۰ هزار سال کار می‌کند؛ لوسی ۳٫۲ میلیون ساله است.","radiocarbon"],
 ["انسان‌ها از نظر ژنتیکی به چند نژاد زیستیِ جدا تقسیم می‌شوند.",false,"بیشتر تنوع ژنتیکی درون گروه‌هاست و تنوع انسان‌ها پیوسته است.","race-myth"],
 ["یکجانشینی در برخی جاها پیش از کشاورزی کامل آغاز شد.",true,"ناتوفیان و سازندگان گوبکلی‌تپه نمونه‌اند.","sedentism"]];
function quiz(){
  view.innerHTML=head('ابزار','افسانه یا واقعیت',`${FA(QZ.length)} جمله دربارهٔ تبار انسان. درست است یا نادرست؟ پس از پاسخ، توضیح و پیوند مقاله می‌آید.`)+`<div id="qz"></div><p class="lede" id="qs"></p>`;
  let score=0,done=0;const box=document.getElementById('qz');
  box.innerHTML=QZ.map((q,i)=>`<div class="q" id="q${i}"><p class="st">${FA(i+1)}. ${q[0]}</p><div class="ctrl"><button data-i="${i}" data-v="1">درست</button><button data-i="${i}" data-v="0">نادرست</button></div><div class="ans" hidden></div></div>`).join('');
  box.querySelectorAll('button').forEach(b=>b.onclick=()=>{const i=+b.dataset.i,q=QZ[i],qd=document.getElementById('q'+i);if(qd.dataset.done)return;qd.dataset.done=1;done++;
    const ok=(b.dataset.v==='1')===q[1];if(ok)score++;b.classList.add('on');const an=qd.querySelector('.ans');an.hidden=false;
    an.innerHTML=`<span class="${ok?'ok':'no'}">${ok?'آفرین، درست گفتی.':'نه دقیقاً.'}</span> این جمله ${q[1]?'درست':'نادرست'} است. ${q[2]} <a href="#/a/${q[3]}">بیشتر بخوان</a>`;
    document.getElementById('qs').textContent=`${FA(score)} از ${FA(done)} پاسخ درست`});
}

/* ============ PEOPLE / LIBRARY / GAPS ============ */
function people(){view.innerHTML=head('','دانشمندان و نویسندگان','کسانی که داستان تبار انسان را کشف کردند یا روایت کردند.')+`<div class="cards" style="margin-top:18px">${W.people.map(p=>`<a class="pcard" href="#/p/${p.id}"><b>${p.n}</b><small>${p.y} · ${p.role}</small><span>${esc(p.sum.replace(/\[\[[^\]|]+\|?([^\]]*)\]\]/g,'$1')).slice(0,140)}…</span></a>`).join('')}</div>`}
function library(){
  const SH={cosmos:'کیهان و حیات',evolution:'فرگشت و روش علم',humans:'پیدایش انسان',ha:'پادکست خداحافظ آفریقا',history:'تاریخ جهان و تمدن‌ها',future:'جهان امروز و آینده',mind:'ذهن، فلسفه و معنا'};
  const order=['humans','ha','evolution','cosmos','history','future','mind'];
  view.innerHTML=head('','کتابخانه','کتاب‌ها، مقاله‌ها، داده‌ها و ویدیوهایی که این ویکی بر آن‌ها ساخته شده یا باید ساخته شود. «دارم» یعنی متن یا فایلش در دست است.')+
  `<section class="sec"><header><h2>کتاب و مقاله</h2></header><div class="box list" style="max-height:none"><table><tr><th>عنوان</th><th>نویسنده / مترجم</th><th>وضعیت</th></tr>${W.books.map(b=>`<tr><td>${esc(b.t)}<br><small class="chip">${b.k}</small></td><td>${esc(b.a)}${b.note?`<br><small style="color:var(--muted)">${esc(b.note)}</small>`:''}</td><td class="${b.have?'have':'need'}">${b.have?'دارم':'لازم'}</td></tr>`).join('')}</table></div></section>
  <section class="sec"><header><h2>داده‌ها</h2></header><div class="cards">${W.datasets.map(d=>`<a class="pcard" href="${d.u}" target="_blank" rel="noopener"><b class="latin" style="text-align:start">${esc(d.t)}</b><small class="${d.have?'have':'need'}">${d.have?'در ویکی استفاده شده':'هنوز نگرفته‌ایم'}</small><span>${esc(d.d)}</span></a>`).join('')}</div></section>
  <section class="sec"><header><h2>ویدیوها</h2><p>${FA(V.length)} ویدیو با متن کامل در <a href="archive.html">آرشیو</a>.</p></header>${order.map(k=>{const vs=V.filter(v=>v.s===k);return vs.length?`<div class="shelf"><h3>${SH[k]}</h3><ul class="vlist">${vs.map(v=>`<li><a href="https://youtu.be/${v.id}" target="_blank" rel="noopener">${esc(v.t)}</a><span class="dur">${hms(v.dur)}</span></li>`).join('')}</ul></div>`:''}).join('')}</section>`;
}
function allGaps(){
  const g=[["کل ویکی","متن قسمت‌های ۱ تا ۱۰ پادکست خداحافظ آفریقا"],["کل ویکی","متن قسمت‌های ۲۳، ۲۴، ۲۸ و ۲۹"],...(W.extraGaps||[])];
  W.articles.forEach(a=>(a.gaps||[]).forEach(x=>g.push([a.id,x])));W.people.forEach(p=>(p.gaps||[]).forEach(x=>g.push([p.id,x])));
  W.articles.forEach(a=>{const n=(a.body.join(' ').match(/\(؟\)/g)||[]).length;if(n)g.push([a.id,`${FA(n)} جمله با نشان (؟) که منبع می‌خواهد`])});
  return g;
}
function gaps(){
  const g=allGaps();
  view.innerHTML=head('','جاهای خالی',`${FA(g.length)} چیز که هنوز کم است. اگر هر کدام را پیدا کردی، بفرست تا جایش بنشیند.`)+
  `<div class="box list" style="max-height:none;margin-top:18px"><table><tr><th>کجا</th><th>چه لازم است</th></tr>${g.map(x=>`<tr><td>${href(x[0])?`<a href="${href(x[0])}">${label(x[0])}</a>`:x[0]}</td><td>${esc(x[1])}</td></tr>`).join('')}</table></div>`;
}

/* ============ ROUTER ============ */
function route(){
  if(cleanup){cleanup();cleanup=null} hideTip();
  const h=(location.hash||'#/').slice(1); const [,a,b]=h.split('/');
  ({'':()=>{home();const v=(W.versions||[])[0];if(v)view.insertAdjacentHTML('afterbegin',`<a class="vbanner" href="#/news"><b>نسخهٔ ${v.v}</b> · ${esc(v.t)} — ببین چه اضافه شده و نظرت را بگو ←</a>`)},a:()=>article(b),p:()=>person(b),graph,coexist,brain,migrate,sites,iran,news,c14,dna:()=>dna(b),genes,mtree,need,clocks,gen,lithics,search:()=>searchPage(b),path:()=>pathPage(b),dom,clock,quiz,people,library,gaps}[a||'']||notFound)();
  setNav(); window.scrollTo(0,0);
  const t=a==='a'&&A[b]?A[b].t:a==='p'&&P[b]?P[b].n:null; document.title=t?t+' — ویکی تبار':'ویکی تبار';
}
const lazy={c14:['data/p3k.js','P3K'],dna:['data/aadr.js','AADR'],sites:['data/road.js','ROAD'],iran:['data/road.js','ROAD']};
function go(){const k=(location.hash||'').split('/')[1];if(lazy[k]&&!window[lazy[k][1]]){const s=document.createElement('script');s.src=lazy[k][0];s.onload=route;document.body.appendChild(s);view.innerHTML='<p class="lede">در حال بارگذاری داده…</p>';return}route()}
const sf=document.getElementById('sf');
if(sf){sf.onsubmit=e=>{e.preventDefault();const v=document.getElementById('sq').value.trim();if(v){location.hash='#/search/'+encodeURIComponent(v);document.getElementById('sq').blur()}}}
addEventListener('hashchange',go); go();
document.addEventListener('click',e=>{document.querySelectorAll('#nav details[open]').forEach(d=>{if(!d.contains(e.target))d.removeAttribute('open')})});
document.addEventListener('keydown',e=>{if((e.key==='/'||(e.key==='k'&&(e.metaKey||e.ctrlKey)))&&!/^(input|textarea|select)$/i.test(e.target.tagName)){e.preventDefault();const q=document.getElementById('sq');if(q)q.focus()}});
document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('#nav details[open]').forEach(d=>d.removeAttribute('open'))});
})();
