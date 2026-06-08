/* Estorides front-end controller */
(function () {
  'use strict';

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  // ---- leaflet map ----
  const map = L.map('map', { zoomControl: true, worldCopyJump: true }).setView([20, 0], 2);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors',
  }).addTo(map);

  let mapMarkers = [];

  function clearMap() {
    mapMarkers.forEach((m) => map.removeLayer(m));
    mapMarkers = [];
  }

  function plotPoints(coords) {
    clearMap();
    if (!coords.length) return;
    const bounds = [];
    coords.forEach((c) => {
      const m = L.circleMarker([c.lat, c.lon], {
        radius: 6,
        color: c.color || '#5fb4ff',
        fillColor: c.color || '#5fb4ff',
        fillOpacity: 0.8,
        weight: 2,
      })
        .bindPopup(
          `<b>${c.label || ''}</b><br>` +
            `<small>${c.type || ''}</small><br>` +
            (c.value ? `<code>${c.value}</code><br>` : '') +
            (c.sources ? `<i>via: ${c.sources.join(', ')}</i><br>` : '') +
            // The "expand" button calls the intel resolver for this
            // entity and merges the new nodes into the D3 graph.
            // `c.expandKey` is `{type, value}`; missing for raw
            // observation coords where the type isn't an entity.
            (c.expandKey
              ? `<button class="map-expand" data-type="${c.expandKey.type}" data-value="${escapeAttr(c.expandKey.value)}">Resolve & expand</button>`
              : '')
        )
        .addTo(map);
      mapMarkers.push(m);
      bounds.push([c.lat, c.lon]);
    });
    if (bounds.length === 1) {
      map.setView(bounds[0], 6);
    } else {
      map.fitBounds(bounds, { padding: [40, 40] });
    }
    // Wire the resolve buttons (live, not on popup open).
    document.querySelectorAll('.map-expand').forEach((btn) => {
      btn.addEventListener('click', (ev) => {
        ev.preventDefault();
        const t = btn.getAttribute('data-type');
        const v = btn.getAttribute('data-value');
        expandNode(t, v);
      });
    });
  }

  // ---- tabs ----
  $$('.tab').forEach((t) => {
    t.addEventListener('click', () => {
      $$('.tab').forEach((x) => x.classList.remove('active'));
      $$('.tab-panel').forEach((x) => x.classList.remove('active'));
      t.classList.add('active');
      $('#tab-' + t.dataset.tab).classList.add('active');
    });
  });
  $$('.canvas-tab').forEach((t) => {
    t.addEventListener('click', () => {
      $$('.canvas-tab').forEach((x) => x.classList.remove('active'));
      $$('.map-canvas, .graph-canvas, .timeline-canvas').forEach((x) => x.classList.remove('active'));
      t.classList.add('active');
      // Panels are keyed by the `<name>-canvas` class, not by id (the map panel's
      // id is "map", not "map-canvas"), so select by class to stay consistent.
      const panel = $('.' + t.dataset.canvas + '-canvas');
      if (panel) panel.classList.add('active');
      if (t.dataset.canvas === 'map') map.invalidateSize();
      if (t.dataset.canvas === 'graph') drawGraph();
    });
  });

  // ---- run query ----
  $('#run-btn').addEventListener('click', runQuery);
  $('#query').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') runQuery();
  });
  $('#clear-btn').addEventListener('click', () => {
    $('#query').value = '';
    clearAll();
  });
  $('#discover-btn').addEventListener('click', startDiscover);
  $('#discover-stop').addEventListener('click', stopDiscover);

  // Live cross-search state. A run streams source results and pivoted
  // selectors over SSE so the panels fill within seconds instead of
  // blocking on the slowest source.
  let _runStream = null;
  let _runJobId = null;
  let _streamSeenSrc = new Set();
  let _streamSeenEnt = new Set();
  let _streamSrcCount = 0;
  let _streamEntCount = 0;
  // Accumulated payloads so the map, timeline and graph can be rebuilt
  // from the full set on every streamed update, exactly as the blocking
  // renderer did from one complete response.
  let _streamObsAll = [];
  let _streamEntsAll = [];

  // Rebuild the geospatial + temporal views from everything seen so far.
  // plotPoints clears and redraws from the full coord set, so feeding it
  // the accumulated observations makes the map grow as sources resolve.
  function replotStreamData() {
    // generated_at is required by renderTimeline (it builds a Date from it);
    // streamed data has no single timestamp, so stamp "now" in seconds.
    const data = {
      observations: _streamObsAll,
      entities: _streamEntsAll,
      generated_at: Date.now() / 1000,
    };
    plotPoints(buildMapCoords(data));
    renderTimeline(data);
  }

  function stopRunStream() {
    if (_runJobId) {
      fetch('/api/run/stream/stop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_id: _runJobId }),
      }).catch(() => { /* best effort */ });
    }
    if (_runStream) {
      _runStream.close();
      _runStream = null;
    }
    _runJobId = null;
  }

  async function runQuery() {
    const q = $('#query').value.trim();
    if (!q) return;
    stopRunStream();
    setStatus('running…');
    $('#run-btn').disabled = true;
    // Fresh panels for the streamed run.
    $('#results-list').innerHTML = '';
    $('#entities-list').innerHTML = '';
    $('#analysis-body').textContent = '';
    _streamSeenSrc = new Set();
    _streamSeenEnt = new Set();
    _streamSrcCount = 0;
    _streamEntCount = 0;
    _streamObsAll = [];
    _streamEntsAll = [];
    clearMap();

    let start;
    try {
      const r = await fetch('/api/run/stream/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q }),
      });
      start = await r.json();
      if (!r.ok || start.error) throw new Error(start.error || ('HTTP ' + r.status));
    } catch (e) {
      // Streaming layer unavailable — fall back to the blocking run so
      // the feature degrades cleanly rather than failing.
      setStatus('stream unavailable, falling back…');
      return runQueryBlocking(q);
    }

    _runJobId = start.job_id;
    setStatus(`streaming · ${start.query_type || ''}`);
    _runStream = new EventSource(start.stream_url);
    _runStream.addEventListener('message', (ev) => {
      let d;
      try { d = JSON.parse(ev.data); } catch (_) { return; }
      if (d && d.type) handleRunStreamEvent(d);
    });
    _runStream.addEventListener('closed', () => {
      setStatus(`done · ${_streamSrcCount} sources · ${_streamEntCount} entities`);
      stopRunStream();
      $('#run-btn').disabled = false;
    });
    _runStream.onerror = () => { /* auto-reconnects; 'closed' ends the stream */ };
  }

  // Blocking fallback: the original one-shot render path.
  async function runQueryBlocking(q) {
    try {
      const r = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q }),
      });
      const data = await r.json();
      if (data.error) {
        setStatus('error: ' + data.error);
        return;
      }
      renderResult(data);
      setStatus(`done · ${data.sources_succeeded}/${data.sources_queried} sources · ${data.entities.length} entities`);
    } catch (e) {
      setStatus('error: ' + e.message);
    } finally {
      $('#run-btn').disabled = false;
    }
  }

  function handleRunStreamEvent(d) {
    switch (d.type) {
      case 'target_start':
        setStatus(`resolving ${d.target && d.target.value} (depth ${d.depth})`);
        break;
      case 'source_result':
        appendStreamObservation(d.observation);
        break;
      case 'entity':
        appendStreamEntity(d.entity, d.from);
        break;
      case 'target_done':
        if (d.analysis && d.analysis.content) {
          $('#analysis-meta').innerHTML = d.analysis.backend
            ? `<span class="pill">${escapeHTML(d.analysis.backend)}</span><span class="pill">${escapeHTML(d.analysis.model || '')}</span>`
            : '';
          $('#analysis-body').textContent = d.analysis.content;
        }
        if (d.graph) renderGraphSummary(d.graph);
        break;
      case 'fatal':
        setStatus('error: ' + (d.error || 'pivot failed'));
        break;
    }
  }

  function appendStreamObservation(obs) {
    if (!obs || !obs.source) return;
    if (_streamSeenSrc.has(obs.source)) return;
    _streamSeenSrc.add(obs.source);
    _streamSrcCount++;
    _streamObsAll.push(obs);
    const failed = obs.meta && obs.meta.error;
    const div = document.createElement('div');
    div.className = 'result-item' + (failed ? ' failed' : '');
    const status = (obs.meta && obs.meta.status) || (failed ? 'ERR' : '');
    const dur = obs.meta && obs.meta.cached ? ' (cached)' : '';
    div.innerHTML = `
      <div class="head">
        <span class="src">${escapeHTML(obs.source)}</span>
        <span class="cat">${escapeHTML(obs.category || '')}</span>
      </div>
      <pre>${escapeHTML(truncate(JSON.stringify(obs.parsed, null, 2) || (obs.meta && obs.meta.error) || '', 1200))}</pre>
      <div class="meta-line">${escapeHTML(String(status))}${dur}</div>
    `;
    $('#results-list').appendChild(div);
    $('#results-meta').innerHTML =
      `<span class="pill">${_streamSrcCount} sources</span>` +
      `<span class="pill">${_streamEntCount} entities</span>`;
    // Repaint the map/timeline from the full accumulated set so geolocated
    // sources (ipapi, ipinfo, nominatim) drop pins as they resolve.
    replotStreamData();
  }

  function appendStreamEntity(entity, from) {
    if (!entity || !entity.value) return;
    const sig = (entity.type || '') + '|' + (entity.value || '');
    if (_streamSeenEnt.has(sig)) return;
    _streamSeenEnt.add(sig);
    _streamEntCount++;
    _streamEntsAll.push(entity);
    const list = $('#entities-list');
    const div = document.createElement('div');
    div.className = 'entity';
    div.setAttribute('data-sig', sig);
    div.setAttribute('data-type', entity.type);
    div.setAttribute('data-value', entity.value);
    div.innerHTML = `
      <span class="type">${escapeHTML(entity.type || '')}</span>
      <span class="value">${escapeHTML(entity.value)}</span>
      <span class="srcs">via ${escapeHTML((from && from.value) || 'seed')}</span>
    `;
    div.addEventListener('click', () => {
      document.dispatchEvent(new CustomEvent('estorides:expand', {
        detail: { type: entity.type, value: entity.value },
      }));
    });
    list.appendChild(div);
    $('#results-meta').innerHTML =
      `<span class="pill">${_streamSrcCount} sources</span>` +
      `<span class="pill">${_streamEntCount} entities</span>`;
  }

  function clearAll() {
    clearMap();
    $('#results-list').innerHTML = '';
    $('#entities-list').innerHTML = '';
    $('#analysis-body').innerHTML = '';
    $('#graph-top').innerHTML = '';
    $('#results-meta').innerHTML = '';
    $('#analysis-meta').innerHTML = '';
    $('#graph-summary').innerHTML = '';
    if (window._d3svg) window._d3svg.remove();
    setStatus('idle');
  }

  function setStatus(s) {
    $('#footer-status').textContent = s;
    $('#last-run').textContent = s;
  }

  // ---- result rendering ----
  function renderResult(data) {
    // results panel
    const meta = data.sources_queried
      ? `<span class="pill">${data.sources_succeeded}/${data.sources_queried} sources</span>` +
        `<span class="pill">${data.entities.length} entities</span>` +
        `<span class="pill">${data.graph.summary?.node_count || 0} nodes</span>` +
        `<span class="pill">${data.graph.summary?.edge_count || 0} edges</span>`
      : '';
    $('#results-meta').innerHTML = meta;
    const list = $('#results-list');
    list.innerHTML = '';
    (data.observations || []).forEach((obs) => {
      const failed = obs.meta && obs.meta.error;
      const div = document.createElement('div');
      div.className = 'result-item' + (failed ? ' failed' : '');
      const status = obs.meta?.status || (failed ? 'ERR' : '');
      const dur = obs.meta?.cached ? ' (cached)' : '';
      div.innerHTML = `
        <div class="head">
          <span class="src">${obs.source}</span>
          <span class="cat">${obs.category}</span>
        </div>
        <pre>${escapeHTML(truncate(JSON.stringify(obs.parsed, null, 2) || obs.meta?.error || '', 1200))}</pre>
        <div class="meta-line">${status}${dur}${obs.meta?.attempts ? ` · ${obs.meta.attempts} attempt(s)` : ''}</div>
      `;
      list.appendChild(div);
    });

    // entities
    renderEntities(data.entities || []);

    // analysis
    const a = data.analysis || {};
    $('#analysis-meta').innerHTML = a.backend
      ? `<span class="pill">${a.backend}</span><span class="pill">${a.model || ''}</span>`
      : '';
    $('#analysis-body').textContent = a.content || '(no analysis)';

    // graph
    renderGraphSummary(data.graph);

    // map
    plotPoints(buildMapCoords(data));

    // timeline
    renderTimeline(data);
  }

  // ---- v1.1: click-to-expand ----
  // Called from two places:
  //   1. The "Resolve & expand" button in a Leaflet popup.
  //   2. A click on a row in the Entities tab.
  //   3. A `document` CustomEvent('estorides:expand', {detail:{type,value}})
  //      fired by the v1.2 background discoverer when it streams
  //      a new entity into the panel.
  // Hits /api/intel/resolve?type=...&id=... and merges the
  // returned nodes/links into both the D3 graph AND the map.
  // Cached by the server (24h TTL) so a re-click is instant.
  document.addEventListener('estorides:expand', (ev) => {
    const d = ev.detail || {};
    if (d.type && d.value) {
      expandNode(d.type, d.value);
    }
  });
  let _expanding = false;
  async function expandNode(type, value) {
    if (_expanding) return;
    _expanding = true;
    setStatus(`expanding ${type}:${value}...`);
    let payload;
    try {
      const r = await fetch('/api/intel/resolve?type=' +
        encodeURIComponent(type) + '&id=' + encodeURIComponent(value));
      payload = await r.json();
    } catch (e) {
      setStatus('expand failed: ' + e);
      _expanding = false;
      return;
    }
    if (payload.error) {
      setStatus('expand: ' + payload.error);
      _expanding = false;
      return;
    }
    const added = await mergeExpansionIntoGraph(payload);
    setStatus(`expanded ${type}:${value} → +${added.nodes} nodes, +${added.links} links`);
    _expanding = false;
  }

  // Merge a /api/intel/resolve response into the current D3 graph
  // and Leaflet map. Idempotent: re-clicking the same node won't
  // duplicate edges. Returns {nodes, links} counts of what was
  // actually added.
  function mergeExpansionIntoGraph(payload) {
    const nodes = payload.nodes || [];
    const links = payload.links || [];
    // Dedupe by id (so a re-click doesn't pile on duplicates).
    if (!window._expansionSeen) window._expansionSeen = new Set();
    const seen = window._expansionSeen;
    let newNodes = 0, newLinks = 0;
    nodes.forEach((n) => {
      if (seen.has(n.id)) return;
      seen.add(n.id);
      newNodes++;
    });
    links.forEach((l) => {
      const k = (l.source || '') + '|' + (l.target || '') + '|' + (l.relation || '');
      if (seen.has('link:' + k)) return;
      seen.add('link:' + k);
      newLinks++;
    });
    // Repaint D3 with the new nodes/links.
    if (newNodes || newLinks) {
      drawGraphWithExtras(nodes, links);
    }
    // For each new node, drop a marker on the map: precise lat/lon when
    // present, otherwise fall back to the country centroid so a resolved
    // country/geo node still enriches the map from a graph click.
    nodes.forEach((n) => {
      const p = n.properties || {};
      const lat = p.lat || p.latitude;
      const lon = p.lon || p.lng || p.longitude;
      let mlat, mlon;
      if (validCoord(parseFloat(lat), parseFloat(lon))) {
        mlat = parseFloat(lat); mlon = parseFloat(lon);
      } else {
        const cc = p.code || p.countryCode || p.country_code;
        if (cc && COUNTRY_CENTROIDS[cc]) { mlon = COUNTRY_CENTROIDS[cc][0]; mlat = COUNTRY_CENTROIDS[cc][1]; }
      }
      if (mlat == null) return;
      L.circleMarker([mlat, mlon], {
        radius: 5,
        color: '#ff9e64',
        fillColor: '#ff9e64',
        fillOpacity: 0.7,
        weight: 1,
        dashArray: '4 3',
      })
        .bindPopup(
          `<b>${escapeHTML(n.label || n.id)}</b><br>` +
          `<small>${escapeHTML(n.type || n.kind || '')}</small><br>` +
          (p.source ? `<i>via: ${escapeHTML(p.source)}</i>` : '')
        )
        .addTo(map);
      mapMarkers.push({ _expansion: true });
    });
    return { nodes: newNodes, links: newLinks };
  }

  // Re-draws the D3 graph with the original nodes/edges PLUS
  // any extras passed in (from a /api/intel/resolve call). The
  // extras are translated to the shape the drawGraph() function
  // already understands (id, label, type, color, size).
  function drawGraphWithExtras(extraNodes, extraLinks) {
    // Fetch the live graph and merge.
    return fetch('/api/graph?limit=300').then((r) => r.json()).then((data) => {
      const seen = new Set();
      const mergedNodes = [];
      (data.nodes || []).forEach((n) => {
        if (seen.has(n.id)) return;
        seen.add(n.id);
        mergedNodes.push(n);
      });
      (extraNodes || []).forEach((n) => {
        if (seen.has(n.id)) return;
        seen.add(n.id);
        // Freshly resolved nodes have no server-side cluster/level yet —
        // they join the rendered surface as un-clustered raw data and get
        // properly classified on the next full /api/graph fetch.
        mergedNodes.push({
          id: n.id, label: n.label || n.id, type: n.type || n.kind || 'entity',
          color: '#ff9e64', cluster_color: '#ff9e64', size: 6,
          cluster: -1, level: 'data', properties: n.properties || {},
        });
      });
      const mergedLinks = [];
      const seenLink = new Set();
      function pushLink(src, tgt, rel, inter) {
        const k = src + '|' + tgt + '|' + (rel || '');
        if (seenLink.has(k)) return;
        seenLink.add(k);
        mergedLinks.push({ source: src, target: tgt, relation: rel, inter_cluster: !!inter });
      }
      (data.edges || []).forEach((e) => pushLink(e.source, e.target, e.relation, e.inter_cluster));
      (extraLinks || []).forEach((e) => pushLink(e.source, e.target, e.relation));
      renderGraphCore(mergedNodes, mergedLinks, data.clusters || deriveClusters(mergedNodes));
    });
  }

  // =====================================================================
  // v1.3 — interactive graph intelligence (Maltego-style)
  // =====================================================================
  // Node colour = cluster, ring = intelligence tier. Left-click expands
  // (resolver + VT relationships) and selects; right-click opens the
  // transform menu; clicking a dashed inter-cluster link shows the
  // cross-referenced bridge tooltip.

  const LEVEL_COLORS = {
    data: '#6b7280', information: '#5fb4ff',
    intelligence: '#f6bd16', counter_intelligence: '#ff5c5c',
  };
  const LEVEL_STROKE = {
    data: 1, information: 2, intelligence: 3, counter_intelligence: 3.5,
  };
  const CLUSTER_PALETTE = [
    '#5B8FF9', '#5AD8A6', '#F6BD16', '#E8684A', '#6DC8EC',
    '#9270CA', '#FF9D4D', '#269A99', '#FF99C3', '#A0D911',
    '#FF6B6B', '#36CFC9', '#B37FEB', '#FFC53D', '#7CB305',
  ];

  // Map a graph node's type/kind onto a resolver/transform entity type.
  function resolverTypeFor(node) {
    const t = String(node.type || node.kind || '').toLowerCase();
    return ({
      ipv4: 'ip', ipv6: 'ip', ip: 'ip', domain: 'domain', email: 'email',
      cve: 'cve', btc_address: 'btc_address', eth_address: 'eth_address',
      md5: 'file', sha1: 'file', sha256: 'file', hash: 'file', file: 'file',
      person: 'person', company: 'company', org: 'company',
      country: 'country', username: 'username',
    }[t]) || t;
  }

  // ---- per-user intel-level overrides (persisted in localStorage) ----
  const LEVEL_STORE_KEY = 'estorides.levelOverrides';
  let _levelOverrides = {};
  try { _levelOverrides = JSON.parse(localStorage.getItem(LEVEL_STORE_KEY) || '{}'); }
  catch (_) { _levelOverrides = {}; }
  function saveLevelOverrides() {
    try { localStorage.setItem(LEVEL_STORE_KEY, JSON.stringify(_levelOverrides)); }
    catch (_) { /* storage may be unavailable; non-fatal */ }
  }
  function levelOf(node) {
    return _levelOverrides[node.id] || node.level || 'data';
  }

  function clusterColor(cid, clusters) {
    if (cid == null || cid < 0) return '#888';
    const c = (clusters || []).find((x) => x.id === cid);
    return (c && c.color) || CLUSTER_PALETTE[cid % CLUSTER_PALETTE.length];
  }

  // Build a clusters[] summary from a flat node list (used after a merge
  // when the server-side clusters array isn't carried along).
  function deriveClusters(nodes) {
    const agg = {};
    nodes.forEach((n) => {
      const cid = (n.cluster == null) ? -1 : n.cluster;
      if (cid < 0) return;
      const a = agg[cid] || (agg[cid] = { id: cid, size: 0, color: n.cluster_color || clusterColor(cid), label: '' });
      a.size++;
      if (!a.label) a.label = n.label || n.type || '';
    });
    return Object.values(agg);
  }

  // ---- floating overlays (tooltip + context menu) ----
  function hideTooltip() {
    const el = $('#graph-tooltip');
    if (el) el.style.display = 'none';
  }
  function showTooltipAt(ev, html) {
    const el = $('#graph-tooltip');
    if (!el) return;
    const host = $('#graph-canvas').getBoundingClientRect();
    el.innerHTML = html;
    el.style.display = 'block';
    el.style.left = (ev.clientX - host.left + 12) + 'px';
    el.style.top = (ev.clientY - host.top + 12) + 'px';
  }
  function hideContextMenu() {
    const el = $('#graph-context-menu');
    if (el) el.style.display = 'none';
  }

  // Cross-referenced tooltip for an inter-cluster (bridge) link.
  function showBridgeTooltip(ev, d, clusters) {
    const s = d.source, t = d.target;
    const cs = clusterColor(s.cluster, clusters), ct = clusterColor(t.cluster, clusters);
    const labelFor = (cid) => {
      const c = (clusters || []).find((x) => x.id === cid);
      return c ? (c.label || ('cluster ' + cid)) : ('cluster ' + cid);
    };
    showTooltipAt(ev, `
      <div class="tt-title">Cross-reference</div>
      <div class="tt-row"><span class="tt-chip" style="background:${cs}">${escapeHTML(labelFor(s.cluster))}</span>
        <span class="tt-rel">${escapeHTML(d.relation || 'related')}</span>
        <span class="tt-chip" style="background:${ct}">${escapeHTML(labelFor(t.cluster))}</span></div>
      <div class="tt-row"><b>${escapeHTML(s.label || s.id)}</b> <small>${escapeHTML(s.type || '')}</small></div>
      <div class="tt-row"><b>${escapeHTML(t.label || t.id)}</b> <small>${escapeHTML(t.type || '')}</small></div>
      <div class="tt-foot">bridges ${escapeHTML(labelFor(s.cluster))} ↔ ${escapeHTML(labelFor(t.cluster))}</div>
    `);
  }

  function showNodeTooltip(ev, d) {
    showTooltipAt(ev, `
      <div class="tt-title">${escapeHTML(d.label || d.id)}</div>
      <div class="tt-row"><small>${escapeHTML(d.type || '')}</small></div>
      <div class="tt-row"><span class="lvl-dot lvl-${levelOf(d)}"></span>${levelOf(d).replace('_', '-')}</div>
    `);
  }

  // ---- context menu: transforms grouped by intel tier ----
  function showContextMenu(ev, d) {
    const menu = $('#graph-context-menu');
    if (!menu) return;
    const type = resolverTypeFor(d);
    const value = d.label || d.id;
    const host = $('#graph-canvas').getBoundingClientRect();
    menu.innerHTML = '<div class="ctx-head">' + escapeHTML(value) +
      ' <small>' + escapeHTML(type) + '</small></div>' +
      '<div class="ctx-item" data-act="expand">⤴ Expand (resolve)</div>' +
      '<div class="ctx-item" data-act="focus">⊙ Focus</div>' +
      '<div class="ctx-sub">Set intel level</div>' +
      ['data', 'information', 'intelligence', 'counter_intelligence'].map((lv) =>
        '<div class="ctx-item ctx-level" data-level="' + lv + '"><span class="lvl-dot lvl-' + lv + '"></span>' +
        lv.replace('_', '-') + '</div>').join('') +
      '<div class="ctx-loading">loading transforms…</div>';
    menu.style.display = 'block';
    menu.style.left = (ev.clientX - host.left) + 'px';
    menu.style.top = (ev.clientY - host.top) + 'px';

    menu.querySelector('[data-act="expand"]').onclick = () => {
      hideContextMenu();
      const rt = resolverTypeFor(d);
      if (rt) expandNode(rt, value);
    };
    menu.querySelector('[data-act="focus"]').onclick = () => { hideContextMenu(); focusNode(d); };
    menu.querySelectorAll('.ctx-level').forEach((el) => {
      el.onclick = () => { setNodeLevel(d, el.getAttribute('data-level')); hideContextMenu(); };
    });

    // Lazy-load the type's transforms and append them grouped by tier.
    fetch('/api/transforms?type=' + encodeURIComponent(type))
      .then((r) => r.json())
      .then((j) => {
        const loading = menu.querySelector('.ctx-loading');
        if (loading) loading.remove();
        const tr = (j && j.transforms) || [];
        if (!tr.length) { menu.insertAdjacentHTML('beforeend', '<div class="ctx-empty">no transforms</div>'); return; }
        let lastTier = '';
        tr.forEach((t) => {
          if (t.tier !== lastTier) {
            lastTier = t.tier;
            menu.insertAdjacentHTML('beforeend',
              '<div class="ctx-sub ctx-tier-' + t.tier + '">' + t.tier.replace('_', '-') + '</div>');
          }
          const item = document.createElement('div');
          item.className = 'ctx-item ctx-transform';
          item.title = t.description || '';
          item.textContent = t.label;
          item.onclick = () => { hideContextMenu(); runTransform(t.id, type, value); };
          menu.appendChild(item);
        });
      })
      .catch(() => { /* menu still usable for expand/focus/level */ });
  }

  function setNodeLevel(d, level) {
    _levelOverrides[d.id] = level;
    saveLevelOverrides();
    d.level = level;
    applyLevelStyles();
    if (window._selectedNodeId === d.id) selectNode(d);
  }

  // Re-apply level rings to every rendered node circle.
  function applyLevelStyles() {
    if (!window._nodeSel) return;
    window._nodeSel.select('circle.node')
      .attr('stroke', (d) => LEVEL_COLORS[levelOf(d)])
      .attr('stroke-width', (d) => LEVEL_STROKE[levelOf(d)])
      .attr('stroke-dasharray', (d) => levelOf(d) === 'counter_intelligence' ? '2 2' : null);
  }

  function focusNode(d) {
    if (!window._d3svg || d.x == null) return;
    const container = $('#graph-canvas');
    const W = container.clientWidth, H = container.clientHeight;
    const t = d3.zoomIdentity.translate(W / 2 - d.x * 1.4, H / 2 - d.y * 1.4).scale(1.4);
    window._d3svg.transition().duration(400).call(d3.zoom().on('zoom', (e) => {
      window._d3svg.select('g').attr('transform', e.transform);
    }).transform, t);
  }

  // Run a Maltego-style transform and merge the result into the graph+map.
  async function runTransform(transformId, type, value) {
    setStatus(`transform ${transformId}…`);
    try {
      const r = await fetch('/api/transform/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transform_id: transformId, type, value }),
      });
      const payload = await r.json();
      if (payload.error) { setStatus('transform: ' + payload.error); return; }
      const added = await mergeExpansionIntoGraph(payload);
      setStatus(`transform ${transformId} → +${added.nodes} nodes, +${added.links} links`);
    } catch (e) {
      setStatus('transform failed: ' + e);
    }
  }

  // ---- side inspector panel ----
  function selectNode(d) {
    window._selectedNodeId = d.id;
    const panel = $('#graph-inspector');
    if (!panel) return;
    panel.style.display = 'block';
    $('#inspector-title').textContent = d.label || d.id;
    const type = resolverTypeFor(d);
    const value = d.label || d.id;
    const props = d.properties || {};
    const propRows = Object.keys(props).filter((k) => props[k] != null && props[k] !== '')
      .slice(0, 12)
      .map((k) => `<div class="insp-prop"><span>${escapeHTML(k)}</span><code>${escapeHTML(String(props[k]))}</code></div>`)
      .join('') || '<div class="insp-empty">no properties</div>';
    $('#inspector-body').innerHTML = `
      <div class="insp-meta">
        <span class="pill">${escapeHTML(d.type || '')}</span>
        <span class="pill"><span class="lvl-dot lvl-${levelOf(d)}"></span>${levelOf(d).replace('_', '-')}</span>
        ${d.cluster >= 0 ? `<span class="pill">cluster ${d.cluster}</span>` : ''}
      </div>
      <div class="insp-section">Intel level
        <select id="insp-level">
          ${['data', 'information', 'intelligence', 'counter_intelligence'].map((lv) =>
            `<option value="${lv}"${levelOf(d) === lv ? ' selected' : ''}>${lv.replace('_', '-')}</option>`).join('')}
        </select>
      </div>
      <div class="insp-section">Properties</div>
      ${propRows}
      <div class="insp-section">Transforms</div>
      <div id="insp-transforms" class="insp-transforms">loading…</div>
    `;
    $('#insp-level').onchange = (e) => setNodeLevel(d, e.target.value);
    fetch('/api/transforms?type=' + encodeURIComponent(type))
      .then((r) => r.json())
      .then((j) => {
        const box = $('#insp-transforms');
        if (!box) return;
        const tr = (j && j.transforms) || [];
        if (!tr.length) { box.innerHTML = '<div class="insp-empty">none for this type</div>'; return; }
        box.innerHTML = '';
        let lastTier = '';
        tr.forEach((t) => {
          if (t.tier !== lastTier) {
            lastTier = t.tier;
            box.insertAdjacentHTML('beforeend',
              `<div class="insp-tier ctx-tier-${t.tier}">${t.tier.replace('_', '-')}</div>`);
          }
          const b = document.createElement('button');
          b.className = 'insp-tbtn';
          b.title = t.description || '';
          b.textContent = t.label;
          b.onclick = () => runTransform(t.id, type, value);
          box.appendChild(b);
        });
      })
      .catch(() => { const box = $('#insp-transforms'); if (box) box.innerHTML = '<div class="insp-empty">unavailable</div>'; });
  }

  // ---- unified force-graph renderer (clusters + rings + interactions) ----
  function renderGraphCore(nodes, edges, clusters) {
    if (window._d3svg) window._d3svg.remove();
    hideContextMenu();
    hideTooltip();
    const container = $('#graph-canvas');
    const W = container.clientWidth, H = container.clientHeight;
    const svg = d3.select(container).append('svg').attr('width', W).attr('height', H);
    window._d3svg = svg;
    const g = svg.append('g');
    svg.call(d3.zoom().scaleExtent([0.15, 5]).on('zoom', (e) => g.attr('transform', e.transform)));
    svg.on('click', () => { hideContextMenu(); hideTooltip(); });

    const hullLayer = g.append('g').attr('class', 'hull-layer');
    const linkLayer = g.append('g').attr('class', 'link-layer');
    const nodeLayer = g.append('g').attr('class', 'node-layer');
    const labelLayer = g.append('g').attr('class', 'label-layer');

    const sim = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(edges).id((d) => d.id)
        .distance((d) => d.inter_cluster ? 130 : 55)
        .strength((d) => d.inter_cluster ? 0.12 : 0.5))
      .force('charge', d3.forceManyBody().strength(-150))
      .force('center', d3.forceCenter(W / 2, H / 2))
      .force('collide', d3.forceCollide(14));

    const link = linkLayer.selectAll('line').data(edges).enter().append('line')
      .attr('class', (d) => 'link' + (d.inter_cluster ? ' inter' : ''))
      .attr('stroke', (d) => d.inter_cluster ? '#ff9e64' : '#3a4a63')
      .attr('stroke-opacity', (d) => d.inter_cluster ? 0.9 : 0.35)
      .attr('stroke-width', (d) => d.inter_cluster ? 2 : 0.7)
      .attr('stroke-dasharray', (d) => d.inter_cluster ? '5 4' : null)
      .style('cursor', (d) => d.inter_cluster ? 'pointer' : 'default')
      .on('click', (ev, d) => { if (d.inter_cluster) { ev.stopPropagation(); showBridgeTooltip(ev, d, clusters); } });

    let _dragMoved = false;
    const node = nodeLayer.selectAll('g.node').data(nodes).enter().append('g')
      .attr('class', 'node')
      .style('cursor', 'pointer')
      .call(d3.drag()
        .on('start', (e, d) => { _dragMoved = false; if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
        .on('drag', (e, d) => { _dragMoved = true; d.fx = e.x; d.fy = e.y; })
        .on('end', (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }));
    window._nodeSel = node;

    node.append('circle')
      .attr('class', 'node')
      .attr('r', (d) => d.size || 6)
      .attr('fill', (d) => d.cluster_color || d.color || '#5fb4ff')
      .attr('stroke', (d) => LEVEL_COLORS[levelOf(d)])
      .attr('stroke-width', (d) => LEVEL_STROKE[levelOf(d)])
      .attr('stroke-dasharray', (d) => levelOf(d) === 'counter_intelligence' ? '2 2' : null);

    node
      .on('click', (ev, d) => {
        ev.stopPropagation();
        if (_dragMoved) return;
        selectNode(d);
        const rt = resolverTypeFor(d);
        if (rt) expandNode(rt, d.label || d.id);
      })
      .on('dblclick', (ev, d) => { ev.stopPropagation(); focusNode(d); })
      .on('contextmenu', (ev, d) => { ev.preventDefault(); ev.stopPropagation(); hideTooltip(); showContextMenu(ev, d); })
      .on('mouseover', (ev, d) => showNodeTooltip(ev, d))
      .on('mouseout', hideTooltip);

    const label = labelLayer.selectAll('text').data(nodes).enter().append('text')
      .attr('class', 'node-label')
      .attr('dx', 9).attr('dy', 4)
      .text((d) => d.label);

    function drawHulls() {
      const groups = {};
      nodes.forEach((n) => {
        if (n.cluster == null || n.cluster < 0 || n.x == null) return;
        (groups[n.cluster] = groups[n.cluster] || []).push([n.x, n.y]);
      });
      const data = Object.keys(groups).map((k) => {
        if (groups[k].length < 3) return null;
        const h = d3.polygonHull(groups[k]);
        return h ? { cluster: +k, hull: h } : null;
      }).filter(Boolean);
      const sel = hullLayer.selectAll('path').data(data, (d) => d.cluster);
      sel.enter().append('path').attr('class', 'hull')
        .merge(sel)
        .attr('d', (d) => 'M' + d.hull.join('L') + 'Z')
        .attr('fill', (d) => clusterColor(d.cluster, clusters))
        .attr('stroke', (d) => clusterColor(d.cluster, clusters));
      sel.exit().remove();
    }

    sim.on('tick', () => {
      link
        .attr('x1', (d) => d.source.x).attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x).attr('y2', (d) => d.target.y);
      node.attr('transform', (d) => `translate(${d.x},${d.y})`);
      label.attr('x', (d) => d.x).attr('y', (d) => d.y);
      drawHulls();
    });
  }

  // Low-level D3 redraw given a flat nodes/links list (back-compat shim).
  function _redrawGraph(nodes, edges) {
    renderGraphCore(nodes, edges, deriveClusters(nodes));
  }

  function setStatus(text) {
    const el = $('#footer-status');
    if (el) el.textContent = text;
  }

  function escapeAttr(s) {
    return String(s || '').replace(/"/g, '&quot;').replace(/</g, '&lt;');
  }

  // v1.1 — small country centroid table so we can drop entities
  // that only carry a country code (not a precise lat/lon) onto
  // the map. The list is intentionally short — the resolver
  // returns the precise coords for fresh lookups.
  const COUNTRY_CENTROIDS = {
    US: [-98.5795, 39.8283], GB: [-3.4360, 55.3781], DE: [10.4515, 51.1657],
    FR: [2.2137, 46.2276], RU: [105.3188, 61.5240], CN: [104.1954, 35.8617],
    JP: [138.2529, 36.2048], BR: [-51.9253, -14.2350], IN: [78.9629, 20.5937],
    AU: [133.7751, -25.2744], CA: [-106.3468, 56.1304], UA: [31.1656, 48.3794],
    MX: [-102.5528, 23.6345], ES: [-3.7492, 40.4637], IT: [12.5674, 41.8719],
    NL: [5.2913, 52.1326], SE: [18.6435, 60.1282], PL: [19.1451, 51.9194],
    TR: [35.2433, 38.9637], IR: [53.6880, 32.4279], IL: [34.8516, 31.0461],
    SA: [45.0792, 23.8859], AR: [-63.6167, -38.4161], ZA: [22.9375, -30.5595],
    KR: [127.7669, 35.9078], KP: [127.5101, 40.3399], TW: [120.9605, 23.6978],
    HK: [114.1694, 22.3193], SG: [103.8198, 1.3521], ID: [113.9213, -0.7893],
    NG: [8.6753, 9.0820], EG: [30.8025, 26.8206], KE: [37.9062, -0.0236],
    VE: [-66.5897, 6.4238], CL: [-71.5430, -35.6751], PE: [-75.0152, -9.1900],
    CO: [-74.2973, 4.5709], CU: [-77.7812, 21.5218], BO: [-64.9912, -16.2902],
    DO: [-70.1627, 18.7357], GT: [-90.2308, 15.7835], HN: [-86.2419, 15.1999],
    SV: [-88.8965, 13.7942], NI: [-85.2072, 12.8654], CR: [-83.7534, 9.7489],
    PA: [-80.7821, 8.5380], CH: [8.2275, 46.8182],
    AT: [14.5501, 47.5162], BE: [4.4699, 50.5039], DK: [9.5018, 56.2639],
    FI: [25.7482, 61.9241], NO: [8.4689, 60.4720], IE: [-7.6921, 53.1424],
    CZ: [15.4730, 49.8175], GR: [21.8243, 39.0742], PT: [-8.2245, 39.3999],
    HU: [19.5033, 47.1625], RO: [24.9668, 45.9432], BG: [25.4858, 42.7339],
    RS: [21.0059, 44.0165], HR: [15.2, 45.1], SK: [19.6990, 48.6690],
    SI: [14.9955, 46.1512], BA: [17.6791, 43.9159], AL: [20.1683, 41.1533],
    MK: [21.7453, 41.6086], MD: [28.3699, 47.4116], LT: [23.8813, 55.1694],
    LV: [24.6032, 56.8796], EE: [25.0136, 58.5953], IS: [-19.0208, 64.9631],
    LU: [6.1296, 49.8153], MT: [14.3754, 35.9375], CY: [33.4299, 35.1264],
  };

  function buildMapCoords(data) {
    const coords = [];
    // Geolocated observations (ipapi, nominatim, etc.).
    (data.observations || []).forEach((obs) => {
      const p = obs.parsed;
      if (!p) return;
      // Many parsers yield {lat, lon}
      if (typeof p.lat === 'string' || typeof p.lat === 'number') {
        if (validCoord(p.lat, p.lon)) {
          coords.push({
            lat: parseFloat(p.lat), lon: parseFloat(p.lon),
            label: obs.source, value: p.ip || p.query || obs.source,
            type: obs.category, sources: [obs.source],
            color: colorFor(obs.category),
            // No expandKey here — the marker is the source itself,
            // not an entity. The user can click on a matching entity
            // in the Entities tab to expand.
          });
        }
      }
      // Nominatim returns list
      if (Array.isArray(p)) {
        p.forEach((h) => {
          if (validCoord(h.lat, h.lon)) {
            coords.push({
              lat: parseFloat(h.lat), lon: parseFloat(h.lon),
              label: h.display_name || obs.source,
              type: obs.category, sources: [obs.source],
              color: colorFor(obs.category),
            });
          }
        });
      }
      // ipinfo.loc "lat,lon"
      if (p.loc && typeof p.loc === 'string') {
        const [la, lo] = p.loc.split(',').map(parseFloat);
        if (validCoord(la, lo)) {
          coords.push({
            lat: la, lon: lo, label: p.ip || obs.source,
            value: p.org, type: obs.category, sources: [obs.source],
            color: colorFor(obs.category),
            // ipinfo yields an ipv4 entity — make it expandable so
            // a click pulls the org/ASN/country from the resolver.
            expandKey: (p.ip && p.ip.match(/^(\d+\.){3}\d+$/))
              ? { type: 'ip', value: p.ip } : null,
          });
        }
      }
    });

    // Geolocated entities (parsed.lat / parsed.lon) AND country codes.
    // Many parsers stash coords on the entity itself (e.g. abuseipdb
    // has a "countryCode" field). The whole point of v1.1 is to
    // make entities first-class on the map, not just observations.
    (data.entities || []).forEach((e) => {
      // Already had lat/lon in the parser output?
      const lat = e.attributes && (e.attributes.lat || e.attributes.latitude);
      const lon = e.attributes && (e.attributes.lon || e.attributes.lng || e.attributes.longitude);
      if (validCoord(parseFloat(lat), parseFloat(lon))) {
        coords.push({
          lat: parseFloat(lat),
          lon: parseFloat(lon),
          label: e.value,
          value: e.value,
          type: e.type,
          sources: (e.sources && e.sources.length) ? e.sources : [e.source],
          color: colorForKind(
            ({domain:'domain',ipv4:'ip',ipv6:'ip',email:'person',cve:'vulnerability',
              btc_address:'crypto',eth_address:'crypto',asn:'infrastructure'}[e.type]) || e.type
          ),
          expandKey: { type: e.type, value: e.value },
        });
        return;
      }
      // Country code: stamp at the country centroid so the entity
      // shows up even if no lat/lng was reported. Cheap, deterministic.
      const cc = e.attributes && (e.attributes.countryCode || e.attributes.country_code);
      if (cc && COUNTRY_CENTROIDS[cc]) {
        const [lng, clat] = COUNTRY_CENTROIDS[cc];
        coords.push({
          lat: clat, lon: lng,
          label: e.value,
          value: e.value,
          type: e.type,
          sources: (e.sources && e.sources.length) ? e.sources : [e.source],
          color: colorForKind(
            ({domain:'domain',ipv4:'ip',ipv6:'ip',email:'person',cve:'vulnerability',
              btc_address:'crypto',eth_address:'crypto',asn:'infrastructure'}[e.type]) || e.type
          ),
          expandKey: { type: e.type, value: e.value },
        });
      }
    });
    return coords;
  }

  function validCoord(lat, lon) {
    return Number.isFinite(lat) && Number.isFinite(lon) && Math.abs(lat) <= 90 && Math.abs(lon) <= 180;
  }

  function colorFor(category) {
    const map = {
      '01. DNS Intelligence': '#5B8FF9',
      '02. IP & Infrastructure': '#F6BD16',
      '03. Web Intelligence': '#5AD8A6',
      '04. Social Media': '#E8684A',
      '05. Threat Intelligence': '#FF6B6B',
      '06. Breach Intelligence': '#9270CA',
      '07. Geolocation': '#6DC8EC',
      '08. Knowledge': '#FF99C3',
      '09. Wireless': '#269A99',
      '10. Blockchain': '#F99F80',
      '11. Paste & Leaks': '#C25B5B',
      '12. Visual': '#9FB40F',
      '13. Reputation': '#FF5C5C',
    };
    return map[category] || '#5fb4ff';
  }

  function renderEntities(entities) {
    const filterEl = $('#entity-filter');
    if (!filterEl.dataset.bound) {
      filterEl.addEventListener('input', () => renderEntities(entities));
      filterEl.dataset.bound = '1';
    }
    const f = filterEl.value.trim().toLowerCase();
    const list = $('#entities-list');
    list.innerHTML = '';
    const filtered = entities.filter((e) =>
      !f || e.type.toLowerCase().includes(f) || e.value.toLowerCase().includes(f)
    );
    filtered.slice(0, 800).forEach((e) => {
      const div = document.createElement('div');
      div.className = 'entity';
      // v1.1: make every entity clickable. The "Resolve & expand"
      // button on the right is just a visual cue that the row
      // is interactive. Click anywhere on the row to expand.
      div.setAttribute('data-type', e.type);
      div.setAttribute('data-value', e.value);
      div.innerHTML = `
        <span class="type">${e.type}</span>
        <span class="value">${escapeHTML(e.value)}</span>
        <span class="srcs">${e.source}</span>
        <button class="entity-expand" type="button" title="Resolve and add to graph">⤴</button>
      `;
      // Click anywhere on the row → expand
      div.addEventListener('click', (ev) => {
        ev.preventDefault();
        expandNode(e.type, e.value);
      });
      // Don't fire the row click when the button itself is pressed
      // (avoids double-handling and gives the button its own
      // affordance: focus / keyboard activation).
      const btn = div.querySelector('.entity-expand');
      if (btn) {
        btn.addEventListener('click', (ev) => {
          ev.stopPropagation();
          expandNode(e.type, e.value);
        });
      }
      list.appendChild(div);
    });
    if (!filtered.length) list.innerHTML = '<div style="color:var(--text-2);padding:12px;text-align:center">no entities</div>';
  }

  function renderGraphSummary(g) {
    const s = g.summary || {};
    $('#graph-summary').innerHTML = `
      <span class="pill">${s.node_count || 0} nodes</span>
      <span class="pill">${s.edge_count || 0} edges</span>
      <span class="pill">${s.components || 0} components</span>
      <span class="pill">density ${(s.density || 0).toFixed(4)}</span>
    `;
    const list = $('#graph-top');
    list.innerHTML = '<h4 style="font-size:11px;color:var(--text-2);text-transform:uppercase;margin-bottom:6px">Top entities (degree)</h4>';
    (g.top_entities || []).slice(0, 30).forEach((e) => {
      const row = document.createElement('div');
      row.className = 'row';
      row.innerHTML = `<span style="color:${colorForKind(e.kind)}">${e.type}</span><span class="v">${escapeHTML(e.value || '')}</span><span class="score">${(e.score || 0).toFixed(1)}</span>`;
      list.appendChild(row);
    });
  }

  function colorForKind(k) {
    return ({
      domain: '#5B8FF9', ip: '#F6BD16', person: '#9270CA',
      vulnerability: '#FF6B6B', crypto: '#F99F80',
      hash: '#C25B5B', infrastructure: '#FF99C3',
    }[k]) || '#9CA3AF';
  }

  function renderTimeline(data) {
    const tl = $('#timeline');
    tl.innerHTML = '<h3 style="color:var(--accent-2);margin-bottom:8px">Acquisition Timeline</h3>';
    const obs = (data.observations || []).slice().sort((a, b) => {
      return (a.meta?.status || 0) - (b.meta?.status || 0);
    });
    obs.forEach((o) => {
      const ev = document.createElement('div');
      ev.className = 'timeline-event';
      const when = new Date(data.generated_at * 1000).toISOString();
      ev.innerHTML = `
        <div class="when">${when}</div>
        <div class="what"><b>${o.source}</b> · <span style="color:var(--text-2)">${o.category}</span><br>
          <small style="color:var(--text-2)">${escapeHTML(truncate(JSON.stringify(o.parsed || o.meta?.error || ''), 200))}</small>
        </div>
      `;
      tl.appendChild(ev);
    });
  }

  // ---- D3 graph view ----
  async function drawGraph() {
    const r = await fetch('/api/graph?limit=300');
    const data = await r.json();
    if (!data.nodes || !data.nodes.length) return;
    window._graphData = { nodes: data.nodes, edges: data.edges, clusters: data.clusters || [] };
    renderGraphCore(data.nodes, data.edges, data.clusters || []);
  }

  // Inspector close + global dismiss of the floating overlays.
  (function wireGraphOverlays() {
    const close = $('#inspector-close');
    if (close) close.addEventListener('click', () => {
      const p = $('#graph-inspector');
      if (p) p.style.display = 'none';
      window._selectedNodeId = null;
    });
    document.addEventListener('click', (ev) => {
      const menu = $('#graph-context-menu');
      if (menu && menu.style.display !== 'none' && !menu.contains(ev.target)) hideContextMenu();
    });
    document.addEventListener('keydown', (ev) => {
      if (ev.key === 'Escape') { hideContextMenu(); hideTooltip(); }
    });
  })();

  // ---- v1.1: Cases tab ----
  const caseSearch = $('#case-search');
  if (caseSearch) {
    caseSearch.addEventListener('input', debounce(loadCases, 250));
    loadCases();
  }
  function loadCases() {
    const q = (caseSearch && caseSearch.value) || '';
    const list = $('#cases-list');
    if (!list) return;
    fetch('/api/cases?q=' + encodeURIComponent(q) + '&limit=50')
      .then((r) => r.json())
      .then((data) => {
        const cases = data.cases || [];
        if (!cases.length) {
          list.innerHTML = '<div class="empty">No cases yet — run a query to create one.</div>';
          return;
        }
        list.innerHTML = cases.map(renderCaseItem).join('');
        list.querySelectorAll('.case-item').forEach((el) => {
          el.addEventListener('click', () => {
            const id = el.getAttribute('data-id');
            fetch('/api/cases/' + id + '?full=1')
              .then((r) => r.json())
              .then((c) => alert(
                'Case ' + c.id + '\nQuery: ' + c.query +
                '\nType: ' + c.query_type + '\nEntities: ' + c.entity_count +
                '\nObservations: ' + c.obs_count + '\nStatus: ' + c.status
              ));
          });
        });
      });
  }
  function renderCaseItem(c) {
    const ts = new Date((c.created_at || 0) * 1000).toISOString().slice(0, 16).replace('T', ' ');
    // Saved cases get a visible bookmark pill so the operator can
    // scan the list for "things I came back to" at a glance.
    const saved = (c.notes || '').indexOf('[saved]') === 0;
    return (
      '<div class="case-item" data-id="' + escapeHTML(c.id) + '">' +
        '<div class="case-query">' + escapeHTML(truncate(c.query, 60)) + '</div>' +
        '<div class="case-meta">' +
          '<span class="pill">' + escapeHTML(c.query_type || 'unknown') + '</span>' +
          '<span class="pill">' + escapeHTML(c.status || '') + '</span>' +
          '<span class="pill">' + (c.entity_count || 0) + ' ents</span>' +
          '<span class="pill">' + (c.obs_count || 0) + ' obs</span>' +
          (saved ? '<span class="pill saved">saved</span>' : '') +
          '<span>' + escapeHTML(ts) + '</span>' +
        '</div>' +
        '<div class="case-actions">' +
          '<button class="ghost" data-action="save" data-id="' + escapeHTML(c.id) + '" type="button">' +
            (saved ? 'edit note' : 'save') +
          '</button>' +
          '<button class="ghost" data-action="diff" data-id="' + escapeHTML(c.id) + '" type="button">diff with...</button>' +
          '<button class="ghost" data-action="report" data-id="' + escapeHTML(c.id) + '" type="button">report</button>' +
        '</div>' +
      '</div>'
    );
  }
  function debounce(fn, ms) {
    let t;
    return function () {
      clearTimeout(t);
      t = setTimeout(() => fn.apply(null, arguments), ms);
    };
  }

  // ---- v1.1: Intel tab ----
  const intelBtn = $('#intel-resolve-btn');
  if (intelBtn) {
    intelBtn.addEventListener('click', () => {
      const t = $('#intel-type').value;
      const id = $('#intel-id').value.trim();
      const out = $('#intel-out');
      if (!id) { out.textContent = 'enter a value to resolve'; return; }
      out.textContent = 'resolving...';
      fetch('/api/intel/resolve?type=' + encodeURIComponent(t) + '&id=' + encodeURIComponent(id))
        .then((r) => r.json())
        .then((data) => {
          out.textContent = JSON.stringify(data, null, 2);
        })
        .catch((e) => { out.textContent = 'error: ' + e; });
    });
  }
  // Osiris probes
  document.querySelectorAll('.osiris-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const name = btn.getAttribute('data-osiris');
      let args = {};
      try { args = JSON.parse(btn.getAttribute('data-args') || '{}'); } catch (e) {}
      // Allow the user to override the placeholder value via prompt
      // for one-shot probes (e.g. "try your own number").
      const firstKey = Object.keys(args)[0];
      const current = firstKey ? args[firstKey] : '';
      const v = prompt('Value for ' + name + ' (' + firstKey + '):', current);
      if (v === null) return;
      if (firstKey) args[firstKey] = v;
      const out = $('#osiris-out');
      out.textContent = 'querying ' + name + '...';
      const params = new URLSearchParams(args);
      fetch('/api/osiris/' + name + '?' + params.toString())
        .then((r) => r.json())
        .then((data) => { out.textContent = JSON.stringify(data, null, 2); })
        .catch((e) => { out.textContent = 'error: ' + e; });
    });
  });

  // ---- utils ----
  function escapeHTML(s) {
    return String(s || '')
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function truncate(s, n) {
    s = String(s || '');
    return s.length > n ? s.slice(0, n) + '…' : s;
  }

  // ---- v1.3: case actions (save / diff / report) ----
  // Wire the per-case buttons rendered by renderCaseItem(). One
  // delegated listener so we don't rebind on every reload.
  const casesList = $('#cases-list');
  if (casesList) {
    casesList.addEventListener('click', (ev) => {
      const btn = ev.target.closest('button[data-action]');
      if (!btn) return;
      const id = btn.getAttribute('data-id');
      const action = btn.getAttribute('data-action');
      if (action === 'save')  return caseActionSave(id, btn);
      if (action === 'diff')  return caseActionDiff(id);
      if (action === 'report') return caseActionReport(id);
    });
  }

  // Bookmark a case. The endpoint prefixes the notes column with
  // "[saved]" so the bookmarked case surfaces in the list at a glance.
  function caseActionSave(id, btn) {
    const note = prompt('Optional note for this case:', '');
    if (note === null) return;  // user cancelled
    btn.disabled = true;
    fetch('/api/cases/' + encodeURIComponent(id) + '/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ note: note }),
    })
      .then((r) => r.json().then((j) => ({ ok: r.ok, j })))
      .then(({ ok, j }) => {
        if (!ok) throw new Error(j.error || 'save failed');
        btn.textContent = 'saved';
        loadCases();
      })
      .catch((e) => { alert('save failed: ' + e.message); btn.disabled = false; });
  }

  // Compare this case to another. The user picks the baseline; the
  // response is rendered inline in a diff panel under the case.
  function caseActionDiff(id) {
    const baseline = prompt(
      'Compare to which case id? (case A — the older one)\n\n' +
      'Tip: the id is in the URL or in the case detail.', ''
    );
    if (!baseline) return;
    fetch('/api/cases/diff?a=' + encodeURIComponent(baseline) +
          '&b=' + encodeURIComponent(id))
      .then((r) => r.json().then((j) => ({ ok: r.ok, j })))
      .then(({ ok, j }) => {
        if (!ok) throw new Error(j.error || 'diff failed');
        renderCaseDiffPanel(id, j);
      })
      .catch((e) => alert('diff failed: ' + e.message));
  }

  // Render the diff result below the case. The panel survives until
  // the user reloads the cases list (or opens another diff).
  function renderCaseDiffPanel(caseId, diff) {
    let panel = document.getElementById('case-diff-panel');
    if (!panel) {
      panel = document.createElement('div');
      panel.id = 'case-diff-panel';
      panel.className = 'case-diff-panel';
      casesList.parentElement.appendChild(panel);
    }
    const rows = (diff.added || []).slice(0, 25).map((e) =>
      `<li><span class="pill">${escapeHTML(e.type)}</span> <code>${escapeHTML(e.value)}</code></li>`
    ).join('');
    const removed = (diff.removed || []).slice(0, 10).map((e) =>
      `<li><span class="pill">${escapeHTML(e.type)}</span> <code>${escapeHTML(e.value)}</code></li>`
    ).join('') || '<li class="muted">none</li>';
    panel.innerHTML = `
      <div class="case-diff-head">
        <strong>Diff</strong> ${escapeHTML(diff.case_a)} → ${escapeHTML(diff.case_b)}
        <button class="ghost" id="case-diff-close" type="button">close</button>
      </div>
      <div class="case-diff-meta">
        +${diff.added_count} new · -${diff.removed_count} dropped · ${diff.common_count} common
      </div>
      <div class="case-diff-cols">
        <div>
          <h4>Added (${diff.added_count})</h4>
          <ul>${rows || '<li class="muted">none</li>'}</ul>
        </div>
        <div>
          <h4>Removed (${diff.removed_count})</h4>
          <ul>${removed}</ul>
        </div>
      </div>
    `;
    document.getElementById('case-diff-close').addEventListener('click', () => {
      panel.remove();
    });
  }

  // Render the Markdown report. We just dump the text into a modal
  // overlay — keeping it in-browser is enough; the CLI command produces
  // a file copy for sharing.
  function caseActionReport(id) {
    fetch('/api/cases/' + encodeURIComponent(id) + '?full=1')
      .then((r) => r.json())
      .then((c) => {
        const lines = [];
        lines.push('# ' + (c.query || 'unknown') + ' — case report');
        lines.push('');
        lines.push('Case id: `' + c.id + '` · status: `' + (c.status || '?') +
                   '` · entities: ' + (c.entity_count || 0) +
                   ' · observations: ' + (c.obs_count || 0));
        if (c.notes) lines.push('Notes: ' + c.notes);
        lines.push('');
        const byType = {};
        (c.entities || []).forEach((e) => {
          byType[e.type] = (byType[e.type] || 0) + 1;
        });
        lines.push('## Top entity types');
        Object.entries(byType).sort((a, b) => b[1] - a[1]).slice(0, 8).forEach(([t, n]) => {
          lines.push('- ' + t + ': ' + n);
        });
        lines.push('');
        // Use the CLI command as the canonical export — copy/paste ready.
        lines.push('## Export to file');
        lines.push('');
        lines.push('```');
        lines.push('estorides report ' + c.id + ' --out ' + c.id + '.md');
        if (c.notes && c.notes.indexOf('[saved]') === 0) {
          lines.push('# or compare against an older case:');
          lines.push('estorides report ' + c.id + ' --diff <older_case_id> --out ' + c.id + '.md');
        }
        lines.push('```');
        showReportModal(lines.join('\n'));
      })
      .catch((e) => alert('report failed: ' + e.message));
  }

  function showReportModal(text) {
    let modal = document.getElementById('estorides-modal');
    if (modal) modal.remove();
    modal = document.createElement('div');
    modal.id = 'estorides-modal';
    modal.className = 'estorides-modal';
    modal.innerHTML = `
      <div class="estorides-modal-body">
        <div class="estorides-modal-head">
          <strong>Case report (Markdown)</strong>
          <button class="ghost" id="estorides-modal-close" type="button">close</button>
        </div>
        <pre class="estorides-modal-pre">${escapeHTML(text)}</pre>
      </div>
    `;
    document.body.appendChild(modal);
    document.getElementById('estorides-modal-close').addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (ev) => {
      if (ev.target === modal) modal.remove();
    });
  }


  // ---- startup ----
  fetch('/api/status').then((r) => r.json()).then((s) => {
    $('#src-count').textContent = `${s.total} sources · ${s.categories.length} cats`;
  });
})();


// =====================================================================
// v1.2 — background discoverer (SSE-driven UI)
// =====================================================================
// Lives outside the IIFE so the EventSource instance and its state
// survive tab navigation; the inner module only owns the per-render
// helpers.

let _discoverEventSource = null;
let _discoverJobId = null;
let _discoverStep = 0;
let _discoverMax = 0;
let _discoverFound = 0;
// Cache of entities and observations streamed in so far — we
// merge them into the next render of results/graph/map rather
// than re-fetching from the server.
let _discoverEntities = [];

// The discoverer code lives outside the IIFE, so the module-private
// setStatus is not in scope here. Provide a global one that writes to the
// same footer element, guarded so a missing node can never throw.
function setStatus(text) {
  const el = document.getElementById('footer-status');
  if (el) el.textContent = text;
  const last = document.getElementById('last-run');
  if (last) last.textContent = text;
}

function setDiscoverProgress(step, found, max) {
  _discoverStep = step;
  _discoverFound = found;
  _discoverMax = max;
  const el = document.getElementById('discover-progress');
  if (!el) return;
  el.style.display = '';
  document.getElementById('discover-step').textContent = step;
  document.getElementById('discover-found').textContent = found;
  document.getElementById('discover-max').textContent = max;
}

function hideDiscoverProgress() {
  const el = document.getElementById('discover-progress');
  if (el) el.style.display = 'none';
}

function startDiscover() {
  const q = document.getElementById('query').value.trim();
  if (!q) return;
  // Cancel any prior stream first.
  stopDiscover();
  document.getElementById('discover-btn').disabled = true;
  setDiscoverProgress(0, 0, 0);
  // Reset the entity cache — the new job is a fresh surface.
  _discoverEntities = [];
  fetch('/api/discover/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      value: q,
      type: 'auto',
      max_depth: 2,
      max_steps: 30,
      max_entities: 1000,
      deadline_s: 20,
      parallel: 4,
    }),
  })
    .then((r) => r.json())
    .then((j) => {
      if (j.error) {
        setStatus('discover: ' + j.error);
        document.getElementById('discover-btn').disabled = false;
        return;
      }
      _discoverJobId = j.job_id;
      // Pull max_steps out of the response so the progress bar
      // knows where it is going.
      _discoverMax = j.max_steps || 0;
      setStatus(`discover started · ${j.job_id} · case ${j.case_id}`);
      // Open the SSE stream.
      _discoverEventSource = new EventSource('/api/discover/stream?job_id=' + j.job_id);
      _discoverEventSource.addEventListener('hello', (ev) => {
        try {
          const d = JSON.parse(ev.data);
          _discoverMax = d.cursor ? 0 : 0;  // we update on step events
        } catch (_) { /* ignore */ }
      });
      _discoverEventSource.addEventListener('message', (ev) => {
        let d;
        try { d = JSON.parse(ev.data); } catch (_) { return; }
        if (!d || !d.type) return;
        handleDiscoverEvent(d);
      });
      _discoverEventSource.addEventListener('closed', (ev) => {
        let d = {};
        try { d = JSON.parse(ev.data || '{}'); } catch (_) { /* ignore */ }
        setStatus(`discover ${d.status || 'done'} · ${d.steps_done || 0} steps · ${d.entities_seen || 0} entities`);
        hideDiscoverProgress();
        document.getElementById('discover-btn').disabled = false;
        if (_discoverEventSource) {
          _discoverEventSource.close();
          _discoverEventSource = null;
        }
        // Final render of all collected entities into the
        // entities tab and the graph.
        flushDiscoverEntities();
      });
      _discoverEventSource.onerror = () => {
        // EventSource auto-reconnects; the 'closed' event will
        // fire when the server actually ends the stream.
      };
    })
    .catch((e) => {
      setStatus('discover failed: ' + e);
      document.getElementById('discover-btn').disabled = false;
      hideDiscoverProgress();
    });
}

function stopDiscover() {
  if (_discoverJobId) {
    fetch('/api/discover/stop', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ job_id: _discoverJobId }),
    }).catch(() => { /* swallow — best effort */ });
  }
  if (_discoverEventSource) {
    _discoverEventSource.close();
    _discoverEventSource = null;
  }
  _discoverJobId = null;
  document.getElementById('discover-btn').disabled = false;
  hideDiscoverProgress();
}

function handleDiscoverEvent(ev) {
  switch (ev.type) {
    case 'started':
      setDiscoverProgress(0, 0, ev.max_steps || 0);
      break;
    case 'step_start':
      setDiscoverProgress(ev.step || _discoverStep, _discoverFound, _discoverMax);
      setStatus(`discover · resolving ${ev.target && ev.target.value} (depth ${ev.depth})`);
      break;
    case 'node_found':
      // Push the new entity into the cache; the next render
      // pass will pick it up. We also add it to the entities
      // tab inline so the user sees it appear in real time.
      _discoverFound++;
      if (ev.entity) {
        _discoverEntities.push(Object.assign(
          { source: 'discoverer' },
          ev.entity,
          { sources: [ev.from && ev.from.value].filter(Boolean) }
        ));
        addDiscoverEntityToTab(ev.entity, ev.from);
        // Also drop a marker on the map if it has coords.
        maybePlotDiscoverEntity(ev.entity);
      }
      setDiscoverProgress(_discoverStep, _discoverFound, _discoverMax);
      break;
    case 'step_done':
      // Bump the step counter; a small log line in status.
      break;
    case 'finished':
      setStatus(`discover done · ${ev.steps_done} steps · ${ev.entities_seen} entities`);
      hideDiscoverProgress();
      break;
    case 'error':
      setStatus('discover error: ' + ev.error);
      break;
  }
}

function addDiscoverEntityToTab(entity, from) {
  const list = document.getElementById('entities-list');
  if (!list) return;
  // Avoid duplicates with the simple in-memory check.
  const sig = (entity.type || '') + '|' + (entity.value || '');
  if (list.querySelector(`[data-sig="${CSS.escape(sig)}"]`)) return;
  const div = document.createElement('div');
  div.className = 'entity';
  div.setAttribute('data-sig', sig);
  div.setAttribute('data-type', entity.type);
  div.setAttribute('data-value', entity.value);
  div.innerHTML = `
    <span class="type">${entity.type}</span>
    <span class="value">${escapeHtml(entity.value)}</span>
    <span class="srcs">via ${escapeHtml((from && from.value) || 'discoverer')}</span>
    <button class="entity-expand" type="button" title="Resolve and add to graph">⤴</button>
  `;
  div.addEventListener('click', () => {
    // Defer to the in-module expandNode defined in the IIFE.
    // We can't call it directly because of the closure, so we
    // dispatch a custom event the module listens for.
    document.dispatchEvent(new CustomEvent('estorides:expand', {
      detail: { type: entity.type, value: entity.value }
    }));
  });
  list.appendChild(div);
}

function escapeHtml(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function maybePlotDiscoverEntity(entity) {
  // The discoverer mostly surfaces domains, not lat/lng. We can
  // still drop a flag at the country centroid if attributes
  // surface a country code; for now we skip — a follow-up
  // /api/intel/resolve click by the user gives a richer plot.
}

function flushDiscoverEntities() {
  // Trigger a redraw of the D3 graph with all collected nodes
  // so the user can see the full attack surface at once.
  if (!_discoverEntities.length) return;
  if (typeof window._drawDiscoverGraph === 'function') {
    window._drawDiscoverGraph(_discoverEntities);
  }
}
