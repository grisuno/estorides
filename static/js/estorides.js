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
            (c.sources ? `<i>via: ${c.sources.join(', ')}</i>` : '')
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

  async function runQuery() {
    const q = $('#query').value.trim();
    if (!q) return;
    setStatus('running…');
    $('#run-btn').disabled = true;

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

  function buildMapCoords(data) {
    const coords = [];
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
          });
        }
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
      div.innerHTML = `
        <span class="type">${e.type}</span>
        <span class="value">${escapeHTML(e.value)}</span>
        <span class="srcs">${e.source}</span>
      `;
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
    if (window._d3svg) window._d3svg.remove();
    const r = await fetch('/api/graph?limit=300');
    const data = await r.json();
    if (!data.nodes.length) return;

    const container = $('#graph-canvas');
    const W = container.clientWidth, H = container.clientHeight;
    const svg = d3.select(container).append('svg')
      .attr('width', W).attr('height', H);
    window._d3svg = svg;

    const g = svg.append('g');
    svg.call(d3.zoom().scaleExtent([0.2, 5]).on('zoom', (e) => g.attr('transform', e.transform)));

    const sim = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.edges).id((d) => d.id).distance(60).strength(0.4))
      .force('charge', d3.forceManyBody().strength(-120))
      .force('center', d3.forceCenter(W / 2, H / 2))
      .force('collide', d3.forceCollide(12));

    const link = g.selectAll('line').data(data.edges).enter().append('line')
      .attr('class', (d) => 'link ' + (d.relation || 'related-to'))
      .attr('stroke', (d) => d.relation === 'observed_by' ? '#ff9e64' : '#5fb4ff')
      .attr('stroke-opacity', 0.4)
      .attr('stroke-width', 0.5);

    const node = g.selectAll('circle').data(data.nodes).enter().append('circle')
      .attr('class', 'node')
      .attr('r', (d) => d.size || 5)
      .attr('fill', (d) => d.color || '#5fb4ff')
      .call(d3.drag()
        .on('start', (e, d) => { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
        .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
        .on('end', (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }));

    node.append('title').text((d) => `${d.type}: ${d.label}`);
    g.selectAll('text').data(data.nodes).enter().append('text')
      .attr('class', 'node-label')
      .attr('dx', 8).attr('dy', 4)
      .text((d) => d.label);

    sim.on('tick', () => {
      link
        .attr('x1', (d) => d.source.x).attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x).attr('y2', (d) => d.target.y);
      node.attr('cx', (d) => d.x).attr('cy', (d) => d.y);
      g.selectAll('text').attr('x', (d) => d.x).attr('y', (d) => d.y);
    });
  }

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

  // ---- startup ----
  fetch('/api/status').then((r) => r.json()).then((s) => {
    $('#src-count').textContent = `${s.total} sources · ${s.categories.length} cats`;
  });
})();
