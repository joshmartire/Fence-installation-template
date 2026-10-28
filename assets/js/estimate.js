/* Fence Template — instant fence estimate (no dependencies).
   Pricing comes from site.config.json ("estimator"), written into the page as #est-config by the build.
   Everything is calculated in the browser; nothing is sent until the visitor submits the lead form.

   price = (per_ft × height mult × terrain mult + removal/ft + per-foot extras) × length
           + walk gates × walk_gate + double gates × double_gate + flat extras
   → never below minimum_job, shown as ± range_pct, rounded to round_to. */
(function () {
  "use strict";
  var cfgEl = document.getElementById("est-config");
  var form = document.getElementById("est-form");
  if (!cfgEl || !form) return;
  var C = JSON.parse(cfgEl.textContent);
  var $ = function (id) { return document.getElementById(id); };
  var byId = function (list, id) { for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i]; return list[0]; };
  var money = function (n) { return "$" + Math.round(n).toLocaleString("en-CA"); };
  var round = function (n) { var r = C.round_to || 50; return Math.round(n / r) * r; };
  var L = C.length || {}, LMIN = L.min || 20, LMAX = L.max || 600, MAXG = C.max_gates || 6;
  var result = $("est-result"), low = $("est-low"), high = $("est-high"), sum = $("est-sum");
  var lenIn = $("est-len"), lenRange = $("est-len-range"), walkIn = $("est-walk"), dblIn = $("est-double"), removal = $("est-removal");
  var previews = Array.prototype.slice.call(document.querySelectorAll(".est-preview > .fence-card"));
  var prevH = $("est-prev-h"), preview = document.querySelector(".est-preview");

  /* deep link from the home page picker: ?material=vinyl */
  try {
    var q = new URLSearchParams(location.search).get("material");
    if (q) { var r = form.querySelector('input[name="material"][value="' + q.replace(/[^a-z0-9\-]/gi, "") + '"]'); if (r) r.checked = true; }
  } catch (e) {}

  var val = function (name) { var el = form.querySelector('input[name="' + name + '"]:checked'); return el ? el.value : null; };
  var int = function (el, lo, hi, d) { var v = parseInt(el && el.value, 10); if (isNaN(v)) v = d; return Math.max(lo, Math.min(hi, v)); };
  var lastMat = null;

  var calc = function () {
    var mat = byId(C.materials, val("material"));
    /* heights: only the ones this material comes in; keep the visitor's choice if it's still offered */
    var hBoxes = form.querySelectorAll("#est-heights .opt");
    Array.prototype.forEach.call(hBoxes, function (lab) {
      var ok = mat.heights.indexOf(lab.getAttribute("data-height")) !== -1;
      lab.hidden = !ok; var inp = lab.querySelector("input"); inp.disabled = !ok; if (!ok) inp.checked = false;
    });
    if (mat.id !== lastMat || !val("height")) {
      var want = val("height") && mat.heights.indexOf(val("height")) !== -1 ? val("height") : (mat.default_height || mat.heights[mat.heights.length - 1]);
      var hr = form.querySelector('input[name="height"][value="' + want + '"]'); if (hr) hr.checked = true;
      lastMat = mat.id;
    }
    var h = byId(C.heights, val("height"));
    var t = byId(C.terrain, val("terrain"));
    var len = int(lenIn, LMIN, LMAX, L.default || 150);
    var walk = int(walkIn, 0, MAXG, 0), dbl = int(dblIn, 0, MAXG, 0);
    if (walkIn) walkIn.value = walk; if (dblIn) dblIn.value = dbl;
    if (lenRange && document.activeElement !== lenRange) lenRange.value = len;
    if (lenRange) lenRange.style.setProperty("--fill", ((len - LMIN) / (LMAX - LMIN) * 100).toFixed(1));

    /* extras: only those that apply to this material; prices shown from config */
    var perFt = 0, flat = 0, names = [];
    Array.prototype.forEach.call(form.querySelectorAll("#est-addons .chk"), function (lab) {
      var a = byId(C.addons || [], lab.getAttribute("data-addon"));
      var ok = !a.materials || a.materials.indexOf(mat.id) !== -1;
      var cb = lab.querySelector("input");
      lab.hidden = !ok; if (!ok) cb.checked = false;
      var pr = lab.querySelector(".chk__price"); if (pr) pr.textContent = a.per_ft ? "+" + money(a.per_ft) + "/ft" : "+" + money(a.flat || 0);
      if (ok && cb.checked) { names.push(a.label); if (a.per_ft) perFt += a.per_ft; else flat += a.flat || 0; }
    });
    var rem = removal && removal.checked;
    if (removal) { var rp = removal.parentNode.querySelector(".chk__price"); if (rp) rp.textContent = "+" + money(C.removal_per_ft || 0) + "/ft"; }

    var fence = mat.per_ft * h.mult * t.mult;
    var mid = (fence + (rem ? (C.removal_per_ft || 0) : 0) + perFt) * len + walk * mat.walk_gate + dbl * mat.double_gate + flat;
    mid = Math.max(C.minimum_job || 0, mid);
    var pct = (C.range_pct || 12) / 100;
    var lo = round(mid * (1 - pct)), hi = round(mid * (1 + pct));
    if (lo < (C.minimum_job || 0)) lo = round(C.minimum_job);
    low.textContent = money(lo); high.textContent = money(hi);
    var lv = $("est-live-v"); if (lv) lv.textContent = money(lo) + " – " + money(hi);
    var gates = [];
    if (walk) gates.push(walk + " walk gate" + (walk > 1 ? "s" : ""));
    if (dbl) gates.push(dbl + " double gate" + (dbl > 1 ? "s" : ""));
    sum.textContent = mat.label + " · " + h.label + " · " + len + " ft" + (gates.length ? " · " + gates.join(" · ") : "") + (rem ? " · removal" : "") + (names.length ? " · +" + names.length + " extra" + (names.length > 1 ? "s" : "") : "");
    if (result) { result.classList.remove("is-new"); void result.offsetWidth; result.classList.add("is-new"); }

    /* preview: the chosen material, scaled to the chosen height */
    previews.forEach(function (c) { c.classList.toggle("is-sel", c.getAttribute("data-fence") === mat.id); });
    var cur = previews.filter(function (c) { return c.getAttribute("data-fence") === mat.id; })[0];
    if (preview && cur) preview.style.setProperty("--hs", (parseInt(h.id, 10) / (parseInt(cur.getAttribute("data-height"), 10) || 6)).toFixed(3));
    if (prevH) prevH.textContent = h.label.toUpperCase() + " · " + len + " FT";

    /* keep the lead form's hidden fields in sync */
    var set = function (id, v) { var el = $(id); if (el) el.value = v; };
    set("lead-material", mat.label);
    set("lead-height", h.label);
    set("lead-length", len + " ft");
    set("lead-gates", gates.join(", ") || "none");
    set("lead-terrain", t.label);
    set("lead-extras", (rem ? ["Old fence removal"] : []).concat(names).join(", ") || "none");
    set("lead-estimate-shown", money(lo) + " – " + money(hi) + " " + (C.currency || "CAD"));
  };
  form.addEventListener("change", calc);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  if (lenIn) lenIn.addEventListener("input", function () { if (lenIn.value !== "") calc(); });
  if (lenIn) lenIn.addEventListener("blur", calc);
  if (lenRange) lenRange.addEventListener("input", function () { lenIn.value = lenRange.value; calc(); });
  Array.prototype.forEach.call(document.querySelectorAll(".gate-row .stepper__b"), function (b) {
    b.addEventListener("click", function () {
      var inp = b.parentNode.querySelector("input");
      inp.value = Math.max(0, Math.min(MAXG, (parseInt(inp.value, 10) || 0) + (+b.getAttribute("data-step")))); calc();
    });
  });
  [walkIn, dblIn].forEach(function (i) { if (i) i.addEventListener("input", calc); });
  calc();

  /* ---------- measure my yard: width × depth and the sides being fenced ---------- */
  var mw = $("m-w"), md = $("m-d"), mout = $("m-out"), muse = $("m-use"), measured = 0;
  var sides = Array.prototype.slice.call(document.querySelectorAll(".measure__sides input"));
  var upMeasure = function () {
    var w = parseFloat(mw.value) || 0, d = parseFloat(md.value) || 0, total = 0;
    sides.forEach(function (s) {
      var on = s.checked, bar = document.querySelector(".measure__yard .m-" + s.value);
      if (bar) bar.classList.toggle("is-on", on);
      if (on) total += (s.value === "back" || s.value === "front") ? w : d;
    });
    measured = Math.round(total);
    if (!w || !d) { mout.textContent = "Enter your yard's width and depth."; muse.disabled = true; return; }
    if (!measured) { mout.textContent = "Tick at least one side to fence."; muse.disabled = true; return; }
    mout.innerHTML = "About <strong>" + measured + " ft</strong> of fence" + (measured > LMAX ? " (the tool goes up to " + LMAX + " ft; we'll quote the rest)" : "") + ".";
    muse.disabled = false;
  };
  if (mw && md && mout && muse) {
    [mw, md].forEach(function (i) { i.addEventListener("input", upMeasure); });
    sides.forEach(function (s) { s.addEventListener("change", function (e) { e.stopPropagation(); upMeasure(); }); });
    [mw, md].forEach(function (i) { i.addEventListener("change", function (e) { e.stopPropagation(); }); });
    muse.addEventListener("click", function () {
      lenIn.value = Math.max(LMIN, Math.min(LMAX, measured)); calc();
      lenIn.focus();
    });
    upMeasure();
  }

  /* phones: show the live price bar while the result card is off screen */
  var live = $("est-live");
  if (live && result && "IntersectionObserver" in window) {
    var tool = document.getElementById("estimator"), inTool = false, resVis = false;
    var upLive = function () { live.classList.toggle("is-visible", inTool && !resVis); };
    new IntersectionObserver(function (en) { resVis = en[0].isIntersecting; upLive(); }).observe(result);
    new IntersectionObserver(function (en) { inTool = en[0].isIntersecting; upLive(); }).observe(tool);
  }

  /* reveal the lead form */
  var open = $("est-lead-open"), lead = $("est-lead");
  if (open && lead) open.addEventListener("click", function () {
    lead.hidden = false;
    open.setAttribute("aria-expanded", "true");
    lead.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    setTimeout(function () { var n = $("lead-name"); if (n) n.focus({ preventScroll: true }); }, 350);
  });
})();
