/* Estorides front-end controller */
(function () {
  'use strict';

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  // ---- auth: attach the bearer token to every /api/* call when present ----
  // The token is rendered into <meta name="estorides-auth-token"> in index.html
  // when ESTORIDES_AUTH_TOKEN is set in the operator's environment. When the
  // meta tag is empty, this wrapper is a no-op (local-trust single-user mode).
  (function installAuthFetch() {
    const meta = document.querySelector('meta[name="estorides-auth-token"]');
    const token = meta ? (meta.getAttribute('content') || '').trim() : '';
    if (!token) return;
    const origFetch = window.fetch.bind(window);
    window.fetch = function (input, init) {
      init = init || {};
      init.headers = init.headers || {};
      // Headers may be a Headers instance, an object, or absent.
      const set = (k, v) => {
        if (init.headers instanceof Headers) init.headers.set(k, v);
        else init.headers[k] = v;
      };
      set('Authorization', 'Bearer ' + token);
      return origFetch(input, init);
    };
  })();

  const TELEMETRY = (function readTelemetry() {
    const fallback = { brand: 'Estorides', phases: [], shortcuts: [], tips: [] };
    const node = document.getElementById('estorides-telemetry');
    if (!node) return fallback;
    try {
      const parsed = JSON.parse(node.textContent || '{}');
      return Object.assign(fallback, parsed);
    } catch (e) {
      return fallback;
    }
  })();
  window.ESTORIDES_TELEMETRY = TELEMETRY;

  // ---- UX helpers (v1.4) ----
  function detectQueryTypeLocal(q) {
    q = String(q || '').trim();
    if (/^(\d{1,3}\.){3}\d{1,3}$/.test(q)) return 'ipv4';
    if (/^(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|::1)$/.test(q)) return 'ipv6';
    if (/^CVE-\d{4}-\d{4,}$/i.test(q)) return 'cve';
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(q)) return 'email';
    if (/^1[A-Za-z0-9]{25,34}$/.test(q)) return 'btc_address';
    if (/^0x[a-fA-F0-9]{40}$/.test(q)) return 'eth_address';
    if (/^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$/.test(q)) return 'domain';
    return 'unknown';
  }
  function showToast(type, title, body, duration) {
    const stack = document.getElementById('toast-stack');
    if (!stack) return;
    const t = document.createElement('div');
    t.className = 'toast ' + (type || 'info');
    t.innerHTML = '<div class="toast-title">' + escapeHTML(title) + '</div>' +
                  '<div class="toast-body">' + escapeHTML(body) + '</div>';
    stack.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; setTimeout(() => t.remove(), 250); }, duration || 3500);
  }
  function updateQueryChip(type) {
    const chip = document.getElementById('query-chip');
    if (!chip) return;
    if (type && type !== 'unknown') {
      chip.textContent = type;
      chip.classList.remove('hidden');
    } else {
      chip.classList.add('hidden');
    }
  }
  function setRunProgress(current, total) {
    const wrap = document.getElementById('run-progress');
    const bar = document.getElementById('run-progress-bar');
    const txt = document.getElementById('run-progress-text');
    if (!wrap || !bar || !txt) return;
    if (total > 0) {
      wrap.style.display = 'flex';
      const pct = Math.min(100, Math.round((current / total) * 100));
      bar.style.width = pct + '%';
      txt.textContent = current + ' / ' + total;
      wrap.setAttribute('aria-busy', current < total ? 'true' : 'false');
      wrap.setAttribute('aria-valuenow', String(pct));
      wrap.setAttribute('aria-valuetext', current + ' of ' + total + ' sources, ' + pct + '%');
    } else {
      wrap.style.display = 'none';
      bar.style.width = '0%';
      txt.textContent = '0 / 0';
      wrap.setAttribute('aria-busy', 'false');
      wrap.removeAttribute('aria-valuenow');
    }
  }
  function showEmptyState(show) {
    const el = document.getElementById('results-empty');
    const filters = document.getElementById('result-filters');
    if (el) el.style.display = show ? 'flex' : 'none';
    if (filters) filters.style.display = show ? 'none' : 'flex';
  }
  function summariseObservation(obs) {
    const p = obs.parsed;
    if (obs.meta && obs.meta.error) return { lines: ['Source returned an error'], error: true };
    if (p == null) return { lines: ['No structured data returned'], error: false };
    if (Array.isArray(p)) {
      const lines = ['Array with ' + p.length + ' item(s)'];
      p.slice(0, 3).forEach((it, i) => lines.push('  #' + (i + 1) + ': ' + truncate(JSON.stringify(it), 120)));
      return { lines, error: false };
    }
    if (typeof p === 'object') {
      const keys = Object.keys(p).slice(0, 6);
      const lines = keys.map((k) => {
        let v = p[k];
        if (v == null) return k + ': —';
        if (typeof v === 'object') return k + ': ' + (Array.isArray(v) ? '[' + v.length + ']' : '{object}');
        return k + ': ' + truncate(String(v), 120);
      });
      if (Object.keys(p).length > 6) lines.push('... and ' + (Object.keys(p).length - 6) + ' more fields');
      return { lines, error: false };
    }
    return { lines: [String(p)], error: false };
  }
  function buildResultCard(obs) {
    const failed = obs.meta && obs.meta.error;
    const summary = summariseObservation(obs);
    const div = document.createElement('div');
    div.className = 'result-card' + (failed ? ' failed' : '');
    div.setAttribute('data-source', obs.source || '');
    div.setAttribute('data-category', obs.category || '');
    div.setAttribute('data-status', failed ? 'error' : 'ok');
    const status = (obs.meta && obs.meta.status) || (failed ? 'ERR' : 'OK');
    const dur = obs.meta && obs.meta.cached ? 'cached' : '';
    const bodyId = 'rc-body-' + Math.random().toString(36).slice(2, 9);
    div.innerHTML = `
      <div class="card-head">
        <div>
          <div class="src">${escapeHTML(obs.source)}</div>
          <div class="cat">${escapeHTML(obs.category || '')}</div>
        </div>
        <div class="card-actions">
          <span class="badge">${escapeHTML(String(status))}${dur ? ' · ' + dur : ''}</span>
          <button class="ghost" type="button" data-toggle="${bodyId}">show JSON</button>
        </div>
      </div>
      <div class="card-body" id="${bodyId}">
        <div class="summary">
          ${summary.error ? '<span class="none">' + escapeHTML(summary.lines[0]) + '</span>' :
            '<ul>' + summary.lines.map((l) => '<li>' + escapeHTML(l) + '</li>').join('') + '</ul>'}
        </div>
        <pre>${escapeHTML(truncate(JSON.stringify(obs.parsed, null, 2) || (obs.meta && obs.meta.error) || '', 1800))}</pre>
        <div class="meta-line">
          <span>${escapeHTML(String(status))}</span>
          ${dur ? '<span>' + dur + '</span>' : ''}
          ${obs.meta && obs.meta.attempts ? '<span>' + obs.meta.attempts + ' attempt(s)</span>' : ''}
        </div>
      </div>
    `;
    div.querySelector('.card-head').addEventListener('click', () => div.classList.toggle('open'));
    const toggle = div.querySelector('[data-toggle]');
    if (toggle) {
      toggle.addEventListener('click', (ev) => {
        ev.stopPropagation();
        div.classList.toggle('open');
        toggle.textContent = div.classList.contains('open') ? 'hide JSON' : 'show JSON';
      });
    }
    return div;
  }
  function populateCategoryFilter(categories) {
    const sel = document.getElementById('result-filter-cat');
    if (!sel) return;
    const existing = new Set(Array.from(sel.options).map((o) => o.value));
    categories.forEach((c) => { if (c && !existing.has(c)) { const o = document.createElement('option'); o.value = c; o.textContent = c; sel.appendChild(o); existing.add(c); } });
  }
  function applyResultFilters() {
    const text = (document.getElementById('result-filter-text') && document.getElementById('result-filter-text').value || '').toLowerCase();
    const cat = (document.getElementById('result-filter-cat') && document.getElementById('result-filter-cat').value) || '';
    const status = (document.getElementById('result-filter-status') && document.getElementById('result-filter-status').value) || '';
    const cards = document.querySelectorAll('#results-list .result-card');
    cards.forEach((card) => {
      const matchText = !text || (card.textContent || '').toLowerCase().includes(text);
      const matchCat = !cat || card.getAttribute('data-category') === cat;
      const matchStatus = !status || card.getAttribute('data-status') === status;
      card.style.display = (matchText && matchCat && matchStatus) ? '' : 'none';
    });
  }
  function bindResultFilters() {
    const txt = document.getElementById('result-filter-text');
    const cat = document.getElementById('result-filter-cat');
    const st = document.getElementById('result-filter-status');
    if (txt && !txt.dataset.bound) { txt.addEventListener('input', applyResultFilters); txt.dataset.bound = '1'; }
    if (cat && !cat.dataset.bound) { cat.addEventListener('change', applyResultFilters); cat.dataset.bound = '1'; }
    if (st && !st.dataset.bound) { st.addEventListener('change', applyResultFilters); st.dataset.bound = '1'; }
  }
  function showFriendlyError(message, retryFn) {
    const list = document.getElementById('results-list');
    if (!list) return;
    const div = document.createElement('div');
    div.className = 'friendly-error';
    div.innerHTML = '<span>' + escapeHTML(message) + '</span>';
    const btn = document.createElement('button');
    btn.className = 'retry-btn';
    btn.textContent = 'Retry';
    btn.addEventListener('click', () => { div.remove(); retryFn(); });
    div.appendChild(btn);
    list.appendChild(div);
  }
  function focusGraphNodeByValue(value) {
    const data = window._graphData;
    if (!data || !data.nodes || !data.nodes.length) return false;
    const node = data.nodes.find((n) => n.label === value || n.id === value);
    if (!node || typeof window.focusNode !== 'function') return false;
    window.focusNode(node);
    window.selectNode(node);
    return true;
  }
  function switchSidebarTab(index) {
    const tabs = $$('.tab');
    if (tabs[index]) tabs[index].click();
  }
  function switchCanvasTab(name) {
    const tab = $(`.canvas-tab[data-canvas="${name}"]`);
    if (tab) tab.click();
  }

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
  $('#query').addEventListener('input', () => {
    updateQueryChip(detectQueryTypeLocal($('#query').value));
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
  var _runStartTs = 0;

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
    updateQueryChip(detectQueryTypeLocal(q));
    showEmptyState(false);
    setRunProgress(0, window._totalSources || 0);
    showWorkingIndicator();
    bindResultFilters();
    stopRunStream();
    setStatus('starting');
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
    _runStartTs = Date.now();
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
    setStatus('streaming');
    _runStream = new EventSource(start.stream_url);
    _runStream.addEventListener('message', (ev) => {
      let d;
      try { d = JSON.parse(ev.data); } catch (_) { return; }
      if (d && d.type) handleRunStreamEvent(d);
    });
    _runStream.addEventListener('closed', () => {
      var elapsed = '';
      if (_runStartTs) {
        var sec = Math.round((Date.now() - _runStartTs) / 1000);
        elapsed = ' ' + (sec >= 60 ? Math.floor(sec / 60) + 'm ' + (sec % 60) + 's' : sec + 's');
      }
      setStatusDot('done');
      setStatus(_streamSrcCount + ' sources · ' + _streamEntCount + ' entities' + elapsed);
      setRunProgress(window._totalSources || _streamSrcCount, window._totalSources || _streamSrcCount);
      showToast('ok', 'Run complete', _streamSrcCount + ' sources · ' + _streamEntCount + ' entities');
      stopRunStream();
      $('#run-btn').disabled = false;
      hideWorkingIndicator();
      if (typeof loadCases === 'function') setTimeout(loadCases, 800);
    });
    _runStream.onerror = function() {
      setStatusDot('error');
    };
  }

  // Blocking fallback: the original one-shot render path.
  async function runQueryBlocking(q) {
    showWorkingIndicator();
    try {
      const r = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q }),
      });
      const data = await r.json();
      if (data.error) {
        setStatus('error: ' + data.error);
        showFriendlyError('Run failed: ' + data.error, () => runQueryBlocking(q));
        hideWorkingIndicator();
        return;
      }
      renderResult(data);
      renderTieredResults(data);
      setStatusDot('done');
      setStatus(data.sources_succeeded + '/' + data.sources_queried + ' sources · ' + data.entities.length + ' entities');
      showToast('ok', 'Run complete', data.sources_succeeded + '/' + data.sources_queried + ' sources · ' + data.entities.length + ' entities');
    } catch (e) {
      setStatusDot('error');
      setStatus('error: ' + e.message);
      showFriendlyError('Network error: ' + e.message, () => runQueryBlocking(q));
    } finally {
      $('#run-btn').disabled = false;
      setRunProgress(0, 0);
      hideWorkingIndicator();
    }
  }

  // Deep-search an entity through the full OSINT pipeline without
  // clearing existing data — appends and merges into current state.
  async function searchEntity(entityType, query) {
    if (!query) return;
    stopRunStream();
    showWorkingIndicator();
    setStatus('searching ' + query);
    $('#run-btn').disabled = true;
    var q = query.trim();
    try {
      var r = await fetch('/api/run/stream/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q, max_depth: 0, max_steps: 30 }),
      });
      var start = await r.json();
      if (!r.ok || start.error) throw new Error(start.error || 'HTTP ' + r.status);
    } catch (e) {
      setStatusDot('error');
      setStatus('search failed: ' + e.message);
      $('#run-btn').disabled = false;
      hideWorkingIndicator();
      return;
    }
    _runJobId = start.job_id;
    setStatus('searching ' + query);
    _runStream = new EventSource(start.stream_url);
    _runStream.addEventListener('message', function(ev) {
      var d;
      try { d = JSON.parse(ev.data); } catch (_) { return; }
      if (d && d.type) handleRunStreamEvent(d);
    });
    _runStream.addEventListener('closed', function() {
      setStatusDot('done');
      setStatus('done: ' + query + ' (' + _streamSrcCount + ' sources, ' + _streamEntCount + ' entities)');
      showToast('ok', 'Search complete', query + ': ' + _streamSrcCount + ' sources, ' + _streamEntCount + ' entities');
      stopRunStream();
      $('#run-btn').disabled = false;
      hideWorkingIndicator();
    });
    _runStream.onerror = function() {
      setStatusDot('error');
    };
  }

  function handleRunStreamEvent(d) {
    switch (d.type) {
      case 'target_start':
        setStatusDot('busy');
        setStatus('querying');
        break;
      case 'source_tick':
        setStatusDot('busy');
        if (d.source) {
          setStatus('querying ' + d.source);
        }
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
            ? '<span class="pill">' + escapeHTML(d.analysis.backend) + '</span><span class="pill">' + escapeHTML(d.analysis.model || '') + '</span>'
            : '';
          $('#analysis-body').textContent = d.analysis.content;
        }
        if (d.graph) renderGraphSummary(d.graph);
        break;
      case 'stopping':
        setStatus('stopping: ' + (d.reason || 'budget exhausted'));
        break;
      case 'fatal':
        setStatusDot('error');
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
    const card = buildResultCard(obs);
    $('#results-list').appendChild(card);
    populateCategoryFilter([obs.category]);
    applyResultFilters();
    setRunProgress(_streamSrcCount, window._totalSources || 0);
    $('#results-meta').innerHTML =
      `<span class="pill">${_streamSrcCount} sources</span>` +
      `<span class="pill">${_streamEntCount} entities</span>`;
    if (obs.meta && obs.meta.error) {
      showToast('warn', 'Source failed', obs.source + ' returned an error', 2500);
    }
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
    stopRunStream();
    clearMap();
    $('#results-list').innerHTML = '';
    $('#entities-list').innerHTML = '';
    $('#analysis-body').innerHTML = '';
    $('#graph-top').innerHTML = '';
    $('#results-meta').innerHTML = '';
    $('#analysis-meta').innerHTML = '';
    $('#graph-summary').innerHTML = '';
    if (window._d3svg) window._d3svg.remove();
    if (window._d3sim) window._d3sim.stop();
    window._expansionSeen = null;
    updateQueryChip('');
    setRunProgress(0, 0);
    showEmptyState(true);
    setStatusDot('idle');
    setStatus('idle');
    _streamSeenSrc = new Set();
    _streamSeenEnt = new Set();
    _streamSrcCount = 0;
    _streamEntCount = 0;
    _streamObsAll = [];
    _streamEntsAll = [];
    _runStartTs = 0;
  }

  function setStatus(s) {
    $('#footer-status').textContent = s;
    $('#last-run').textContent = s;
  }

  // ---- result rendering ----
  function renderResult(data) {
    showEmptyState(false);
    bindResultFilters();
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
    const categories = [];
    (data.observations || []).forEach((obs) => {
      list.appendChild(buildResultCard(obs));
      if (obs.category) categories.push(obs.category);
    });
    populateCategoryFilter(categories);
    applyResultFilters();

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
  // v1.3 — interactive graph intelligence (node expand + pivot transforms)
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
  const CLUSTER_PALETTE = (TELEMETRY.cluster_palette || [
    '#5B8FF9', '#5AD8A6', '#F6BD16', '#E8684A', '#6DC8EC',
    '#9270CA', '#FF9D4D', '#269A99', '#FF99C3', '#A0D911',
    '#FF6B6B', '#36CFC9', '#B37FEB', '#FFC53D', '#7CB305',
  ]);

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
  function showTooltipAt(ev, html, paint) {
    const el = $('#graph-tooltip');
    if (!el) return;
    const host = $('#graph-canvas').getBoundingClientRect();
    el.innerHTML = html;
    if (typeof paint === 'function') paint(el);
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
      <div class="tt-row"><span class="tt-chip" data-cluster-color></span>
        <span class="tt-rel">${escapeHTML(d.relation || 'related')}</span>
        <span class="tt-chip" data-cluster-color></span></div>
      <div class="tt-row"><b>${escapeHTML(s.label || s.id)}</b> <small>${escapeHTML(s.type || '')}</small></div>
      <div class="tt-row"><b>${escapeHTML(t.label || t.id)}</b> <small>${escapeHTML(t.type || '')}</small></div>
      <div class="tt-foot">bridges ${escapeHTML(labelFor(s.cluster))} ↔ ${escapeHTML(labelFor(t.cluster))}</div>
    `, (root) => {
      // CSP-safe: dynamic per-cluster colour goes through the CSSOM,
      // not an inline `style="background:…"` attribute. `style-src`
      // only governs attribute parsing, not property assignment.
      const chips = root.querySelectorAll('.tt-chip');
      if (chips[0]) chips[0].style.background = cs;
      if (chips[1]) chips[1].style.background = ct;
      // The labels were dropped to keep the template literal
      // attribute-free; restore them now via textContent.
      if (chips[0]) chips[0].textContent = labelFor(s.cluster);
      if (chips[1]) chips[1].textContent = labelFor(t.cluster);
    });
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
      '<div class="ctx-item" data-act="deepsearch">∘ Deep search</div>' +
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
    menu.querySelector('[data-act="deepsearch"]').onclick = () => {
      hideContextMenu();
      var q = value;
      // For known types, use the raw query format the orchestrator expects
      if (type === 'ip' || type === 'domain' || type === 'email' || type === 'cve') {
        q = value;
      }
      searchEntity(type, q);
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
  window.focusNode = focusNode;

  // Run a graph pivot transform and merge the result into the graph+map.
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
  window.selectNode = selectNode;

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

  // ---- Professional UI enhancements (relevance tiers, loading) ----

  function setStatusDot(state) {
    var el = $('#status-indicator');
    if (!el) return;
    el.className = 'status-dot ' + state;
  }

  function showWorkingIndicator() {
    setStatusDot('busy');
    $('#footer-status').classList.add('status-text-busy');
  }

  function hideWorkingIndicator() {
    setStatusDot('idle');
    $('#footer-status').classList.remove('status-text-busy');
  }

  function toggleTierSection(key, header) {
    const body = document.getElementById('tier-body-' + key);
    if (!body) return;
    const expanded = body.style.display !== 'none';
    body.style.display = expanded ? 'none' : 'block';
    header.setAttribute('aria-expanded', String(!expanded));
  }

  function renderTieredResults(data) {
    const list = $('#results-list');
    if (!list) return;
    const tiers = data.tiers;
    if (!tiers || typeof tiers !== 'object') return;
    var hasTiers = Object.keys(tiers).some(function(k) { return (tiers[k] || []).length > 0; });
    if (!hasTiers) return;
    var fragment = document.createDocumentFragment();
    var tierSummary = document.createElement('div');
    tierSummary.className = 'tier-summary';
    var tierLabels = {
      critical: { label: 'Critical', color: '#f43f5e', expanded: true },
      high: { label: 'High', color: '#f59e0b', expanded: true },
      medium: { label: 'Medium', color: '#eab308', expanded: false },
      low: { label: 'Low', color: '#6b7280', expanded: false },
      noise: { label: 'Noise', color: '#374151', expanded: false },
    };
    ['critical', 'high', 'medium', 'low', 'noise'].forEach(function(key) {
      var groups = tiers[key] || [];
      if (groups.length === 0) return;
      var cfg = tierLabels[key] || { label: key, color: '#888', expanded: false };
      var section = document.createElement('section');
      section.className = 'tier-section tier-' + key;
      var header = document.createElement('div');
      header.className = 'tier-header';
      header.setAttribute('role', 'button');
      header.setAttribute('tabindex', '0');
      header.setAttribute('aria-expanded', String(cfg.expanded));
      header.setAttribute('aria-controls', 'tier-body-' + key);
      header.innerHTML = '<span class="tier-label">' +
        escapeHTML(cfg.label) + '</span>' +
        '<span class="tier-badge" style="background:' + cfg.color + '">' + groups.length + '</span>';
      header.addEventListener('click', function() { toggleTierSection(key, header); });
      header.addEventListener('keydown', function(e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleTierSection(key, header); } });
      section.appendChild(header);
      var body = document.createElement('div');
      body.id = 'tier-body-' + key;
      body.className = 'tier-body fade-in';
      body.style.display = cfg.expanded ? 'block' : 'none';
      groups.forEach(function(group) {
        var card = document.createElement('div');
        card.className = 'tier-group';
        card.innerHTML = '<div class="tier-group-head">' +
          '<span class="tier-group-type">' + escapeHTML(group.type) + '</span>' +
          '<span class="tier-group-value">' + escapeHTML(group.value) + '</span>' +
          '<span class="tier-group-score">' + (group.relevance_score * 100).toFixed(0) + '%</span>' +
          '<span class="tier-group-sources">' + group.source_count + ' src</span>' +
          '</div>' +
          (group.key_findings && group.key_findings.length
            ? '<div class="tier-group-findings">' + group.key_findings.map(function(f) { return '<span class="finding">' + escapeHTML(f) + '</span>'; }).join('') + '</div>'
            : '') +
          (group.direct_match ? '<span class="tier-group-match">direct</span>' : '');
        body.appendChild(card);
      });
      section.appendChild(body);
      fragment.appendChild(section);
    });
    list.insertBefore(fragment, list.firstChild);
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
        $$('.entity').forEach((x) => x.classList.remove('highlight'));
        div.classList.add('highlight');
        expandNode(e.type, e.value);
        // If the graph already has this value, focus it.
        setTimeout(() => focusGraphNodeByValue(e.value), 120);
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
    if (!filtered.length) list.innerHTML = '<div class="empty-entities">no entities</div>';
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
    list.innerHTML = '<h4 class="graph-top-title">Top entities (degree)</h4>';
    (g.top_entities || []).slice(0, 30).forEach((e) => {
      const row = document.createElement('div');
      row.className = 'row';
      // CSP-safe: dynamic per-kind colour via CSSOM (style.color =),
      // not via an inline `style="…"` attribute that style-src would block.
      const kindEl = document.createElement('span');
      kindEl.style.color = colorForKind(e.kind);
      kindEl.textContent = e.type || '';
      const valEl = document.createElement('span');
      valEl.className = 'v';
      valEl.textContent = e.value || '';
      const scoreEl = document.createElement('span');
      scoreEl.className = 'score';
      scoreEl.textContent = (e.score || 0).toFixed(1);
      row.append(kindEl, valEl, scoreEl);
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
    var tl = $('#timeline');
    var eventsContainer = $('#timeline-events');
    if (!tl) return;
    var obs = (data.observations || []).slice();
    if (obs.length === 0) {
      eventsContainer.innerHTML = '<div class="empty-state" style="padding:24px;text-align:center"><p>No timeline data yet — run a query to populate.</p></div>';
      return;
    }
    // Assign observed_at if missing (backward compat for old runs)
    var now = Date.now() / 1000;
    obs.forEach(function(o, i) {
      if (!o.observed_at) {
        // Stagger by index so they don't all collapse to one second
        o.observed_at = (data.generated_at || now) + i * 0.001;
      }
    });
    obs.sort(function(a, b) { return a.observed_at - b.observed_at; });
    var minTs = obs[0].observed_at;
    var maxTs = obs[obs.length - 1].observed_at;
    var range = maxTs - minTs || 1;

    // Calculate which timestamp maps to which fractional position for events
    var slider = document.getElementById('timeline-slider');
    var minLabel = document.getElementById('timeline-min-label');
    var maxLabel = document.getElementById('timeline-max-label');
    var playBtn = document.getElementById('timeline-play-btn');
    var controls = document.getElementById('timeline-controls');

    // Build event DOM nodes
    eventsContainer.innerHTML = '';
    obs.forEach(function(o) {
      var ev = document.createElement('div');
      ev.className = 'timeline-event';
      var ts = o.observed_at;
      var d = new Date(ts * 1000);
      var timeStr = d.toISOString().replace('T', ' ').replace('Z', '');
      var frac = ((ts - minTs) / range);
      ev.setAttribute('data-t', String(ts));
      ev.setAttribute('data-frac', String(frac));
      ev.innerHTML =
        '<div class="when">' + timeStr + '</div>' +
        '<div class="what"><b>' + escapeHTML(o.source) + '</b> · <span class="timeline-meta">' + escapeHTML(o.category) + '</span><br>' +
        '  <small class="timeline-meta">' + escapeHTML(truncate(JSON.stringify(o.parsed || o.meta?.error || ''), 200)) + '</small>' +
        '</div>';
      eventsContainer.appendChild(ev);
    });

    // Show controls and set up slider
    controls.style.display = '';
    function fmtTime(ts) {
      var d2 = new Date(ts * 1000);
      return d2.toISOString().replace('T', ' ').substring(0, 19);
    }
    minLabel.textContent = fmtTime(minTs);
    maxLabel.textContent = fmtTime(maxTs);

    // Filter events by slider position
    var _timelinePlaying = false;
    var _timelineInterval = null;

    function filterTimeline(fracVal) {
      var cutoff = minTs + fracVal * range;
      var all = eventsContainer.querySelectorAll('.timeline-event');
      var visible = 0;
      all.forEach(function(el) {
        var t = parseFloat(el.getAttribute('data-t'));
        if (t <= cutoff) {
          el.classList.remove('filtered-out');
          visible++;
        } else {
          el.classList.add('filtered-out');
        }
      });
      // Update label to show "N / M visible"
    }

    slider.oninput = function() {
      var fracVal = parseInt(this.value, 10) / 100;
      filterTimeline(fracVal);
    };
    slider.value = '100';
    // Show all by default

    playBtn.onclick = function() {
      if (_timelinePlaying) {
        _timelinePlaying = false;
        clearInterval(_timelineInterval);
        playBtn.textContent = '\u25B6';
        return;
      }
      _timelinePlaying = true;
      playBtn.textContent = '\u23F8';
      slider.value = '0';
      filterTimeline(0);
      _timelineInterval = setInterval(function() {
        var cur = parseInt(slider.value, 10);
        if (cur >= 100) {
          clearInterval(_timelineInterval);
          _timelinePlaying = false;
          playBtn.textContent = '\u25B6';
          return;
        }
        slider.value = String(Math.min(100, cur + 2));
        filterTimeline(cur + 2);
      }, 200);
    };
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
  showEmptyState(true);
  bindResultFilters();

  // Example chips in the empty state fill the query box.
  document.querySelectorAll('.example-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      $('#query').value = chip.textContent;
      updateQueryChip(detectQueryTypeLocal(chip.textContent));
      $('#query').focus();
    });
  });

  // Onboarding: show once per browser.
  document.addEventListener('DOMContentLoaded', function() {
    var splash = document.getElementById('splash-screen');
    if (splash) {
      setTimeout(function() { splash.classList.add('hidden'); }, 1500);
    }
  });

  (function initOnboarding() {
    const seen = localStorage.getItem('estorides.onboarding');
    const overlay = document.getElementById('onboarding');
    if (!seen && overlay) {
      overlay.style.display = 'flex';
      document.getElementById('onboarding-start').addEventListener('click', () => {
        localStorage.setItem('estorides.onboarding', '1');
        overlay.style.display = 'none';
      });
      document.getElementById('onboarding-skip').addEventListener('click', () => {
        localStorage.setItem('estorides.onboarding', '1');
        overlay.style.display = 'none';
      });
    }
  })();

  // Keyboard shortcuts.
  document.addEventListener('keydown', (ev) => {
    const tag = (ev.target && ev.target.tagName) || '';
    const typing = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT';
    if (ev.key === '/' && !typing) { ev.preventDefault(); $('#query').focus(); }
    if (ev.key === '?' && !typing) { ev.preventDefault(); document.getElementById('kbd-help').style.display = 'flex'; }
    if (ev.key === 'Escape') {
      const kbd = document.getElementById('kbd-help');
      const onboard = document.getElementById('onboarding');
      if (kbd && kbd.style.display !== 'none') { kbd.style.display = 'none'; return; }
      if (onboard && onboard.style.display !== 'none') { onboard.style.display = 'none'; return; }
      if (!typing) clearAll();
    }
    if (ev.ctrlKey && ev.key === 'Enter') { ev.preventDefault(); runQuery(); }
    if (!typing) {
      if (ev.key >= '1' && ev.key <= '6') {
        ev.preventDefault();
        switchSidebarTab(parseInt(ev.key, 10) - 1);
      }
      if (ev.key === 'g' || ev.key === 'G') { ev.preventDefault(); switchCanvasTab('graph'); }
      if (ev.key === 'm' || ev.key === 'M') { ev.preventDefault(); switchCanvasTab('map'); }
      if (ev.key === 't' || ev.key === 'T') { ev.preventDefault(); switchCanvasTab('timeline'); }
    }
  });
  document.getElementById('kbd-help-close').addEventListener('click', () => {
    document.getElementById('kbd-help').style.display = 'none';
  });
  document.getElementById('kbd-help').addEventListener('click', (ev) => {
    if (ev.target.id === 'kbd-help') document.getElementById('kbd-help').style.display = 'none';
  });

  // Responsive sidebar toggle + resizable divider.
  function loadSidebarWidth() {
    try {
      var saved = localStorage.getItem('estorides.sidebarWidth');
      if (saved) {
        var w = parseInt(saved, 10);
        if (w >= 280 && w <= 900) {
          sidebarEl.style.width = w + 'px';
        }
      }
    } catch (_) {}
  }
  function saveSidebarWidth(w) {
    try { localStorage.setItem('estorides.sidebarWidth', String(w)); } catch (_) {}
  }
  function loadSidebarCollapsed() {
    try {
      if (localStorage.getItem('estorides.sidebarCollapsed') === '1') {
        sidebarEl.classList.add('sidebar-collapsed');
        sidebarEl.style.display = 'none';
      }
    } catch (_) {}
  }
  function saveSidebarCollapsed(v) {
    try { localStorage.setItem('estorides.sidebarCollapsed', v ? '1' : '0'); } catch (_) {}
  }

  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebarEl = document.getElementById('sidebar');
  if (sidebarToggle && sidebarEl) {
    loadSidebarWidth();
    loadSidebarCollapsed();
    sidebarToggle.addEventListener('click', function() {
      sidebarEl.classList.toggle('sidebar-collapsed');
      if (sidebarEl.classList.contains('sidebar-collapsed')) {
        sidebarEl.style.display = 'none';
        saveSidebarCollapsed(true);
      } else {
        sidebarEl.style.display = '';
        loadSidebarWidth();
        saveSidebarCollapsed(false);
      }
    });
  }

  // Resizable divider
  var resizeHandle = document.getElementById('sidebar-resize-handle');
  if (resizeHandle && sidebarEl) {
    var _resizing = false;
    var _startX = 0;
    var _startW = 0;

    resizeHandle.addEventListener('mousedown', function(ev) {
      _resizing = true;
      _startX = ev.clientX;
      _startW = sidebarEl.offsetWidth;
      document.body.classList.add('resizing');
      ev.preventDefault();
    });

    document.addEventListener('mousemove', function(ev) {
      if (!_resizing) return;
      var dx = ev.clientX - _startX;
      var newW = Math.max(280, Math.min(900, _startW + dx));
      sidebarEl.style.width = newW + 'px';
    });

    document.addEventListener('mouseup', function() {
      if (!_resizing) return;
      _resizing = false;
      document.body.classList.remove('resizing');
      saveSidebarWidth(sidebarEl.offsetWidth);
    });
  }

  fetch('/api/status').then((r) => r.json()).then((s) => {
    window._totalSources = s.total || 0;
    $('#src-count').textContent = `${s.total} sources · ${s.categories.length} cats`;
  });

  // ---- Fusion tab ----
  function switchSidebarTab(idx) {
    var tabs = document.querySelectorAll('.sidebar .tab');
    var panels = document.querySelectorAll('.sidebar .tab-panel');
    tabs.forEach(function(t, i) { t.classList.toggle('active', i === idx); });
    panels.forEach(function(p, i) { p.classList.toggle('active', i === idx); });
    // Reload fusion data when switching to fusion tab
    if (idx === 4) loadFusionTab();
  }

  function loadFusionTab() {
    loadFusionStats();
    loadFusionTopChanged();
    loadFusionSearch();
  }

  function loadFusionStats() {
    var container = $('#fusion-stats');
    if (!container) return;
    fetch('/api/fusion/stats').then(function(r) { return r.json(); }).then(function(s) {
      if (s.error) { container.innerHTML = '<div class="empty-state"><p>' + escapeHTML(s.error) + '</p></div>'; return; }
      container.innerHTML =
        '<div class="fusion-stat-card meta-row">' +
          '<span class="pill">' + (s.entities || 0) + ' entities</span>' +
          '<span class="pill">' + (s.observations || 0) + ' observations</span>' +
          '<span class="pill">' + (s.sources || 0) + ' sources</span>' +
          '<span class="pill">' + (s.properties || 0) + ' properties</span>' +
          '<span class="pill">' + (s.relationships || 0) + ' relationships</span>' +
          (s.multi_source_entities != null ? '<span class="pill">' + s.multi_source_entities + ' multi-source</span>' : '') +
        '</div>';
    }).catch(function(e) {
      container.innerHTML = '<div class="empty-state"><p>Stats unavailable: ' + escapeHTML(e.message) + '</p></div>';
    });
  }

  function loadFusionTopChanged() {
    var el = $('#fusion-top-changed');
    if (!el) return;
    fetch('/api/fusion/analytics/top-changed?days=7&limit=20').then(function(r) { return r.json(); }).then(function(j) {
      var entities = j.entities || [];
      if (!entities.length) { el.innerHTML = '<div class="empty-state"><p>No recent changes.</p></div>'; return; }
      el.innerHTML = entities.map(function(e) {
        return '<div class="case-item" data-eid="' + escapeAttr(e.entity_id) + '">' +
          '<span class="pill">' + escapeHTML(e.type) + '</span> ' +
          '<code>' + escapeHTML(e.value) + '</code> ' +
          '<span class="srcs">+' + e.new_observations + ' obs · +' + e.new_properties + ' props · +' + e.new_relationships + ' rels</span>' +
          '<button class="ghost view-btn" data-eid="' + escapeAttr(e.entity_id) + '">View</button>' +
          '</div>';
      }).join('');
      el.querySelectorAll('.view-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
          var eid = btn.getAttribute('data-eid');
          if (eid) loadFusionEntityDetail(eid);
        });
      });
    }).catch(function() { el.innerHTML = ''; });
  }

  function loadFusionSearch() {
    var termEl = $('#fusion-search-term');
    var typeEl = $('#fusion-search-type');
    var minSrcEl = $('#fusion-min-sources');
    var resultsEl = $('#fusion-results');
    if (!termEl || !typeEl || !minSrcEl || !resultsEl) return;

    function doSearch() {
      var term = termEl.value.trim();
      var etype = typeEl.value;
      var min_s = parseInt(minSrcEl.value, 10) || 0;
      var params = new URLSearchParams({ min_sources: String(min_s), limit: '50' });
      if (term) params.set('q', term);
      if (etype) params.set('type', etype);
      fetch('/api/fusion/entities?' + params.toString()).then(function(r) { return r.json(); }).then(function(j) {
        var entities = j.entities || [];
        if (!entities.length) { resultsEl.innerHTML = '<div class="empty-state"><p>No results.</p></div>'; return; }
        resultsEl.innerHTML = '<div class="meta-row"><span class="pill">' + entities.length + ' results</span></div>' +
          entities.map(function(e) {
            return '<div class="entity" data-eid="' + escapeAttr(e.id) + '">' +
              '<span class="type">' + escapeHTML(e.type) + '</span> ' +
              '<span class="value">' + escapeHTML(e.value) + '</span> ' +
              '<span class="srcs">' + e.source_count + ' sources · ' + e.observation_count + ' obs</span>' +
              '<button class="ghost view-btn" data-eid="' + escapeAttr(e.id) + '">View</button>' +
              '</div>';
          }).join('');
        resultsEl.querySelectorAll('.view-btn').forEach(function(btn) {
          btn.addEventListener('click', function() {
            var eid = btn.getAttribute('data-eid');
            if (eid) loadFusionEntityDetail(eid);
          });
        });
      }).catch(function() { resultsEl.innerHTML = '<div class="empty-state"><p>Search failed.</p></div>'; });
    }

    $('#fusion-search-btn').onclick = doSearch;
    termEl.addEventListener('keydown', function(ev) { if (ev.key === 'Enter') doSearch(); });
  }

  function loadFusionEntityDetail(eid) {
    var el = $('#fusion-entity-detail');
    if (!el || !eid) return;
    el.innerHTML = '<div class="meta-row"><span class="pill">Loading ' + escapeHTML(eid) + '...</span></div>';
    fetch('/api/fusion/analytics/entity-summary/' + encodeURIComponent(eid))
      .then(function(r) { return r.json(); })
      .then(function(s) {
        if (s.error) { el.innerHTML = '<div class="empty-state"><p>' + escapeHTML(s.error) + '</p></div>'; return; }
        el.innerHTML =
          '<div class="case-diff-panel" id="fusion-entity-panel">' +
          '<div class="diff-a">' +
          '<h4>' + escapeHTML(s.type) + ': <code>' + escapeHTML(s.value) + '</code></h4>' +
          '<p>Confidence: ' + (s.confidence * 100).toFixed(0) + '% · ' +
          'Sources: ' + s.source_count + ' · Observations: ' + s.observation_count + '</p>' +
          '<p>Intel level: <span class="lvl-dot lvl-' + s.intel_level + '"></span> ' + s.intel_level + '</p>' +
          '<p>Properties: ' + s.properties_summary.total + ' total, ' + s.properties_summary.corroborated + ' corroborated</p>' +
          '<p>Relationships: ' + s.relationships_summary.total + ' total, ' +
          s.relationships_summary.distinct_targets + ' distinct targets</p>' +
          '<p>First seen: ' + new Date((s.first_seen || 0) * 1000).toISOString().replace('T', ' ').substring(0, 19) +
          ' · Last seen: ' + new Date((s.last_seen || 0) * 1000).toISOString().replace('T', ' ').substring(0, 19) + '</p>' +
          '<p><strong>Sources:</strong> ' + (s.sources || []).join(', ') + '</p>' +
          '<p><strong>Property keys:</strong> ' + (s.properties_summary.keys || []).join(', ') + '</p>' +
          '<p><strong>Relationship types:</strong> ' + (s.relationships_summary.types || []).join(', ') + '</p>' +
          '<button class="ghost" onclick="document.getElementById(\'fusion-entity-detail\').innerHTML=\'\'">Close</button>' +
          '</div></div>';
      }).catch(function(e) {
        el.innerHTML = '<div class="empty-state"><p>Error: ' + escapeHTML(e.message) + '</p></div>';
      });
  }

  $('#fusion-refresh-btn').addEventListener('click', loadFusionTab);
  // Override switchSidebarTab to trigger fusion load on tab 5
  document.querySelectorAll('.sidebar .tabs .tab').forEach(function(tab, i) {
    tab.addEventListener('click', function() { switchSidebarTab(i); });
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
    <span class="type">${escapeHtml(entity.type || '')}</span>
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
