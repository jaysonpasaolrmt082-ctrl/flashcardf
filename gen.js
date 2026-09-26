// Anti-memorization helpers.
//   GEN       : question makers that create the same kind of problem with new numbers every time
//   GEN_LINK  : which fixed cards can be swapped for a fresh-number version
//   Traps     : builds tricky wrong choices (look-alike words, common number mistakes)
(function () {
  function R(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function P(a) { return a[R(0, a.length - 1)]; }
  function gcd(a, b) { return b ? gcd(b, a % b) : Math.abs(a); }
  function lcm(a, b) { return a / gcd(a, b) * b; }
  function fmt(n) { return Number(n).toLocaleString("en-US"); }
  function frac(p, q) { var g = gcd(p, q); p /= g; q /= g; return q === 1 ? String(p) : p + "/" + q; }
  function fracAnswer(p, q) {
    var g = gcd(p, q); p /= g; q /= g;
    if (q === 1) return String(p);
    if (p < q) return p + "/" + q;
    var w = Math.floor(p / q), r = p % q;
    return p + "/" + q + " or " + w + " " + r + "/" + q;
  }
  function mixedText(w, n, d) { return w + " " + n + "/" + d; }
  function clock(totalMin) {
    var h24 = Math.floor(totalMin / 60) % 24, m = totalMin % 60;
    var ap = h24 < 12 ? "AM" : "PM", h = h24 % 12 || 12;
    return h + ":" + (m < 10 ? "0" : "") + m + " " + ap;
  }
  var NAMES = ["Ana", "Ben", "Carlo", "Dina", "Eli", "Faye", "Gino", "Hana", "Ivan", "Joy", "Kiko", "Lia", "Migo", "Nina", "Paolo", "Rica"];
  function two() { var a = P(NAMES), b; do { b = P(NAMES); } while (b === a); return [a, b]; }

  var GEN = {
    prism: function () {
      var a = P([3, 4, 5, 6, 8]), b = P([4, 6, 8, 10]), base = a * b / 2, h = R(3, 12), V = base * h;
      if (Math.random() < 0.5) return { cat: "Geometry", q: "A triangular prism has a right-triangle base with legs " + a + " cm and " + b + " cm. Its volume is " + V + " cm³. What is the height of the prism?",
        a: h + " cm", e: "Triangle floor: " + a + " × " + b + " ÷ 2 = " + base + ". Then " + base + " × what = " + V + "? Answer: " + h + ".", m: "Half, then times height.", h: ["legs " + a + " cm and " + b + " cm", V + " cm³", "height"] };
      return { cat: "Geometry", q: "A triangular prism has a right-triangle base with legs " + a + " cm and " + b + " cm, and a height of " + h + " cm. What is its volume?",
        a: V + " cm³", e: "Triangle floor: " + a + " × " + b + " ÷ 2 = " + base + ". Then " + base + " × " + h + " = " + V + ".", m: "Half, then times height.", h: ["legs " + a + " cm and " + b + " cm", "height of " + h + " cm", "volume"] };
    },
    ratioProduct: function () {
      var r = P([[1, 2, 3], [2, 3, 4], [1, 3, 5], [2, 3, 5], [1, 2, 4], [3, 4, 5], [1, 4, 5]]), k = R(2, 4);
      var rp = r[0] * r[1] * r[2], prod = rp * k * k * k, ask = P(["largest", "smallest"]);
      var nums = r.map(function (x) { return x * k; });
      return { cat: "Ratio", q: "Three numbers are in the ratio " + r.join(":") + ". Their product is " + fmt(prod) + ". What is the " + ask + " number?",
        a: String(ask === "largest" ? nums[2] : nums[0]),
        e: r.join(" × ") + " = " + rp + ". " + fmt(prod) + " ÷ " + rp + " = " + (k * k * k) + " = " + k + " × " + k + " × " + k + ". Multiply each part by " + k + ": " + nums.join(", ") + ".",
        h: ["ratio " + r.join(":"), "product", ask] };
    },
    pizza: function () {
      var parts = [[1, 2], [1, 3], [3, 4], [2, 3], [1, 4]], gifts = [[1, 2], [1, 3], [2, 3], [1, 4], [3, 4], [1, 6], [5, 6]];
      var w = R(2, 3), sp = P(parts), g1 = P(gifts), g2; do { g2 = P(gifts); } while (g2 === g1);
      var tw = function (f) { return f[0] * 12 / f[1]; };
      var start = w * 12 + tw(sp), rem = start - tw(g1) - tw(g2);
      var n = two();
      return { cat: "Fractions", q: n[0] + " had " + mixedText(w, sp[0], sp[1]) + " pizzas. " + n[0] + " gave " + g1[0] + "/" + g1[1] + " of a pizza to " + n[1] + " and " + g2[0] + "/" + g2[1] + " of a pizza to a cousin. How much pizza is left?",
        a: fracAnswer(rem, 12),
        e: "Cut every pizza into 12 slices. " + mixedText(w, sp[0], sp[1]) + " pizzas = " + start + " slices. " + n[1] + " gets " + tw(g1) + ", the cousin gets " + tw(g2) + ". " + start + " − " + tw(g1) + " − " + tw(g2) + " = " + rem + " slices = " + frac(rem, 12) + ".",
        m: "Cut everything into the same size slices.", h: ["How much pizza is left"] };
    },
    paintedCube: function () {
      var n = R(3, 6), V = n * n * n, t = P([3, 2, 1, 0]), m = n - 2;
      var ans = t === 3 ? 8 : t === 2 ? 12 * m : t === 1 ? 6 * m * m : m * m * m;
      var why = t === 3 ? "Only corner pieces have 3 painted faces. A cube always has 8 corners."
        : t === 2 ? "Edge-middle pieces have 2 painted faces. Each of the 12 edges has " + m + " of them: 12 × " + m + " = " + ans + "."
        : t === 1 ? "Face-middle pieces have 1 painted face. Each of the 6 faces has " + m + " × " + m + " = " + (m * m) + ": 6 × " + (m * m) + " = " + ans + "."
        : "The hidden inside is a smaller " + m + " × " + m + " × " + m + " cube = " + ans + ".";
      return { cat: "Geometry", q: "A cube with a volume of " + V + " cubic units is painted on all sides, then cut into unit cubes. How many small cubes have " + (t === 0 ? "NO painted faces" : "exactly " + t + " painted face" + (t > 1 ? "s" : "")) + "?",
        a: String(ans), e: V + " = " + n + " × " + n + " × " + n + ". " + why, m: "Corners 3, edges 2, faces 1, inside 0.", h: [t === 0 ? "NO painted faces" : "exactly " + t + " painted face" + (t > 1 ? "s" : "")] };
    },
    speed: function () {
      var t = P([2, 3, 4, 5]), v = P([20, 30, 40, 45, 50, 60]), d = v * t, car = P(["jeepney", "tricycle", "bus", "motorcycle"]);
      return { cat: "Motion", q: "A " + car + " travels " + d + " km in " + t + " hours. What is its average speed?", a: v + " km/h",
        e: "Speed = distance ÷ time. " + d + " ÷ " + t + " = " + v + ".", m: "Speed = distance ÷ time.", h: [d + " km", t + " hours", "average speed"] };
    },
    pulse: function () {
      var win = P([10, 15, 20, 30]), mult = 60 / win, bpm, beats;
      do { bpm = R(60, 100); } while (bpm % mult);
      beats = bpm / mult;
      return { cat: "Human body", q: "A nurse counts a patient's pulse at the wrist: " + beats + " beats in " + win + " seconds. What is the heart rate per minute?",
        a: bpm + " beats per minute", k: [String(bpm), bpm + " bpm"], e: win + " seconds × " + mult + " = 1 minute, so " + beats + " × " + mult + " = " + bpm + ".", h: [beats + " beats", win + " seconds"] };
    },
    percentRatio: function () {
      var p = P([10, 20, 25, 40, 50]), a = 100 - p, b = 100 + p, g = gcd(a, b), n = two();
      var A0 = a * 4, B0 = b * 4, up = A0 * p / 100, down = B0 * p / 100;
      return { cat: "Ratio & percent", q: n[0] + "'s allowance was increased by " + p + "% while " + n[1] + "'s was decreased by " + p + "%. Now they are equal. What is the ratio of " + n[0] + "'s original allowance to " + n[1] + "'s?",
        a: (a / g) + ":" + (b / g),
        e: "Try numbers. " + n[0] + " ₱" + A0 + " + " + p + "% (₱" + up + ") = ₱" + (A0 + up) + ". " + n[1] + " ₱" + B0 + " − " + p + "% (₱" + down + ") = ₱" + (B0 - down) + ". Equal! So " + A0 + " : " + B0 + " = " + (a / g) + " : " + (b / g) + ".",
        m: "The one who got the raise started smaller.", h: ["increased by " + p + "%", "decreased by " + p + "%"] };
    },
    scoring: function () {
      var n = R(6, 12), x = P([2, 3, 4, 5]), y = P([1, 2, 3]), c, s;
      do { c = R(1, n - 1); s = c * x - (n - c) * y; } while (s <= 0);
      var who = P(NAMES);
      return { cat: "Equations", q: "In a quiz, " + who + " answered " + n + " questions: +" + x + " points for each correct answer and −" + y + " for each wrong one. The total score was " + s + ". How many were correct?",
        a: String(c), e: "Try " + c + ": " + c + " × " + x + " = " + (c * x) + ". " + (n - c) + " wrong × " + y + " = " + ((n - c) * y) + " lost. " + (c * x) + " − " + ((n - c) * y) + " = " + s + ".",
        m: "Guess, check, adjust.", h: ["+" + x + " points", "−" + y, "total score was " + s] };
    },
    consecutiveEven: function () {
      var m = P([4, 5, 6, 7]), times = (m % 2 && Math.random() < 0.5) ? 3 : 2;
      var s = times === 2 ? 2 * (m - 1) : m - 1, nums = [];
      for (var i = 0; i < m; i++) nums.push(s + 2 * i);
      var ask = P(["second largest", "largest", "sum"]);
      var ans = ask === "sum" ? nums.reduce(function (a, b) { return a + b; }, 0) : ask === "largest" ? nums[m - 1] : nums[m - 2];
      return { cat: "Numbers", q: "There are " + m + " consecutive even numbers. The largest is " + (times === 2 ? "two" : "three") + " times the smallest. What is the " + (ask === "sum" ? "sum of all the numbers" : ask + " number") + "?",
        a: String(ans), e: "The largest is " + (2 * (m - 1)) + " more than the smallest. Try " + s + ": " + nums.join(", ") + ". Is " + nums[m - 1] + " = " + times + " × " + s + "? Yes!",
        h: [m + " consecutive even numbers", (times === 2 ? "two" : "three") + " times the smallest", ask] };
    },
    lcmTime: function () {
      var pool = [6, 8, 9, 10, 12, 15, 18, 20, 24, 30], items, L;
      do {
        items = [P(pool), P(pool)]; if (Math.random() < 0.5) items.push(P(pool));
        items = items.filter(function (v, i, a) { return a.indexOf(v) === i; }).sort(function (a, b) { return a - b; });
        L = items.reduce(lcm);
      } while (items.length < 2 || L > 180 || L === items[items.length - 1]);
      var start = R(6, 11) * 60 + P([0, 15, 30, 45]);
      var what = P([["Bells ring", "ring"], ["Buses leave", "leave"], ["Signal lights flash", "flash"]]);
      return { cat: "LCM", q: what[0] + " every " + items.join(", ").replace(/, (\d+)$/, " and $1") + " minutes. They " + what[1] + " together at " + clock(start) + ". When will they " + what[1] + " together again?",
        a: clock(start + L), e: "Smallest number they all go into (LCM) = " + L + " minutes" + (L >= 60 ? " = " + Math.floor(L / 60) + " h " + (L % 60) + " min" : "") + ". " + clock(start) + " + " + L + " min = " + clock(start + L) + ".",
        m: "Together again = LCM. Watch AM and PM!", h: ["every " + items.join(", ").replace(/, (\d+)$/, " and $1") + " minutes", "together again"] };
    },
    primeProduct: function () {
      var primes = [2, 3, 5, 7, 11, 13, 17, 19, 23], p;
      do { p = [P(primes), P(primes), P(primes)].sort(function (a, b) { return a - b; }); } while (p[0] === p[1] || p[1] === p[2] || p[0] * p[1] * p[2] > 2500);
      var prod = p[0] * p[1] * p[2];
      return { cat: "Prime numbers", q: "The product of three different prime numbers is added to 1, and the result is " + fmt(prod + 1) + ". What is the sum of the three primes?",
        a: String(p[0] + p[1] + p[2]), e: "Take away the 1: " + fmt(prod) + " = " + p.join(" × ") + ". So " + p.join(" + ") + " = " + (p[0] + p[1] + p[2]) + ".",
        m: "Test primes in order: 2, 3, 5, 7, 11, 13…", h: ["added to 1", fmt(prod + 1)] };
    },
    waveSpeed: function () {
      var f = P([2, 4, 5, 10, 20, 50, 170]), l = P([0.5, 2, 3, 4, 5]), v = f * l;
      if (Math.random() < 0.5) return { cat: "Waves", q: "A wave has a frequency of " + f + " Hz and a wavelength of " + l + " m. What is its speed?", a: v + " m/s",
        e: "Speed = frequency × wavelength. " + f + " × " + l + " = " + v + ".", m: "v = f × λ.", h: [f + " Hz", l + " m", "speed"] };
      return { cat: "Waves", q: "A wave travels at " + v + " m/s with a frequency of " + f + " Hz. What is its wavelength?", a: l + " m",
        e: "Wavelength = speed ÷ frequency. " + v + " ÷ " + f + " = " + l + ".", m: "λ = v ÷ f.", h: [v + " m/s", f + " Hz", "wavelength"] };
    },
    accel: function () {
      var t = P([2, 4, 5, 8, 10]), a = P([2, 3, 4, 5]), v = a * t;
      return { cat: "Motion", q: "A car speeds up from 0 to " + v + " m/s in " + t + " seconds. What is its acceleration?", a: a + " m/s²", k: [String(a), a + " m/s2"],
        e: "Acceleration = change in speed ÷ time = " + v + " ÷ " + t + " = " + a + ".", h: ["0 to " + v + " m/s", t + " seconds", "acceleration"] };
    },
    senior: function () {
      var n = R(8, 15), s = R(2, 4), price = 5 * R(40, 100), sp = price * 0.8, meals = (n - s) + s * 0.8, total = (n - s) * price + s * sp;
      return { cat: "Discounts", q: n + " people ate at a restaurant. " + s + " of them were senior citizens with a 20% discount. The bill was ₱" + fmt(total) + ". How much did each senior citizen pay?",
        a: "₱" + fmt(sp), e: "A senior pays 8/10 of a meal, so " + s + " seniors = " + (s * 0.8).toFixed(1) + " meals. Total = " + (n - s) + " + " + (s * 0.8).toFixed(1) + " = " + meals.toFixed(1) + " meals. One meal = " + fmt(total) + " ÷ " + meals.toFixed(1) + " = ₱" + price + ". Senior pays " + price + " − " + (price * 0.2) + " = ₱" + sp + ".",
        m: "A senior counts as 0.8 of a person.", h: [s + " of them were senior citizens", "20% discount"] };
    },
    dilution: function () {
      var V, a, b;
      do { V = P([10, 20, 30, 40, 50, 60]); a = P([10, 12, 15, 20, 25, 30, 40]); b = P([4, 5, 6, 8, 10, 12, 15, 20]); } while (b >= a || (V * a) % b);
      var total = V * a / b, W = total - V, pure = V * a / 100, what = P(["acid solution", "salt water", "juice concentrate", "sugar syrup"]);
      return { cat: "Percentage", q: "You have " + V + " liters of " + a + "% " + what + ". How many liters of water must you add to make it " + b + "%?",
        a: W + " L", e: "The pure part: " + a + "% of " + V + " L = " + pure + " L. Water does not change it. " + b + "% of what = " + pure + "? " + b + "% of " + total + " = " + pure + ". Total must be " + total + " L, so add " + total + " − " + V + " = " + W + " L.",
        m: "Adding water never changes the pure part. Find it first.", h: [V + " liters", a + "%", b + "%"] };
    },
    walkers: function () {
      var v1 = P([40, 50, 60, 70]), v2 = v1 + P([10, 20, 30]), t = R(2, 6), d = t * (v2 - v1) / 2, D = (v1 + v2) * t, n = two();
      return { cat: "Motion", q: n[0] + " walks toward " + n[1] + "'s house at " + v1 + " m/min. At the same time " + n[1] + " walks toward " + n[0] + "'s house at " + v2 + " m/min. They meet " + d + " m from the midpoint. How far apart are the houses?",
        a: fmt(D) + " m", e: n[1] + " is faster and walks 2 × " + d + " = " + (2 * d) + " m more. " + n[1] + " gains " + (v2 - v1) + " m each minute, so it takes " + t + " minutes. Together they walk " + (v1 + v2) + " m each minute × " + t + " = " + fmt(D) + " m.",
        m: "Faster one walks 2 × (distance from midpoint) extra.", h: [v1 + " m/min", v2 + " m/min", d + " m from the midpoint"] };
    },
    digitSum: function () {
      var k = P([3, 4]), ds = [];
      while (ds.length < k) { var x = R(1, 9); if (ds.indexOf(x) < 0) ds.push(x); }
      ds.sort(function (a, b) { return a - b; });
      var S = ds.reduce(function (a, b) { return a + b; }, 0), per = k === 3 ? 2 : 6, rep = k === 3 ? 111 : 1111, total = S * per * rep;
      return { cat: "Counting", q: "What is the sum of all " + k + "-digit numbers that use the digits " + ds.join(", ").replace(/, (\d)$/, " and $1") + " (each used once)?",
        a: fmt(total), e: "There are " + (k === 3 ? 6 : 24) + " such numbers. Each digit sits in each place " + per + " times. " + ds.join(" + ") + " = " + S + ". " + S + " × " + per + " × " + fmt(rep) + " = " + fmt(total) + ".",
        m: "4 digits: sum × 6 × 1,111. 3 digits: sum × 2 × 111.", h: ["digits " + ds.join(", ").replace(/, (\d)$/, " and $1")] };
    },
    lightning: function () {
      var s = R(2, 9), d = 340 * s, place = P(["Surigao", "Butuan", "Bayugan", "Tandag", "Bislig", "Siargao"]);
      return { cat: "Sound", q: "During a storm in " + place + ", you see lightning and hear the thunder " + s + " seconds later. Sound travels about 340 m/s. How far away was the lightning?",
        a: fmt(d) + " m", k: [String(d), (d / 1000) + " km"], e: "Light arrives almost instantly. Distance = 340 × " + s + " = " + fmt(d) + " m.", m: "Count seconds × 340 m.", h: [s + " seconds later", "340 m/s"] };
    }
  };

  var LINK = {
    "e25:2": "prism", "et:2": "prism", "e25:4": "ratioProduct", "et:4": "ratioProduct", "e25:7": "pizza", "et:7": "pizza",
    "e25:9": "paintedCube", "ep:9": "paintedCube", "a25:0": "percentRatio", "at:0": "percentRatio", "ap:0": "percentRatio",
    "a25:3": "scoring", "at:3": "scoring", "ap:3": "scoring", "a25:4": "consecutiveEven", "at:4": "consecutiveEven",
    "a25:7": "lcmTime", "at:7": "lcmTime", "ap:7": "lcmTime", "a25:8": "primeProduct", "at:8": "primeProduct",
    "d25:2": "senior", "dt:2": "senior", "dp:2": "senior", "d25:4": "dilution", "dt:4": "dilution", "dp:4": "dilution",
    "d25:6": "walkers", "dt:6": "walkers", "d25:8": "digitSum", "dt:8": "digitSum", "dp:8": "digitSum",
    "se:0": "speed", "sa:0": "waveSpeed", "ap:2": "waveSpeed", "sa:6": "accel", "sd:0": "lightning", "sd:1": "pulse"
  };

  // "New numbers every time" decks: each card is a question type, filled in fresh when played.
  window.GROUPS.splice(3, 0, { id: "fresh", name: "New numbers every time", note: "The same kinds of problems as 2025, but the numbers change every time. No memorizing!" });
  window.DECKS.push(
    { id: "gE", group: "fresh", name: "Easy · new numbers", round: "easy", pts: 1, time: 15 },
    { id: "gA", group: "fresh", name: "Average · new numbers", round: "average", pts: 2, time: 30 },
    { id: "gD", group: "fresh", name: "Difficult · new numbers", round: "difficult", pts: 3, time: 60 }
  );
  function slots(list) { return list.map(function (g) { return { gen: g, q: "(new numbers each time)", a: "" }; }); }
  window.CARDS.gE = slots(["prism", "ratioProduct", "pizza", "paintedCube", "speed", "pulse"]);
  window.CARDS.gA = slots(["percentRatio", "scoring", "consecutiveEven", "lcmTime", "primeProduct", "waveSpeed", "accel"]);
  window.CARDS.gD = slots(["senior", "dilution", "walkers", "digitSum", "lightning"]);

  // ---------- Tricky choices ----------
  // Look-alike groups: when the answer is one of these, the others become the wrong choices.
  var LOOKALIKE = [
    ["Conduction", "Convection", "Radiation", "Insulation"],
    ["Reflection", "Refraction", "Diffraction", "Dispersion", "Absorption"],
    ["Perihelion", "Aphelion", "Perigee", "Apogee"],
    ["Veins", "Arteries", "Capillaries", "Valves"],
    ["Brachial artery", "Radial artery", "Carotid artery", "Femoral artery", "Aorta", "Pulmonary vein", "Pulmonary artery"],
    ["Evaporation", "Condensation", "Sublimation", "Melting", "Freezing", "Deposition"],
    ["Epicenter", "Focus (hypocenter)", "Fault line", "Magnitude", "Intensity"],
    ["Amihan", "Habagat", "El Niño", "La Niña"],
    ["Mutualism", "Commensalism", "Parasitism", "Predation", "Competition"],
    ["Phototropism", "Gravitropism", "Hydrotropism", "Thigmotropism"],
    ["Cerebellum", "Cerebrum", "Brainstem", "Spinal cord"],
    ["Mitochondrion", "Nucleus", "Chloroplast", "Ribosome", "Cell membrane", "Cell wall"],
    ["Fermentation", "Photosynthesis", "Respiration", "Digestion", "Decomposition"],
    ["Pleiades", "Orion's belt", "Big Dipper", "Southern Cross"],
    ["Balatik", "Moroporo", "Tres Marias", "Bakunawa"],
    ["Vegetative reproduction", "Sexual reproduction", "Budding", "Binary fission", "Pollination"],
    ["Tissue culture", "Grafting", "Marcotting", "Cross-pollination"],
    ["Ectopic pregnancy", "Appendicitis", "Miscarriage", "Ovarian cyst"],
    ["Appendicitis", "Tonsillitis", "Gastritis", "Hepatitis"],
    ["Stratosphere", "Troposphere", "Mesosphere", "Thermosphere", "Exosphere"],
    ["Sedimentary rock", "Igneous rock", "Metamorphic rock"],
    ["Magma", "Lava", "Ash", "Pumice"],
    ["Kinetic energy", "Potential energy", "Thermal energy", "Chemical energy", "Light energy"],
    ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
    ["Barometer", "Anemometer", "Thermometer", "Hygrometer", "Rain gauge", "Seismograph"],
    ["Dominant", "Recessive", "Mutation", "Hybrid"],
    ["Antibiotic", "Antibodies", "Antiseptic", "Antiviral", "Vaccine"],
    ["Insulin", "Adrenaline", "Glucagon", "Estrogen"],
    ["Liver", "Kidneys", "Pancreas", "Gallbladder", "Stomach"],
    ["Static electricity", "Current electricity", "Magnetism", "Friction"],
    ["Echolocation", "Reverberation", "Resonance", "Hibernation"],
    ["Doppler effect", "Echo", "Resonance", "Refraction"],
    ["Concave mirror", "Convex mirror", "Plane mirror", "Convex lens"],
    ["Subduction", "Weathering", "Erosion", "Folding", "Faulting"],
    ["Tsunami", "Storm surge", "Landslide", "Liquefaction", "Flash flood"],
    ["Dry season", "Rainy season", "Cool dry season", "Hot dry season"],
    ["Inertia", "Momentum", "Friction", "Gravity", "Acceleration"],
    ["Decibels (dB)", "Hertz (Hz)", "Newton (N)", "Watt (W)", "Joule (J)"],
    ["Ohm", "Volt", "Ampere", "Watt"],
    ["Nitrogen", "Oxygen", "Carbon dioxide", "Argon", "Hydrogen"],
    ["Distillation", "Filtration", "Evaporation", "Decantation", "Chromatography"],
    ["Atom", "Molecule", "Element", "Compound"],
    ["Secondary consumer", "Primary consumer", "Tertiary consumer", "Producer", "Decomposer"],
    ["Stomata", "Xylem", "Phloem", "Chlorophyll"],
    ["Nocturnal", "Diurnal", "Hibernating", "Migratory"],
    ["Diaphragm", "Trachea", "Alveoli", "Bronchi", "Larynx"],
    ["White blood cells", "Red blood cells", "Platelets", "Plasma"],
    ["Hinatuan", "Bislig City", "Lianga", "Tandag City", "Cantilan"],
    ["Agusan del Sur", "Agusan del Norte", "Surigao del Sur", "Surigao del Norte", "Dinagat Islands"],
    ["Siargao Island", "Dinagat Island", "Bucas Grande Island", "Camiguin"],
    ["Ramsar Convention", "Paris Agreement", "Kyoto Protocol", "Montreal Protocol"],
    ["Odette (Rai)", "Yolanda (Haiyan)", "Pablo (Bopha)", "Sendong (Washi)"],
    ["Mindanao", "Luzon", "Visayas", "Palawan"],
    ["Batangas", "Albay", "Pampanga", "Zambales"],
    ["Cone", "Dome", "Shield", "Caldera"],
    ["Diwata-1", "Maya-1", "Diwata-2", "Agila-2"],
    ["Balangay", "Vinta", "Bangka", "Caracoa"],
    ["Stainless steel", "Bronze", "Brass", "Cast iron"],
    ["Los Baños", "Calamba", "San Pablo", "Santa Cruz"],
    ["Rusting", "Tarnishing", "Melting", "Evaporation"],
    ["Indicator", "Catalyst", "Solvent", "Solute"],
    ["Thermal expansion", "Contraction", "Conduction", "Melting"],
    ["Solar panel", "Generator", "Battery", "Transformer"],
    ["Skin", "Liver", "Heart", "Brain", "Lungs"],
    ["Herbivores", "Carnivores", "Omnivores", "Decomposers"],
    ["Invertebrates", "Vertebrates", "Arthropods", "Amphibians", "Reptiles"],
    ["Wavelength", "Amplitude", "Crest", "Trough", "Frequency"],
    ["Photosynthesis", "Transpiration", "Respiration", "Germination"],
    ["Seismograph", "Barometer", "Thermometer", "Anemometer"],
    ["Pleiades", "Orion", "Taurus", "Scorpius"]
  ];
  function strip(s) { return String(s).replace(/^[A-D] · /, "").replace(/\s*\([^)]*\)/g, "").split(/\s+or\s+/)[0].trim(); }
  function low(s) { return s.toLowerCase().replace(/s$/, ""); }

  function lookalikes(right) {
    var r = low(right);
    for (var i = 0; i < LOOKALIKE.length; i++) {
      var g = LOOKALIKE[i];
      for (var j = 0; j < g.length; j++) {
        var it = low(strip(g[j]));
        if (it.length >= 3 && (r === it || (r.indexOf(it) === 0 && it.length >= 5) || (it.indexOf(r) === 0 && r.length >= 5))) {
          return g.filter(function (x, k) { return k !== j; });
        }
      }
    }
    return [];
  }

  // Common mistakes with numbers: flipped ratios, AM/PM swaps, doubled, halved, off by a little.
  function numberTraps(right) {
    var out = [], m;
    if ((m = right.match(/^(\d{1,2}):(\d{2}) (AM|PM)$/))) {
      var h = +m[1], mm = m[2], ap = m[3], other = ap === "AM" ? "PM" : "AM";
      out.push(h + ":" + mm + " " + other, ((h % 12) + 1) + ":" + mm + " " + ap, h + ":" + (mm[1] + mm[0]) + " " + ap, ((h + 10) % 12 + 1) + ":" + mm + " " + ap);
      return out;
    }
    if ((m = right.match(/^(\d+):(\d+)$/))) {
      var a = +m[1], b = +m[2];
      out.push(b + ":" + a, a + ":" + (b + 1), (a + 1) + ":" + b, (a * 2) + ":" + b);
      return out;
    }
    if ((m = right.match(/^(\d+)\/(\d+)$/))) {
      var p = +m[1], q = +m[2];
      out.push(q + "/" + p, (p + 1) + "/" + q, (p + 2) + "/" + q, (p - 1 > 0 ? p - 1 : p + 3) + "/" + q);
      return out;
    }
    if ((m = right.match(/^([^\d]*)([\d,]*\.?\d+)(.*)$/))) {
      var pre = m[1], raw = m[2], post = m[3], comma = raw.indexOf(",") >= 0, n = parseFloat(raw.replace(/,/g, ""));
      if (isNaN(n)) return out;
      var dec = (raw.split(".")[1] || "").length, step = n >= 20 ? Math.max(1, Math.round(n * 0.1)) : 1;
      var cands = [n * 2, n / 2, n + step, n - step, n * 10, n + 2 * step, Number(String(Math.round(n)).split("").reverse().join(""))];
      cands.forEach(function (v) {
        if (!(v > 0) || v === n) return;
        if (!dec && v % 1) return;
        var s = v % 1 ? String(+v.toFixed(dec)) : (comma || v >= 10000 ? fmt(v) : String(v));
        out.push(pre + s + post);
      });
      return out;
    }
    return out;
  }

  // Build 4 choices: the right one plus 3 tricky wrong ones. pool = other answers to fall back on.
  function make(card, pool) {
    var right = strip(card.a);
    var wrong = [];
    function add(x) {
      x = String(x).trim();
      if (x && low(x) !== low(right) && wrong.every(function (w) { return low(w) !== low(x); }) && wrong.length < 3) wrong.push(x);
    }
    shuffle(lookalikes(right)).map(strip).forEach(add);
    if (/\d/.test(right)) shuffle(numberTraps(right).slice(0, 4)).forEach(add);
    var isNum = /^[₱\d]/.test(right);
    shuffle((pool || []).map(strip).filter(function (a) { return /^[₱\d]/.test(a) === isNum; })).forEach(add);
    var all = shuffle(wrong.concat([right]));
    return { choices: all, right: all.indexOf(right) };
  }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  window.GEN = GEN;
  window.GEN_LINK = LINK;
  // Multi-part or long answers stay as typed questions.
  function canChoose(card) { var r = strip(card.a); return !card.self && r.length <= 40 && !/[;,]/.test(r.replace(/\d,\d/g, "")) && !(card.k || []).some(function (k) { return k.indexOf("+") >= 0; }); }
  window.Traps = { make: make, strip: strip, canChoose: canChoose };
})();
