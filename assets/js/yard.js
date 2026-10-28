/* Fence Template — 3D yard scroll scene at the top of the home page (needs three.js, self-hosted in js/vendor).

   The hero section is pinned for several screens. Scroll progress p (0-1) drives everything:
     0.00-0.11  the hero copy over an aerial view of an open backyard (house, patio with the family, pool, dog,
                swing set, shed)
     0.06-0.18  a string line and stakes trace the fence line
     0.16-0.80  the fence is built around the whole perimeter: posts drop in, rails run, pickets close in,
                while the camera flies around the yard and the messages change (family, pets, belongings, privacy)
     0.80-0.88  the gate swings shut and latches
     0.55-0.95  the sun sets; house windows, string lights, pool lights and post-cap lights come on
     0.87+      the tags over the family, dog, shed and pool flip to "Protected"; the estimate card appears
   No WebGL, no three.js or reduced motion: the section stays a normal hero (html.yard-off / CSS media query). */
(function () {
  "use strict";
  var doc = document.documentElement;
  var sec = document.querySelector("[data-yard]");
  if (!sec) return;
  var off = function () { doc.classList.add("yard-off"); };
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) { off(); return; }
  if (!window.THREE) { off(); return; }
  var T = window.THREE;
  var canvas = sec.querySelector(".yard__canvas");
  var renderer;
  try { renderer = new T.WebGLRenderer({ canvas: canvas, antialias: true, powerPreference: "high-performance" }); }
  catch (e) { off(); return; }
  if (!renderer.getContext()) { off(); return; }

  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var seg = function (p, a, b) { return clamp((p - a) / (b - a)); };
  var ease = function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  var lerp = function (a, b, t) { return a + (b - a) * t; };
  var seed = 7; var rnd = function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  var css = getComputedStyle(doc);
  var ACC = new T.Color((css.getPropertyValue("--accent") || "#f5a524").trim());
  var BIG = window.innerWidth > 900;

  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, BIG ? 1.75 : 1.5));
  renderer.outputEncoding = T.sRGBEncoding;
  renderer.toneMapping = T.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 0.95;
  if (BIG) { renderer.shadowMap.enabled = true; renderer.shadowMap.type = T.PCFSoftShadowMap; }

  var scene = new T.Scene();
  var cam = new T.PerspectiveCamera(42, 1, 0.5, 2200);

  /* ---------------- sky + fog ---------------- */
  var skyU = { top: { value: new T.Color("#21324f") }, mid: { value: new T.Color("#d9a26a") }, bot: { value: new T.Color("#f3c98f") } };
  var sky = new T.Mesh(new T.SphereGeometry(1200, 32, 16), new T.ShaderMaterial({
    side: T.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: "varying float h;void main(){h=normalize(position).y;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}",
    fragmentShader: "uniform vec3 top;uniform vec3 mid;uniform vec3 bot;varying float h;void main(){vec3 c=h>0.?mix(mid,top,smoothstep(0.,.45,h)):mix(mid,bot,smoothstep(0.,-.2,h));gl_FragColor=vec4(c,1.);}"
  }));
  scene.add(sky);
  scene.fog = new T.Fog(0xd9a26a, 220, 900);

  /* ---------------- lights ---------------- */
  var hemi = new T.HemisphereLight(0xbfd4ff, 0x3a3020, 0.75); scene.add(hemi);
  var sun = new T.DirectionalLight(0xffd29a, 1.5);
  sun.position.set(-90, 110, -70);
  if (BIG) {
    sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
    var sc = sun.shadow.camera; sc.left = -110; sc.right = 110; sc.top = 110; sc.bottom = -110; sc.near = 10; sc.far = 400;
    sun.shadow.bias = -0.0006;
  }
  scene.add(sun);

  var M = function (c, o) { var m = new T.MeshStandardMaterial(Object.assign({ color: c, roughness: 0.85, metalness: 0 }, o || {})); return m; };
  var box = function (w, h, d, mat, x, y, z, parent) {
    var m = new T.Mesh(new T.BoxGeometry(w, h, d), mat); m.position.set(x, y, z);
    m.castShadow = BIG; m.receiveShadow = BIG; (parent || scene).add(m); return m;
  };
  var cyl = function (r1, r2, h, mat, x, y, z, seg, parent) {
    var m = new T.Mesh(new T.CylinderGeometry(r1, r2, h, seg || 10), mat); m.position.set(x, y, z);
    m.castShadow = BIG; (parent || scene).add(m); return m;
  };
  var prism = function (w, h, d, mat, x, y, z, rotY) {   /* gable roof: triangle w x h extruded d */
    var s = new T.Shape(); s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(0, h); s.lineTo(-w / 2, 0);
    var g = new T.ExtrudeGeometry(s, { depth: d, bevelEnabled: false }); g.translate(0, 0, -d / 2);
    var m = new T.Mesh(g, mat); m.position.set(x, y, z); m.rotation.y = rotY || 0; m.castShadow = BIG; scene.add(m); return m;
  };

  /* ---------------- ground: lawn texture with mowing stripes, patio, pool deck, driveway ---------------- */
  var LX0 = -45, LX1 = 45, LZ0 = -72, LZ1 = 84, PX = 6;    /* lot extents (ft) and texture pixels per foot */
  var gc = document.createElement("canvas"); gc.width = (LX1 - LX0) * PX; gc.height = (LZ1 - LZ0) * PX;
  var g = gc.getContext("2d");
  var fx = function (x) { return (x - LX0) * PX; }, fz = function (z) { return (z - LZ0) * PX; };
  g.fillStyle = "#3f6a2c"; g.fillRect(0, 0, gc.width, gc.height);
  for (var sx = LX0; sx < LX1; sx += 6) { g.fillStyle = ((sx / 6) & 1) ? "rgba(255,255,255,.05)" : "rgba(0,0,0,.06)"; g.fillRect(fx(sx), 0, 6 * PX, gc.height); }
  for (var n = 0; n < 4000; n++) { g.fillStyle = "rgba(" + (rnd() < .5 ? "20,40,10" : "120,160,70") + "," + (0.08 + rnd() * 0.1) + ")"; g.fillRect(rnd() * gc.width, rnd() * gc.height, 2, 2); }
  var rect = function (c, x0, z0, x1, z1) { g.fillStyle = c; g.fillRect(fx(x0), fz(z0), (x1 - x0) * PX, (z1 - z0) * PX); };
  rect("#8d8a84", -19, 5, 5, 20);         /* patio */
  for (var pz = 5; pz < 20; pz += 2.5) { g.fillStyle = "rgba(0,0,0,.08)"; g.fillRect(fx(-19), fz(pz), 24 * PX, 1); }
  rect("#c9c3b8", 4, -23, 31, 13);        /* pool deck */
  rect("#55524e", 24, 20, 42, 84);        /* driveway */
  rect("#b5afa5", -3, 46, 3, 84);         /* front walk */
  var gtex = new T.CanvasTexture(gc); gtex.encoding = T.sRGBEncoding; gtex.anisotropy = 4;
  var lot = new T.Mesh(new T.PlaneGeometry(LX1 - LX0, LZ1 - LZ0), M(0xffffff, { map: gtex, roughness: 1 }));
  lot.rotation.x = -Math.PI / 2; lot.position.set((LX0 + LX1) / 2, 0.02, (LZ0 + LZ1) / 2); lot.receiveShadow = BIG; scene.add(lot);
  var world = new T.Mesh(new T.PlaneGeometry(2400, 2400), M(0x2c4520, { roughness: 1 }));
  world.rotation.x = -Math.PI / 2; world.receiveShadow = BIG; scene.add(world);
  box(2400, 0.1, 22, M(0x2a2a2c, { roughness: .95 }), 0, 0.03, 96);                 /* street */
  box(2400, 0.16, 5, M(0x9a958d), 0, 0.06, 86.5);                                     /* sidewalk */
  for (var lm = -600; lm < 600; lm += 24) box(10, 0.12, 0.6, M(0xd8c25a), lm, 0.07, 96);

  /* ---------------- house + neighbours ---------------- */
  var windowMats = [];
  var winMat = function () { var m = M(0x1a1a1c, { emissive: new T.Color("#ffb85c"), emissiveIntensity: 0.05, roughness: .3 }); windowMats.push(m); return m; };
  var house = function (x, z, w, h, d, wall, roof, lit) {
    box(w, h, d, M(wall), x, h / 2, z);
    prism(w + 2, h * 0.42, d + 2, M(roof, { roughness: .9 }), x, h, z, 0);
    var wm = lit ? winMat() : M(0x15161a, { emissive: new T.Color("#ffb85c"), emissiveIntensity: 0.0 });
    if (!lit) windowMats.push(wm);
    [-1, 1].forEach(function (side) {
      for (var i = 0; i < 4; i++) {
        var wx = x - w / 2 + w * (i + 0.5) / 4;
        [h * 0.3, h * 0.72].forEach(function (wy) { box(w / 8, h * 0.2, 0.2, wm, wx, wy, z + side * (d / 2 + 0.06)); });
      }
    });
  };
  house(0, 33, 44, 18, 26, 0xd6cdbf, 0x2b2b30, true);
  box(8, 7.5, 0.2, winMat(), -8, 3.75, 19.94);                         /* patio slider */
  house(-82, 30, 40, 17, 28, 0x9c9488, 0x34302c, false);
  house(82, 34, 42, 18, 26, 0xa59d92, 0x2f2f33, false);
  house(-100, -140, 40, 16, 26, 0x8e877d, 0x30302f, false);
  house(105, -145, 44, 17, 26, 0x968f86, 0x2c2c30, false);

  /* ---------------- backyard: patio set, family, pool, swing set, shed, bikes, trees, BBQ, dog ---------------- */
  var wood = M(0x6b4a30), steel = M(0x6f767d, { metalness: .5, roughness: .45 });
  cyl(2.4, 2.4, 0.25, M(0x2a2a2c), -8, 3, 12, 20); cyl(0.12, 0.12, 3, steel, -8, 1.5, 12);
  cyl(0.1, 0.1, 6, steel, -8, 4.5, 12); var umb = new T.Mesh(new T.ConeGeometry(5, 1.8, 10), M(0xe4dccb, { side: T.DoubleSide })); umb.position.set(-8, 7.6, 12); umb.castShadow = BIG; scene.add(umb);
  [[-11, 12], [-5, 12], [-8, 9], [-8, 15]].forEach(function (c) { box(1.4, 1.8, 1.4, M(0x2f2f33), c[0], 0.9, c[1]); });
  var person = function (x, z, h, col, ry) {
    var gp = new T.Group(); gp.position.set(x, 0, z); gp.rotation.y = ry || 0;
    cyl(0.62 * h / 5, 0.78 * h / 5, h * 0.62, M(col), 0, h * 0.31 + 0.3, 0, 10, gp);
    var hd = new T.Mesh(new T.SphereGeometry(0.42 * h / 5 + 0.15, 14, 10), M(0xc99a76)); hd.position.y = h * 0.62 + 0.3 + 0.5; hd.castShadow = BIG; gp.add(hd);
    scene.add(gp); return gp;
  };
  person(-11.6, 12.3, 5.6, 0x3e5a76, Math.PI / 2);      /* parents at the patio table */
  person(-4.6, 11.6, 5.2, 0x8c3b34, -Math.PI / 2);
  var kid1 = person(-14, -18, 3.4, 0x2f7a52, 0), kid2 = person(-20, -24, 3.1, 0xd29a2e, 0);
  /* pool */
  box(17, 0.6, 28, M(0xe9e4da, { roughness: .6 }), 17.5, 0.3, -5);
  var waterMat = M(0x1f7fae, { emissive: new T.Color("#2bb4ff"), emissiveIntensity: 0.15, roughness: .15, metalness: .1 });
  var water = new T.Mesh(new T.PlaneGeometry(15, 26), waterMat); water.rotation.x = -Math.PI / 2; water.position.set(17.5, 0.62, -5); scene.add(water);
  var poolLight = new T.PointLight(0x5fd0ff, 0, 40); poolLight.position.set(17.5, 2, -5); scene.add(poolLight);
  box(2.4, 0.15, 6, M(0x2c6f9b), 25, 0.75, 6);                         /* diving board */
  /* swing set */
  var red = M(0xb5452e, { roughness: .6 });
  [-1, 1].forEach(function (s) {
    [[-1.6], [1.6]].forEach(function (o) { var l = cyl(0.18, 0.18, 9.5, red, -26 + s * 6, 4.4, -34 + o[0]); l.rotation.x = o[0] > 0 ? -0.36 : 0.36; });
  });
  cyl(0.2, 0.2, 13, red, -26, 8.7, -34).rotation.z = Math.PI / 2;
  var swings = [];
  [-28.5, -23.5].forEach(function (sx2) {
    var pv = new T.Group(); pv.position.set(sx2, 8.6, -34); scene.add(pv);
    var r1 = cyl(0.04, 0.04, 6.4, steel, -0.6, -3.2, 0, 4, pv), r2 = cyl(0.04, 0.04, 6.4, steel, 0.6, -3.2, 0, 4, pv);
    box(1.6, 0.18, 0.8, M(0x222226), 0, -6.4, 0, pv); swings.push(pv);
  });
  /* shed + bikes + mower */
  box(11, 8, 9, M(0x7a5c45), 24, 4, -52); prism(12, 3.4, 10, M(0x2d2a28), 24, 8, -52, Math.PI / 2);
  box(3.4, 6, 0.2, M(0x4a372a), 24, 3, -47.4);
  var tire = M(0x111113);
  [[15, -50], [17.6, -48.6]].forEach(function (b) {
    [-1.1, 1.1].forEach(function (o) { var w = new T.Mesh(new T.TorusGeometry(0.85, 0.14, 8, 18), tire); w.position.set(b[0] + o, 0.95, b[1]); w.castShadow = BIG; scene.add(w); });
    box(2.2, 0.12, 0.12, M(0x2e7dd6, { metalness: .4 }), b[0], 1.5, b[1]);
  });
  box(2, 1.2, 1.6, M(0xc2402e), 29.5, 0.6, -46);
  /* BBQ */
  box(2.6, 2.6, 1.6, M(0x222226, { metalness: .4, roughness: .4 }), 2, 1.3, 18);
  /* trees */
  var tree = function (x, z, s) {
    cyl(0.6 * s, 0.8 * s, 7 * s, M(0x4a3526), x, 3.5 * s, z);
    var fol = M(0x2f5a2a, { flatShading: true, roughness: 1 });
    [[0, 9, 0, 5], [2.4, 8, 1.4, 3.8], [-2.2, 8.4, -1.2, 3.6], [0.4, 11.6, -0.6, 3.4]].forEach(function (f) {
      var m = new T.Mesh(new T.IcosahedronGeometry(f[3] * s, 0), fol); m.position.set(x + f[0] * s, f[1] * s, z + f[2] * s); m.castShadow = BIG; scene.add(m);
    });
  };
  tree(-29, -54, 1.2); tree(6, -52, 1); tree(-38, 64, 1.1); tree(38, 72, 0.9); tree(-90, -60, 1.3); tree(95, -55, 1.2); tree(60, -165, 1.6); tree(-120, 20, 1.5);
  /* dog: walks a small loop on the lawn */
  var dog = new T.Group(); var fur = M(0x8a5a2b);
  box(2.4, 1, 0.9, fur, 0, 1.4, 0, dog); box(0.9, 0.9, 0.8, fur, 1.4, 2, 0, dog); box(0.5, 0.3, 0.5, M(0x3a2414), 1.95, 1.9, 0, dog);
  [[-0.9, -.3], [-0.9, .3], [0.9, -.3], [0.9, .3]].forEach(function (l) { box(0.25, 0.9, 0.25, fur, l[0], 0.45, l[1], dog); });
  var tail = box(0.9, 0.18, 0.18, fur, -1.5, 1.9, 0, dog); tail.rotation.z = 0.6;
  scene.add(dog);
  /* string lights over the patio: house wall to two poles */
  cyl(0.15, 0.15, 10, M(0x2a2a2c), -19, 5, 5); cyl(0.15, 0.15, 10, M(0x2a2a2c), 5, 5, 5);
  var bulbMat = new T.MeshBasicMaterial({ color: 0x3a2a12 });
  var bulbs = [];
  var strand = function (a, b, sag) {
    for (var i = 0; i <= 14; i++) {
      var t = i / 14, x = lerp(a[0], b[0], t), y = lerp(a[1], b[1], t) - Math.sin(t * Math.PI) * sag, z = lerp(a[2], b[2], t);
      var m = new T.Mesh(new T.SphereGeometry(0.22, 8, 6), bulbMat); m.position.set(x, y, z); scene.add(m); bulbs.push(m);
    }
  };
  strand([-19, 9.6, 19.8], [5, 9.6, 5], 1.6); strand([5, 9.6, 19.8], [-19, 9.6, 5], 1.6); strand([-19, 9.6, 5], [5, 9.6, 5], 1.2);
  var patioGlow = new T.PointLight(0xffb85c, 0, 45); patioGlow.position.set(-7, 8, 12); scene.add(patioGlow);

  /* ---------------- the fence ---------------- */
  var PATH = [[-22, 20], [-35, 20], [-35, -60], [35, -60], [35, 20], [22, 20]];
  var CX = 0, CZ = -20;                                   /* inside of the yard, for "good side out" */
  var GATE_A = 4, GATE_B = 8;                              /* gate opening along the last run, in feet */
  var segs = [], L = 0;
  for (var i = 0; i < PATH.length - 1; i++) {
    var a = PATH[i], b = PATH[i + 1], dx = b[0] - a[0], dz = b[1] - a[1], len = Math.hypot(dx, dz);
    var ux = dx / len, uz = dz / len, nx = -uz, nz = ux;
    var mx = (a[0] + b[0]) / 2, mz = (a[1] + b[1]) / 2;
    if ((mx + nx - CX) * (mx + nx - CX) + (mz + nz - CZ) * (mz + nz - CZ) < (mx - CX) * (mx - CX) + (mz - CZ) * (mz - CZ)) { nx = -nx; nz = -nz; }
    segs.push({ a: a, b: b, len: len, ux: ux, uz: uz, nx: nx, nz: nz, d0: L, ang: Math.atan2(-uz, ux) });
    L += len;
  }
  var last = segs.length - 1;
  var at = function (s, t) { return [s.a[0] + s.ux * t, s.a[1] + s.uz * t]; };
  var posts = [], rails = [], pickets = [];
  segs.forEach(function (s, si) {
    var stops = [];
    if (si === last) stops = [0, GATE_A, GATE_B, s.len];
    else { var n = Math.ceil(s.len / 8); for (var k = 0; k <= n; k++) stops.push(s.len * k / n); }
    stops.forEach(function (t, k) {
      if (k === 0 && si > 0) return;
      var p = at(s, t); posts.push({ x: p[0], z: p[1], d: s.d0 + t });
    });
    for (var k2 = 0; k2 < stops.length - 1; k2++) {
      var t0 = stops[k2], t1 = stops[k2 + 1];
      if (si === last && t0 === GATE_A) continue;
      [1.2, 5.0].forEach(function (yy) { rails.push({ s: s, t0: t0, t1: t1, y: yy }); });
    }
    for (var t = 0.25; t < s.len; t += 0.5) {
      if (si === last && t > GATE_A - 0.1 && t < GATE_B + 0.1) continue;
      var pp = at(s, t); pickets.push({ x: pp[0] + s.nx * 0.42, z: pp[1] + s.nz * 0.42, d: s.d0 + t, ang: s.ang, tone: rnd() });
    }
  });
  var cedar = M(0xb07446, { roughness: .8 }), postMat = M(0x8a5a35, { roughness: .85 });
  var geoPost = new T.BoxGeometry(0.62, 7.4, 0.62); geoPost.translate(0, 3.2, 0);
  var geoCap = new T.ConeGeometry(0.62, 0.55, 4); geoCap.rotateY(Math.PI / 4); geoCap.translate(0, 7.2, 0);
  var geoRail = new T.BoxGeometry(1, 0.38, 0.22);
  var geoPk = new T.BoxGeometry(0.47, 6.1, 0.1); geoPk.translate(0, 3.25, 0);
  var iPost = new T.InstancedMesh(geoPost, postMat, posts.length);
  var iCap = new T.InstancedMesh(geoCap, M(0x6e4628), posts.length);
  var iRail = new T.InstancedMesh(geoRail, M(0x7d5232), rails.length);
  var iPk = new T.InstancedMesh(geoPk, cedar, pickets.length);
  var lampMat = new T.MeshBasicMaterial({ color: 0x2a1f12 });
  var iLamp = new T.InstancedMesh(new T.SphereGeometry(0.22, 8, 6), lampMat, posts.length);
  [iPost, iCap, iRail, iPk].forEach(function (m) { m.castShadow = BIG; m.receiveShadow = BIG; m.instanceMatrix.setUsage(T.DynamicDrawUsage); scene.add(m); });
  scene.add(iLamp);
  var col = new T.Color();
  pickets.forEach(function (pk, i) { col.setHSL(0.07 + pk.tone * 0.015, 0.45, 0.42 + pk.tone * 0.09); iPk.setColorAt(i, col); });
  iPk.instanceColor.needsUpdate = true;
  var D = new T.Object3D(), HID = new T.Matrix4().makeScale(0, 0, 0);
  /* gate (hinged on the post at GATE_B, swings shut over the opening) */
  var gs = segs[last], hinge = at(gs, GATE_B);
  var gate = new T.Group(); gate.position.set(hinge[0], 0, hinge[1]); gate.rotation.y = gs.ang;
  var gateLeaf = new T.Group(); gate.add(gateLeaf);
  var gw = GATE_B - GATE_A;
  var gz = (Math.sin(gs.ang) * gs.nx + Math.cos(gs.ang) * gs.nz) > 0 ? 0.42 : -0.42;
  for (var gpk = 0; gpk < 8; gpk++) { box(0.47, 6.1, 0.1, cedar, -(gpk + 0.5) * gw / 8, 3.4, gz, gateLeaf); }
  box(gw, 0.38, 0.22, M(0x7d5232), -gw / 2, 1.3, 0.1, gateLeaf); box(gw, 0.38, 0.22, M(0x7d5232), -gw / 2, 5.1, 0.1, gateLeaf);
  var brace = box(Math.hypot(gw, 3.8), 0.34, 0.2, M(0x7d5232), -gw / 2, 3.2, 0.08, gateLeaf); brace.rotation.z = Math.atan2(3.8, gw);
  box(0.25, 0.25, 0.5, steel, -gw + 0.3, 3.8, 0.1, gateLeaf);
  gate.visible = false; scene.add(gate);
  /* string line + stakes along the fence line */
  var linePts = []; segs.forEach(function (s) { for (var t2 = 0; t2 <= s.len; t2 += 1) { var q = at(s, t2); linePts.push(new T.Vector3(q[0], 0.55, q[1])); } });
  var lineGeo = new T.BufferGeometry().setFromPoints(linePts);
  var line = new T.Line(lineGeo, new T.LineBasicMaterial({ color: ACC, transparent: true })); scene.add(line);
  var stakes = PATH.map(function (pt) { var g2 = new T.Group(); g2.position.set(pt[0], 0, pt[1]); box(0.3, 2.2, 0.3, M(0xd8c4a0), 0, 1.1, 0, g2); box(0.05, 0.6, 0.9, new T.MeshBasicMaterial({ color: ACC }), 0, 2, 0.45, g2); scene.add(g2); return g2; });
  /* the build head: a warm light and sparks that follow the crew around the yard */
  var head = new T.PointLight(ACC.getHex(), 0, 34); scene.add(head);
  var NS = 70, sparkPos = new Float32Array(NS * 3), sparkVel = [];
  for (var sp = 0; sp < NS; sp++) sparkVel.push([0, 0, 0, 0]);
  var sparkGeo = new T.BufferGeometry(); sparkGeo.setAttribute("position", new T.BufferAttribute(sparkPos, 3));
  var sparks = new T.Points(sparkGeo, new T.PointsMaterial({ color: ACC, size: 0.5, transparent: true, depthWrite: false, blending: T.AdditiveBlending }));
  scene.add(sparks);
  var pointOnPath = function (dist) {
    dist = Math.max(0, Math.min(L - 0.001, dist));
    for (var k = 0; k < segs.length; k++) { var s = segs[k]; if (dist <= s.d0 + s.len) return at(s, dist - s.d0); }
    return PATH[PATH.length - 1];
  };

  /* ---------------- camera path ---------------- */
  var KEYS = [
    [0.00, [-92, 118, -168], [6, 0, -12]],
    [0.14, [-118, 52, -36], [-24, 0, -8]],
    [0.30, [-98, 34, -108], [-30, 2, -38]],
    [0.44, [-18, 32, -138], [0, 2, -54]],
    [0.58, [78, 34, -116], [30, 2, -40]],
    [0.72, [104, 26, -8], [32, 3, -10]],
    [0.84, [58, 13, 50], [27, 4, 14]],
    [1.00, [-44, 52, -122], [40, 2, -8]]
  ];
  var camAt = function (p) {
    var k = 0; while (k < KEYS.length - 2 && p > KEYS[k + 1][0]) k++;
    var A = KEYS[k], B = KEYS[k + 1], t = ease(seg(p, A[0], B[0]));
    return [[lerp(A[1][0], B[1][0], t), lerp(A[1][1], B[1][1], t), lerp(A[1][2], B[1][2], t)],
            [lerp(A[2][0], B[2][0], t), lerp(A[2][1], B[2][1], t), lerp(A[2][2], B[2][2], t)]];
  };

  /* ---------------- overlay (HUD, messages, tags) ---------------- */
  var stepsTxt = []; try { stepsTxt = JSON.parse(sec.getAttribute("data-steps")); } catch (e) {}
  var hudStep = sec.querySelector(".yard__step"), hudFt = sec.querySelector(".yard__ft b"), meter = sec.querySelector(".yard__meter b");
  var msgs = [].slice.call(sec.querySelectorAll(".ymsg"));
  var MSG_AT = [[0.18, 0.34], [0.36, 0.52], [0.54, 0.70], [0.72, 0.85]];
  var tags = {}; [].slice.call(sec.querySelectorAll(".ytag")).forEach(function (el) { tags[el.getAttribute("data-tag")] = el; });
  var anchors = { family: new T.Vector3(-8, 10, 12), pets: new T.Vector3(), belongings: new T.Vector3(24, 13, -52), privacy: new T.Vector3(17.5, 5, -5) };
  var v3 = new T.Vector3();

  /* ---------------- size, scroll, loop ---------------- */
  var W = 0, H = 0, portrait = false;
  var resize = function () {
    W = canvas.clientWidth; H = canvas.clientHeight; if (!W || !H) return;
    renderer.setSize(W, H, false); cam.aspect = W / H; portrait = cam.aspect < 0.9;
    cam.fov = portrait ? 58 : 42; cam.updateProjectionMatrix();
  };
  window.addEventListener("resize", resize);
  var target = 0, prog = 0, visible = true, running = false, lastStep = -1, lastFt = -1;
  var readScroll = function () {
    var r = sec.getBoundingClientRect(), span = r.height - window.innerHeight;
    target = span > 0 ? clamp(-r.top / span) : 0;
  };
  window.addEventListener("scroll", readScroll, { passive: true });

  var frame = function (now) {
    var time = now / 1000;
    prog += (target - prog) * 0.09; if (Math.abs(target - prog) < 0.0004) prog = target;
    var p = prog;
    sec.style.setProperty("--yp", p.toFixed(4));
    /* camera */
    var c = camAt(p), k = portrait ? 1.38 : 1;
    cam.position.set(c[1][0] + (c[0][0] - c[1][0]) * k, c[1][1] + (c[0][1] - c[1][1]) * k, c[1][2] + (c[0][2] - c[1][2]) * k);
    cam.position.x += Math.sin(time * 0.3) * 0.6; cam.position.y += Math.sin(time * 0.4) * 0.4;
    cam.lookAt(c[1][0], c[1][1], c[1][2]);
    /* string line + stakes */
    var lay = seg(p, 0.06, 0.18);
    lineGeo.setDrawRange(0, Math.floor(linePts.length * lay));
    line.material.opacity = 1 - seg(p, 0.6, 0.8);
    stakes.forEach(function (s, i) { var v = seg(lay, i / stakes.length, i / stakes.length + 0.1); s.scale.setScalar(Math.max(0.001, v)); s.visible = p < 0.82; });
    /* fence build: B = feet built */
    var B = seg(p, 0.16, 0.8) * L;
    posts.forEach(function (o, i) {
      var t = clamp((B + 3 - o.d) / 4);
      if (t <= 0) { iPost.setMatrixAt(i, HID); iCap.setMatrixAt(i, HID); iLamp.setMatrixAt(i, HID); return; }
      D.position.set(o.x, (1 - t) * (1 - t) * 34, o.z); D.rotation.set(0, 0, 0); D.scale.set(1, 1, 1); D.updateMatrix();
      iPost.setMatrixAt(i, D.matrix); iCap.setMatrixAt(i, D.matrix);
      D.position.y += 7.55; D.updateMatrix(); iLamp.setMatrixAt(i, D.matrix);
    });
    rails.forEach(function (r, i) {
      var t = clamp((B - 1 - (r.s.d0 + r.t0)) / (r.t1 - r.t0));
      if (t <= 0) { iRail.setMatrixAt(i, HID); return; }
      var lenNow = (r.t1 - r.t0) * t, q = at(r.s, r.t0 + lenNow / 2);
      D.position.set(q[0] - r.s.nx * 0.05, r.y, q[1] - r.s.nz * 0.05); D.rotation.set(0, r.s.ang, 0); D.scale.set(lenNow, 1, 1); D.updateMatrix();
      iRail.setMatrixAt(i, D.matrix);
    });
    pickets.forEach(function (o, i) {
      var t = clamp((B - 5 - o.d) / 3);
      if (t <= 0) { iPk.setMatrixAt(i, HID); return; }
      D.position.set(o.x, (1 - t) * (1 - t) * 16, o.z); D.rotation.set(0, o.ang, 0); D.scale.set(1, 1, 1); D.updateMatrix();
      iPk.setMatrixAt(i, D.matrix);
    });
    iPost.instanceMatrix.needsUpdate = iCap.instanceMatrix.needsUpdate = iRail.instanceMatrix.needsUpdate = iPk.instanceMatrix.needsUpdate = iLamp.instanceMatrix.needsUpdate = true;
    /* build head light + sparks */
    var building = p > 0.16 && p < 0.8;
    var hp = pointOnPath(B);
    head.position.set(hp[0], 7, hp[1]); head.intensity = building ? 2.4 : Math.max(0, head.intensity - 0.08);
    for (var s2 = 0; s2 < NS; s2++) {
      var v = sparkVel[s2];
      if (v[3] <= 0 && building && rnd() < 0.35) { sparkPos[s2 * 3] = hp[0]; sparkPos[s2 * 3 + 1] = 6.8; sparkPos[s2 * 3 + 2] = hp[1]; v[0] = (rnd() - .5) * .5; v[1] = .2 + rnd() * .35; v[2] = (rnd() - .5) * .5; v[3] = 30 + rnd() * 25; }
      if (v[3] > 0) { sparkPos[s2 * 3] += v[0]; sparkPos[s2 * 3 + 1] += v[1]; sparkPos[s2 * 3 + 2] += v[2]; v[1] -= 0.02; v[3]--; if (sparkPos[s2 * 3 + 1] < 0.2) v[3] = 0; }
      else sparkPos[s2 * 3 + 1] = -50;
    }
    sparkGeo.attributes.position.needsUpdate = true;
    /* gate swings shut and latches */
    gate.visible = p > 0.74;
    var gt = seg(p, 0.8, 0.88);
    gateLeaf.rotation.y = -1.75 * (1 - ease(gt)) + (gt >= 1 ? 0 : Math.sin(gt * Math.PI) * 0.0);
    /* dusk: sky, sun, lights */
    var dusk = seg(p, 0.55, 0.95);
    skyU.top.value.setRGB(lerp(0.13, 0.03, dusk), lerp(0.2, 0.04, dusk), lerp(0.31, 0.1, dusk));
    skyU.mid.value.setRGB(lerp(0.85, 0.55, dusk), lerp(0.64, 0.25, dusk), lerp(0.42, 0.18, dusk));
    skyU.bot.value.setRGB(lerp(0.95, 0.35, dusk), lerp(0.79, 0.18, dusk), lerp(0.56, 0.12, dusk));
    scene.fog.color.copy(skyU.mid.value);
    sun.intensity = lerp(1.5, 0.3, dusk); sun.color.setRGB(1, lerp(0.82, 0.55, dusk), lerp(0.6, 0.35, dusk));
    sun.position.set(-90, lerp(110, 40, dusk), -70);
    hemi.intensity = lerp(0.75, 0.32, dusk);
    var lightsOn = seg(p, 0.84, 0.95);
    windowMats.forEach(function (m, i) { m.emissiveIntensity = lerp(0.05, i === 0 || i === 1 ? 1.6 : 0.7, seg(p, 0.6, 0.9)); });
    bulbMat.color.setRGB(lerp(0.23, 1, lightsOn), lerp(0.16, 0.78, lightsOn), lerp(0.07, 0.42, lightsOn));
    patioGlow.intensity = lightsOn * 1.8;
    poolLight.intensity = lightsOn * 1.6; waterMat.emissiveIntensity = 0.15 + lightsOn * 0.9 + Math.sin(time * 2) * 0.05;
    var capOn = seg(p, 0.88, 0.96);
    lampMat.color.setRGB(lerp(0.16, 1, capOn), lerp(0.12, 0.72, capOn), lerp(0.07, 0.3, capOn));
    renderer.toneMappingExposure = lerp(0.95, 1.2, dusk);
    /* life in the yard */
    var da = time * 0.35; dog.position.set(4 + Math.cos(da) * 7, 0, -22 + Math.sin(da) * 5); dog.rotation.y = -da - Math.PI / 2;
    tail.rotation.y = Math.sin(time * 12) * 0.5;
    swings.forEach(function (sw, i) { sw.rotation.x = Math.sin(time * 1.6 + i * 1.7) * 0.45; });
    kid1.position.y = Math.abs(Math.sin(time * 3)) * 0.6; kid2.position.x = -20 + Math.sin(time * 0.8) * 2;
    /* overlay */
    var step = p < 0.16 ? 0 : p < 0.5 ? 1 : p < 0.8 ? 2 : p < 0.88 ? 3 : 4;
    if (step !== lastStep && hudStep && stepsTxt[step]) { hudStep.textContent = stepsTxt[step]; lastStep = step; }
    var ft = Math.round(Math.min(L, B + (gt >= 1 ? GATE_B - GATE_A : 0)));
    if (ft !== lastFt && hudFt) { hudFt.textContent = String(ft).padStart(3, "0"); lastFt = ft; }
    if (meter) meter.style.transform = "scaleX(" + seg(p, 0.06, 0.88).toFixed(4) + ")";
    msgs.forEach(function (m, i) {
      var r = i < MSG_AT.length ? MSG_AT[i] : [0.9, 1.01];
      m.classList.toggle("is-on", p >= r[0] && p < r[1]);
    });
    var safe = p > 0.875;
    sec.classList.toggle("is-built", safe);
    sec.classList.toggle("is-end", p > 0.9);
    sec.classList.toggle("is-start", p < 0.1);
    anchors.pets.set(dog.position.x, 4.5, dog.position.z);
    Object.keys(tags).forEach(function (key) {
      var el = tags[key]; v3.copy(anchors[key]).project(cam);
      var vis = v3.z < 1 && Math.abs(v3.x) < 1.05 && Math.abs(v3.y) < 1.05 && p > 0.8 && p < 0.99;
      el.classList.toggle("is-vis", vis);
      el.classList.toggle("is-safe", safe);
      if (vis) el.style.transform = "translate3d(" + ((v3.x * 0.5 + 0.5) * W).toFixed(1) + "px," + ((-v3.y * 0.5 + 0.5) * H).toFixed(1) + "px,0)";
    });
    renderer.render(scene, cam);
  };
  var loop = function (now) { if (!running) return; frame(now); requestAnimationFrame(loop); };
  var setRun = function (on) {
    if (on && !running && visible && !document.hidden) { running = true; requestAnimationFrame(loop); }
    else if (!on) running = false;
  };
  if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible); }).observe(sec);
  document.addEventListener("visibilitychange", function () { setRun(!document.hidden); });
  /* for automated checks: jump straight to a point in the scene (QA screenshots) */
  window.__yardSeek = function (v) { target = prog = clamp(v); frame(performance.now()); };
  resize(); readScroll(); prog = target;
  frame(performance.now());
  doc.classList.add("yard-live");
  setRun(true);
})();
