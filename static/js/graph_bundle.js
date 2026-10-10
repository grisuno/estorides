/* Estorides Bundles — circle 2D + sphere 3D hierarchical edge bundling.
 *
 * Port of ReadMenator `graph-bundle.html` (Holten 2006 hierarchical edge
 * bundling; leaves on a community-grouped ring in 2D, on community caps of
 * a Fibonacci sphere projected through a small perspective camera in 3D;
 * every edge re-routed live through the cluster tree as a B-spline whose
 * strength (beta) the operator adjusts). Adapted to OSINT: files→entities,
 * imports→relations, layers→intel levels, languages→entity kinds.
 *
 * Self-contained canvas, zero CDN, zero WebGL: works offline. Remote labels
 * never touch innerHTML (mk() uses textContent; canvas fillText cannot
 * interpret HTML). Dynamic colours go through CSSOM (el.style.*), never
 * through style="..." markup, per spec/csp_safe_styles.md.
 *
 * Key handling is scoped to the Bundles sidebar tab: this script loads
 * BEFORE graph_force.js so its document-level listener runs first and
 * stops handled keys (2/3/c/x/r/[/]/slash) from also driving the Graph
 * view. Escape is left to propagate so both views clear together.
 */
(function () {
'use strict';

var TAB_ID = 'bundles-canvas';
var $ = function (id) { return document.getElementById(id); };

var TIER_COLORS = {
  data: '#6b7280',
  information: '#5fb4ff',
  intelligence: '#f6bd16',
  counter_intelligence: '#ff5c5c'
};

function djb2KindColor(name) {
  var h = 5381, i, sat, light, hue;
  name = String(name || 'unknown');
  for (i = 0; i < name.length; i++) {
    h = ((h << 5) + h + name.charCodeAt(i)) >>> 0;
  }
  hue = h % 360;
  sat = 55 + ((h >> 8) % 12);
  light = 58 + ((h >> 16) % 10);
  return 'hsl(' + hue + ', ' + sat + '%, ' + light + '%)';
}

var NODES = [], GROUPS = [], EDGES = [];
var CFG = null;
var OUT = [], INN = [], byId = {}, groupByKey = {}, maxRank = 1e-9, byRank = [], topSet = new Set();
var C2 = [], C3 = [], INK = null, proj = null, labelMargin = 40, INSIDE = 0;
var SCREEN = [], PLACED = [];
var canvas = null, ctx = null, stage = null, loaded = false, loadFailed = false;

var reduceMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
var S = {
  view: '2d', beta: 0.85, color: 'community', dir: 'both', cross: false,
  rotate: !reduceMotion, focus: -1, group: -1, key: null, hover: -1,
  hoverGroup: -1, yaw: 0.7, pitch: -0.32, zoom: 1, panX: 0, panY: 0,
  reveal: reduceMotion ? 1 : 0, revealStart: 0, w: 0, h: 0, dpr: 1
};
var aim = null, drag = null, last = 0;

function mk(tag, cls, text) {
  var el = document.createElement(tag);
  if (cls) el.className = cls;
  if (text !== undefined && text !== null) el.textContent = String(text);
  return el;
}
function clip(text, max) {
  text = String(text || '');
  return text.length > max ? text.slice(0, Math.max(1, max - 1)) + '…' : text;
}
function tabActive() {
  var t = $(TAB_ID);
  return !!(t && t.classList.contains('active'));
}
function ink() {
  if (!INK) {
    var cs = getComputedStyle(document.documentElement);
    var v = function (k) { return cs.getPropertyValue(k).trim(); };
    INK = {
      accent: v('--gb-accent') || '#22d3ee', accent2: v('--gb-accent2') || '#f472b6',
      ink: v('--gb-ink') || '#f8fafc', muted: v('--gb-muted') || '#94a3b8',
      faint: v('--gb-faint') || '#475569', labelBg: v('--gb-label-bg') || 'rgba(2,6,23,.80)',
      labelInk: v('--gb-label-ink') || '#e2e8f0', sphere: v('--gb-sphere') || 'rgba(148,163,184,.10)',
      light: document.documentElement.getAttribute('data-theme') === 'light'
    };
  }
  return INK;
}
function colorOf(i) {
  var n = NODES[i];
  if (S.color === 'layer') return TIER_COLORS[n.ly] || n.c;
  if (S.color === 'kind') return djb2KindColor(n.lg);
  return n.c;
}
function keyOf(i) {
  var n = NODES[i];
  return S.color === 'layer' ? n.ly : S.color === 'kind' ? n.lg : String(n.g);
}

function bspline(ctrl, samples, dims) {
  var out = [], d, k, s, t, t2, t3, b0, b1, b2, b3, p0, p1, p2, p3;
  if (ctrl.length < 3) {
    var a = ctrl[0], b = ctrl[ctrl.length - 1];
    for (k = 0; k <= samples; k++) for (d = 0; d < dims; d++) out.push(a[d] + (b[d] - a[d]) * k / samples);
    return out;
  }
  var pts = [ctrl[0], ctrl[0]].concat(ctrl, [ctrl[ctrl.length - 1], ctrl[ctrl.length - 1]]);
  var segs = pts.length - 3, per = Math.max(2, Math.floor(samples / Math.max(1, segs)));
  for (s = 0; s < segs; s++) {
    p0 = pts[s]; p1 = pts[s + 1]; p2 = pts[s + 2]; p3 = pts[s + 3];
    var extra = s === segs - 1 ? 1 : 0;
    for (k = 0; k < per + extra; k++) {
      t = k / per; t2 = t * t; t3 = t2 * t;
      b0 = (1 - t) * (1 - t) * (1 - t) / 6; b1 = (3 * t3 - 6 * t2 + 4) / 6;
      b2 = (-3 * t3 + 3 * t2 + 3 * t + 1) / 6; b3 = t3 / 6;
      for (d = 0; d < dims; d++) out.push(b0 * p0[d] + b1 * p1[d] + b2 * p2[d] + b3 * p3[d]);
    }
  }
  return out;
}
function curve(la, lb, ga, gb, hub, root, dims) {
  var ctrl, d;
  if (ga === gb) {
    var h = hub(ga), inner = [];
    for (d = 0; d < dims; d++) inner.push((h[d] + la[d] + lb[d]) / 3);
    ctrl = [la, inner, lb];
  } else {
    ctrl = [la, hub(ga), root, hub(gb), lb];
  }
  var m = ctrl.length - 1, beta = Math.max(0, Math.min(1, S.beta));
  var st = ctrl.map(function (p, jj) {
    var q = [];
    for (var dd = 0; dd < dims; dd++) q.push(beta * p[dd] + (1 - beta) * (la[dd] + jj / m * (lb[dd] - la[dd])));
    return q;
  });
  return new Float32Array(bspline(st, CFG.samples, dims));
}
function buildCurves() {
  C2 = EDGES.map(function (e) {
    var a = NODES[e[0]], b = NODES[e[1]];
    return curve([Math.cos(a.a), Math.sin(a.a)], [Math.cos(b.a), Math.sin(b.a)], a.g, b.g, function (g) { return GROUPS[g].h2; }, [0, 0], 2);
  });
  C3 = EDGES.map(function (e) {
    var a = NODES[e[0]], b = NODES[e[1]];
    return curve(a.p, b.p, a.g, b.g, function (g) { return GROUPS[g].h3; }, [0, 0, 0], 3);
  });
}

function resize() {
  if (!stage) return;
  var r = stage.getBoundingClientRect();
  S.dpr = window.devicePixelRatio || 1;
  S.w = Math.max(1, r.width); S.h = Math.max(1, r.height);
  canvas.width = Math.round(S.w * S.dpr); canvas.height = Math.round(S.h * S.dpr);
  ctx.font = '11px ui-monospace,Menlo,Consolas,monospace';
  var showAll = NODES.length <= CFG.labelAllMax, widest = 0;
  if (showAll) NODES.forEach(function (n) { widest = Math.max(widest, ctx.measureText(clip(n.l, CFG.labelMax)).width); });
  labelMargin = showAll ? Math.min(widest + 34, Math.min(S.w, S.h) * 0.26) : 46;
  draw();
}
function radius() {
  var fit = S.view === '2d' ? 1 : Math.max(0.2, (CFG.perspective - 1) / CFG.perspective);
  return Math.max(40, (Math.min(S.w, S.h) / 2 - (S.view === '2d' ? labelMargin : 28)) * fit) * S.zoom;
}
function center() { return [S.w / 2 + S.panX, S.h / 2 + S.panY]; }
function makeProjector() {
  var c = center(), cx = c[0], cy = c[1], R = radius();
  if (S.view === '2d') return function (x, y) { return [cx + x * R, cy + y * R, 0, 1]; };
  var cyw = Math.cos(S.yaw), syw = Math.sin(S.yaw), cp = Math.cos(S.pitch), sp = Math.sin(S.pitch), f = CFG.perspective;
  return function (x, y, z) {
    var x1 = x * cyw + z * syw, z1 = -x * syw + z * cyw;
    var y2 = y * cp - z1 * sp, z2 = y * sp + z1 * cp, s = f / (f + z2);
    return [cx + x1 * R * s, cy + y2 * R * s, z2, s];
  };
}
function depthAlpha(z) { return S.view === '3d' ? 1 - CFG.depthFade * (z + 1) / 2 : 1; }

function focusState() {
  var f = S.focus >= 0 ? S.focus : S.hover;
  if (f >= 0) return { node: f };
  var g = S.group >= 0 ? S.group : S.hoverGroup;
  if (g >= 0) return { group: g };
  if (S.key !== null) return { key: S.key };
  return null;
}
function edgeState(k, fs) {
  var e = EDGES[k], a = NODES[e[0]], b = NODES[e[1]];
  if (S.cross && a.g === b.g) return 0;
  if (!fs) return 2;
  if (fs.node !== undefined && fs.node !== null) {
    if (e[0] === fs.node && S.dir !== 'in') return 3;
    if (e[1] === fs.node && S.dir !== 'out') return 4;
    return 1;
  }
  if (fs.group !== undefined && fs.group !== null) {
    var sa = a.g === fs.group, sb = b.g === fs.group;
    if (sa && sb) return S.dir === 'both' ? 5 : 1;
    if (sa && S.dir !== 'in') return 3;
    if (sb && S.dir !== 'out') return 4;
    return 1;
  }
  var ka = keyOf(e[0]) === fs.key, kb = keyOf(e[1]) === fs.key;
  if ((ka && S.dir !== 'in') || (kb && S.dir !== 'out')) return 5;
  return 1;
}
function nodeLit(i, fs) {
  if (!fs) return true;
  if (fs.node !== undefined && fs.node !== null) {
    if (i === fs.node) return true;
    return OUT[fs.node].some(function (k) { return EDGES[k][1] === i; }) ||
           INN[fs.node].some(function (k) { return EDGES[k][0] === i; });
  }
  if (fs.group !== undefined && fs.group !== null) return NODES[i].g === fs.group;
  return keyOf(i) === fs.key;
}

function strokeCurve(pts, dims, prefix) {
  var n = pts.length / dims, stop = Math.max(2, Math.ceil(n * prefix)), j, p, zs;
  p = proj(pts[0], pts[1], dims === 3 ? pts[2] : 0);
  ctx.moveTo(p[0], p[1]); zs = p[2];
  for (j = 1; j < stop; j++) {
    p = proj(pts[j * dims], pts[j * dims + 1], dims === 3 ? pts[j * dims + 2] : 0);
    ctx.lineTo(p[0], p[1]); zs += p[2];
  }
  return zs / stop;
}
function pointOn(pts, dims, t) {
  var n = pts.length / dims, f = t * (n - 1), j = Math.min(n - 2, Math.floor(f)), u = f - j;
  function g(d) { return pts[j * dims + d] + (pts[(j + 1) * dims + d] - pts[j * dims + d]) * u; }
  return proj(g(0), g(1), dims === 3 ? g(2) : 0);
}
function draw(now) {
  if (!S.w || !CFG || !loaded) return;
  var K = ink(), fs = focusState(), dims = S.view === '3d' ? 3 : 2;
  var curves = dims === 3 ? C3 : C2, k, st, z, a;
  proj = makeProjector();
  ctx.setTransform(S.dpr, 0, 0, S.dpr, 0, 0);
  ctx.clearRect(0, 0, S.w, S.h);
  var c = center(), cx = c[0], cy = c[1], R = radius(), s, lat, t, cc, p;
  if (dims === 3) {
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.fillStyle = K.sphere; ctx.globalAlpha = 0.35; ctx.fill(); ctx.globalAlpha = 1;
    ctx.strokeStyle = K.sphere; ctx.lineWidth = 1;
    for (lat = -60; lat <= 60; lat += 30) {
      ctx.beginPath();
      for (s = 0; s <= 48; s++) {
        t = s / 48 * Math.PI * 2; cc = Math.cos(lat * Math.PI / 180);
        p = proj(cc * Math.cos(t), Math.sin(lat * Math.PI / 180), cc * Math.sin(t));
        if (s) ctx.lineTo(p[0], p[1]); else ctx.moveTo(p[0], p[1]);
      }
      ctx.stroke();
    }
  }
  var prefix = S.reveal, order = [];
  for (k = 0; k < EDGES.length; k++) { st = edgeState(k, fs); if (st) order.push([k, st]); }
  var blend = !K.light;
  ctx.lineCap = 'round';
  var dimA = CFG.dimAlpha, baseA = CFG.edgeAlpha;
  if (blend) ctx.globalCompositeOperation = 'lighter';
  for (var o = 0; o < order.length; o++) {
    if (order[o][1] > 2) continue;
    ctx.beginPath(); z = strokeCurve(curves[order[o][0]], dims, prefix);
    a = (order[o][1] === 1 ? dimA : baseA * (fs ? 1 : Math.min(1, 0.55 + 60 / Math.max(60, EDGES.length)))) * depthAlpha(z);
    ctx.strokeStyle = colorOf(EDGES[order[o][0]][0]);
    ctx.globalAlpha = Math.max(0.01, a); ctx.lineWidth = 1; ctx.stroke();
  }
  var lit = order.filter(function (x) { return x[1] > 2; });
  for (var l = 0; l < lit.length; l++) {
    ctx.beginPath(); z = strokeCurve(curves[lit[l][0]], dims, prefix);
    ctx.strokeStyle = lit[l][1] === 3 ? K.accent : lit[l][1] === 4 ? K.accent2 : colorOf(EDGES[lit[l][0]][0]);
    ctx.globalAlpha = Math.min(1, 0.85 * depthAlpha(z) + 0.15);
    ctx.lineWidth = lit[l][1] === 5 ? 1.3 : 1.8; ctx.stroke();
  }
  if (fs && !reduceMotion && CFG.particles > 0 && S.reveal >= 1) {
    var t0 = (now || 0) / 1000;
    ctx.fillStyle = K.light ? K.ink : '#ffffff';
    lit.slice(0, 400).forEach(function (pair) {
      for (var pp = 0; pp < CFG.particles; pp++) {
        var tt = ((t0 * 0.35) + pp / CFG.particles + ((pair[0] * 0.6180339) % 1)) % 1;
        var q = pointOn(curves[pair[0]], dims, tt);
        ctx.globalAlpha = 0.85 * depthAlpha(q[2]);
        ctx.beginPath(); ctx.arc(q[0], q[1], 1.8, 0, Math.PI * 2); ctx.fill();
      }
    });
  }
  ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
  drawGroups(K, fs, cx, cy, R);
  drawNodes(K, fs);
  drawLabels(K, fs, cx, cy, R);
  drawHud(order.length);
}
function drawGroups(K, fs, cx, cy, R) {
  var i, g;
  if (S.view === '2d') {
    GROUPS.forEach(function (gg, ii) {
      var lit = !fs || fs.group === ii || (fs.node !== undefined && fs.node !== null && NODES[fs.node].g === ii) || fs.key !== undefined && fs.key !== null;
      ctx.beginPath(); ctx.arc(cx, cy, R + 7, gg.a0, gg.a1);
      ctx.strokeStyle = gg.c; ctx.globalAlpha = lit ? 0.95 : 0.3;
      ctx.lineWidth = (S.hoverGroup === ii || S.group === ii) ? 7 : 4; ctx.stroke();
    });
    ctx.globalAlpha = 1;
    if (NODES.length > CFG.labelAllMax) {
      ctx.font = '600 11px ui-monospace,Menlo,Consolas,monospace';
      GROUPS.forEach(function (gg, ii) {
        if (gg.n < 2 && S.group !== ii) return;
        var mid = (gg.a0 + gg.a1) / 2, x = cx + (R + 20) * Math.cos(mid), y = cy + (R + 20) * Math.sin(mid);
        ctx.textAlign = Math.cos(mid) >= 0 ? 'left' : 'right'; ctx.textBaseline = 'middle';
        ctx.fillStyle = gg.c; ctx.globalAlpha = (!fs || fs.group === ii) ? 0.95 : 0.4;
        ctx.fillText(clip(gg.l, 22) + ' (' + gg.n + ')', x, y);
      });
      ctx.globalAlpha = 1;
    }
    return;
  }
  ctx.font = '600 11px ui-monospace,Menlo,Consolas,monospace';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  PLACED = [];
  GROUPS.forEach(function (gg, ii) {
    var p = proj(gg.u[0] * 1.08, gg.u[1] * 1.08, gg.u[2] * 1.08);
    if (p[2] > 0.25) return;
    if (gg.n < 2 && S.group !== ii) return;
    var lit = !fs || fs.group === ii;
    var text = clip(gg.l, 22), w = ctx.measureText(text).width + 12;
    var box = [p[0] - w / 2, p[1] - 9, p[0] + w / 2, p[1] + 9];
    if (PLACED.some(function (b) { return !(box[2] < b[0] || b[2] < box[0] || box[3] < b[1] || b[3] < box[1]); })) return;
    PLACED.push(box);
    ctx.globalAlpha = (lit ? 0.95 : 0.35) * depthAlpha(p[2]);
    ctx.fillStyle = K.labelBg; ctx.fillRect(p[0] - w / 2, p[1] - 9, w, 18);
    ctx.strokeStyle = gg.c; ctx.lineWidth = 1; ctx.strokeRect(p[0] - w / 2, p[1] - 9, w, 18);
    ctx.fillStyle = gg.c; ctx.fillText(text, p[0], p[1]);
  });
  ctx.globalAlpha = 1;
}
function nodeRadius(i) {
  return (CFG.nodeMin + (CFG.nodeMax - CFG.nodeMin) * Math.sqrt((NODES[i].r || 0) / maxRank)) *
    (S.view === '3d' ? 1 : Math.min(1.6, Math.sqrt(S.zoom)));
}
function screenNodes() {
  return NODES.map(function (n, i) {
    var p = S.view === '3d' ? proj(n.p[0], n.p[1], n.p[2]) : proj(Math.cos(n.a), Math.sin(n.a), 0);
    return { i: i, x: p[0], y: p[1], z: p[2], s: p[3], r: nodeRadius(i) * (S.view === '3d' ? p[3] : 1) };
  });
}
function drawNodes(K, fs) {
  SCREEN = screenNodes();
  var order = SCREEN.slice().sort(function (a, b) { return b.z - a.z; });
  for (var o = 0; o < order.length; o++) {
    var q = order[o], lit = nodeLit(q.i, fs);
    ctx.globalAlpha = (lit ? 1 : 0.22) * depthAlpha(q.z);
    ctx.beginPath(); ctx.arc(q.x, q.y, q.r, 0, Math.PI * 2);
    ctx.fillStyle = colorOf(q.i); ctx.fill();
    if (q.i === S.focus || q.i === S.hover) { ctx.lineWidth = 2; ctx.strokeStyle = K.ink; ctx.stroke(); }
  }
  ctx.globalAlpha = 1;
}
function labelSet(fs) {
  var set = new Set();
  if (NODES.length <= CFG.labelAllMax && S.view === '2d') { NODES.forEach(function (n, i) { set.add(i); }); return set; }
  topSet.forEach(function (i) { set.add(i); });
  if (fs && fs.node !== undefined && fs.node !== null) {
    set.add(fs.node);
    OUT[fs.node].forEach(function (k) { set.add(EDGES[k][1]); });
    INN[fs.node].forEach(function (k) { set.add(EDGES[k][0]); });
  }
  if (S.hover >= 0) set.add(S.hover);
  return set;
}
function drawLabels(K, fs, cx, cy, R) {
  var set = labelSet(fs);
  ctx.font = '11px ui-monospace,Menlo,Consolas,monospace'; ctx.textBaseline = 'middle';
  if (S.view === '2d') {
    set.forEach(function (i) {
      var n = NODES[i], a = n.a, flip = Math.cos(a) < 0, lit = nodeLit(i, fs);
      ctx.save();
      ctx.translate(cx + (R + 16) * Math.cos(a), cy + (R + 16) * Math.sin(a));
      ctx.rotate(flip ? a + Math.PI : a);
      ctx.textAlign = flip ? 'right' : 'left';
      ctx.globalAlpha = lit ? (i === S.focus || i === S.hover ? 1 : 0.85) : 0.25;
      ctx.fillStyle = (i === S.focus || i === S.hover) ? K.ink : (lit && fs ? colorOf(i) : K.labelInk);
      ctx.fillText(clip(n.l, CFG.labelMax), 0, 0);
      ctx.restore();
    });
    ctx.globalAlpha = 1; return;
  }
  var placed = PLACED.slice(), items = [];
  set.forEach(function (i) {
    var q = SCREEN[i];
    if (q.z > 0.35 && i !== S.focus && i !== S.hover) return;
    items.push(q);
  });
  items.sort(function (a, b) { return ((b.i === S.focus) - (a.i === S.focus)) || (NODES[b.i].r - NODES[a.i].r); });
  for (var o = 0; o < items.length; o++) {
    var q = items[o], text = clip(NODES[q.i].l, CFG.labelMax);
    var w = ctx.measureText(text).width + 10, x = q.x + q.r + 4, y = q.y;
    var box = [x, y - 8, x + w, y + 8];
    if (placed.some(function (b) { return !(box[2] < b[0] || b[2] < box[0] || box[3] < b[1] || b[3] < box[1]); })) continue;
    placed.push(box);
    var lit = nodeLit(q.i, fs);
    ctx.globalAlpha = (lit ? 0.95 : 0.35) * depthAlpha(q.z);
    ctx.fillStyle = K.labelBg; ctx.fillRect(box[0], box[1], w, 16);
    ctx.fillStyle = (q.i === S.focus || q.i === S.hover) ? K.ink : K.labelInk;
    ctx.textAlign = 'left'; ctx.fillText(text, x + 5, y);
  }
  ctx.globalAlpha = 1;
}
function drawHud(visible) {
  var hud = $('gb-hud');
  if (!hud) return;
  hud.textContent = '';
  var inside = INSIDE;
  function add(label, value) {
    var s = mk('span'); s.append(mk('b', null, value), ' ' + label); hud.append(s);
  }
  add('entities', NODES.length); add('relations', EDGES.length);
  add('clusters', GROUPS.filter(function (g) { return g.k !== CFG.unassignedKey; }).length);
  add('inside', inside); add('crossing', EDGES.length - inside);
  if (visible !== EDGES.length) add('shown', visible);
  hud.append(mk('span', null, S.view === '3d' ? 'drag rotates, wheel zooms' : 'drag pans, wheel zooms, click an entity or arc'));
}

function hitNode(x, y) {
  var best = -1, bd = Infinity;
  for (var o = 0; o < SCREEN.length; o++) {
    var q = SCREEN[o], d = Math.hypot(q.x - x, q.y - y) - q.r, lim = Math.max(CFG.hitPx, q.r);
    if (d < lim) {
      var score = d + (S.view === '3d' ? q.z * 20 : 0);
      if (score < bd) { bd = score; best = q.i; }
    }
  }
  if (best < 0 && S.view === '2d') {
    var c = center(), cx = c[0], cy = c[1], R = radius(), r = Math.hypot(x - cx, y - cy);
    if (r > R && r < R + labelMargin) {
      var ang = Math.atan2(y - cy, x - cx), bestA = Infinity;
      NODES.forEach(function (n, i) {
        var dd = Math.abs(Math.atan2(Math.sin(ang - n.a), Math.cos(ang - n.a)));
        if (dd < bestA) { bestA = dd; best = i; }
      });
      var step = Math.PI * 2 / Math.max(1, NODES.length);
      if (bestA > Math.max(step, 0.02) || r < R + 12) best = -1;
    }
  }
  return best;
}
function hitGroup(x, y) {
  if (S.view === '2d') {
    var c = center(), cx = c[0], cy = c[1], R = radius(), r = Math.hypot(x - cx, y - cy);
    if (r < R + 2 || r > R + 13) return -1;
    var ang = Math.atan2(y - cy, x - cx);
    if (ang < -Math.PI / 2) ang += Math.PI * 2;
    return GROUPS.findIndex(function (gg) { return ang >= gg.a0 && ang <= gg.a1; });
  }
  var best = -1, bd = 24;
  GROUPS.forEach(function (gg, i) {
    var p = proj(gg.u[0] * 1.08, gg.u[1] * 1.08, gg.u[2] * 1.08);
    if (p[2] > 0.25) return;
    var d = Math.hypot(p[0] - x, p[1] - y);
    if (d < bd) { bd = d; best = i; }
  });
  return best;
}

function tipFor(x, y, i, g) {
  var tip = $('gb-tip');
  if (!tip) return;
  tip.textContent = '';
  if (i < 0 && g < 0) { tip.style.display = 'none'; return; }
  if (i >= 0) {
    var n = NODES[i];
    tip.append(mk('b', null, n.l), mk('br'), mk('span', 'gb-m', n.lg + ' · ' + n.ly), mk('br'));
    tip.append(mk('span', 'gb-m', GROUPS[n.g].l + '  |  rank #' + n.rp), mk('br'));
    tip.append(mk('span', 'gb-o', OUT[i].length + ' out'), '  ', mk('span', 'gb-i', INN[i].length + ' in'));
    if (n.d) tip.append(mk('br'), mk('span', null, clip(n.d, CFG.tipDocChars)));
  } else {
    var gr = GROUPS[g];
    tip.append(mk('b', null, gr.l), mk('br'), mk('span', 'gb-m', gr.n + ' entities'));
    var f = flowsOf(g);
    tip.append(mk('br'), mk('span', 'gb-o', f.outTotal + ' out'), '  ', mk('span', 'gb-i', f.inTotal + ' in'), '  ', mk('span', 'gb-m', f.inside + ' inside'));
  }
  tip.style.display = 'block';
  var r = tip.getBoundingClientRect();
  tip.style.left = Math.min(window.innerWidth - r.width - 8, x + 14) + 'px';
  tip.style.top = Math.min(window.innerHeight - r.height - 8, y + 14) + 'px';
}
function flowsOf(g) {
  var out = {}, inn = {}, inside = 0, outTotal = 0, inTotal = 0;
  EDGES.forEach(function (e) {
    var a = NODES[e[0]].g, b = NODES[e[1]].g;
    if (a === g && b === g) inside++;
    else if (a === g) { out[b] = (out[b] || 0) + 1; outTotal++; }
    else if (b === g) { inn[a] = (inn[a] || 0) + 1; inTotal++; }
  });
  function rank(o) {
    return Object.keys(o).map(function (k) { return [+k, o[k]]; }).sort(function (x, y) { return (y[1] - x[1]) || (x[0] - y[0]); });
  }
  return { out: rank(out), inn: rank(inn), inside: inside, outTotal: outTotal, inTotal: inTotal };
}

function inspectInGraph(id) {
  try { window.location.hash = '#node=' + encodeURIComponent(id); } catch (e) { /* ignore */ }
  var t = document.querySelector('.tab[data-tab="graph"]');
  if (t) t.click();
  var c = document.querySelector('.canvas-tab[data-canvas="graph"]');
  if (c) c.click();
}
function nodeButton(i, extra) {
  var b = mk('button', 'gb-nb'), dot = mk('i');
  dot.style.background = colorOf(i);
  b.append(dot, mk('span', null, NODES[i].l), mk('em', null, extra !== undefined && extra !== null ? extra : GROUPS[NODES[i].g].l));
  b.title = NODES[i].l;
  b.addEventListener('click', function () { focusNode(i); });
  return b;
}
function groupButton(g, count) {
  var b = mk('button', 'gb-nb'), dot = mk('i');
  dot.style.background = GROUPS[g].c;
  b.append(dot, mk('span', null, GROUPS[g].l), mk('em', null, String(count)));
  b.addEventListener('click', function () { focusGroup(g); });
  return b;
}
function listInto(panel, title, cls, items, render) {
  var sec = mk('div', 'gb-sec');
  sec.append(mk('span', cls, title), mk('span', null, String(items.length)));
  panel.append(sec);
  var list = mk('div', 'gb-list');
  items.slice(0, CFG.listMax).forEach(function (it) { list.append(render(it)); });
  if (items.length > CFG.listMax) list.append(mk('div', 'gb-more', '+' + (items.length - CFG.listMax) + ' more'));
  if (!items.length) list.append(mk('div', 'gb-more', 'none'));
  panel.append(list);
}
function renderPanel() {
  var panel = $('gb-panel');
  if (!panel) return;
  panel.textContent = '';
  var i, n, head, type, dot, badges, gb, m, act, outs, ins;
  if (S.focus >= 0) {
    i = S.focus; n = NODES[i];
    head = mk('div', 'gb-p-head'); type = mk('div', 'gb-type'); dot = mk('i');
    dot.style.background = colorOf(i); type.append(dot, 'entity');
    head.append(type, mk('h2', null, n.l), mk('div', 'gb-path', n.lg + ' · ' + n.ly));
    badges = mk('div', 'gb-badges');
    gb = mk('button', 'gb-badge', GROUPS[n.g].l);
    gb.title = 'Focus this cluster';
    gb.addEventListener('click', function () { focusGroup(n.g); });
    badges.append(gb, mk('span', 'gb-badge', n.ly), mk('span', 'gb-badge', n.lg));
    if (n.fd) badges.append(mk('span', 'gb-badge', n.fd + ' findings'));
    head.append(badges); panel.append(head);
    m = mk('div', 'gb-metrics');
    [['#' + n.rp, 'rank'], [OUT[i].length, 'relations out'], [INN[i].length, 'relations in']].forEach(function (pair) {
      var cc = mk('div', 'gb-metric'); cc.append(mk('b', null, pair[0]), mk('span', null, pair[1])); m.append(cc);
    });
    panel.append(m);
    if (n.d) panel.append(mk('div', 'gb-doc', n.d));
    act = mk('div', 'gb-actions');
    var go = mk('button', null, 'Inspect in Graph');
    go.addEventListener('click', function () { inspectInGraph(n.id); });
    act.append(go); panel.append(act);
    outs = OUT[i].map(function (k) { return EDGES[k][1]; }).sort(function (a, b) { return NODES[b].r - NODES[a].r; });
    ins = INN[i].map(function (k) { return EDGES[k][0]; }).sort(function (a, b) { return NODES[b].r - NODES[a].r; });
    listInto(panel, 'Relations out', 'gb-o', outs, function (j) { return nodeButton(j); });
    listInto(panel, 'Relations in', 'gb-i', ins, function (j) { return nodeButton(j); });
    return;
  }
  if (S.group >= 0) {
    var g = S.group, gr = GROUPS[g], f = flowsOf(g);
    head = mk('div', 'gb-p-head'); type = mk('div', 'gb-type'); dot = mk('i');
    dot.style.background = gr.c; type.append(dot, 'cluster');
    head.append(type, mk('h2', null, gr.l), mk('div', 'gb-path', gr.n + ' entities'));
    panel.append(head);
    var total = f.inside + f.outTotal + f.inTotal;
    m = mk('div', 'gb-metrics');
    [[f.inside, 'inside'], [f.outTotal, 'out'], [f.inTotal, 'in']].forEach(function (pair) {
      var cc = mk('div', 'gb-metric'); cc.append(mk('b', null, pair[0]), mk('span', null, pair[1])); m.append(cc);
    });
    panel.append(m);
    panel.append(mk('div', 'gb-doc', 'Cohesion ' + (total ? Math.round(100 * f.inside / total) : 0) + '%: share of this cluster wires that stay inside it. Cyan wires leave it, pink wires arrive.'));
    listInto(panel, 'Relations to', 'gb-o', f.out.slice(0, CFG.flowTopN), function (pair) { return groupButton(pair[0], pair[1]); });
    listInto(panel, 'Relations from', 'gb-i', f.inn.slice(0, CFG.flowTopN), function (pair) { return groupButton(pair[0], pair[1]); });
    var members = NODES.map(function (nn, ii) { return ii; }).filter(function (ii) { return NODES[ii].g === g; })
      .sort(function (a, b) { return NODES[b].r - NODES[a].r; });
    listInto(panel, 'Entities by rank', null, members, function (j) { return nodeButton(j, '#' + NODES[j].rp); });
    return;
  }
  var intro = mk('div', 'gb-intro');
  intro.append(mk('h2', null, 'Hierarchical edge bundling'));
  intro.append(mk('p', null, 'Every entity sits on the rim, grouped into its cluster arc. Every relation is drawn as a curve routed through the cluster tree: wires that leave a cluster travel together, so thick bundles are the real seams between intelligence clusters.'));
  intro.append(mk('p', null, 'Hover an entity to light its wires: cyan is what it points to, pink is what points to it. Click to pin it, click an arc or a legend row to focus a cluster. Beta 0 draws straight chords; 1 bundles fully. The sphere puts every cluster on its own cap of a globe.'));
  panel.append(intro);
  var flows = {};
  EDGES.forEach(function (e) {
    var a = NODES[e[0]].g, b = NODES[e[1]].g;
    if (a !== b) { var kk = a + '>' + b; flows[kk] = (flows[kk] || 0) + 1; }
  });
  var top = Object.keys(flows).map(function (k) { return [k, flows[k]]; })
    .sort(function (x, y) { return (y[1] - x[1]) || (x[0] < y[0] ? -1 : 1); }).slice(0, CFG.flowTopN);
  var sec = mk('div', 'gb-sec');
  sec.append(mk('span', null, 'Thickest seams'), mk('span', null, String(top.length)));
  panel.append(sec);
  var list = mk('div', 'gb-list'), peak = top.length ? top[0][1] : 1;
  top.forEach(function (pair) {
    var ab = pair[0].split('>').map(Number), aa = ab[0], bb = ab[1], cc2 = pair[1];
    var btn = mk('button', 'gb-nb'), d2 = mk('i');
    d2.style.background = GROUPS[aa].c;
    btn.append(d2, mk('span', null, clip(GROUPS[aa].l, 16) + ' → ' + clip(GROUPS[bb].l, 16)), mk('em', null, String(cc2)));
    btn.addEventListener('click', function () { focusGroup(aa); });
    list.append(btn);
    var bar = mk('div', 'gb-bar'), fill = mk('i');
    fill.style.width = (100 * cc2 / peak) + '%';
    fill.style.background = GROUPS[aa].c;
    bar.append(fill); list.append(bar);
  });
  if (!top.length) list.append(mk('div', 'gb-more', 'no relations cross clusters'));
  panel.append(list);
}
function renderLegend() {
  var body = $('gb-lgbody');
  if (!body) return;
  body.textContent = '';
  var titles = { community: 'Clusters', layer: 'Levels', kind: 'Kinds' };
  $('gb-lgtitle').textContent = titles[S.color] || 'Clusters';
  if (S.color === 'community') {
    GROUPS.forEach(function (g, i) {
      var b = mk('button', 'gb-key'), dot = mk('i');
      dot.style.background = g.c; dot.style.color = g.c;
      b.append(dot, mk('span', null, g.l), mk('em', null, String(g.n)));
      b.setAttribute('aria-pressed', String(S.group === i));
      b.addEventListener('click', function () { focusGroup(S.group === i ? -1 : i); });
      body.append(b);
    });
    return;
  }
  var counts = {};
  NODES.forEach(function (n, i) { var k = keyOf(i); counts[k] = (counts[k] || 0) + 1; });
  Object.keys(counts).sort(function (a, b) { return (counts[b] - counts[a]) || (a < b ? -1 : 1); }).forEach(function (k) {
    var b = mk('button', 'gb-key'), dot = mk('i');
    var col = S.color === 'layer' ? (TIER_COLORS[k] || ink().muted) : djb2KindColor(k);
    dot.style.background = col; dot.style.color = col;
    b.append(dot, mk('span', null, k), mk('em', null, String(counts[k])));
    b.setAttribute('aria-pressed', String(S.key === k));
    b.addEventListener('click', function () {
      S.key = S.key === k ? null : k; S.focus = -1; S.group = -1; sync();
    });
    body.append(b);
  });
}

function focusNode(i) {
  S.focus = i; S.group = -1; S.key = null;
  if (S.view === '3d' && i >= 0) aimAt(NODES[i].p);
  sync();
}
function focusGroup(g) {
  S.group = g; S.focus = -1; S.key = null;
  if (S.view === '3d' && g >= 0) aimAt(GROUPS[g].u);
  sync();
}
function facing(p) {
  return {
    yaw: Math.PI - Math.atan2(p[0], p[2]),
    pitch: Math.max(-1.2, Math.min(1.2, -Math.asin(Math.max(-1, Math.min(1, p[1])))))
  };
}
function aimAt(p) {
  var f = facing(p);
  S.rotate = false;
  if (reduceMotion) { S.yaw = f.yaw; S.pitch = f.pitch; return; }
  aim = { yaw: f.yaw, pitch: f.pitch, t0: performance.now(), y0: S.yaw, p0: S.pitch };
}
function setView(v) {
  S.view = v === '3d' ? '3d' : '2d'; S.panX = S.panY = 0; S.zoom = 1;
  resize(); sync();
}
function setColor(c) {
  if (['community', 'layer', 'kind'].indexOf(c) < 0) return;
  S.color = c; S.key = null; sync();
}
function setDir(d) {
  if (['both', 'out', 'in'].indexOf(d) < 0) return;
  S.dir = d; sync();
}
function setBeta(b) {
  S.beta = Math.max(0, Math.min(1, +b || 0));
  var slider = $('gb-beta');
  if (slider) slider.value = String(S.beta);
  var bv = $('gb-betav');
  if (bv) bv.textContent = S.beta.toFixed(2);
  buildCurves(); sync();
}
function sync() {
  document.querySelectorAll('#bundles-canvas [data-view]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.view === S.view)); });
  document.querySelectorAll('#bundles-canvas [data-color]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.color === S.color)); });
  document.querySelectorAll('#bundles-canvas [data-dir]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.dir === S.dir)); });
  var cross = $('gb-cross'), rot = $('gb-rotate'), bv = $('gb-betav');
  if (cross) cross.setAttribute('aria-pressed', String(S.cross));
  if (rot) { rot.setAttribute('aria-pressed', String(S.rotate)); rot.hidden = S.view !== '3d'; }
  if (bv) bv.textContent = S.beta.toFixed(2);
  renderPanel(); renderLegend(); writeHash(); draw(performance.now());
}
function writeHash() {
  if (!tabActive()) return;
  var p = new URLSearchParams();
  if (S.view === '3d') p.set('bview', '3d');
  if (S.focus >= 0) p.set('bundle', NODES[S.focus].id);
  if (S.group >= 0) p.set('bgroup', GROUPS[S.group].k);
  if (Math.abs(S.beta - CFG.beta) > 1e-9) p.set('bbeta', S.beta.toFixed(2));
  if (S.color !== 'community') p.set('bcolor', S.color);
  if (S.dir !== 'both') p.set('bdir', S.dir);
  if (S.cross) p.set('bcross', '1');
  try { history.replaceState(null, '', '#' + p.toString()); } catch (e) { /* ignore */ }
}
function readHash() {
  var p;
  try { p = new URLSearchParams((location.hash || '').slice(1)); } catch (e) { return; }
  if (p.get('bview') === '3d' || p.get('bview') === '2d') S.view = p.get('bview');
  var b = parseFloat(p.get('bbeta'));
  if (!isNaN(b)) S.beta = Math.max(0, Math.min(1, b));
  var c = p.get('bcolor');
  if (['community', 'layer', 'kind'].indexOf(c) >= 0) S.color = c;
  var d = p.get('bdir');
  if (['both', 'out', 'in'].indexOf(d) >= 0) S.dir = d;
  S.cross = p.get('bcross') === '1';
  var n = p.get('bundle');
  if (n !== null && byId[n] !== undefined) S.focus = byId[n];
  var g = p.get('bgroup');
  if (g !== null && groupByKey[g] !== undefined && S.focus < 0) S.group = groupByKey[g];
}

function ingest(bundle, settings) {
  NODES = (bundle && bundle.nodes) || [];
  GROUPS = (bundle && bundle.groups) || [];
  EDGES = (bundle && bundle.edges) || [];
  CFG = settings || CFG;
  if (!CFG) return false;
  OUT = NODES.map(function () { return []; });
  INN = NODES.map(function () { return []; });
  EDGES.forEach(function (e, k) {
    if (e && e[0] >= 0 && e[0] < NODES.length && e[1] >= 0 && e[1] < NODES.length) {
      OUT[e[0]].push(k); INN[e[1]].push(k);
    }
  });
  byId = {}; NODES.forEach(function (n, i) { byId[n.id] = i; });
  groupByKey = {}; GROUPS.forEach(function (g, i) { groupByKey[g.k] = i; });
  maxRank = Math.max.apply(null, [1e-9].concat(NODES.map(function (n) { return n.r || 0; })));
  byRank = NODES.map(function (n, i) { return i; })
    .sort(function (a, b) { return (NODES[b].r - NODES[a].r) || (NODES[a].f < NODES[b].f ? -1 : 1); });
  topSet = new Set(byRank.slice(0, CFG.labelTopN));
  INSIDE = EDGES.filter(function (e) { return NODES[e[0]].g === NODES[e[1]].g; }).length;
  S.beta = CFG.beta; S.focus = -1; S.group = -1; S.key = null; S.hover = -1; S.hoverGroup = -1;
  buildCurves();
  readHash();
  if (S.view === '3d') {
    var p = S.focus >= 0 ? NODES[S.focus].p : S.group >= 0 ? GROUPS[S.group].u : null;
    if (p) { var f = facing(p); S.yaw = f.yaw; S.pitch = f.pitch; S.rotate = false; }
  }
  var slider = $('gb-beta');
  if (slider) slider.value = String(S.beta);
  loaded = true; loadFailed = false;
  var empty = $('gb-empty');
  if (empty) empty.hidden = NODES.length > 0;
  resize(); sync();
  return true;
}

function refresh() {
  var gd = window._graphData || {};
  if (gd.bundle && gd.bundle_settings) {
    if (!CFG) CFG = gd.bundle_settings;
    ingest(gd.bundle, gd.bundle_settings);
    return;
  }
  if (loadFailed) return;
  fetch('/api/graph?limit=300').then(function (r) { return r.json(); }).then(function (data) {
    window._graphData = data;
    if (data && data.bundle && data.bundle_settings) {
      ingest(data.bundle, data.bundle_settings);
    } else {
      loadFailed = true;
      var empty = $('gb-empty');
      if (empty) { empty.hidden = false; empty.textContent = 'No bundle data yet — run a query first, then open this tab.'; }
    }
  }).catch(function () {
    loadFailed = true;
    var empty = $('gb-empty');
    if (empty) { empty.hidden = false; empty.textContent = 'Could not load bundle data (network or auth).'; }
  });
}

function frame(now) {
  var dt = Math.min(0.1, (now - last) / 1000);
  last = now;
  var busy = false;
  if (!CFG || !loaded) { requestAnimationFrame(frame); return; }
  if (S.reveal < 1) {
    if (!S.revealStart) S.revealStart = now;
    S.reveal = Math.min(1, (now - S.revealStart) / Math.max(1, CFG.revealMs));
    busy = true;
  }
  if (S.view === '3d' && aim) {
    var u = Math.min(1, (now - aim.t0) / Math.max(1, CFG.flyMs || 700));
    var e = u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
    var dy = Math.atan2(Math.sin(aim.yaw - aim.y0), Math.cos(aim.yaw - aim.y0));
    S.yaw = aim.y0 + dy * e; S.pitch = aim.p0 + (aim.pitch - aim.p0) * e;
    if (u >= 1) aim = null;
    busy = true;
  } else if (S.view === '3d' && S.rotate && !drag) {
    S.yaw += dt * CFG.rotateSpeed * Math.PI * 2 / 6;
    busy = true;
  }
  if (!reduceMotion && CFG.particles > 0 && focusState()) busy = true;
  if (busy) draw(now);
  requestAnimationFrame(frame);
}

function init() {
  canvas = $('gb-c'); stage = $('gb-stage');
  if (!canvas || !stage) return;
  ctx = canvas.getContext('2d');

  stage.addEventListener('pointerdown', function (ev) {
    if (ev.target !== canvas) return;
    drag = { x: ev.clientX, y: ev.clientY, moved: false, yaw: S.yaw, pitch: S.pitch, px: S.panX, py: S.panY };
    try { stage.setPointerCapture(ev.pointerId); } catch (e) { /* ignore */ }
  });
  stage.addEventListener('pointermove', function (ev) {
    if (!loaded) return;
    var r = stage.getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top;
    if (drag) {
      var dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
      if (!drag.moved && Math.hypot(dx, dy) > CFG.dragPx) {
        drag.moved = true; stage.classList.add('gb-dragging'); aim = null;
      }
      if (drag.moved) {
        if (S.view === '3d') {
          S.yaw = drag.yaw + dx * 0.008;
          S.pitch = Math.max(-1.4, Math.min(1.4, drag.pitch + dy * 0.008));
        } else { S.panX = drag.px + dx; S.panY = drag.py + dy; }
        var tip0 = $('gb-tip');
        if (tip0) tip0.style.display = 'none';
        draw(performance.now()); return;
      }
    }
    var i = hitNode(x, y), g = i < 0 ? hitGroup(x, y) : -1;
    if (i !== S.hover || g !== S.hoverGroup) { S.hover = i; S.hoverGroup = g; draw(performance.now()); }
    stage.classList.toggle('gb-pointing', i >= 0 || g >= 0);
    tipFor(ev.clientX, ev.clientY, i, g);
  });
  stage.addEventListener('pointerup', function (ev) {
    var was = drag;
    drag = null; stage.classList.remove('gb-dragging');
    if (was && !was.moved && loaded) {
      var r = stage.getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top;
      var i = hitNode(x, y);
      if (i >= 0) { focusNode(i); return; }
      var g = hitGroup(x, y);
      if (g >= 0) { focusGroup(g); return; }
      if (S.focus >= 0 || S.group >= 0 || S.key !== null) { S.focus = -1; S.group = -1; S.key = null; sync(); }
    }
  });
  stage.addEventListener('pointerleave', function () {
    S.hover = -1; S.hoverGroup = -1;
    var tip = $('gb-tip');
    if (tip) tip.style.display = 'none';
    if (loaded) draw(performance.now());
  });
  stage.addEventListener('wheel', function (ev) {
    ev.preventDefault();
    S.zoom = Math.max(0.4, Math.min(6, S.zoom * Math.exp(-ev.deltaY * 0.0015)));
    if (loaded) draw(performance.now());
  }, { passive: false });
  stage.addEventListener('dblclick', function () {
    S.zoom = 1; S.panX = S.panY = 0; S.yaw = 0.7; S.pitch = -0.32;
    S.focus = -1; S.group = -1; S.key = null; sync();
  });

  document.querySelectorAll('#bundles-canvas [data-view]').forEach(function (b) {
    b.addEventListener('click', function () { setView(b.dataset.view); });
  });
  document.querySelectorAll('#bundles-canvas [data-color]').forEach(function (b) {
    b.addEventListener('click', function () { setColor(b.dataset.color); });
  });
  document.querySelectorAll('#bundles-canvas [data-dir]').forEach(function (b) {
    b.addEventListener('click', function () { setDir(b.dataset.dir); });
  });
  var beta = $('gb-beta');
  if (beta) beta.addEventListener('input', function (ev) { setBeta(ev.target.value); });
  var cross = $('gb-cross');
  if (cross) cross.addEventListener('click', function () { S.cross = !S.cross; sync(); });
  var rot = $('gb-rotate');
  if (rot) rot.addEventListener('click', function () { S.rotate = !S.rotate; aim = null; sync(); });
  var reset = $('gb-reset');
  if (reset) reset.addEventListener('click', function () {
    S.zoom = 1; S.panX = S.panY = 0; S.yaw = 0.7; S.pitch = -0.32;
    S.focus = -1; S.group = -1; S.key = null; S.cross = false; S.dir = 'both';
    setBeta(CFG ? CFG.beta : 0.85);
  });
  var png = $('gb-png');
  if (png) png.addEventListener('click', function () {
    try {
      var a = document.createElement('a');
      a.download = 'graph-bundle-' + S.view + '.png';
      a.href = canvas.toDataURL('image/png');
      a.click();
    } catch (e) { /* ignore */ }
  });
  var lgt = $('gb-lgtoggle');
  if (lgt) lgt.addEventListener('click', function () {
    var l = $('gb-legend');
    if (!l) return;
    l.classList.toggle('gb-collapsed');
    lgt.textContent = l.classList.contains('gb-collapsed') ? '+' : '-';
  });

  var q = $('gb-q'), results = $('gb-results');
  function search(text) {
    if (!results) return [];
    results.textContent = '';
    var t = String(text || '').trim().toLowerCase();
    if (!t) { results.classList.remove('open'); return []; }
    var hits = NODES.map(function (n, i) { return i; })
      .filter(function (i) { return NODES[i].f.toLowerCase().indexOf(t) >= 0; })
      .sort(function (a, b) {
        return ((NODES[b].l.toLowerCase().indexOf(t) === 0) - (NODES[a].l.toLowerCase().indexOf(t) === 0)) || (NODES[b].r - NODES[a].r);
      }).slice(0, CFG ? CFG.searchResults : 8);
    hits.forEach(function (i) {
      var b = mk('button', 'gb-result'), dot = mk('i');
      dot.style.background = colorOf(i);
      b.append(dot, mk('span', null, NODES[i].l), mk('em', null, NODES[i].lg));
      b.addEventListener('click', function () { focusNode(i); results.classList.remove('open'); q.blur(); });
      results.append(b);
    });
    results.classList.toggle('open', hits.length > 0);
    return hits;
  }
  if (q) {
    q.addEventListener('input', function () { search(q.value); });
    q.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') {
        var h = search(q.value);
        if (h.length) { focusNode(h[0]); results.classList.remove('open'); q.blur(); }
      } else if (ev.key === 'Escape') { q.value = ''; search(''); q.blur(); }
    });
  }

  document.querySelectorAll('.canvas-tab[data-canvas="bundles"]').forEach(function (t) {
    t.addEventListener('click', function () { refresh(); resize(); });
  });

  if (typeof ResizeObserver !== 'undefined' && stage) new ResizeObserver(function () { resize(); }).observe(stage);
  window.addEventListener('resize', resize);
  window.EstoridesBundles = Object.freeze({ refresh: refresh, focusNode: focusNode, focusGroup: focusGroup, setView: setView, setBeta: setBeta, setColor: setColor, setDir: setDir, state: S });
  refresh();
  requestAnimationFrame(frame);
}

// Registered at eval time (this script loads BEFORE graph_force.js), so
// when the Bundles tab is active these keys never reach the Graph view.
// Escape is left to propagate so both views clear together.
document.addEventListener('keydown', function (ev) {
  var tag = (ev.target && ev.target.tagName) || '';
  if (tag === 'INPUT' || tag === 'TEXTAREA' || (ev.target && ev.target.isContentEditable)) return;
  if (!tabActive()) return;
  var k = ev.key, handled = true;
  if (k === '2') setView('2d');
  else if (k === '3') setView('3d');
  else if (k === 'r' || k === 'R') { if (S.view === '3d') { S.rotate = !S.rotate; aim = null; sync(); } else handled = false; }
  else if (k === 'c' || k === 'C') {
    var modes = ['community', 'layer', 'kind'];
    setColor(modes[(modes.indexOf(S.color) + 1) % modes.length]);
  }
  else if (k === 'x' || k === 'X') { S.cross = !S.cross; sync(); }
  else if (k === '[' || k === ']') setBeta(S.beta + (k === ']' ? 0.05 : -0.05));
  else if (k === '/') {
    ev.preventDefault();
    var qq = $('gb-q');
    if (qq) qq.focus();
  }
  else handled = false;
  if (handled && ev.stopImmediatePropagation) ev.stopImmediatePropagation();
});

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
else init();

})();
