/* Source travels with the content: copy carries a citation, screenshots and prints carry a faint mark. */
(() => {
  const host = location.host + location.pathname.replace(/[^/]*$/, "");
  const cite = () => "منبع: " + document.title + " — " + location.href.split("#")[0] + (location.hash || "") +
    " (برداشت " + new Date().toISOString().slice(0, 10) + ")";
  document.addEventListener("copy", e => {
    const sel = getSelection(); const txt = sel ? sel.toString() : "";
    if (!e.clipboardData || txt.trim().length < 60) return;
    const box = document.createElement("div");
    for (let i = 0; i < sel.rangeCount; i++) box.appendChild(sel.getRangeAt(i).cloneContents());
    const c = cite();
    e.clipboardData.setData("text/plain", txt + "\n\n" + c);
    e.clipboardData.setData("text/html", box.innerHTML + '<p style="font-size:.85em;color:#666">' +
      c.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</p>");
    e.preventDefault();
  });
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="420" height="260"><text x="210" y="130" ' +
    'text-anchor="middle" transform="rotate(-24 210 130)" font-family="sans-serif" font-size="15" ' +
    'fill="#808080" fill-opacity=".5">' + host.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</text></svg>";
  const st = document.createElement("style");
  st.textContent = "body::after{content:'';position:fixed;inset:0;pointer-events:none;z-index:2147483000;" +
    "opacity:.11;background-image:url(\"data:image/svg+xml," + encodeURIComponent(svg) + "\")}" +
    "@media print{body::after{opacity:.22}body::before{content:'" + host + "';display:block;font:12px sans-serif;color:#555;margin-bottom:8px}}";
  document.head.appendChild(st);
  const note = document.createElement("div");
  note.setAttribute("dir", "rtl");
  note.style.cssText = "margin:28px auto 16px;max-width:900px;padding:10px 16px;font-size:.8rem;line-height:1.9;opacity:.75;text-align:center";
  const b = document.createElement("button");
  b.type = "button"; b.textContent = "کپی ارجاع این صفحه";
  b.style.cssText = "font:inherit;margin-inline-start:8px;padding:2px 10px;border:1px solid currentColor;border-radius:999px;background:none;color:inherit;cursor:pointer";
  b.addEventListener("click", () => { const c = cite(); (navigator.clipboard ? navigator.clipboard.writeText(c) : Promise.reject()).then(() => { b.textContent = "کپی شد"; }, () => { b.textContent = c; }); });
  note.append("استفاده از این متن با ذکر منبع و نشانی صفحه آزاد است؛ استفادهٔ تجاری یا بازنشر انبوه فقط با اجازه. ", b);
  const put = () => document.body.appendChild(note);
  document.body ? put() : addEventListener("DOMContentLoaded", put);
})();
