/* Shared language helpers for the atlas (Persian is the default). */
window.EarthLang = (function () {
  function get() { try { return localStorage.getItem("earth-time-lang") === "en" ? "en" : "fa"; } catch (e) { return "fa"; } }
  function t(k) { var l = get(); return (window.I18N && window.I18N[l] && window.I18N[l][k]) || k; }
  function field(era, name) {
    if (get() === "fa" && era[name + "Fa"]) return era[name + "Fa"];
    return era[name] || "";
  }
  return { get: get, t: t, field: field };
})();
