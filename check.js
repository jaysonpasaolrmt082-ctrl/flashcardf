// Answer checking for typed answers. Forgiving about spacing, units,
// commas, ₱ signs and small spelling slips; strict about the actual value.
(function (root) {
  var GENERIC = ["triangle", "system", "energy", "volcano", "rock", "forest", "eclipse", "reproduction", "season", "artery"];

  function norm(s) {
    s = String(s || "").toLowerCase();
    s = s.replace(/[₀-₉]/g, function (c) { return String(c.charCodeAt(0) - 8320); });
    s = s.replace(/³/g, "3").replace(/²/g, "2").replace(/[−–—]/g, "-").replace(/×/g, "x").replace(/÷/g, "/");
    s = s.replace(/₱|\bphp\b/g, " ");
    s = s.replace(/(^|\s)p\s*(?=\d)/g, "$1");
    s = s.replace(/(\d),(?=\d{3}(\D|$))/g, "$1");
    s = s.replace(/(\d),(?=\d{3}(\D|$))/g, "$1");
    s = s.replace(/^\s*[a-z]\s*=\s*/, "");
    s = s.replace(/(\d)\s*(%|percent|°\s*c|°|degrees?|cm3|cm2|cm|mm|km\/h|kph|km\/s|kilometers?|km|m\/s|meters?|metres?|m|liters?|litres?|l|ml|kg|grams?|g|minutes?|mins?|hours?|hrs?|days?|seconds?|secs?|s|units?|points?|pts?|pesos?)(?![a-z])/g, "$1");
    s = s.replace(/(\d)\s*(am|pm)\b/g, "$1 $2");
    s = s.replace(/[^a-z0-9:\/.\s+-]/g, " ");
    s = s.replace(/(^|[^\d])\./g, "$1 ").replace(/\.(?!\d)/g, " ");
    s = s.replace(/\s*([:\/])\s*/g, "$1");
    s = s.replace(/\b(the|a|an|of|is|it|its|called|about)\b/g, " ");
    s = s.replace(new RegExp("\\b(" + GENERIC.join("|") + ")s?\\b", "g"), " ");
    return s.replace(/\s+/g, " ").trim();
  }

  function lev(a, b) {
    if (a === b) return 0;
    var m = a.length, n = b.length, prev = [], cur, i, j;
    for (j = 0; j <= n; j++) prev[j] = j;
    for (i = 1; i <= m; i++) {
      cur = [i];
      for (j = 1; j <= n; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      prev = cur;
    }
    return prev[n];
  }
  // Small spelling slips only; the first letter must match so "sexual" never passes for "asexual".
  function tol(v) { return v.length <= 4 ? 0 : v.length <= 11 ? 1 : 2; }
  function close(t, v) {
    if (t === v) return true;
    if (/^[\d.:\/ -]+$/.test(v) && t.replace(/^(\S+)\s+[a-z]+$/, "$1") === v) return true; // "45 handshakes"
    return !/\d/.test(v) && t[0] === v[0] && lev(t, v) <= tol(v);
  }

  // Accepted forms for a card: extra keys plus the printed answer and its parts.
  function variants(card) {
    var out = [], ks = card.k || [], multi = ks.some(function (k) { return k.indexOf("+") >= 0; });
    ks.forEach(function (k) { out.push(k); });
    var base = String(card.a).replace(/^[A-D] · /, "");
    out.push(base);
    out.push(base.replace(/\([^)]*\)/g, " "));
    if (!multi) {
      (base.match(/\(([^)]*)\)/g) || []).forEach(function (p) { out.push(p.slice(1, -1)); });
      out.slice().forEach(function (v) {
        if (/\sor\s/.test(v)) v.split(/\s+or\s+/).forEach(function (x) { out.push(x); });
      });
    }
    return out.map(function (v) { return v.replace(/^\s*or\s+/, ""); }).filter(Boolean);
  }

  function matchOne(t, v) {
    if (v.indexOf("+") >= 0) {
      var words = t.split(/[\s,;&]+|\band\b/).filter(Boolean);
      return v.split("+").every(function (part) {
        var p = norm(part);
        if (!p) return true;
        if (/\d/.test(p)) return words.indexOf(p) >= 0;
        if (t.indexOf(p) >= 0) return true;
        return p.indexOf(" ") < 0 && words.some(function (w) { return w[0] === p[0] && lev(w, p) <= tol(p); });
      });
    }
    return close(t, norm(v));
  }

  function check(card, typed) {
    var t = norm(typed);
    if (!t) return false;
    return variants(card).some(function (v) { return matchOne(t, v); });
  }

  root.Check = { norm: norm, check: check, variants: variants };
})(typeof window !== "undefined" ? window : globalThis);
