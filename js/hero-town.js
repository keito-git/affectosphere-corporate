// Hero background: the daytime-town study from Chromasphere Atelier
// (affectosphere_waves_v3_day_town). People walk the streets, each one
// broadcasting its emotion distribution as a wave; the interference of all
// of them is the layer of air above the town — the affectosphere.
//
// Differences from the gallery piece: no control panel, no pointer
// interaction (the hero must not swallow clicks or scrolling), the camera is
// framed lower so the headline sits over open sky, and the loop idles when
// the hero is off screen. Requires THREE (r128) on the global scope.
(function () {
  "use strict";

  // ── Emotion palette (shared with affectoscope.js) and arousal priors ──────
  const EMO = [
    { key: "joy",          ja: "喜び",   hex: "#C4974A", arousal: 0.65 },
    { key: "trust",        ja: "信頼",   hex: "#8DB462", arousal: 0.30 },
    { key: "fear",         ja: "恐れ",   hex: "#6B8F7A", arousal: 0.80 },
    { key: "surprise",     ja: "驚き",   hex: "#547B84", arousal: 0.95 },
    { key: "sadness",      ja: "悲しみ", hex: "#3D6B8C", arousal: 0.20 },
    { key: "disgust",      ja: "嫌悪",   hex: "#6E5584", arousal: 0.50 },
    { key: "anger",        ja: "怒り",   hex: "#B5737A", arousal: 0.90 },
    { key: "anticipation", ja: "期待",   hex: "#BD8560", arousal: 0.55 },
  ];
  const K = EMO.length;
  const EMO_RGB = EMO.map(e => new THREE.Color(e.hex));

  // ── Seeded PRNG (mulberry32); Math.random() is never used ───────────────
  const SEED = 0xA3F7C2B1;
  function mulberry32(seed) {
    let s = seed >>> 0;
    return function () {
      s += 0x6D2B79F5;
      let t = Math.imul(s ^ (s >>> 15), 1 | s);
      t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  let rand = mulberry32(SEED);

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const MAX_PEOPLE = 48;
  const INITIAL_WALKERS = 30;
  const INITIAL_PARK = 10;

  // ── Town plan: a 4×4 street grid; the centre block is a park ────────────
  const STREETS = [-12, -4, 4, 12];      // street centre lines (x and z)
  const STREET_W = 2.2;
  const PARK = 2.6;                      // walkable half-size of the central park
  const LAYER_HEIGHTS = [0.03, 1.8, 3.6, 5.6];   // ground + three air layers

  // ── Emotion distribution → wave parameters ──────────────────────────────
  function sampleDistribution(dominant, boost) {
    const w = new Array(K);
    for (let k = 0; k < K; k++) w[k] = -Math.log(1 - rand() * 0.999);
    w[dominant] += boost;
    const sum = w.reduce((a, b) => a + b, 0);
    return w.map(x => x / sum);
  }

  function makePerson(probs) {
    let dominant = 0;
    for (let k = 1; k < K; k++) if (probs[k] > probs[dominant]) dominant = k;
    let H = 0;
    for (const p of probs) if (p > 0) H -= p * Math.log(p);
    H /= Math.log(K);
    const sharp = Math.max(0, Math.min(1, (1 - H) * 2.2));
    let arousal = 0;
    probs.forEach((p, k) => { arousal += p * EMO[k].arousal; });
    const mix = new THREE.Color(0, 0, 0);
    probs.forEach((p, k) => { mix.r += p * EMO_RGB[k].r; mix.g += p * EMO_RGB[k].g; mix.b += p * EMO_RGB[k].b; });
    const color = EMO_RGB[dominant].clone().lerp(mix, Math.min(1, H * 1.1));
    const interval = 3.2 - 2.0 * arousal;
    return {
      pos: new THREE.Vector2(), target: new THREE.Vector2(),
      speed: (0.7 + 1.5 * arousal) * (reduceMotion ? 0.3 : 1),
      probs, dominant, H, sharp, arousal, color,
      omega: 1.2 + 3.6 * arousal,
      k: 1.0 + 1.8 * sharp,
      amp: 0.3 + 0.5 * probs[dominant],
      phase: rand() * Math.PI * 2,
      interval, next: rand() * interval,
      reach: 2.8 + 3.2 * probs[dominant],
      mode: "walk", lane: 0, node: [0, 0],
    };
  }

  // Walkers move between street intersections on a lane offset from the centre line.
  function nodePos(ix, iz, lane) {
    return new THREE.Vector2(STREETS[ix] + lane, STREETS[iz] + lane);
  }
  function pickNextNode(p) {
    const [ix, iz] = p.node, options = [];
    if (ix > 0) options.push([ix - 1, iz]);
    if (ix < 3) options.push([ix + 1, iz]);
    if (iz > 0) options.push([ix, iz - 1]);
    if (iz < 3) options.push([ix, iz + 1]);
    p.node = options[Math.floor(rand() * options.length)];
    p.target = nodePos(p.node[0], p.node[1], p.lane);
  }
  function parkPoint() {
    return new THREE.Vector2((rand() * 2 - 1) * PARK, (rand() * 2 - 1) * PARK);
  }
  function asWalker(p, ix, iz) {
    p.mode = "walk";
    p.lane = (rand() < 0.5 ? -1 : 1) * (0.55 + rand() * 0.35);
    p.node = [ix, iz];
    p.pos.copy(nodePos(ix, iz, p.lane));
    pickNextNode(p);
    // Start somewhere along the first segment so the street is not empty at t = 0.
    p.pos.lerp(p.target, rand());
    return p;
  }
  function asParkGoer(p, at) {
    p.mode = "park";
    p.speed *= 0.45;
    p.pos.copy(at || parkPoint());
    p.target = parkPoint();
    return p;
  }

  function initialPeople() {
    rand = mulberry32(SEED);
    const list = [];
    // The park holds a cheerful group; one avenue carries a hurried, tense crowd.
    for (let i = 0; i < INITIAL_PARK; i++) {
      const dominant = rand() < 0.7 ? (rand() < 0.6 ? 0 : 1) : Math.floor(rand() * K);
      list.push(asParkGoer(makePerson(sampleDistribution(dominant, 0.5 + rand() * 7))));
    }
    for (let i = 0; i < INITIAL_WALKERS; i++) {
      const ix = Math.floor(rand() * 4), iz = Math.floor(rand() * 4);
      let dominant = Math.floor(rand() * K);
      if (ix === 3 && rand() < 0.6) dominant = rand() < 0.5 ? 6 : 2;   // a busy east avenue
      const boost = 0.2 + Math.pow(rand(), 0.8) * 7.5;
      list.push(asWalker(makePerson(sampleDistribution(dominant, boost)), ix, iz));
    }
    return list;
  }

  // ── Renderer / scene ────────────────────────────────────────────────────
  const canvas = document.querySelector("[data-hero-town]");
  if (!canvas) return;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0xE6EEF2, 1);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(0xE6EEF2, 55, 110);
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 200);
  const orbit = { theta: 0.72, phi: 0.82, radius: 44, target: new THREE.Vector3(0, 0.5, 0) };
  function placeCamera() {
    const { theta, phi, radius, target } = orbit;
    camera.position.set(
      target.x + radius * Math.sin(phi) * Math.sin(theta),
      target.y + radius * Math.cos(phi),
      target.z + radius * Math.sin(phi) * Math.cos(theta)
    );
    camera.lookAt(target);
  }

  // Daylight.
  scene.add(new THREE.HemisphereLight(0xF4F8FA, 0xB8B2A6, 0.75));
  const sun = new THREE.DirectionalLight(0xFFF6E8, 0.85);
  sun.position.set(-18, 30, 12);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -26, right: 26, top: 26, bottom: -26, near: 1, far: 80 });
  sun.shadow.bias = -0.0006;
  scene.add(sun);

  // Ground: pavement blocks, asphalt streets, a lawn in the park.
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), new THREE.MeshLambertMaterial({ color: 0xD7D8D3 }));
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);
  const asphalt = new THREE.MeshLambertMaterial({ color: 0xA9AFB4 });
  const markMat = new THREE.MeshBasicMaterial({ color: 0xF2F2EE });
  STREETS.forEach(c => {
    const a = new THREE.Mesh(new THREE.PlaneGeometry(STREET_W, 34), asphalt);
    a.rotation.x = -Math.PI / 2; a.position.set(c, 0.01, 0); a.receiveShadow = true; scene.add(a);
    const b = new THREE.Mesh(new THREE.PlaneGeometry(34, STREET_W), asphalt);
    b.rotation.x = -Math.PI / 2; b.position.set(0, 0.011, c); b.receiveShadow = true; scene.add(b);
  });
  // Zebra crossings at every intersection.
  STREETS.forEach(x => STREETS.forEach(z => {
    for (let s = -0.8; s <= 0.81; s += 0.4) {
      const m1 = new THREE.Mesh(new THREE.PlaneGeometry(0.22, 0.9), markMat);
      m1.rotation.x = -Math.PI / 2; m1.position.set(x + s, 0.02, z + STREET_W / 2 + 0.5); scene.add(m1);
      const m2 = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.22), markMat);
      m2.rotation.x = -Math.PI / 2; m2.position.set(x + STREET_W / 2 + 0.5, 0.02, z + s); scene.add(m2);
    }
  }));
  const lawn = new THREE.Mesh(new THREE.PlaneGeometry(5.6, 5.6), new THREE.MeshLambertMaterial({ color: 0xA9BE92 }));
  lawn.rotation.x = -Math.PI / 2; lawn.position.y = 0.015; lawn.receiveShadow = true;
  scene.add(lawn);

  // Buildings and park trees.
  (function addTown() {
    const r = mulberry32(SEED ^ 0x2F6B1D3);
    const box = new THREE.BoxGeometry(1, 1, 1);
    const facades = [0xEDE8DF, 0xE2E5E6, 0xD9D2C6, 0xE9E3D6, 0xD5DADC, 0xF1EEE8].map(c => new THREE.MeshLambertMaterial({ color: c }));
    const roof = new THREE.MeshLambertMaterial({ color: 0x9FA6AA });
    // Block centres sit between streets; the centre block is the park.
    const blocks = [-16.6, -8, 0, 8, 16.6];
    for (let bi = 0; bi < blocks.length; bi++) {
      for (let bj = 0; bj < blocks.length; bj++) {
        const cx = blocks[bi], cz = blocks[bj];
        if (cx === 0 && cz === 0) continue;
        const half = (Math.abs(cx) > 12 || Math.abs(cz) > 12) ? 1.8 : 2.6;
        // 2×2 lots per block.
        for (const ox of [-0.5, 0.5]) for (const oz of [-0.5, 0.5]) {
          if (r() < 0.12) continue;   // the odd empty lot
          const w = half - 0.35 - r() * 0.4, d = half - 0.35 - r() * 0.4;
          const central = Math.max(Math.abs(cx), Math.abs(cz)) < 10;
          const h = central ? 1.6 + Math.pow(r(), 1.6) * 4.8 : 1.2 + Math.pow(r(), 1.8) * 2.6;
          const m = new THREE.Mesh(box, facades[Math.floor(r() * facades.length)]);
          m.scale.set(w, h, d);
          m.position.set(cx + ox * half, h / 2, cz + oz * half);
          m.castShadow = true; m.receiveShadow = true;
          scene.add(m);
          const cap = new THREE.Mesh(box, roof);
          cap.scale.set(w * 0.96, 0.08, d * 0.96);
          cap.position.set(m.position.x, h + 0.04, m.position.z);
          scene.add(cap);
        }
      }
    }
    const trunk = new THREE.MeshLambertMaterial({ color: 0x8A7560 });
    const leaf = new THREE.MeshLambertMaterial({ color: 0x7FA06B });
    const trunkGeo = new THREE.CylinderGeometry(0.07, 0.09, 0.7, 6);
    const crownGeo = new THREE.SphereGeometry(0.55, 10, 8);
    [[-2.2, -2.2], [2.2, -2.2], [-2.2, 2.2], [2.2, 2.2], [0, -2.5], [-2.5, 0.4]].forEach(([x, z]) => {
      const t = new THREE.Mesh(trunkGeo, trunk); t.position.set(x, 0.35, z); t.castShadow = true; scene.add(t);
      const c = new THREE.Mesh(crownGeo, leaf); c.position.set(x, 1.05, z); c.castShadow = true; scene.add(c);
    });
  })();

  // ── Affectosphere: interference field sampled on stacked horizontal layers ─
  const posArr = Array.from({ length: MAX_PEOPLE }, () => new THREE.Vector3());
  const colArr = Array.from({ length: MAX_PEOPLE }, () => new THREE.Vector3());
  const parArr = Array.from({ length: MAX_PEOPLE }, () => new THREE.Vector4());
  const sharedField = { uTime: { value: 0 }, uCount: { value: 0 }, uPos: { value: posArr }, uCol: { value: colArr }, uParam: { value: parArr } };

  const layerVS = `
    varying vec2 vXZ;
    void main() {
      vec4 wp = modelMatrix * vec4(position, 1.0);
      vXZ = wp.xz;
      gl_Position = projectionMatrix * viewMatrix * wp;
    }`;
  const layerFS = `
    #define N ${MAX_PEOPLE}
    uniform float uTime;
    uniform int uCount;
    uniform vec3 uPos[N];
    uniform vec3 uCol[N];
    uniform vec4 uParam[N]; // x = omega, y = spatial k, z = amplitude, w = phase
    uniform float uH;
    uniform float uAlpha;
    uniform float uSpread;
    varying vec2 vXZ;
    void main() {
      float f = 0.0; vec3 ca = vec3(0.0); float wa = 0.0;
      for (int i = 0; i < N; i++) {
        if (i >= uCount) break;
        vec2 dd = vXZ - uPos[i].xz;
        float d = sqrt(dot(dd, dd) + uH * uH);
        vec4 p = uParam[i];
        float env = exp(-d * d * uSpread);
        float c = p.z * env * sin(p.y * d - p.x * uTime + p.w);
        f += c; ca += uCol[i] * abs(c); wa += abs(c);
      }
      vec3 base = wa > 1e-4 ? ca / wa : vec3(0.6);
      float inten = clamp(abs(f), 0.0, 1.0);
      float crest = smoothstep(0.35, 1.0, inten);
      float body = clamp(wa * 0.6, 0.0, 1.0);
      float edge = 1.0 - smoothstep(15.0, 19.0, max(abs(vXZ.x), abs(vXZ.y)));
      float a = (0.08 * body + 0.45 * inten + 0.35 * crest) * uAlpha * edge;
      float g = dot(base, vec3(0.3333));
      vec3 vivid = clamp(mix(vec3(g), base, 2.0), 0.0, 1.0);
      vec3 col = mix(vivid, vivid * 0.78, crest);
      gl_FragColor = vec4(col, clamp(a, 0.0, 0.85));
    }`;

  const sphereGroup = new THREE.Group();
  scene.add(sphereGroup);
  const layerGeo = new THREE.PlaneGeometry(40, 40, 1, 1);
  LAYER_HEIGHTS.forEach((h, idx) => {
    const mat = new THREE.ShaderMaterial({
      uniforms: Object.assign({}, sharedField, {
        uH: { value: Math.max(0, h - 0.6) },
        uAlpha: { value: [0.7, 0.42, 0.3, 0.2][idx] },
        uSpread: { value: [0.07, 0.05, 0.035, 0.022][idx] },
      }),
      vertexShader: layerVS, fragmentShader: layerFS,
      transparent: true, depthWrite: false, side: THREE.DoubleSide,
    });
    const m = new THREE.Mesh(layerGeo, mat);
    m.rotation.x = -Math.PI / 2;
    m.position.y = h;
    m.renderOrder = 2 + idx;
    sphereGroup.add(m);
  });

  // ── Radio waves: domes expanding from each person ───────────────────────
  const domeGeo = new THREE.SphereGeometry(1, 48, 20, 0, Math.PI * 2, 0, Math.PI / 2);
  const shellVS = `
    uniform float uSharp; uniform float uTime; uniform float uSeed;
    varying float vRim;
    void main() {
      vec3 n = normalize(position);
      float wob = (1.0 - uSharp) * 0.12 * (sin(n.x * 7.0 + uTime * 1.3 + uSeed) * sin(n.z * 6.0 - uTime * 0.9) + 0.5 * sin(n.y * 9.0 + uSeed));
      vec3 pos = position * (1.0 + wob);
      vec4 mv = modelViewMatrix * vec4(pos, 1.0);
      vec3 vn = normalize(normalMatrix * n);
      vRim = 1.0 - abs(dot(vn, normalize(-mv.xyz)));
      gl_Position = projectionMatrix * mv;
    }`;
  const shellFS = `
    uniform vec3 uColor; uniform float uAge; uniform float uSharp;
    varying float vRim;
    void main() {
      float rim = pow(vRim, mix(1.2, 4.5, uSharp));
      float fade = pow(1.0 - uAge, 1.5) * smoothstep(0.0, 0.06, uAge);
      float a = rim * fade * mix(0.22, 0.7, uSharp);
      float g = dot(uColor, vec3(0.3333));
      gl_FragColor = vec4(clamp(mix(vec3(g), uColor, 1.8), 0.0, 1.0), a);
    }`;
  const SHELLS = 120;
  const shells = [];
  const wavesGroup = new THREE.Group();
  scene.add(wavesGroup);
  for (let i = 0; i < SHELLS; i++) {
    const mat = new THREE.ShaderMaterial({
      uniforms: {
        uColor: { value: new THREE.Color() }, uAge: { value: 1 }, uSharp: { value: 1 },
        uTime: { value: 0 }, uSeed: { value: i * 1.37 },
      },
      vertexShader: shellVS, fragmentShader: shellFS,
      transparent: true, depthWrite: false, side: THREE.DoubleSide,
    });
    const m = new THREE.Mesh(domeGeo, mat);
    m.visible = false;
    m.renderOrder = 1;
    wavesGroup.add(m);
    shells.push({ mesh: m, born: -1, life: 3.6, reach: 3 });
  }
  let shellCursor = 0;

  // ── People ──────────────────────────────────────────────────────────────
  const bodyGeo = new THREE.CylinderGeometry(0.18, 0.26, 0.95, 10);
  const headGeo = new THREE.SphereGeometry(0.2, 12, 8);
  const peopleGroup = new THREE.Group();
  scene.add(peopleGroup);
  let people = [];
  let figures = [];

  function buildFigure(p) {
    const g = new THREE.Group();
    const mat = new THREE.MeshLambertMaterial({ color: p.color, emissive: p.color.clone().multiplyScalar(0.25) });
    const body = new THREE.Mesh(bodyGeo, mat); body.position.y = 0.48; body.castShadow = true;
    const head = new THREE.Mesh(headGeo, mat); head.position.y = 1.16; head.castShadow = true;
    g.add(body, head);
    g.userData.mat = mat;
    return g;
  }

  function syncPeople() {
    figures.forEach(f => { peopleGroup.remove(f); f.userData.mat.dispose(); });
    figures = people.map(p => { const f = buildFigure(p); peopleGroup.add(f); return f; });
    people.forEach((p, i) => {
      colArr[i].set(p.color.r, p.color.g, p.color.b);
      parArr[i].set(p.omega, p.k, p.amp, p.phase);
    });
    sharedField.uCount.value = people.length;
  }

  function emit(p, i, t) {
    const s = shells[shellCursor];
    shellCursor = (shellCursor + 1) % SHELLS;
    s.born = t; s.reach = p.reach; s.life = 2.8 + 1.8 * (1 - p.arousal);
    s.mesh.position.set(p.pos.x, 0.7, p.pos.y);
    s.mesh.material.uniforms.uColor.value.copy(p.color);
    s.mesh.material.uniforms.uSharp.value = p.sharp;
    s.mesh.visible = true;
    if (figures[i]) figures[i].userData.pulse = t;
  }

  function reset() {
    shells.forEach(s => { s.mesh.visible = false; s.born = -1; });
    people = initialPeople();
    syncPeople();
  }

  // The scene turns slowly on its own; nothing here reacts to the pointer.
  const AUTO_SPIN = reduceMotion ? 0 : 0.0006;
  let spin = AUTO_SPIN;

  // ── Resize & loop ───────────────────────────────────────────────────────
  function resize() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    const wide = w > 820;
    camera.setViewOffset(w, h, 0, -h * (wide ? 0.17 : 0.10), w, h);
    camera.updateProjectionMatrix();
  }
  window.addEventListener("resize", resize);

  const clock = new THREE.Clock();
  const timeScale = reduceMotion ? 0.3 : 1;
  let simT = 0, lastReal = 0;
  let rafId = 0, drawn = false, running = false;
  const tmp = new THREE.Vector2();

  function frame() {
    const real = clock.getElapsedTime();
    const dt = Math.min(0.05, real - lastReal) * timeScale;
    lastReal = real; simT += dt;
    const t = simT;

    orbit.theta += spin;
    spin += (AUTO_SPIN - spin) * 0.03;
    placeCamera();

    people.forEach((p, i) => {
      tmp.copy(p.target).sub(p.pos);
      const dist = tmp.length();
      if (dist < 0.12) {
        if (p.mode === "walk") pickNextNode(p); else p.target = parkPoint();
      } else {
        p.pos.add(tmp.multiplyScalar(Math.min(dist, p.speed * dt) / dist));
      }
      posArr[i].set(p.pos.x, 0, p.pos.y);
      const f = figures[i];
      if (f) {
        f.position.set(p.pos.x, 0, p.pos.y);
        const k = f.userData.pulse === undefined ? 0 : Math.max(0, 1 - (t - f.userData.pulse) / 0.5);
        f.scale.setScalar(1 + k * 0.3);
      }
      if (t >= p.next) {
        emit(p, i, t);
        p.next = t + p.interval * (0.8 + 0.4 * rand());
      }
    });

    for (const s of shells) {
      if (s.born < 0) continue;
      const age = (t - s.born) / s.life;
      if (age >= 1) { s.mesh.visible = false; s.born = -1; continue; }
      s.mesh.scale.setScalar(0.08 + s.reach * (1 - Math.pow(1 - age, 2)));
      s.mesh.material.uniforms.uAge.value = age;
      s.mesh.material.uniforms.uTime.value = t;
    }

    sharedField.uTime.value = t;
    renderer.render(scene, camera);
    if (!drawn) {
      drawn = true;
      canvas.dataset.heroTownReady = "1";
      canvas.style.opacity = "1";   // cross-fade from the still
    }
    rafId = requestAnimationFrame(frame);
  }

  function play() {
    if (running) return;
    running = true;
    lastReal = clock.getElapsedTime();   // skip the time spent paused
    rafId = requestAnimationFrame(frame);
  }
  function pause() {
    running = false;
    cancelAnimationFrame(rafId);
  }

  // Idle whenever the hero is scrolled away or the tab is in the background:
  // a WebGL loop left running costs battery for nothing.
  if (typeof IntersectionObserver === "function") {
    new IntersectionObserver(entries => {
      for (const e of entries) (e.isIntersecting ? play : pause)();
    }, { threshold: 0 }).observe(canvas);
  }
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) pause();
    else if (canvas.isConnected) play();
  });

  reset();
  resize();
  placeCamera();
  play();
})();
