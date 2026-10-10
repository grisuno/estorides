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
    flow: true, frozen: false, isolate: false, bridgesOnly: false, orbit: false, hidden: {}, selected: null,
    hover: null, hl: [], hlLinks: {}, famFocus: null, history: [],
    hits: {}, raw: null, settings: DEFAULT_SETTINGS, g3: null, mounting3d: false,
  };

  // Matte data-point look (CAIRN-like): small faceted markers on a dark
  // radial field. Shared by mount and restyle so 2D/3D stay consistent.
  var POINT_STYLE = {
    nodeRelSize: 3, nodeResolution: 10, nodeOpacity: 0.95,
    linkWidth: 0.5, linkOpacity: 0.5, linkHighlightWidth: 2,
  };
  // Glyph scale per node type on the 3D overlay (ReadMenator shapes).
  var GLYPH_SCALE = { community: 1.2, tier: 1.3 };
  function reducedMotion() {
    try { return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
    catch (e) { return false; }
  }

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
      // /api/graph emits embedded node objects as endpoints; reduce to ids.
      var s = e && ((e.source && e.source.id) || e.source);
      var t = e && ((e.target && e.target.id) || e.target);
      if (!e || s == null || t == null || degree[s] == null || degree[t] == null) return;
      valid.push({ source: s, target: t, relation: e.relation, inter_cluster: e.inter_cluster });
      degree[s] += 1;
      degree[t] += 1;
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
      // Bridge derivation: the server payload carries no inter flag, so an
      // OSINT edge joining two known distinct communities is a bridge.
      if (!e.inter && e.type !== 'member_of' && e.type !== 'layered_as') {
        var a = byId[s], b = byId[t];
        if (a && b && a.community != null && b.community != null && a.community !== b.community) {
          e.inter = true;
          outE[s][outE[s].length - 1].inter = true;
          inE[t][inE[t].length - 1].inter = true;
        }
      }
    });
    var entities = (S.raw.nodes || []).filter(function (n) { return n.type === 'entity'; });    entities.forEach(function (n) {
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
    var links = (S.raw.links || []).filter(function (e) {
      var s = (e.source && e.source.id) || e.source;
      var t = (e.target && e.target.id) || e.target;
      if (!keep[s] || !keep[t]) return false;
      if (S.bridgesOnly && !e.inter && e.type !== 'member_of' && e.type !== 'layered_as') return false;
      return true;
    });
    if (S.bridgesOnly) {
      // Bridges-only view: keep bridge edges plus the membership scaffolding
      // (community/tier) of endpoints that survive, so bridges stay anchored.
      var bridgeLinks = links.filter(function (e) { return !!e.inter; });
      var end = {};
      bridgeLinks.forEach(function (e) {
        var s = (e.source && e.source.id) || e.source;
        var t = (e.target && e.target.id) || e.target;
        end[s] = true;
        end[t] = true;
      });
      links = links.filter(function (e) {
        if (e.inter) return true;
        var s = (e.source && e.source.id) || e.source;
        var t = (e.target && e.target.id) || e.target;
        return !!end[s] && !!end[t];
      });
      var keep2 = {};
      links.forEach(function (e) {
        var s = (e.source && e.source.id) || e.source;
        var t = (e.target && e.target.id) || e.target;
        if (keep[s]) keep2[s] = true;
        if (keep[t]) keep2[t] = true;
      });
      return {
        nodes: (S.raw.nodes || []).filter(function (n) { return keep2[n.id]; }),
        links: links,
      };
    }
    return {
      nodes: (S.raw.nodes || []).filter(function (n) { return keep[n.id]; }),
      links: links,
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
    return h + '<div class="m">click to inspect, double-click to expand</div></div>';
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

  // Exclusive render: exactly one engine owns the pixels. Entering 3D
  // hides every D3 SVG layer; leaving 3D hides the stage and pauses the
  // 3D loop so a hidden WebGL canvas can never stack over 2D or steal
  // pointer events.
  function show3DChrome(show) {
    var canvas = $('graph-canvas');
    if (canvas) canvas.classList.toggle('gf-on', show);
    var stage = $('gf-stage');
    if (stage) stage.classList.toggle('is3d', show);
    ['gf-stage', 'gf-hud', 'gf-legend'].forEach(function (id) {
      B.setVisible($(id), show, id === 'gf-stage' ? 'block' : undefined);
    });
    if (canvas) {
      var svgs = canvas.querySelectorAll(':scope > svg');
      svgs.forEach(function (svg) { svg.classList.toggle('gf-hide', show); });
    }
    var legend = $('graph-legend');
    if (legend) B.setVisible(legend, !show);
    if (S.g3) {
      try {
        if (show) { if (S.g3.resumeAnimation) S.g3.resumeAnimation(); }
        else { if (S.g3.pauseAnimation) S.g3.pauseAnimation(); }
      } catch (e) { /* engine quirk: visibility still toggled */ }
    }
    if (show) resize3D();
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
    // The engine wipes its container on init (innerHTML=""), so the 2D
    // glyph overlay is (re)attached AFTER construction. The engine owns
    // links and physics, the overlay owns every node marker (flat shapes,
    // never spheres).
    var ov = $('gf-overlay3d');
    if (ov) ov.remove();
    var st = settings();
    refreshFamList();
    var data = visiblePayload();
    try {
      var g = ForceGraph3D({ controlType: 'orbit' })(el)
        .graphData(data)
        .nodeId('id')
        .nodeVal('val')
        .nodeRelSize(4)
        .nodeVisibility(false)
        .nodeLabel(tip)
        .enablePointerInteraction(false)
        .nodeColor(function (n) { return dimmed(n.id) ? st.dimNode : colorOf(n); })
        .linkColor(function (l) {
          var k = lkey({ source: l.source.id || l.source, target: l.target.id || l.target, type: l.type });
          if (S.hl.length) return S.hlLinks[k] ? '#22d3ee' : st.dimLink;
          return 'rgba(148,163,184,.2)';
        })
        .linkWidth(function (l) {
          var k = lkey({ source: l.source.id || l.source, target: l.target.id || l.target, type: l.type });
          return S.hlLinks[k] ? POINT_STYLE.linkHighlightWidth : POINT_STYLE.linkWidth;
        })
        .linkDirectionalParticles(function (l) {
          if (!S.flow) return 0;
          var k = lkey({ source: l.source.id || l.source, target: l.target.id || l.target, type: l.type });
          return S.hlLinks[k] ? (st.particles || 4) : 0;
        })
        .backgroundColor('rgba(0,0,0,0)')
        .showNavInfo(false);
      if (reducedMotion()) {
        try { g.cooldownTicks(60); } catch (e) { /* optional only */ }
      }
      try {
        if (g.controls) g.controls().autoRotate = S.orbit;
        if (g.controls && S.orbit) g.controls().autoRotateSpeed = 0.6;
      } catch (e) { /* optional only */ }
      g.d3Force('charge').strength(st.charge);
      g.d3Force('link').distance(st.linkDistance).strength(linkStrengthFn(st));
      g.d3Force('cluster', clusterForce(st));
      g.d3Force('radial', radialForce(st));
      g.d3Force('collide', collideForce(st));
      S.g3 = g;
      el.appendChild(ov = document.createElement('canvas'));
      ov.id = 'gf-overlay3d';
      applyLayout3D();
      resize3D();
      startOverlayLoop();
      hud();
      setTimeout(function () {
        try { if (S.g3 && S.engine === '3d') S.g3.zoomToFit(reducedMotion() ? 0 : 1200, 60); } catch (e) { /* noop */ }
      }, 1200);
    } catch (err) {
      // Leave no half-built engine behind: a failed WebGL context still
      // inserts its nav hint and canvas, which would stack over the 2D view.
      try {
        el.querySelectorAll('canvas:not(#gf-overlay3d), .graph-nav-info').forEach(function (x) { x.remove(); });
      } catch (e2) { /* cleanup only */ }
      S.g3 = null;
      fail('Graph engine failed to start: ' + (err && err.message || err));
    }
  }

  /* ---- 3D overlay: flat canvas glyphs projected from the WebGL camera.
     ReadMenator system: the engine renders links + physics, native node
     spheres stay hidden (nodeVisibility false) and every marker is a 2D
     glyph (rounded rect / hexagon / diamond / triangle) with depth fade,
     selection glow, labels and community hulls. No atoms, no planets. ---- */
  var overlayRunning = false;
  function startOverlayLoop() {
    if (overlayRunning) return;
    overlayRunning = true;
    requestAnimationFrame(overlayTick);
  }
  function overlayTick() {
    if (S.engine !== '3d' || !S.g3) {
      overlayRunning = false;
      var dead = $('gf-overlay3d');
      if (dead) { var dctx = dead.getContext('2d'); if (dctx) dctx.clearRect(0, 0, dead.width, dead.height); }
      return;
    }
    try { paintOverlay3D(); } catch (e) { /* overlay never breaks the scene */ }
    requestAnimationFrame(overlayTick);
  }
  function convexHullPts(pts) {
    var p = pts.slice().sort(function (a, b) { return (a.x - b.x) || (a.y - b.y); });
    if (p.length < 3) return p;
    function cross(o, a, b) { return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x); }
    var lower = [];
    p.forEach(function (q) {
      while (lower.length >= 2 && cross(lower[lower.length - 2], lower[lower.length - 1], q) <= 0) lower.pop();
      lower.push(q);
    });
    var upper = [];
    for (var i = p.length - 1; i >= 0; i--) {
      var q2 = p[i];
      while (upper.length >= 2 && cross(upper[upper.length - 2], upper[upper.length - 1], q2) <= 0) upper.pop();
      upper.push(q2);
    }
    lower.pop();
    upper.pop();
    return lower.concat(upper);
  }
  function inflateHull(hull, pad) {
    if (!hull.length) return hull;
    var cx = 0, cy = 0;
    hull.forEach(function (q) { cx += q.x; cy += q.y; });
    cx /= hull.length;
    cy /= hull.length;
    return hull.map(function (q) {
      var dx = q.x - cx, dy = q.y - cy;
      var d = Math.hypot(dx, dy) || 1;
      return { x: q.x + (dx / d) * pad, y: q.y + (dy / d) * pad };
    });
  }
  function traceSmooth(ctx, hull) {
    if (!hull.length) return;
    if (hull.length < 3) {
      ctx.moveTo(hull[0].x, hull[0].y);
      for (var i = 1; i < hull.length; i++) ctx.lineTo(hull[i].x, hull[i].y);
      ctx.closePath();
      return;
    }
    var mid = function (a, b) { return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }; };
    var m0 = mid(hull[hull.length - 1], hull[0]);
    ctx.moveTo(m0.x, m0.y);
    for (var j = 0; j < hull.length; j++) {
      var cur = hull[j], nxt = hull[(j + 1) % hull.length];
      var m = mid(cur, nxt);
      ctx.quadraticCurveTo(cur.x, cur.y, m.x, m.y);
    }
    ctx.closePath();
  }
  function rr(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }
  function glyphPath(ctx, n, x, y, r) {
    var i, a;
    ctx.beginPath();
    if (n.type === 'community') {
      for (i = 0; i < 6; i++) {
        a = (Math.PI / 3) * i + Math.PI / 6;
        var px = x + r * 1.2 * Math.cos(a), py = y + r * 1.2 * Math.sin(a);
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.closePath();
    } else if (n.type === 'tier') {
      var s = r * 1.3;
      ctx.moveTo(x, y - s);
      ctx.lineTo(x + s, y);
      ctx.lineTo(x, y + s);
      ctx.lineTo(x - s, y);
      ctx.closePath();
    } else if (n.type !== 'entity') {
      ctx.moveTo(x, y - r * 1.2);
      ctx.lineTo(x + r * 1.1, y + r * 0.8);
      ctx.lineTo(x - r * 1.1, y + r * 0.8);
      ctx.closePath();
    } else {
      var q = r * 0.9;
      rr(ctx, x - q, y - q, 2 * q, 2 * q, r * 0.34);
    }
  }
  function tierColorOf(n) {
    var lv = n.type === 'tier' ? n.label : n.layer;
    return TIER_COLORS[lv] || '#888';
  }
  function drawGlyph3D(ctx, n, x, y, r, alpha) {
    var col = colorOf(n);
    var isSel = S.selected === n.id;
    var isHov = S.hover === n.id;
    var isHit = !!(S.hits && S.hits[n.id]);
    var faded = dimmed(n.id);
    ctx.save();
    ctx.globalAlpha = alpha * (faded ? 0.55 : 1);
    if ((isSel || isHov) && !faded) { ctx.shadowColor = col; ctx.shadowBlur = 18; }
    glyphPath(ctx, n, x, y, r);
    if (n.type === 'entity') {
      ctx.fillStyle = faded ? 'rgba(80,85,110,.4)' : col;
      ctx.fill();
      ctx.shadowBlur = 0;
      ctx.lineWidth = 1.1;
      ctx.strokeStyle = '#020617';
      ctx.stroke();
      if (r >= 9) {
        ctx.fillStyle = 'rgba(2,6,23,.5)';
        var bw = r, bh = Math.max(1, r * 0.12);
        ctx.fillRect(x - bw / 2, y - r * 0.36, bw, bh);
        ctx.fillRect(x - bw / 2, y - r * 0.06, bw, bh);
        ctx.fillRect(x - bw / 2, y + r * 0.24, bw, bh);
      }
      ctx.beginPath();
      ctx.arc(x, y, r + 2.5, 0, Math.PI * 2);
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = tierColorOf(n);
      ctx.stroke();
    } else {
      ctx.fillStyle = '#030a1c';
      ctx.fill();
      ctx.shadowBlur = 0;
      ctx.lineWidth = 2;
      ctx.strokeStyle = faded ? 'rgba(80,85,110,.4)' : col;
      ctx.stroke();
      glyphPath(ctx, n, x, y, r * 0.42);
      ctx.fillStyle = faded ? 'rgba(80,85,110,.4)' : col;
      ctx.fill();
    }
    ctx.restore();
    if (isSel || isHov || isHit) {
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.beginPath();
      ctx.arc(x, y, r + (isHit && !isSel ? 3 : 4.5), 0, Math.PI * 2);
      ctx.lineWidth = isHit && !isSel ? 1.3 : 1.6;
      ctx.strokeStyle = '#22d3ee';
      ctx.stroke();
      ctx.restore();
    }
  }
  function drawLabel3D(ctx, n, x, y, r, alpha) {
    var text = short(n.label || n.id, 28);
    var fs = n.type === 'entity' ? 11 : 12;
    ctx.save();
    ctx.globalAlpha = Math.max(alpha, 0.7);
    ctx.font = (n.type === 'entity' ? '500 ' : '700 ') + fs + 'px ui-monospace, Menlo, monospace';
    var w = ctx.measureText(text).width;
    var bx = x - w / 2 - 4, by = y + r + 4, bh = fs + 8;
    rr(ctx, bx, by, w + 8, bh, 4);
    ctx.fillStyle = 'rgba(2,6,23,.8)';
    ctx.fill();
    if (S.selected === n.id) {
      ctx.lineWidth = 1;
      ctx.strokeStyle = '#22d3ee';
      ctx.stroke();
    }
    ctx.fillStyle = n.type === 'entity' ? '#e2e8f0' : colorOf(n);
    ctx.textBaseline = 'top';
    ctx.fillText(text, bx + 4, by + 4);
    ctx.restore();
  }
  function paintOverlay3D() {
    var g = S.g3;
    var cv = $('gf-overlay3d');
    var stage = $('gf-stage');
    if (!g || !cv || !stage) return;
    var W = stage.clientWidth, H = stage.clientHeight;
    if (!W || !H) return;
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)) {
      cv.width = Math.round(W * dpr);
      cv.height = Math.round(H * dpr);
    }
    var ctx = cv.getContext('2d');
    if (!ctx) return;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    var data = g.graphData();
    if (!data || !data.nodes) return;
    var cam = null;
    try { cam = g.camera(); } catch (e) { cam = null; }
    var f = 800, hasDepth = false, cx = 0, cy = 0, cz = 0;
    if (cam && cam.position && cam.fov) {
      f = (H / 2) / Math.tan(((cam.fov || 60) * Math.PI) / 360);
      cx = cam.position.x || 0;
      cy = cam.position.y || 0;
      cz = cam.position.z || 0;
      hasDepth = true;
    }
    var st = settings();
    var items = [];
    var dmin = Infinity, dmax = -Infinity;
    data.nodes.forEach(function (n) {
      if (n.x == null || n.y == null) return;
      var s = null;
      try { s = g.graph2ScreenCoords(n.x, n.y, n.z || 0); } catch (e) { s = null; }
      if (!s) return;
      var dist = hasDepth ? Math.hypot(n.x - cx, (n.y || 0) - cy, (n.z || 0) - cz) || 1 : 1;
      if (s.x < -80 || s.x > W + 80 || s.y < -40 || s.y > H + 40) return;
      if (dist < dmin) dmin = dist;
      if (dist > dmax) dmax = dist;
      items.push({ n: n, sx: s.x, sy: s.y, dist: dist });
    });
    if (!items.length) return;
    var span = Math.max(1, dmax - dmin);
    items.forEach(function (it) {
      var base = Math.sqrt(Math.max(0, it.n.val || 1)) * 4;
      base *= GLYPH_SCALE[it.n.type] || 1;
      it.r = hasDepth ? Math.max(2.5, (base * f) / it.dist) : base;
      it.a = hasDepth ? 1 - ((it.dist - dmin) / span) * 0.7 : 1;
    });
    items.sort(function (a, b) { return b.dist - a.dist; });
    S.proj = items;
    if (S.hulls && S.layout !== 'dag') {
      var groups = {};
      items.forEach(function (it) {
        if (it.n.type !== 'entity') return;
        var k = it.n.family || it.n.kind || 'unknown';
        (groups[k] = groups[k] || []).push(it);
      });
      Object.keys(groups).forEach(function (k) {
        var members = groups[k];
        if (members.length < 3) return;
        var hull = inflateHull(convexHullPts(members.map(function (m) { return { x: m.sx, y: m.sy }; })), 18);
        if (hull.length < 3) return;
        var col = (members[0] && colorOf(members[0].n)) || '#888';
        var fadedFam = !!S.famFocus && S.famFocus !== k;
        ctx.save();
        ctx.globalAlpha = (fadedFam ? 0.3 : 1) * 0.07;
        ctx.fillStyle = col;
        traceSmooth(ctx, hull);
        ctx.fill();
        ctx.globalAlpha = (fadedFam ? 0.3 : 1) * 0.5;
        ctx.strokeStyle = col;
        ctx.lineWidth = 1.4;
        ctx.setLineDash([6, 4]);
        traceSmooth(ctx, hull);
        ctx.stroke();
        ctx.setLineDash([]);
        if (S.labels) {
          var top = hull.reduce(function (a, b) { return a.y < b.y ? a : b; });
          ctx.globalAlpha = fadedFam ? 0.35 : 0.95;
          ctx.font = '700 12px ui-monospace, Menlo, monospace';
          ctx.textAlign = 'center';
          ctx.fillStyle = col;
          ctx.fillText(short(k, 32) + '  ·  ' + members.length, top.x, top.y - 8);
          ctx.textAlign = 'left';
        }
        ctx.restore();
      });
    }
    items.forEach(function (it) { drawGlyph3D(ctx, it.n, it.sx, it.sy, it.r, it.a); });
    if (S.labels) {
      var topN = (st.labelTopN || 30);
      var ranked = items.filter(function (it) { return it.n.type === 'entity'; })
        .sort(function (a, b) { return (b.n.rank || 0) - (a.n.rank || 0); })
        .slice(0, topN);
      var want = {};
      ranked.forEach(function (it) { want[it.n.id] = it; });
      items.forEach(function (it) {
        if (it.n.type !== 'entity' && (labelSet[it.n.id] || S.selected === it.n.id)) want[it.n.id] = it;
        if (S.selected === it.n.id || S.hover === it.n.id) want[it.n.id] = it;
        if (S.hits && S.hits[it.n.id]) want[it.n.id] = it;
      });
      Object.keys(want).forEach(function (id) {
        var it = want[id];
        if (it.r >= 9 || S.selected === id) drawLabel3D(ctx, it.n, it.sx, it.sy, it.r, it.a);
      });
    }
  }

  /* ---- 3D pointer: the engine ignores the pointer entirely
     (enablePointerInteraction false); every pick is hit-tested against the
     live overlay projections, so selection always matches the drawn glyph.
     Bound once to #gf-stage, which survives engine remounts. ---- */
  var stageBound = false, downPos = null, hoverQueued = false, hoverXY = null;
  function stageLocal(ev) {
    var stage = $('gf-stage');
    if (!stage) return null;
    var r = stage.getBoundingClientRect();
    return { x: ev.clientX - r.left, y: ev.clientY - r.top };
  }
  function hitNode3D(x, y) {
    var best = null, bestD = Infinity;
    (S.proj || []).forEach(function (it) {
      var pad = Math.max(it.r + 4, 8);
      var d = Math.hypot(x - it.sx, y - it.sy);
      if (d <= pad && d < bestD) { bestD = d; best = it.n; }
    });
    return best;
  }
  function segDist(x, y, ax, ay, bx, by) {
    var dx = bx - ax, dy = by - ay;
    var len2 = dx * dx + dy * dy;
    var t = len2 ? ((x - ax) * dx + (y - ay) * dy) / len2 : 0;
    t = Math.max(0, Math.min(1, t));
    return Math.hypot(x - (ax + t * dx), y - (ay + t * dy));
  }
  function hitEdge3D(x, y) {
    if (!S.g3 || !S.proj) return null;
    var pos = {};
    S.proj.forEach(function (it) { pos[it.n.id] = it; });
    var best = null, bestD = 6;
    var links = [];
    try { links = S.g3.graphData().links || []; } catch (e) { links = []; }
    links.forEach(function (l) {
      var s = pos[l.source.id || l.source], t = pos[l.target.id || l.target];
      if (!s || !t) return;
      var d = segDist(x, y, s.sx, s.sy, t.sx, t.sy);
      if (d < bestD) { bestD = d; best = l; }
    });
    return best;
  }
  function hoverAt3D(x, y) {
    var el = $('gf-stage');
    var n = hitNode3D(x, y);
    if (el) el.style.cursor = (n || hitEdge3D(x, y)) ? 'pointer' : '';
    S.hover = n ? n.id : null;
    if (!S.selected && !S.famFocus) {
      if (n) computeHighlight(n.id, 1);
      else { S.hl = []; S.hlLinks = {}; }
      refresh3D();
    }
  }
  function bindStagePointer() {
    if (stageBound) return;
    var stage = $('gf-stage');
    if (!stage) return;
    stageBound = true;
    stage.addEventListener('pointerdown', function (ev) {
      downPos = { x: ev.clientX, y: ev.clientY };
    });
    stage.addEventListener('click', function (ev) {
      if (S.engine !== '3d') return;
      if (downPos && Math.hypot(ev.clientX - downPos.x, ev.clientY - downPos.y) > 6) return;
      var p = stageLocal(ev);
      if (!p) return;
      var n = hitNode3D(p.x, p.y);
      if (n) {
        onSelect3D(n, ev);
        return;
      }
      var l = hitEdge3D(p.x, p.y);
      if (l) { onEdge3D(l, ev); return; }
      clearSelection();
    });
    stage.addEventListener('dblclick', function (ev) {
      if (S.engine !== '3d') return;
      if (S.selected) { ev.preventDefault(); expandSelected(); }
    });
    stage.addEventListener('contextmenu', function (ev) {
      if (S.engine !== '3d') return;
      var p = stageLocal(ev);
      if (!p) return;
      var n = hitNode3D(p.x, p.y);
      if (n) {
        ev.preventDefault();
        ev.stopPropagation();
        B.showContextMenu(ev, n._src || n);
      }
    });
    stage.addEventListener('pointermove', function (ev) {
      if (S.engine !== '3d') return;
      var p = stageLocal(ev);
      if (!p) return;
      hoverXY = p;
      if (!hoverQueued) {
        hoverQueued = true;
        requestAnimationFrame(function () {
          hoverQueued = false;
          if (S.engine === '3d' && hoverXY) hoverAt3D(hoverXY.x, hoverXY.y);
        });
      }
    });
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
    // Size from the stage box, not the full canvas: the toolbar above the
    // stage would otherwise shift the raycaster frame and every click would
    // land offset from the marker under the cursor.
    var stage = $('gf-stage');
    var host = $('graph-canvas');
    var w = stage && stage.clientWidth ? stage.clientWidth : (host ? host.clientWidth : 0);
    var h = stage && stage.clientHeight ? stage.clientHeight : (host ? host.clientHeight : 0);
    if (w > 0 && h > 0) S.g3.width(w).height(h);
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

  // Click selects and inspects only. Double click, the Enter key or the
  // Expand button pivots through the resolver. Single click never mutates
  // the graph, so inspecting in 3D can no longer repaint a D3 layer on top
  // of the scene.
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
    if (ev && ev.altKey) {
      B.showContextMenu({ clientX: ev.clientX, clientY: ev.clientY, preventDefault: function () {} }, src);
    }
  }

  function expandSelected() {
    var n = S.selected && byId[S.selected];
    if (!n) { toast('Select a node first, then Expand.'); return; }
    var src = n._src || n;
    var rt = B.resolverTypeFor(src);
    if (!rt) { toast('No resolver pivot for this node type.'); return; }
    try { B.expandNode(rt, src.label || src.id); }
    catch (e) { toast('Resolver is offline.'); }
  }

  function focusSelected() {
    if (!S.g3) return;
    var n = S.selected && byId[S.selected];
    if (!n) { toast('Select a node first, then Focus.'); return; }
    var st = settings();
    try {
      S.g3.centerAt(n.x, n.y, 700);
      S.g3.zoom(st.flyZoom || 3.0, 700);
    } catch (e) { /* engine quirk: selection stays */ }
  }

  function copyDeepLink() {
    var link = String(location.href);
    function done() { toast('Deep link copied.'); }
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(link).then(done, function () { toast(link); });
      } else { toast(link); }
    } catch (e) { toast(link); }
  }

  function reheat() {
    if (!S.g3) return;
    try {
      if (S.g3.d3ReheatSimulation) S.g3.d3ReheatSimulation();
      toast('Physics reheated.');
    } catch (e) { /* engine quirk */ }
  }

  function toggleBridges(btn) {
    S.bridgesOnly = !S.bridgesOnly;
    if (btn) btn.setAttribute('aria-pressed', String(S.bridgesOnly));
    if (S.engine === '3d') reload3D();
    else applyFilters();
    toast(S.bridgesOnly ? 'Showing bridge edges only.' : 'Showing all edges.');
  }

  // PNG export composites the WebGL link field with the glyph overlay,
  // so the snapshot matches the screen (native node spheres stay hidden).
  function snapshot3D() {
    var stage = $('gf-stage');
    if (!stage) { toast('Nothing to snapshot yet.'); return; }
    var all = stage.querySelectorAll('canvas');
    var webgl = null, ov = null;
    all.forEach(function (c) {
      if (c.id === 'gf-overlay3d') ov = c;
      else if (!webgl) webgl = c;
    });
    if (!webgl) { toast('Nothing to snapshot yet.'); return; }
    try {
      var out = document.createElement('canvas');
      out.width = webgl.width;
      out.height = webgl.height;
      var octx = out.getContext('2d');
      octx.fillStyle = '#030a1c';
      octx.fillRect(0, 0, out.width, out.height);
      octx.drawImage(webgl, 0, 0);
      if (ov) octx.drawImage(ov, 0, 0, out.width, out.height);
      var a = document.createElement('a');
      a.href = out.toDataURL('image/png');
      a.download = 'estorides-3d.png';
      a.click();
    } catch (e) { toast('Snapshot failed.'); }
  }

  function toggleOrbit(btn) {
    S.orbit = !S.orbit;
    if (btn) btn.setAttribute('aria-pressed', String(S.orbit));
    if (S.g3) {
      try {
        S.g3.controls().autoRotate = S.orbit;
        if (S.orbit) S.g3.controls().autoRotateSpeed = 0.6;
      } catch (e) { /* engine quirk */ }
    }
    toast(S.orbit ? 'Orbit on: slow auto-rotate.' : 'Orbit off.');
  }

  // Edge inspection in 3D: bridge edges open the cross-reference tooltip,
  // plain edges report their relation. Hover only changes the cursor.
  function onEdge3D(l, ev) {
    if (!l) return;
    var s = byId[l.source.id || l.source];
    var t = byId[l.target.id || l.target];
    var rel = l.type || 'related';
    if (s && t && l.inter !== false) {
      var gd = window._graphData || {};
      var sameCluster = s.community != null && s.community === t.community;
      if (!sameCluster && (l.inter || s.community !== t.community)) {
        try {
          B.showBridgeTooltip(
            { clientX: ev ? ev.clientX : 0, clientY: ev ? ev.clientY : 0 },
            { source: s._src || s, target: t._src || t, relation: rel },
            gd.clusters || []
          );
          return;
        } catch (e) { /* fall through to toast */ }
      }
    }
    var a = s ? (s.label || s.id) : String(l.source.id || l.source);
    var b = t ? (t.label || t.id) : String(l.target.id || l.target);
    toast(a + ' --' + rel + '--> ' + b);
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
    m.textContent = S.layout + (S.engine === '3d' ? ' · 3D' : '') +
      (S.bridgesOnly ? ' · bridges' : '');
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
      var edges = (gd.edges || []).filter(function (e) {
        var s = (e.source && e.source.id) || e.source;
        var t = (e.target && e.target.id) || e.target;
        if (!keep[s] || !keep[t]) return false;
        // Bridges-only view: bridge edges plus the community/tier
        // scaffolding, plain same-cluster edges hidden.
        if (S.bridgesOnly && !e.inter_cluster &&
          e.relation !== 'member_of' && e.relation !== 'layered_as') return false;
        return true;
      });
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
    var reheatBtn = $('gf-reheat');
    if (reheatBtn) reheatBtn.addEventListener('click', reheat);
    var orbitBtn = $('gf-orbit');
    if (orbitBtn) orbitBtn.addEventListener('click', function () { toggleOrbit(orbitBtn); });
    var bridgesBtn = $('gf-bridges');
    if (bridgesBtn) bridgesBtn.addEventListener('click', function () { toggleBridges(bridgesBtn); });
    var expandBtn = $('gf-expand');
    if (expandBtn) expandBtn.addEventListener('click', expandSelected);
    var focusBtn = $('gf-focus');
    if (focusBtn) focusBtn.addEventListener('click', focusSelected);
    var linkBtn = $('gf-link');
    if (linkBtn) linkBtn.addEventListener('click', copyDeepLink);
    var png = $('gf-png');
    if (png) png.addEventListener('click', function () {
      if (S.engine === '3d') { snapshot3D(); return; }
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
      else if (e.key === 'Enter') {
        if (S.selected && S.engine === '3d') { e.preventDefault(); expandSelected(); }
      }
      else if (e.key === 'Backspace') {
        e.preventDefault();
        var prev = S.history.pop();
        if (prev && byId[prev]) { if (S.engine === '3d') onSelect3D(byId[prev], null); }
      }
      else if (e.key === 'l' || e.key === 'L') { var b = $('gf-names'); if (b && !b.disabled) b.click(); }
      else if (e.key === 'h' || e.key === 'H') { var h = $('gf-hulls'); if (h && !h.disabled) h.click(); }
      else if (e.key === 'f' || e.key === 'F') {
        if (S.engine === '3d' && S.selected) { e.preventDefault(); focusSelected(); return; }
        var f = $('gf-fit'); if (f && !f.disabled) f.click();
      }
      else if (e.key === 'r' || e.key === 'R') { if (S.engine === '3d') reheat(); }
      else if (e.key === 'o' || e.key === 'O') {
        if (S.engine === '3d') { var ob = $('gf-orbit'); if (ob && !ob.disabled) ob.click(); }
      }
      else if (e.key === 'b' || e.key === 'B') {
        var bb = $('gf-bridges'); if (bb && !bb.disabled) bb.click();
      }
      else if (e.key === 'e' || e.key === 'E') { if (S.engine === '3d' && S.selected) expandSelected(); }
      else if (e.key === 'c' || e.key === 'C') { if (S.selected) copyDeepLink(); }
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
  bindStagePointer();
  setEngineButtons();
  window.GF = {
    to3D: to3D, to2D: to2D, state: S,
    is3D: function () { return S.engine === '3d'; },
    expandSelected: expandSelected, focusSelected: focusSelected,
    reheat: reheat, toggleBridges: toggleBridges, toggleOrbit: toggleOrbit,
    copyDeepLink: copyDeepLink,
    context: function () { return { nodes: (S.raw || {}).nodes, edges: (S.raw || {}).links }; },
  };
})();
