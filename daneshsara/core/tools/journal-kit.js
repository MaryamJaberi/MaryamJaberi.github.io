/* Shared helpers for the «دفتر میدانی» (field journal) pages. Needs lab-kit.js.
   JournalKit.start({id, wiki, labels, exps, first}) wraps LabKit.start and adds progress (kept only in this browser).
   J.finish(key) marks a leaf done; J.next(key) is a «برگ بعد» button; J.dots() is a stacked dot plot (one dot = one individual);
   J.quiz(Q, summary) builds a picture quiz: Q = [[question, [[svg, label], ...], correctIndex, explanation]]. */
(function(){
const K=LabKit, fa=K.fa, J={};
let ORDER=[], done={}, KEY="";
J.finish=k=>{ if(done[k])return; done[k]=1; try{localStorage.setItem(KEY,JSON.stringify(done))}catch(_){} prog(); };
function prog(){
  const n=ORDER.filter(k=>done[k]).length;
  document.getElementById("prog").textContent=`${fa(n)} از ${fa(ORDER.length)} برگ کامل شده است.`;
  document.querySelectorAll("#tabs button").forEach(b=>b.classList.toggle("done",!!done[b.dataset.k]));
}
J.next=k=>{const i=ORDER.indexOf(k); return i<ORDER.length-1?`<p><a class="btn" href="#${ORDER[i+1]}">برگ بعد</a></p>`:""};
J.mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
J.rnd=seed=>{let s=seed; return ()=>{s=(s*16807)%2147483647; return s/2147483647}};
J.norm=r=>Math.sqrt(-2*Math.log(r()+1e-9))*Math.cos(6.2832*r());
/* stacked dot plot: one dot = one individual */
J.dots=function(rows,o){
  const W=o.w||340, pad=14, min=o.min, max=o.max, r=o.r||2.4, st=o.st||r*2+.4;
  const X=v=>pad+(v-min)/(max-min)*(W-2*pad);
  let top=0; const layers=rows.map(row=>{const c={}; let m=0; const pts=row.vals.map(v=>{const b=Math.round(v*10); c[b]=(c[b]||0)+1; m=Math.max(m,c[b]); return [v,c[b]-1]}); top=Math.max(top,m); return {row,pts,m}});
  let y=8, out="";
  layers.forEach(L=>{
    const h=Math.max(L.m*st+8,26), base=y+h;
    out+=`<line x1="${pad}" x2="${W-pad}" y1="${base}" y2="${base}" stroke="${K.css("--line-strong")}"/>`;
    out+=L.pts.map(p=>`<circle cx="${X(p[0]).toFixed(1)}" cy="${(base-r-1-p[1]*st).toFixed(1)}" r="${r}" fill="${L.row.color}" fill-opacity="${L.row.op||.85}"/>`).join("");
    (L.row.marks||[]).forEach(mk=>{out+=`<line x1="${X(mk.x)}" x2="${X(mk.x)}" y1="${y}" y2="${base+4}" stroke="${mk.color}" stroke-width="2" ${mk.dash?'stroke-dasharray="4 3"':""}/><text x="${X(mk.x)+(mk.dx||0)}" y="${y-1+(mk.dx?11:0)}" font-size="10" text-anchor="middle" fill="${mk.color}" direction="rtl">${mk.label}</text>`});
    if(L.row.label) out+=`<text x="${W-pad}" y="${y+10}" font-size="10.5" text-anchor="start" fill="${K.css("--ink-2")}" direction="rtl">${L.row.label}</text>`;
    y=base+ (o.gap||22);
  });
  const ay=y-(o.gap||22);
  for(let t=Math.ceil(min);t<=max;t+=o.tick||1) out+=`<line x1="${X(t)}" x2="${X(t)}" y1="${ay}" y2="${ay+4}" stroke="${K.css("--ink-3")}"/><text x="${X(t)}" y="${ay+15}" font-size="10" text-anchor="middle" fill="${K.css("--ink-2")}">${fa(t,1)}</text>`;
  out+=`<text x="${W/2}" y="${ay+29}" font-size="10.5" text-anchor="middle" fill="${K.css("--ink-2")}" direction="rtl">${o.axis}</text>`;
  return `<svg class="fig" viewBox="0 -6 ${W} ${ay+40}" role="img" aria-label="${o.alt}">${out}</svg>`;
};
J.quiz=(Q,summary)=>(pn,out)=>{
  let score=0, ans=0;
  pn.innerHTML=Q.map((q,i)=>`<div class="q" data-q="${i}"><p>${fa(i+1)}. ${q[0]}</p><div class="opts${q[1][0][0]?"":" txt"}">${q[1].map((o,j)=>`<button type="button" class="opt" data-j="${j}">${o[0]}<span>${o[1]}</span></button>`).join("")}</div><div class="fb"></div></div>`).join("");
  pn.addEventListener("click",e=>{
    const b=e.target.closest(".opt"); if(!b) return; const qd=b.closest(".q"); if(qd.dataset.d) return; qd.dataset.d=1;
    const i=+qd.dataset.q, j=+b.dataset.j, q=Q[i]; ans++; if(j===q[2]) score++;
    qd.querySelectorAll(".opt").forEach((o,k)=>{o.disabled=true; if(k===q[2]) o.classList.add("good"); else if(k===j) o.classList.add("bad")});
    qd.querySelector(".fb").innerHTML=`<div class="ans"><b>${j===q[2]?"درست.":"نه."}</b> ${q[3]}</div>`;
    if(ans===Q.length){ J.finish("check"); out.innerHTML=`<div class="res"><h3>${fa(score)} از ${fa(Q.length)}</h3>${summary}</div>`; }
  });
};
J.start=cfg=>{
  ORDER=Object.keys(cfg.exps); KEY="ds-journal-"+cfg.id;
  try{done=JSON.parse(localStorage.getItem(KEY)||"{}")||{}}catch(_){done={}}
  K.start(cfg); prog();
};
window.JournalKit=J;
})();
