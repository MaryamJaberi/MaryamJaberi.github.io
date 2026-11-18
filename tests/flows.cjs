// تست‌های کارکردی مخصوص هر پروژه: یک مسیر کوتاه کاربر، بدون شبکهٔ بیرونی (هیچ داده‌ای جایی فرستاده نمی‌شود)
const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const ROOT=require('path').resolve(__dirname,'..');
const T={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2','.mp3':'audio/mpeg','.webmanifest':'application/manifest+json'};
const srv=http.createServer((q,s)=>{let f=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]));if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){s.writeHead(404);return s.end()}s.writeHead(200,{'Content-Type':T[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(s)}).listen(8792);
const B='http://localhost:8792/';
const FLOWS={
 tiktak:['Dour/',['شروع بازی جدید']],
 polyglot:['Language-Learning-Party-Game/',['رد کردن','شروع بازی دورهمی']],
 planet:['earth-through-time/',['۶۶ میلیون','انسان‌ها','پخش']],
 nightshift:['mafia/',['ورود و راه‌اندازی مسابقه']],
 teamweather:['wellbeing-check/',['Probeer de scan zelf']],
 darang:['darang/',['یک نمونهٔ آماده ببین']],
 slowverse:['ganjoor-no/',['همه ۲۴۶ شاعر']],
};
(async()=>{const b=await chromium.launch();const out={};
for(const [k,[u,steps]] of Object.entries(FLOWS)){
 for(const vw of [[1300,850],[390,844]]){
 const ctx=await b.newContext({viewport:{width:vw[0],height:vw[1]}});await ctx.route(/^https?:\/\/(?!localhost)/,r=>r.abort());
 const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message.slice(0,140)));
 const log=[];
 try{await p.goto(B+u,{waitUntil:'load'});await p.waitForTimeout(1500);
  for(const s of steps){const el=p.getByText(s,{exact:false}).first();
   if(await el.count()&&await el.isVisible()){await el.click({timeout:4000}).then(()=>log.push('ok:'+s)).catch(e=>log.push('noclick:'+s));await p.waitForTimeout(1500)}else log.push('missing:'+s)}
  const ov=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
  const btn=await p.$$eval('button,[role=button]',x=>x.filter(e=>e.offsetParent).map(e=>(e.innerText||e.getAttribute('aria-label')||'').trim().slice(0,24)).filter(Boolean).slice(0,14));
  await p.screenshot({path:`flow_${k}_${vw[0]}.png`});
  out[k+'_'+vw[0]]={log,errs,overflow:ov,next:btn};
 }catch(e){out[k+'_'+vw[0]]={error:String(e).slice(0,160),log,errs}}
 await ctx.close()}}
fs.writeFileSync('flows.json',JSON.stringify(out,null,1));console.log(JSON.stringify(out,null,1).slice(0,6000));await b.close();srv.close()})();
