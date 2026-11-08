const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const ROOT=require('path').resolve(__dirname,'..');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const bad=new Map();let n=0;
async function check(rel, acts){const url='file://'+ROOT+'/'+rel; await p.goto(url); await p.waitForTimeout(400); if(acts) await acts(p);
  const hrefs=await p.evaluate(()=>[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')));
  for(const h of hrefs){ if(!h||/^(https?:|mailto:|#|javascript)/.test(h)) continue; n++;
    let u=h.split('#')[0].split('?')[0]; if(!u) continue; let f=path.normalize(path.join(path.dirname(ROOT+'/'+rel), decodeURIComponent(u))); if(u.endsWith('/')) f=path.join(f,'index.html');
    if(!fs.existsSync(f)&&!fs.existsSync(f+'.html')){ bad.set(rel+' → '+h,1); } } }
await check('index.html'); await check('atlas/index.html'); await check('atlas/lands.html'); await check('atlas/bridge.html'); await check('atlas/bridge.html#psygen'); await check('iran/index.html'); await check('core/people.html'); await check('core/sources.html');
for(const w of ['tabar','soc','phil']){ await check(w+'/index.html'); const ids=await p.evaluate(()=>[...document.querySelectorAll('[data-go]')].map(e=>e.dataset.go.split(':')[1])); for(const id of ids){ await check(w+'/index.html#'+id); } }
console.log(n,'links checked;',bad.size,'broken'); for(const k of bad.keys()) console.log(k); await b.close();})();
