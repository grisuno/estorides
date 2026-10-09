/* Estorides force-graph module (spec/graph_force3d.md).
 * Port of ReadMenator graph-force.html to the OSINT entity graph:
 * same values (SETTINGS, filters, HUD, legend, search, PNG/JSON export,
 * shortcuts, deep-links), engine 2D = vendored force-graph (D3 canvas
 * stays the default 2D renderer) + 3D button loading 3d-force-graph
 * from CDN on demand, exactly like ReadMenator btn-3d.
 *
 * CSP: no inline style attributes anywhere (dynamic colours via CSSOM
 * element properties and classes),
 * every remote string through bridge.escapeHTML before reaching any
 * HTML sink. No eval/Function. CDN URL is a constant (script-src
 * already allows cdn.jsdelivr.net).
 */
(function () {
  'use strict';
  var B = window.EstoridesGraph || null;
  if (!B) return; // main bundle missing: stay inert, 2D keeps working.

  var CDN_3D = 'https://cdn.jsdelivr.net/npm/3d-force-graph@1/dist/3d-force-graph.min.js';
  var $ = function (id) { return document.getElementById(id); };
  var short = function (t, n) {
    t = String(t == null ? '' : t);
    return t.length > n ? t.slice(0, n - 1) + '…' : t;
  };
  var esc = function (t) { return B.escapeHTML(t); };

  var DEFAULT_SETTINGS = {
    charge: -300, linkDistance: 120, linkStrength: 0.3, nodeRelSize: 4,
    hulls: true, hullFill: 0.07, hullStroke: 0.5, hullPad: 18, particles: 4,
    dimNode: 'rgba(80,85,110,.4)', dimLink: 'rgba(255,255,255,.04)',
    labelTopN: 30, labelZoom: 1.6, labelMax: 28, clusterStrength: 0.6,
    collidePad: 4, dagLevel: 60, flyMs: 700, flyZoom: 3.0, searchResults: 8,
  };
  var TIER_ORDER = ['data', 'information', 'intelligence', 'counter_intelligence', 'unknown'];
  var TIER_COLORS = { data: '#6b7280', information: '#5fb4ff', intelligence: '#f6bd16', counter_intelligence: '#ff5c5c' };

  var S = {
    engine: '2d', layout: 'force', depth: 1, labels: true, hulls: true,
    flow: true, frozen: false, isolate: false, hidden: {}, selected: null,
    hover: null, hl: [], hlLinks: {}, famFocus: null, history: [],
    hits: {}, raw: null, settings: DEFAULT_SETTINGS, g3: null, mounting3d: false,
  };

  function toast(msg) {
    var b = $('gf-toast');
    if (!b) return;
    b.textContent = msg;
    B.setVisible(b, true, 'block');
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { B.setVisible(b, false); }, 3200);
  }
  function fail(msg) {
    var b = $('gf-engine-error');
    if (!b) return;
    b.textContent = msg;
    B.setVisible(b, true, 'block');
  }

  function settings() {
    var gd = window._graphData || {};
    return gd.settings || S.settings;
  }

  /* ---- adapt /api/graph nodes to RAW force-graph shape (fallback when
     the server did not send data.force; mirrors graph_force.py) ---- */
  function adaptLocal(nodes, edges, clusters) {
    var degree = {};
    (nodes || []).forEach(function (n) { degree[n.id] = 0; });
    var valid = [];
    (edges || []).forEach(function (e) {
      if (!e || degree[e.source] == null || degree[e.target] == null) return;
      valid.push(e);
      degree[e.source] += 1;
      degree[e.target] += 1;
    });
    var byCluster = {};
    (clusters || []).forEach(function (c) { byCluster[c.id] = c; });
    var maxDeg = 1;
    Object.keys(degree).forEach(function (k) { if (degree[k] > maxDeg) maxDeg = degree[k]; });
    var ordered = (nodes || []).slice().sort(function (a, b) {
      return (degree[b.id] - degree[a.id]) || String(a.id).localeCompare(String(b.id));
    });
    var rankPos = {};
    ordered.forEach(function (n, i) { rankPos[n.id] = i + 1; });
    var out = [], outE = [];
    var seen = {};
    ordered.forEach(function (n) {
      var cid = (n.cluster == null) ? -1 : n.cluster;
      var fam = (cid >= 0 && byCluster[cid]) ? (byCluster[cid].label || n.kind || n.type) : (n.kind || n.type || 'unknown');
      out.push({
        id: n.id, label: n.label || n.id, type: 'entity', kind: n.kind || n.type || 'unknown',
        degree: degree[n.id], findings: 0, community: cid >= 0 ? cid : null,
        community_label: (cid >= 0 && byCluster[cid]) ? (byCluster[cid].label || '') : '',
        family: fam, layer: n.level || 'data',
        color: B.safeColor(n.cluster_color || n.color) || '#888',
        rank: Math.round((degree[n.id] / maxDeg) * 1e6) / 1e6,
        rank_pos: rankPos[n.id],
        val: Math.max(1, Math.log2(degree[n.id] + 1)),
        _src: n,
      });
      seen[n.id] = true;
    });
    Object.keys(byCluster).forEach(function (cid) {
      var c = byCluster[cid];
      out.push({ id: 'community:' + cid, label: c.label || ('cluster ' + cid), type: 'community', community_id: +cid, size: c.size || 0, color: B.safeColor(c.color) || '#888', val: 4 });
    });
    TIER_ORDER.forEach(function (lv) {
      out.push({ id: 'tier:' + lv, label: lv, type: 'tier', color: TIER_COLORS[lv] || '#888', val: 2 });
    });
    out.forEach(function (n) {
      if (n.type !== 'entity') return;
      if (n.community != null) outE.push({ source: n.id, target: 'community:' + n.community, type: 'member_of', weight: 1 });
      outE.push({ source: n.id, target: 'tier:' + n.layer, type: 'layered_as', weight: 1 });
    });
    valid.forEach(function (e) {
      outE.push({ source: e.source, target: e.target, type: e.relation || 'related-to', weight: 1, inter: !!e.inter_cluster });
    });
    return { nodes: out, links: outE };
  }

  function currentRaw() {
    var gd = window._graphData || {};
    if (gd.force && gd.force.nodes) {
      var st = settings();
      return {
        nodes: gd.force.nodes.map(function (n) {
          n.val = n.val || Math.max(1, Math.log2((n.degree || 0) + 1));
          return n;
        }),
        links: gd.force.edges || [],
        settings: st,
      };
    }
    return { nodes: [], links: [], settings: settings(), local: true };
  }

  function rebuildRaw() {
    var gd = window._graphData || {};
    var payload;
    if (gd.force && gd.force.nodes) {
      payload = {
        nodes: gd.force.nodes.map(function (n) {
          var c = {};
          Object.keys(n).forEach(function (k) { c[k] = n[k]; });
          c.val = c.val || Math.max(1, Math.log2((c.degree || 0) + 1));
          var src = (gd.nodes || []).filter(function (x) { return x.id === c.id; })[0];
          if (src) c._src = src;
          return c;
        }),
        links: (gd.force.edges || []).map(function (e) {
          return { source: e.source, target: e.target, type: e.type, weight: 1, inter: e.type !== 'member_of' && e.type !== 'layered_as' && !!e.inter_cluster };
        }),
      };
    } else {
      payload = adaptLocal(gd.nodes || [], gd.edges || [], gd.clusters || []);
    }
    S.raw = payload;
    indexRaw();
    return payload;
  }

  var byId = {}, outE = {}, inE = {}, famColor = {}, famMembers = {}, labelSet = {};
  function indexRaw() {
    byId = {}; outE = {}; inE = {}; famColor = {}; famMembers = {}; labelSet = {};
    var st = settings();
    (S.raw.nodes || []).forEach(function (n) {
      byId[n.id] = n;
      outE[n.id] = [];
      inE[n.id] = [];
      n.val = n.val || 1;
    });
    (S.raw.links || []).forEach(function (e) {
      var s = (e.source && e.source.id) || e.source;
      var t = (e.target && e.target.id) || e.target;
      if (!byId[s] || !byId[t]) return;
      outE[s].push({ source: s, target: t, type: e.type, inter: !!e.inter });
      inE[t].push({ source: s, target: t, type: e.type, inter: !!e.inter });
    });
    var entities = (S.raw.nodes || []).filter(function (n) { return n.type === 'entity'; });
    entities.forEach(function (n) {
      var f = n.family || n.kind || 'unknown';
      if (!famColor[f]) famColor[f] = n.color || '#888';
      (famMembers[f] = famMembers[f] || []).push(n.id);
    });
    entities.slice().sort(function (a, b) {
      return ((b.rank || 0) - (a.rank || 0)) || ((b.degree || 0) - (a.degree || 0));
    }).slice(0, st.labelTopN || 30).forEach(function (n) { labelSet[n.id] = true; });
    (S.raw.nodes || []).forEach(function (n) {
      if (n.type === 'community' || n.type === 'tier') labelSet[n.id] = true;
    });
  }

  function lkey(l) { return l.source + '|' + l.target + '|' + l.type; }
  function colorOf(n) { return B.safeColor(n.color) || '#888'; }
  function dimmed(id) { return S.hl.length > 0 && S.hl.indexOf(id) < 0; }
  function hiddenKind(n) {
    if (n.type !== 'entity') return !!S.hidden[n.type];
    return !!S.hidden['kind:' + (n.kind || 'unknown')];
  }

  function visiblePayload() {
    var keep = {};
    (S.raw.nodes || []).forEach(function (n) {
      if (hiddenKind(n)) return;
      if (S.isolate && S.hl.length && S.hl.indexOf(n.id) < 0) return;
      keep[n.id] = true;
    });
    return {
      nodes: (S.raw.nodes || []).filter(function (n) { return keep[n.id]; }),
      links: (S.raw.links || []).filter(function (e) {
        var s = (e.source && e.source.id) || e.source;
        var t = (e.target && e.target.id) || e.target;
        return keep[s] && keep[t];
      }),
    };
  }

  function computeHighlight(id, depth) {
    var hl = [id], seen = {};
    seen[id] = true;
    var links = {};
    var frontier = [id];
    for (var d = 0; d < depth; d++) {
      var next = [];
      frontier.forEach(function (cur) {
        (outE[cur] || []).forEach(function (e) {
          links[e.source + '|' + e.target + '|' + e.type] = true;
          if (!seen[e.target]) { seen[e.target] = true; hl.push(e.target); next.push(e.target); }
        });
        (inE[cur] || []).forEach(function (e) {
          links[e.source + '|' + e.target + '|' + e.type] = true;
          if (!seen[e.source]) { seen[e.source] = true; hl.push(e.source); next.push(e.source); }
        });
      });
      frontier = next;
    }
    S.hl = hl;
    S.hlLinks = links;
  }

  function tip(n) {
    var h = '<div class="gf-tip"><b>' + esc(n.label) + '</b> <span class="m">' + esc(n.kind || n.type) + '</span>';
    if (n.type === 'entity') {
      h += '<div class="m">' + esc(n.id) + '</div><div>' + (n.degree || 0) + ' links';
      if (n.rank_pos) h += ' · rank #' + n.rank_pos;
      h += '</div>';
      if (n.community_label) h += '<div class="m">' + esc(n.community_label) + ' · ' + esc(String(n.layer || '').replace('_', '-')) + '</div>';
    } else if (n.type === 'community') {
      h += '<div>' + (n.size || 0) + ' entities</div>';
    } else {
      h += '<div>' + (inE[n.id] || []).length + ' incoming</div>';
    }
    return h + '<div class="m">click to inspect + expand</div></div>';
  }

  /* ---- layout forces (same math as ReadMenator, tier rings for OSINT) ---- */
  var famList = [];
  function refreshFamList() {
    famList = Object.keys(famMembers).sort(function (a, b) {
      return (famMembers[b].length - famMembers[a].length) || (a < b ? -1 : 1);
    });
  }
  function famAnchor(f, linkDistance) {
    var i = famList.indexOf(f);
    if (i < 0) return { x: 0, y: 0 };
    var R = linkDistance * Math.max(1.5, Math.sqrt(famList.length) * 1.6);
    if (i === 0 && famList.length > 2) return { x: 0, y: 0 };
    var k = famList.length > 2 ? i - 1 : i;
    var n = famList.length > 2 ? famList.length - 1 : famList.length;
    var a = (2 * Math.PI * k) / Math.max(1, n) - Math.PI / 2;
    return { x: R * Math.cos(a), y: R * Math.sin(a) };
  }
  function famOf(n) {
    if (n.type === 'entity') return n.family;
    if (n.type === 'community') return n.label;
    return null;
  }
  function clusterForce(st) {
    var nodes = [];
    function force(alpha) {
      if (S.layout !== 'cluster') return;
      var k = st.clusterStrength * alpha;
      nodes.forEach(function (n) {
        var f = famOf(n);
        if (f == null) return;
        var t = famAnchor(f, st.linkDistance);
        n.vx += (t.x - n.x) * k;
        n.vy += (t.y - n.y) * k;
        n.vz += ((n.vz == null ? 0 : 0) - (n.z || 0)) * k;
      });
    }
    force.initialize = function (ns) { nodes = ns; };
    return force;
  }
  function ringOf(n) {
    if (n.type === 'entity' || n.type === 'tier') {
      var idx = TIER_ORDER.indexOf(n.type === 'tier' ? n.label : n.layer);
      return (idx < 0 ? TIER_ORDER.length - 1 : idx) + 1;
    }
    if (n.type === 'community') return 0;
    return TIER_ORDER.length + 1;
  }
  function radialForce(st) {
    var nodes = [];
    function force(alpha) {
      if (S.layout !== 'radial') return;
      var ring = st.linkDistance * 1.3, k = st.clusterStrength * alpha;
      nodes.forEach(function (n) {
        var target = ringOf(n) * ring;
        var d = Math.hypot(n.x, n.y, n.z || 0) || 1;
        var s = target / d;
        n.vx += (n.x * s - n.x) * k;
        n.vy += (n.y * s - n.y) * k;
        n.vz += ((n.z || 0) * s - (n.z || 0)) * k;
      });
    }
    force.initialize = function (ns) { nodes = ns; };
    return force;
  }
  function collideForce(st) {
    var nodes = [];
    function force() {
      if (nodes.length > 1500) return;
      var pad = st.collidePad || 4;
      for (var i = 0; i < nodes.length; i++) {
        var a = nodes[i];
        var ra = radius(a) + pad;
        for (var j = i + 1; j < nodes.length; j++) {
          var b = nodes[j];
          var dx = b.x - a.x, dy = b.y - a.y, dz = (b.z || 0) - (a.z || 0);
          var min = ra + radius(b);
          if (Math.abs(dx) > min || Math.abs(dy) > min || Math.abs(dz) > min) continue;
          var d = Math.hypot(dx, dy, dz) || 0.01;
          if (d < min) {
            var m = ((min - d) / d) * 0.5;
            a.x -= dx * m; a.y -= dy * m; a.z = (a.z || 0) - dz * m;
            b.x += dx * m; b.y += dy * m; b.z = (b.z || 0) + dz * m;
          }
        }
      }
    }
    force.initialize = function (ns) { nodes = ns; };
    return force;
  }
  function radius(n) {
    var st = settings();
    return Math.sqrt(Math.max(0, n.val || 1)) * (st.nodeRelSize || 4);
  }
  function linkStrengthFn(st) {
    return function (l) {
      var base = st.linkStrength;
      var src = l.source.id || l.source, tgt = l.target.id || l.target;
      if (l.type === 'layered_as') return S.layout === 'radial' ? 0 : base * 0.15;
      if (l.type === 'member_of') return S.layout === 'radial' ? base * 0.05 : base * 0.6;
      if (S.layout === 'cluster') {
        var a = byId[src], b = byId[tgt];
        return a && b && famOf(a) === famOf(b) ? base : base * 0.08;
      }
      if (S.layout === 'radial') return base * 0.35;
      return base;
    };
  }

  /* ---- 3D mount ---- */
  function setEngineButtons() {
    var btns = document.querySelectorAll('#gf-toolbar [data-engine]');
    btns.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.engine === S.engine));
    });
    var req3d = document.querySelectorAll('#gf-toolbar [data-req="3d"]');
    req3d.forEach(function (b) { b.disabled = S.engine !== '3d'; });
  }

  function show3DChrome(show) {
    var canvas = $('graph-canvas');
    if (canvas) canvas.classList.toggle('gf-on', show);
    ['gf-stage', 'gf-hud', 'gf-legend'].forEach(function (id) {
      B.setVisible($(id), show, id === 'gf-stage' ? 'block' : undefined);
    });
    var svg = canvas ? canvas.querySelector(':scope > svg') : null;
    if (svg) svg.classList.toggle('gf-hide', show);
    var legend = $('graph-legend');
    if (legend) B.setVisible(legend, !show);
  }

  function mount3D() {
    if (typeof ForceGraph3D === 'undefined') {
      if (S.mounting3d) return;
      S.mounting3d = true;
      toast('Loading 3D engine…');
      var s = document.createElement('script');
      s.src = CDN_3D;
      s.onload = function () { S.mounting3d = false; mount3D(); };
      s.onerror = function () { S.mounting3d = false; toast('3D engine needs network access.'); };
      document.head.appendChild(s);
      return;
    }
    var el = $('gf-stage');
    if (!el) return;
    el.textContent = '';
    var st = settings();
    refreshFamList();
    var data = visiblePayload();
    try {
      var g = ForceGraph3D()(el)
        .graphData(data)
        .nodeId('id')
        .nodeVal('val')
        .nodeRelSize(st.nodeRelSize || 4)
        .nodeLabel(tip)
        .nodeColor(function (n) { return dimmed(n.id) ? st.dimNode : colorOf(n); })
        .linkColor(function (l) {
          var k = lkey({ source: l.source.id || l.source, target: l.target.id || l.target, type: l.type });
          if (S.hl.length) return S.hlLinks[k] ? '#22d3ee' : st.dimLink;
          return 'rgba(148,163,184,.2)';
        })
        .linkWidth(function (l) {
          var k = lkey({ source: l.source.id || l.source, target: l.target.id || l.target, type: l.type });
          return S.hlLinks[k] ? 2 : 0.4;
        })
        .linkDirectionalParticles(function (l) {
          if (!S.flow) return 0;
          var k = lkey({ source: l.source.id || l.source, target: l.target.id || l.target, type: l.type });
          return S.hlLinks[k] ? (st.particles || 4) : 0;
        })
        .onNodeClick(function (n, ev) { onSelect3D(n, ev); })
        .onNodeRightClick(function (n, ev) {
          B.showContextMenu({ clientX: ev.clientX, clientY: ev.clientY, preventDefault: function () {} }, n._src || n);
        })
        .onNodeHover(function (n) {
          el.style.cursor = n ? 'pointer' : '';
          S.hover = n ? n.id : null;
          if (!S.selected && !S.famFocus) {
            if (n) computeHighlight(n.id, 1);
            else { S.hl = []; S.hlLinks = {}; }
            refresh3D();
          }
        })
        .onBackgroundClick(function () { clearSelection(); })
        .backgroundColor('rgba(0,0,0,0)')
        .showNavInfo(false);
      g.d3Force('charge').strength(st.charge);
      g.d3Force('link').distance(st.linkDistance).strength(linkStrengthFn(st));
      g.d3Force('cluster', clusterForce(st));
      g.d3Force('radial', radialForce(st));
      g.d3Force('collide', collideForce(st));
      S.g3 = g;
      applyLayout3D();
      resize3D();
      hud();
      setTimeout(function () {
        try { if (S.g3 && S.engine === '3d') S.g3.zoomToFit(0, 60); } catch (e) { /* noop */ }
      }, 1200);
    } catch (err) {
      fail('Graph engine failed to start: ' + (err && err.message || err));
    }
  }

  function refresh3D() {
    var g = S.g3;
    if (!g) return;
    g.nodeColor(g.nodeColor());
    g.linkColor(g.linkColor()).linkWidth(g.linkWidth()).linkDirectionalParticles(g.linkDirectionalParticles());
  }
  function reload3D() {
    if (!S.g3) { mount3D(); return; }
    S.g3.graphData(visiblePayload());
    hud();
  }
  function resize3D() {
    if (!S.g3) return;
    var host = $('graph-canvas');
    if (host) S.g3.width(host.clientWidth).height(host.clientHeight);
  }
  function applyLayout3D() {
    var g = S.g3;
    if (!g) return;
    var st = settings();
    try {
      g.dagMode(S.layout === 'dag' ? 'td' : null);
      if (S.layout === 'dag') g.dagLevelDistance(st.dagLevel || 60);
      g.d3Force('charge').strength((S.layout === 'force' || S.layout === 'dag') ? st.charge : st.charge * 0.4);
      g.d3Force('link').strength(linkStrengthFn(st));
      g.d3ReheatSimulation();
    } catch (e) { /* engine quirk: layout stays */ }
    document.querySelectorAll('#gf-toolbar [data-layout]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.layout === S.layout));
    });
    hud();
  }

  function onSelect3D(n, ev) {
    var src = n._src || n;
    if (S.selected && S.selected !== n.id) S.history.push(S.selected);
    S.selected = n.id;
    S.famFocus = null;
    markFamilies();
    computeHighlight(n.id, S.depth);
    if (S.isolate) reload3D();
    refresh3D();
    hud();
    writeHash();
    B.selectNode(src);
    var rt = B.resolverTypeFor(src);
    if (rt && src.label) {
      var B2 = B;
      setTimeout(function () {
        try { B2.expandNode(rt, src.label || src.id); } catch (e) { /* resolver offline */ }
      }, 60);
    }
    if (ev && ev.altKey) {
      B.showContextMenu({ clientX: ev.clientX, clientY: ev.clientY, preventDefault: function () {} }, src);
    }
  }

  function clearSelection() {
    S.selected = null;
    S.hl = [];
    S.hlLinks = {};
    S.famFocus = null;
    S.history = [];
    markFamilies();
    if (S.isolate) { S.isolate = false; syncIsolateBtn(); reload3D(); }
    refresh3D();
    hud();
    writeHash();
  }

  function focusFamily(fam) {
    if (S.famFocus === fam) { clearSelection(); renderLegend(); return; }
    S.selected = null;
    S.famFocus = fam;
    var ids = {};
    (famMembers[fam] || []).forEach(function (id) { ids[id] = true; });
    (S.raw.nodes || []).forEach(function (n) {
      if (n.type === 'community' && n.label === fam) ids[n.id] = true;
    });
    var hl = Object.keys(ids);
    S.hl = hl;
    var links = {};
    (S.raw.links || []).forEach(function (e) {
      var s = (e.source && e.source.id) || e.source;
      var t = (e.target && e.target.id) || e.target;
      if (ids[s] && ids[t]) links[s + '|' + t + '|' + e.type] = true;
    });
    S.hlLinks = links;
    markFamilies();
    refresh3D();
    hud();
    if (S.g3) {
      try { S.g3.zoomToFit(700, 60, function (n) { return !!ids[n.id]; }); } catch (e) { /* noop */ }
    }
  }
  function markFamilies() {
    document.querySelectorAll('.gf-fam').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.fam === S.famFocus));
    });
  }

  function hud() {
    var box = $('gf-hud');
    if (!box || !S.g3) return;
    box.textContent = '';
    function stat(num, label) {
      var s = document.createElement('span');
      var b = document.createElement('b');
      b.textContent = String(num);
      s.appendChild(b);
      s.appendChild(document.createTextNode(' ' + label));
      return s;
    }
    var d = S.g3.graphData();
    box.appendChild(stat(d.nodes.length, 'nodes'));
    box.appendChild(stat(d.links.length, 'edges'));
    var m = document.createElement('span');
    m.textContent = S.layout + (S.engine === '3d' ? ' · 3D' : '');
    box.appendChild(m);
    if (S.hl.length) box.appendChild(stat(S.hl.length, 'highlighted'));
    if (S.selected && byId[S.selected]) {
      var s = document.createElement('span');
      s.appendChild(document.createTextNode('focus '));
      var b = document.createElement('b');
      b.textContent = short(byId[S.selected].label, 24);
      s.appendChild(b);
      box.appendChild(s);
    }
  }

  /* ---- legend: kind pills + community families ---- */
  function renderLegend() {
    var pills = $('gf-pills');
    if (!pills) return;
    pills.textContent = '';
    var kinds = {};
    (S.raw.nodes || []).forEach(function (n) {
      if (n.type === 'entity') kinds[n.kind || 'unknown'] = (kinds[n.kind || 'unknown'] || 0) + 1;
    });
    Object.keys(kinds).sort().forEach(function (k) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'gf-pill' + (S.hidden['kind:' + k] ? '' : ' active');
      b.textContent = k + ' ' + kinds[k];
      b.title = 'Show or hide ' + k + ' entities';
      b.addEventListener('click', function () {
        var key = 'kind:' + k;
        if (S.hidden[key]) delete S.hidden[key];
        else S.hidden[key] = true;
        b.classList.toggle('active', !S.hidden[key]);
        applyFilters();
      });
      pills.appendChild(b);
    });
    var box = $('gf-families');
    if (!box) return;
    box.textContent = '';
    refreshFamList();
    if (!famList.length) {
      var hint = $('gf-legend-hint');
      if (hint) hint.textContent = 'none';
      return;
    }
    famList.forEach(function (f) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'gf-fam';
      b.dataset.fam = f;
      b.setAttribute('aria-pressed', String(S.famFocus === f));
      b.title = 'Focus ' + f;
      var dot = document.createElement('i');
      dot.style.background = B.safeColor(famColor[f]) || '#888';
      dot.style.color = B.safeColor(famColor[f]) || '#888';
      b.appendChild(dot);
      var sp = document.createElement('span');
      sp.textContent = f;
      b.appendChild(sp);
      var em = document.createElement('em');
      em.textContent = String(famMembers[f].length);
      b.appendChild(em);
      b.addEventListener('click', function () { focusFamily(f); });
      box.appendChild(b);
    });
  }

  function applyFilters() {
    if (S.engine === '3d') reload3D();
    // 2D: pills/search re-render the D3 canvas with the filtered subset.
    else if (window._graphData) {
      var gd = window._graphData;
      var hidden = S.hidden;
      var hits = S.hits;
      var hasHits = Object.keys(hits).length > 0;
      var nodes = (gd.nodes || []).filter(function (n) {
        if (hidden['kind:' + (n.kind || n.type || 'unknown')]) return false;
        if (hasHits && !hits[n.id]) return false;
        return true;
      });
      var keep = {};
      nodes.forEach(function (n) { keep[n.id] = true; });
      var edges = (gd.edges || []).filter(function (e) { return keep[e.source] && keep[e.target]; });
      try {
        var fn = (window.EstoridesGraph || {}).redraw2D;
        if (typeof fn === 'function') fn(nodes, edges, B.deriveClusters(nodes));
      } catch (e) { /* 2D stays as-is */ }
    }
    hud();
  }

  /* ---- search ---- */
  var hits = [], hitIdx = 0;
  function runSearch() {
    var input = $('gf-search');
    var box = $('gf-results');
    if (!input || !box) return;
    var q = input.value.trim().toLowerCase();
    var st = settings();
    if (!q) {
      hits = [];
      S.hits = {};
      box.classList.remove('open');
      box.textContent = '';
      applyFilters();
      if (S.g3) refresh3D();
      return;
    }
    var scored = [];
    (S.raw.nodes || []).forEach(function (n) {
      var label = String(n.label || '').toLowerCase();
      var path = String(n.id || '').toLowerCase();
      var s = 0;
      if (label === q) s = 100;
      else if (label.indexOf(q) === 0) s = 60;
      else if (label.indexOf(q) >= 0) s = 40;
      else if (path.indexOf(q) >= 0) s = 25;
      if (s) scored.push({ n: n, s: s + (n.type === 'entity' ? 5 : 0) + Math.min(5, (n.degree || 0) / 10) });
    });
    scored.sort(function (a, b) { return (b.s - a.s) || (a.n.label < b.n.label ? -1 : 1); });
    hits = scored.slice(0, st.searchResults || 8);
    hitIdx = 0;
    var map = {};
    scored.forEach(function (x) { map[x.n.id] = true; });
    S.hits = map;
    if (S.g3) refresh3D();
    box.textContent = '';
    if (hits.length) {
      hits.forEach(function (x, i) {
        var r = document.createElement('div');
        r.className = 'gf-result';
        r.setAttribute('role', 'option');
        r.dataset.i = String(i);
        r.setAttribute('aria-selected', String(i === 0));
        var dot = document.createElement('i');
        dot.className = 'dot';
        dot.style.background = colorOf(x.n);
        r.appendChild(dot);
        var nm = document.createElement('span');
        nm.className = 'name';
        nm.textContent = x.n.label;
        r.appendChild(nm);
        var sub = document.createElement('span');
        sub.className = 'sub';
        sub.textContent = x.n.kind || x.n.type;
        r.appendChild(sub);
        box.appendChild(r);
      });
    } else {
      var r = document.createElement('div');
      r.className = 'gf-result';
      var sub = document.createElement('span');
      sub.className = 'sub';
      sub.textContent = 'no match';
      r.appendChild(sub);
      box.appendChild(r);
    }
    box.classList.add('open');
  }
  function pickHit(i) {
    var x = hits[i];
    if (!x) return;
    var box = $('gf-results');
    if (box) box.classList.remove('open');
    if (S.engine === '3d') onSelect3D(x.n, null);
    else if (x.n._src) B.selectNode(x.n._src);
    else B.selectNode(x.n);
  }

  /* ---- engine toggle ---- */
  function to3D() {
    if (S.engine === '3d') return;
    S.engine = '3d';
    setEngineButtons();
    show3DChrome(true);
    renderLegend();
    mount3D();
    writeHash();
  }
  function to2D() {
    if (S.engine === '2d') return;
    S.engine = '2d';
    setEngineButtons();
    show3DChrome(false);
    if (window._graphData) applyFilters();
    writeHash();
  }

  function readHash() {
    var params;
    try { params = new URLSearchParams((location.hash || '').slice(1)); }
    catch (e) { return; }
    var layout = params.get('layout');
    if (layout && ['force', 'cluster', 'radial', 'dag'].indexOf(layout) >= 0) {
      S.layout = layout;
      if (S.g3) applyLayout3D();
    }
    var id = params.get('node');
    if (id && byId[id]) {
      if (S.engine === '3d') onSelect3D(byId[id], null);
      else if (byId[id]._src) B.selectNode(byId[id]._src);
    }
  }
  function writeHash() {
    var p = new URLSearchParams();
    if (S.selected) p.set('node', S.selected);
    if (S.layout !== 'force') p.set('layout', S.layout);
    try { history.replaceState(null, '', '#' + p.toString()); } catch (e) { /* noop */ }
  }

  function syncIsolateBtn() {
    var b = $('gf-isolate');
    if (b) b.setAttribute('aria-pressed', String(S.isolate));
  }

  function wireToolbar() {
    document.querySelectorAll('#gf-toolbar [data-engine]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (b.dataset.engine === '3d') to3D();
        else to2D();
      });
    });
    document.querySelectorAll('#gf-toolbar [data-layout]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (S.engine !== '3d') { toast('Layouts apply to the 3D view'); return; }
        S.layout = b.dataset.layout;
        applyLayout3D();
        writeHash();
        toast('Layout: ' + b.textContent);
      });
    });
    document.querySelectorAll('#gf-toolbar [data-depth]').forEach(function (b) {
      b.addEventListener('click', function () {
        S.depth = +b.dataset.depth;
        document.querySelectorAll('#gf-toolbar [data-depth]').forEach(function (x) {
          x.setAttribute('aria-pressed', String(x === b));
        });
        if (S.selected && byId[S.selected] && S.engine === '3d') onSelect3D(byId[S.selected], null);
      });
    });
    function toggle(btnId, key, after) {
      var b = $(btnId);
      if (!b) return;
      b.addEventListener('click', function () {
        S[key] = !S[key];
        b.setAttribute('aria-pressed', String(S[key]));
        if (after) after();
      });
    }
    toggle('gf-names', 'labels');
    toggle('gf-hulls', 'hulls');
    toggle('gf-flow', 'flow', function () { refresh3D(); });
    var fr = $('gf-freeze');
    if (fr) fr.addEventListener('click', function () {
      S.frozen = !S.frozen;
      fr.setAttribute('aria-pressed', String(S.frozen));
      if (!S.g3) return;
      if (S.frozen) S.g3.cooldownTicks(0);
      else { S.g3.cooldownTicks(Infinity); if (S.g3.d3ReheatSimulation) S.g3.d3ReheatSimulation(); }
      toast(S.frozen ? 'Physics frozen' : 'Physics resumed');
    });
    var fit = $('gf-fit');
    if (fit) fit.addEventListener('click', function () {
      if (S.g3 && S.g3.zoomToFit) S.g3.zoomToFit(700, 48);
    });
    var png = $('gf-png');
    if (png) png.addEventListener('click', function () {
      var canvas = document.querySelector('#gf-stage canvas');
      if (!canvas) { toast('Nothing to snapshot yet.'); return; }
      var a = document.createElement('a');
      a.href = canvas.toDataURL('image/png');
      a.download = 'estorides-3d.png';
      a.click();
    });
    var js = $('gf-json');
    if (js) js.addEventListener('click', function () {
      if (!S.raw) { toast('Nothing to export yet.'); return; }
      var blob = new Blob([JSON.stringify(S.raw, null, 1)], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'estorides-graph.json';
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
    });
    var iso = $('gf-isolate');
    if (iso) iso.addEventListener('click', function () {
      S.isolate = !S.isolate;
      syncIsolateBtn();
      if (S.engine === '3d') reload3D();
      else applyFilters();
    });
    var search = $('gf-search');
    if (search) {
      search.addEventListener('input', runSearch);
      search.addEventListener('keydown', function (ev) {
        if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') {
          ev.preventDefault();
          if (!hits.length) return;
          hitIdx = (hitIdx + (ev.key === 'ArrowDown' ? 1 : hits.length - 1)) % hits.length;
          document.querySelectorAll('.gf-result').forEach(function (el, i) {
            el.setAttribute('aria-selected', String(i === hitIdx));
          });
        } else if (ev.key === 'Enter') { ev.preventDefault(); pickHit(hitIdx); }
        else if (ev.key === 'Escape') { search.value = ''; runSearch(); search.blur(); }
      });
      search.addEventListener('blur', function () {
        setTimeout(function () { var b = $('gf-results'); if (b) b.classList.remove('open'); }, 150);
      });
    }
    var res = $('gf-results');
    if (res) res.addEventListener('mousedown', function (ev) {
      var r = ev.target.closest ? ev.target.closest('.gf-result') : null;
      if (r && r.dataset.i != null) pickHit(+r.dataset.i);
    });
    document.addEventListener('keydown', function (e) {
      var tag = (e.target && e.target.tagName) || '';
      if (tag === 'INPUT' || tag === 'TEXTAREA' || (e.target && e.target.isContentEditable)) return;
      var tab = document.querySelector('.canvas-tab[data-canvas="graph"]');
      if (tab && !tab.classList.contains('active')) return;
      if (e.key === '/') { e.preventDefault(); var s = $('gf-search'); if (s) s.focus(); }
      else if (e.key === 'Escape') { clearSelection(); B.hideTooltip(); }
      else if (e.key === 'Backspace') {
        e.preventDefault();
        var prev = S.history.pop();
        if (prev && byId[prev]) { if (S.engine === '3d') onSelect3D(byId[prev], null); }
      }
      else if (e.key === 'l' || e.key === 'L') { var b = $('gf-names'); if (b && !b.disabled) b.click(); }
      else if (e.key === 'h' || e.key === 'H') { var h = $('gf-hulls'); if (h && !h.disabled) h.click(); }
      else if (e.key === 'f' || e.key === 'F') { var f = $('gf-fit'); if (f && !f.disabled) f.click(); }
      else if (e.key === ' ') { e.preventDefault(); var z = $('gf-freeze'); if (z && !z.disabled) z.click(); }
      else if (e.key === 'i' || e.key === 'I') { var o = $('gf-isolate'); if (o && !o.disabled) o.click(); }
      else if (['1', '2', '3', '4'].indexOf(e.key) >= 0) {
        var btns = document.querySelectorAll('#gf-toolbar [data-layout]');
        var t = btns[+e.key - 1];
        if (t && !t.disabled) t.click();
      }
    });
    window.addEventListener('resize', resize3D);
  }

  /* ---- sync loop: follow window._graphData like the 2D renderer does ---- */
  var lastSeen = null;
  setInterval(function () {
    var gd = window._graphData;
    if (!gd || !gd.nodes) return;
    B.setVisible($('gf-toolbar'), true);
    var canvas = $('graph-canvas');
    if (canvas) canvas.classList.add('gf-bar');
    if (gd !== lastSeen) {
      lastSeen = gd;
      rebuildRaw();
      renderLegend();
      if (S.engine === '3d') reload3D();
      else applyFilters();
      readHash();
    }
  }, 600);

  wireToolbar();
  setEngineButtons();
  window.GF = {
    to3D: to3D, to2D: to2D, state: S,
    context: function () { return { nodes: (S.raw || {}).nodes, edges: (S.raw || {}).links }; },
  };
})();
