/* Instrument panels over the hero scene.
 *
 * Two readouts, in the corners the town leaves empty: the field (the whole
 * town, aggregated) and one tracked person. The numbers are an illustrative
 * distribution drawn from the same seed and the same emotion priors as the
 * scene, not measured data; the panels say so.
 *
 * The panels drive themselves, whether or not the WebGL scene is running, so
 * the corners are never empty and the figures always move. The scene's own
 * people hold a fixed distribution for the whole session, so reading them
 * instead would leave the panels frozen.
 */
(function () {
  "use strict";

  var field = document.querySelector('[data-hero-dash="field"]');
  var person = document.querySelector('[data-hero-dash="person"]');
  if (!field || !person) return;

  // Palette and arousal priors: identical to the scene (affectoscope.js).
  var HEX = [
    "#C4974A", "#8DB462", "#6B8F7A", "#547B84",
    "#3D6B8C", "#6E5584", "#B5737A", "#BD8560",
  ];
  var AROUSAL = [0.65, 0.30, 0.80, 0.95, 0.20, 0.50, 0.90, 0.55];
  var K = 8;
  var N = 40;
  var BARS = 4;
  var TRACE = 36;

  function parseList(raw, fallback) {
    try {
      var v = JSON.parse(raw);
      return Array.isArray(v) && v.length ? v : fallback;
    } catch (e) {
      return fallback;
    }
  }
  var names = parseList(field.getAttribute("data-names"), [
    "joy", "trust", "fear", "surprise", "sadness", "disgust", "anger", "anticipation",
  ]);
  var modes = parseList(person.getAttribute("data-modes"), ["walking", "in the park"]);

  function slot(root, name) {
    return root.querySelector('[data-f="' + name + '"]');
  }

  // ── Seeded PRNG (mulberry32); Math.random() is never used ────────────────
  var SEED = 0xA3F7C2B1;
  function mulberry32(seed) {
    var s = seed >>> 0;
    return function () {
      s = (s + 0x6D2B79F5) >>> 0;
      var t = Math.imul(s ^ (s >>> 15), 1 | s);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var rand = mulberry32(SEED);

  // ── Population ───────────────────────────────────────────────────────────
  // Latent Gamma-ish weights; the distribution is their normalisation, so a
  // slow multiplicative walk on the weights keeps the simplex without drift.
  function newWeights() {
    var dominant = rand() < 0.7 ? (rand() < 0.6 ? 0 : 1) : Math.floor(rand() * K);
    var boost = 0.4 + Math.pow(rand(), 0.8) * 6.5;
    var w = new Array(K);
    for (var k = 0; k < K; k++) w[k] = -Math.log(1 - rand() * 0.999);
    w[dominant] += boost;
    return w;
  }
  function probsOf(w) {
    var sum = 0, k;
    for (k = 0; k < K; k++) sum += w[k];
    var p = new Array(K);
    for (k = 0; k < K; k++) p[k] = w[k] / sum;
    return p;
  }
  function entropy(p) {
    var h = 0;
    for (var k = 0; k < K; k++) if (p[k] > 0) h -= p[k] * Math.log(p[k]);
    return h / Math.log(K);
  }
  // How far the field as a whole sits from a flat eight-way split.
  function concentration(p) {
    var top = 0;
    for (var k = 0; k < K; k++) if (p[k] > top) top = p[k];
    return Math.max(0, (top - 1 / K) / (1 - 1 / K));
  }
  function argmax(p) {
    var best = 0;
    for (var k = 1; k < K; k++) if (p[k] > p[best]) best = k;
    return best;
  }

  // Each person keeps the weights they started with as an anchor: the walk
  // wanders around a temperament instead of drifting everyone to uniform.
  var pop = [], anchor = [];
  for (var i = 0; i < N; i++) {
    var w0 = newWeights();
    anchor.push(w0);
    pop.push(w0.slice());
  }
  var TRACKED = 17 % N;

  function step() {
    for (var i = 0; i < N; i++) {
      var w = pop[i], a = anchor[i];
      for (var k = 0; k < K; k++) {
        // Multiplicative walk with reversion: a mood moves, it does not jump,
        // and it comes back.
        w[k] += (a[k] - w[k]) * 0.12;
        w[k] *= Math.exp((rand() - 0.5) * 0.30);
        if (w[k] < 0.02) w[k] = 0.02;
      }
    }
  }

  function measure() {
    var mean = new Array(K), k, i;
    for (k = 0; k < K; k++) mean[k] = 0;
    var meanH = 0;
    for (i = 0; i < N; i++) {
      var p = probsOf(pop[i]);
      meanH += entropy(p);
      for (k = 0; k < K; k++) mean[k] += p[k] / N;
    }
    meanH /= N;
    var me = probsOf(pop[TRACKED]);
    var top = argmax(me);
    var arousal = 0;
    for (k = 0; k < K; k++) arousal += me[k] * AROUSAL[k];
    return {
      n: N,
      mean: mean,
      certainty: 1 - meanH,
      agreement: concentration(mean),
      person: {
        id: TRACKED,
        mode: mean[0] > 0.5 ? 1 : 0,
        probs: me,
        top: top,
        arousal: arousal,
        certainty: 1 - entropy(me),
      },
    };
  }

  // ── Panel construction ───────────────────────────────────────────────────
  var barsHost = slot(field, "bars");
  var rows = [];
  for (var b = 0; b < BARS; b++) {
    var li = document.createElement("li");
    li.style.cssText = "display:flex;align-items:center;gap:8px;";

    var lab = document.createElement("span");
    lab.style.cssText =
      "width:3.6rem;flex:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" +
      'font-family:"Times New Roman","Noto Serif JP",Times,serif;font-size:0.7rem;color:#1A1A1A;';

    var track = document.createElement("span");
    track.style.cssText =
      "position:relative;flex:1 1 auto;height:5px;background:rgba(26,26,26,0.09);";

    var fill = document.createElement("span");
    fill.style.cssText =
      "position:absolute;inset:0 auto 0 0;width:0;transition:width 900ms linear,background-color 900ms linear;";
    track.appendChild(fill);

    var val = document.createElement("span");
    val.style.cssText =
      "width:2.3rem;flex:none;text-align:right;font-variant-numeric:tabular-nums;" +
      'font-family:"JetBrains Mono",ui-monospace,monospace;font-size:0.6rem;color:#4C535C;';

    li.appendChild(lab);
    li.appendChild(track);
    li.appendChild(val);
    barsHost.appendChild(li);
    rows.push({ lab: lab, fill: fill, val: val });
  }

  var out = {
    n: slot(field, "n"),
    certainty: slot(field, "certainty"),
    agreement: slot(field, "agreement"),
    id: slot(person, "id"),
    mode: slot(person, "mode"),
    line: slot(person, "spark"),
    area: slot(person, "spark-area"),
    dot: slot(person, "spark-dot"),
    top: slot(person, "top"),
    topv: slot(person, "topv"),
    pcert: slot(person, "pcertainty"),
    arousal: slot(person, "arousal"),
  };

  function fixed(x, d) {
    return x.toFixed(d === undefined ? 2 : d);
  }

  var trace = [];
  var SW = 100, SH = 26;

  function drawTrace() {
    var pts = [], i;
    for (i = 0; i < trace.length; i++) {
      var x = (i / (TRACE - 1)) * SW;
      var y = SH - Math.max(0, Math.min(1, trace[i] / 0.75)) * (SH - 3) - 1.5;
      pts.push(x.toFixed(1) + "," + y.toFixed(1));
    }
    if (!pts.length) return;
    out.line.setAttribute("points", pts.join(" "));
    out.area.setAttribute("d", "M0," + SH + " L" + pts.join(" L") + " L" + SW + "," + SH + " Z");
    if (out.dot) {
      var last = pts[pts.length - 1].split(",");
      out.dot.setAttribute("cx", last[0]);
      out.dot.setAttribute("cy", last[1]);
    }
  }

  function render(s) {
    var order = [], k;
    for (k = 0; k < K; k++) order.push(k);
    order.sort(function (a, c) { return s.mean[c] - s.mean[a]; });

    out.n.textContent = String(s.n);
    for (var b = 0; b < BARS; b++) {
      var idx = order[b];
      var row = rows[b];
      row.lab.textContent = names[idx] || "";
      var top = s.mean[order[0]] || 1;
      row.fill.style.width = Math.max(4, (s.mean[idx] / top) * 100) + "%";
      row.fill.style.backgroundColor = HEX[idx];
      row.val.textContent = Math.round(s.mean[idx] * 100) + "%";
    }
    out.certainty.textContent = fixed(s.certainty);
    out.agreement.textContent = fixed(s.agreement);

    var p = s.person;
    out.id.textContent = "#" + String(p.id).padStart(2, "0");
    out.mode.textContent = modes[p.mode] || modes[0];
    out.top.textContent = names[p.top] || "";
    out.top.style.color = HEX[p.top];
    out.topv.textContent = fixed(p.probs[p.top]);
    out.pcert.textContent = fixed(p.certainty);
    out.arousal.textContent = fixed(p.arousal);

    out.line.setAttribute("stroke", HEX[p.top]);
    out.area.setAttribute("fill", HEX[p.top]);
    if (out.dot) out.dot.setAttribute("fill", HEX[p.top]);

    trace.push(p.probs[p.top]);
    while (trace.length > TRACE) trace.shift();
    drawTrace();
  }

  // History, so the trace is already a line when the panel first appears.
  for (var w = 0; w < TRACE; w++) {
    step();
    var s0 = measure();
    trace.push(s0.person.probs[s0.person.top]);
  }
  while (trace.length > TRACE) trace.shift();
  trace.pop();
  render(measure());

  field.style.opacity = "1";
  person.style.opacity = "1";

  // ── Driving ──────────────────────────────────────────────────────────────
  var motionOk = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (motionOk) {
    window.setInterval(function () {
      if (document.hidden) return;
      step();
      render(measure());
    }, 1100);
  }
})();
