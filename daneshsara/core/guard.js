/* Source travels with the content: copy carries a citation, screenshots and prints carry a faint mark. */
(() => {
  if (window.__VAULT_PAGE) return;   /* داخل گاوصندوق: محتوای خصوصی، بدون نشان و بدون ارجاع */
  const SELF = document.currentScript;
  const WANT_NOTE = !(SELF && SELF.dataset && SELF.dataset.note === 'off');   /* data-note="off" → بدون یادداشت پانویس */
  const host = location.host + location.pathname.replace(/[^/]*$/, "");
  /* متن یادداشت به زبان صفحه (html lang)؛ هر زبان ناشناخته فارسی می‌ماند تا صفحه‌های دانش‌سرا تغییری نکنند */
  const TX = {
    fa: ["منبع", "برداشت", "استفاده از این متن با ذکر منبع و نشانی صفحه آزاد است؛ استفادهٔ تجاری یا بازنشر انبوه فقط با اجازه. ", "کپی ارجاع این صفحه", "کپی شد"],
    en: ["Source", "retrieved", "You may use this text if you name the source and the page address; commercial use or bulk republication needs permission. ", "Copy a citation for this page", "Copied"],
    nl: ["Bron", "geraadpleegd op", "U mag deze tekst gebruiken met bronvermelding en het adres van de pagina; commercieel gebruik of grootschalige herpublicatie alleen met toestemming. ", "Bronvermelding kopiëren", "Gekopieerd"],
    de: ["Quelle", "abgerufen am", "Sie dürfen diesen Text mit Quellenangabe und Seitenadresse verwenden; kommerzielle Nutzung oder massenhafte Weiterveröffentlichung nur mit Genehmigung. ", "Quellenangabe kopieren", "Kopiert"],
    fr: ["Source", "consulté le", "Vous pouvez utiliser ce texte en citant la source et l'adresse de la page ; usage commercial ou republication en masse uniquement sur autorisation. ", "Copier la référence de cette page", "Copié"],
    es: ["Fuente", "consultado el", "Puede usar este texto citando la fuente y la dirección de la página; el uso comercial o la republicación masiva requieren permiso. ", "Copiar la cita de esta página", "Copiado"],
    pl: ["Źródło", "dostęp", "Tekst można wykorzystać, podając źródło i adres strony; użycie komercyjne lub masowa republikacja tylko za zgodą. ", "Kopiuj przypis do tej strony", "Skopiowano"],
    tr: ["Kaynak", "erişim", "Bu metni kaynak ve sayfa adresini belirterek kullanabilirsiniz; ticari kullanım veya toplu yeniden yayın yalnızca izinle. ", "Bu sayfanın kaynakçasını kopyala", "Kopyalandı"],
    ar: ["المصدر", "تاريخ الاطلاع", "يجوز استخدام هذا النص مع ذكر المصدر وعنوان الصفحة؛ الاستخدام التجاري أو إعادة النشر بالجملة بإذن فقط. ", "نسخ مرجع هذه الصفحة", "تم النسخ"]
  };
  const lang = () => { const l = (document.documentElement.lang || "fa").slice(0, 2).toLowerCase(); return TX[l] ? l : "fa"; };
  const cite = () => { const x = TX[lang()]; return x[0] + ": " + document.title + " — " + location.href.split("#")[0] + (location.hash || "") +
    " (" + x[1] + " " + new Date().toISOString().slice(0, 10) + ")"; };
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
  note.style.cssText = "margin:28px auto 16px;max-width:900px;padding:10px 16px;font-size:.8rem;line-height:1.9;opacity:.75;text-align:center";
  const msg = document.createElement("span");
  const b = document.createElement("button");
  b.type = "button";
  b.style.cssText = "font:inherit;margin-inline-start:8px;padding:2px 10px;border:1px solid currentColor;border-radius:999px;background:none;color:inherit;cursor:pointer";
  const paint = () => { const l = lang(), x = TX[l]; note.setAttribute("dir", l === "fa" || l === "ar" ? "rtl" : "ltr"); note.setAttribute("lang", l); msg.textContent = x[2]; b.textContent = x[3]; };
  b.addEventListener("click", () => { const c = cite(); (navigator.clipboard ? navigator.clipboard.writeText(c) : Promise.reject()).then(() => { b.textContent = TX[lang()][4]; }, () => { b.textContent = c; }); });
  note.append(msg, b); paint();
  new MutationObserver(paint).observe(document.documentElement, {attributes: true, attributeFilter: ["lang"]});   /* صفحه‌هایی که زبان را بدون بارگذاری دوباره عوض می‌کنند */
  if (WANT_NOTE) {
    const put = () => document.body.appendChild(note);
    document.body ? put() : addEventListener("DOMContentLoaded", put);
  }
})();
