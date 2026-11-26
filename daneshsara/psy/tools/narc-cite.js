/* منبع‌دهی و ناوبری مشترک ابزارهای پروندهٔ «خودشیفتگی و کنترل».
   نیاز دارد به narc-sources.js (window.NSRC) که با build/narc_tool_sources.py ساخته می‌شود. */
(function () {
  var FA = function (n) { return String(n).replace(/\d/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'[d]; }); };
  var E = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); };
  var TIER = { 1: 'فراتحلیل یا مرور نظام‌مند', 2: 'مقالهٔ داوری‌شده یا آمار رسمی', 3: 'کتاب یا سخنرانی', 4: 'سرنخ، منبع ضعیف' };

  /* عنوان را از ارجاع به سبک APA بیرون می‌کشد: «نویسنده (سال). عنوان. مجله…» */
  function title(cite) {
    var m = String(cite).match(/\)\.\s*([^.]{8,}?)\.\s/);
    if (m) return m[1].trim();
    return String(cite).slice(0, 120);
  }

  var order = [], idx = {};
  function reg(k) { if (!(k in idx)) { order.push(k); idx[k] = order.length; } return idx[k]; }

  /* ترتیب شماره‌ها را از قبل ثابت می‌کند تا با فیلتر و انتخاب کاربر جابه‌جا نشود. */
  function init(keys) { (keys || []).forEach(reg); }

  /* نشانهٔ بالانویس برای یک یا چند کلید منبع. */
  function mark(keys) {
    if (!keys || !keys.length) return '';
    var ks = (typeof keys === 'string') ? [keys] : keys;
    var out = ks.map(function (k) {
      var s = (window.NSRC || {})[k];
      if (!s) { return ''; }
      return '<a href="#src-' + E(k) + '" title="' + E(s.c) + '">' + FA(reg(k)) + '</a>';
    }).filter(Boolean);
    if (!out.length) return '';
    return '<sup class="cite">' + out.join('<i>،</i>') + '</sup>';
  }

  /* فهرست منبع‌ها در پای صفحه. */
  function list(el, opts) {
    var node = (typeof el === 'string') ? document.getElementById(el) : el;
    if (!node) return;
    opts = opts || {};
    var keys = order.filter(function (k) { return (window.NSRC || {})[k]; });
    var li = keys.map(function (k) {
      var s = window.NSRC[k], t = s.t || 3;
      var cite = E(s.c);
      if (s.u) {
        cite += ' <a href="' + E(s.u) + '" rel="noopener noreferrer" target="_blank">متن&nbsp;منبع&nbsp;↗</a>';
      } else {
        /* بدون نشانیِ مستقیم: فقط جست‌وجوی عنوان، تا ادعای نادرستی دربارهٔ محل متن نکنیم. */
        cite += ' <a class="look" href="https://scholar.google.com/scholar?q=' + encodeURIComponent(title(s.c))
             + '" rel="noopener noreferrer" target="_blank">جست‌وجوی&nbsp;عنوان&nbsp;↗</a>';
      }
      return '<li id="src-' + E(k) + '"><span class="tier t' + t + '" title="' + E(TIER[t] || '') + '">درجهٔ ' + FA(t) + '</span>'
        + '<span class="cc">' + cite + '</span></li>';
    }).join('');
    node.innerHTML =
      '<h2>' + E(opts.title || 'منبع‌ها') + '</h2>'
      + '<p class="k">هر عددی که در این صفحه بالانویس شده به یکی از این منبع‌ها اشاره می‌کند. درجهٔ ۱ یعنی فراتحلیل یا مرور نظام‌مند، '
      + '۲ مقالهٔ داوری‌شده یا آمار رسمی، ۳ کتاب یا سخنرانی، و ۴ سرنخی که هنوز پشتوانهٔ محکمی ندارد. '
      + 'هر جا منبعی نیست، یعنی آن جمله برداشت ماست، نه یافتهٔ پژوهشی. '+ '«متن منبع» یعنی نشانیِ خودِ مقاله را داریم؛ «جست‌وجوی عنوان» یعنی نداریم و فقط عنوان را برایتان جست‌وجو می‌کند.</p>'
      + '<ol>' + li + '</ol>';
    node.classList.add('srcbox');
  }

  /* ناوبری مشترک: هیچ صفحه‌ای بن‌بست نباشد. */
  /* مسیرها نسبت به پوشهٔ psy/ نوشته شده‌اند؛ nav با base آن را تنظیم می‌کند. */
  var MAP = [
    ['narcissism.html', 'پروندهٔ خودشیفتگی و کنترل', 'هجده پرسش در شش ایستگاه، با یک خط «همین امروز» زیر هر پاسخ', 'home'],
    ['tools/control-check.html', 'آیا در این رابطه کنترل هست؟', 'بیست‌وپنج جمله، از هر دو سو'],
    ['tools/triangle.html', 'مثلث قربانی، ظالم، ناجی', 'سه گوشه، و شش گام برای بیرون آمدن'],
    ['tools/arc.html', 'قوس رابطه', 'هفت مرحله در پنج نقش، با عددهایی که واقعاً وجود دارند'],
    ['tools/toll.html', 'آنچه بر تن و روان می‌گذرد', 'با درجهٔ شواهد هر مورد'],
    ['tools/sentences.html', 'جمله‌ساز: به‌جای این، آن', 'پنجاه‌وچند جملهٔ آشنا، و جایگزینشان'],
    ['tools/say.html', 'چه بگویم؟', 'دوازده لحظهٔ سخت، در سه شدت'],
    ['tools/roles.html', 'آینهٔ نقش‌ها', 'شش نقش، و تلهٔ هر کدام'],
    ['tools/week.html', 'هفت روز، هفت کار کوچک', 'پنج وضعیت، هر کدام یک برنامهٔ هفتگی'],
    ['tools/analogies.html', 'این مثل چیست؟', 'شش قیاس، با نقطهٔ شکستشان'],
    ['stories/narcissism-control.html', 'بیست‌وهشت داستان مستند', 'پرونده‌های دادگاهی، گزارش‌های رسمی و خاطرات، با درجهٔ منبع'],
    ['entries.html#narcissism-control', 'همهٔ مدخل‌ها', 'شصت‌وسه مدخل، از رفتار کنترل‌گرانه تا ژنتیک و فلسفه']
  ];
  function nav(el, here, opts) {
    var node = (typeof el === 'string') ? document.getElementById(el) : el;
    if (!node) return;
    opts = opts || {};
    /* base: مسیر پوشهٔ psy/ نسبت به صفحهٔ جاری. اگر داده نشود، از مسیر صفحه حدس زده می‌شود. */
    var base = opts.base;
    if (base == null) {
      var path = location.pathname;
      base = (/\/psy\/(tools|stories)\//.test(path)) ? '../' : '';
    }
    node.innerHTML = '<h2>' + E(opts.title || 'بعدش کجا') + '</h2>'
      + '<p class="k">' + E(opts.note || 'همهٔ بخش‌های این پرونده از هر صفحه در دسترس‌اند، تا هیچ‌جا بن‌بست نباشد.') + '</p>'
      + '<div class="row">' + MAP.map(function (m) {
        var cls = (m[3] ? m[3] + ' ' : '') + (here && m[0].indexOf(here) > -1 ? 'here' : '');
        return '<a class="' + cls.trim() + '" href="' + base + m[0] + '"><b>' + E(m[1]) + '</b><span>' + E(m[2]) + '</span></a>';
      }).join('') + '</div>';
    node.classList.add('nextnav');
  }

  window.NC = { init: init, mark: mark, list: list, nav: nav, fa: FA, order: order };
})();
