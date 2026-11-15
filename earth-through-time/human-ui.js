/* Deep links (#era-<id>) and links from human-story stops to the Persian wiki. */
(function () {
  var eras = window.EARTH_ERAS || [], slider = document.getElementById("time-slider");
  if (!slider) return;
  function lang() { try { return localStorage.getItem("earth-time-lang") === "en" ? "en" : "fa"; } catch (e) { return "fa"; } }
  function go() {
    var m = (location.hash || "").match(/^#era-([\w-]+)/);
    if (!m) return;
    var i = eras.findIndex(function (e) { return e.id === m[1]; });
    if (i < 0) return;
    slider.value = String(i);
    slider.dispatchEvent(new Event("input"));
    slider.dispatchEvent(new Event("change"));
  }
  var body = document.querySelector(".panel-body");
  var a = document.createElement("a");
  a.id = "wiki-link"; a.className = "wiki-link"; a.hidden = true;
  if (body) body.appendChild(a);
  function paintLink() {
    var e = eras[Number(slider.value) || 0];
    if (!e || !e.wikiUrl) { a.hidden = true; return; }
    a.hidden = false; a.href = e.wikiUrl;
    a.textContent = lang() === "en" ? "Read more in the Persian human-origins wiki ↗" : "در ویکی تبار بیشتر بخوان ↗";
  }
  ["input", "change"].forEach(function (ev) { slider.addEventListener(ev, function () { setTimeout(paintLink, 0); }); });
  document.addEventListener("click", function (ev) { if (ev.target.closest && ev.target.closest("button")) setTimeout(paintLink, 0); });
  window.addEventListener("hashchange", go);
  go(); paintLink();
})();
