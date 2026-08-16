/* Estorides Source Manager — form-based YAML editor */

(function () {
  'use strict';

  /* ─── auth ─── */
  function authHeaders() {
    var meta = document.querySelector('meta[name="estorides-auth-token"]');
    var token = meta ? meta.getAttribute('content') : '';
    var h = { 'Content-Type': 'application/json' };
    if (token) h['Authorization'] = 'Bearer ' + token;
    return h;
  }

  function apiFetch(url, opts) {
    opts = opts || {};
    opts.headers = Object.assign(authHeaders(), opts.headers || {});
    return fetch(url, opts).then(function (r) {
      if (r.status === 401) throw new Error('Unauthorized — invalid or missing API token');
      if (!r.ok) return r.json().then(function (d) { throw new Error(d.error || r.statusText); });
      return r.json();
    });
  }

  /* ─── state ─── */
  var sources = [];
  var currentName = null; // the source being edited
  var isDirty = false;

  /* ─── DOM refs ─── */
  var $ = function (id) { return document.getElementById(id); };
  var listEl = $('src-list');
  var filterInput = $('src-filter-input');
  var form = $('source-form');
  var editorEmpty = $('editor-empty');
  var srcCount = $('src-count');
  var formStatus = $('form-status');
  var yamlPreview = $('yaml-preview-content');
  var deleteBtn = $('delete-btn');
  var saveBtn = $('save-btn');
  var isSystemApp = false; // binary sources are YAML-only in this editor

  /* ─── form fields ─── */
  var fields = {
    originalName: $('field-original-name'),
    name: $('field-name'),
    desc: $('field-desc'),
    cat: $('field-cat'),
    os: $('field-os'),
    parser: $('field-parser'),
    reqKey: $('field-req-key'),
    keyEnv: $('field-key-env'),
    contact: $('field-contact'),
    logsQueries: $('field-logs-queries'),
    toolUrl: $('field-tool-url'),
    toolMethod: $('field-tool-method'),
    toolHeaders: $('field-tool-headers'),
    toolParams: $('field-tool-params'),
    toolBody: $('field-tool-body'),
    pagStrategy: $('field-pag-strategy'),
    pagLimit: $('field-pag-limit'),
    pagParam: $('field-pag-param'),
    pagCursorPath: $('field-pag-cursor-path'),
  };

  /* ─── get checked tags ─── */
  function getCheckedTags(containerId) {
    var container = $(containerId);
    if (!container) return [];
    var checks = container.querySelectorAll('input[type="checkbox"]:checked');
    return Array.from(checks).map(function (c) { return c.value; });
  }

  function setCheckedTags(containerId, values) {
    var container = $(containerId);
    if (!container) return;
    var vals = new Set(values || []);
    container.querySelectorAll('input[type="checkbox"]').forEach(function (c) {
      c.checked = vals.has(c.value);
    });
  }

  /* ─── read form → source object ─── */
  function readForm() {
    var s = {
      name: fields.name.value.trim(),
      description: fields.desc.value.trim(),
      category: fields.cat.value.trim(),
      os: fields.os.value,
      parser: fields.parser.value.trim() || 'raw_text',
      requires_key: fields.reqKey.checked,
      key_env: fields.keyEnv.value.trim() || null,
      contact: fields.contact.value,
      logs_queries: fields.logsQueries.checked,
      enabled: true,
      entity_hints: getCheckedTags('field-entity-hints'),
      applies_to: getCheckedTags('field-applies-to'),
      tool: {
        url: fields.toolUrl.value.trim(),
        method: fields.toolMethod.value,
      },
    };
    // Parse JSON fields
    try { var h = JSON.parse(fields.toolHeaders.value.trim() || '{}'); if (Object.keys(h).length) s.tool.headers = h; } catch (e) {}
    try { var p = JSON.parse(fields.toolParams.value.trim() || '{}'); if (Object.keys(p).length) s.tool.params = p; } catch (e) {}
    try { var b = JSON.parse(fields.toolBody.value.trim() || '{}'); if (Object.keys(b).length) s.tool.body = b; } catch (e) {}
    // Pagination
    var strat = fields.pagStrategy.value;
    if (strat) {
      s.pagination = { strategy: strat };
      var lim = parseInt(fields.pagLimit.value, 10);
      if (lim > 0) s.pagination.limit = lim;
      if (fields.pagParam.value.trim()) s.pagination.param = fields.pagParam.value.trim();
      if (fields.pagCursorPath.value.trim()) s.pagination.cursor_path = fields.pagCursorPath.value.trim();
    }
    return s;
  }

  /* ─── write source object → form ─── */
  function writeForm(s) {
    if (!s) {
      form.reset();
      currentName = null;
      isDirty = false;
      isSystemApp = false;
      saveBtn.disabled = false;
      saveBtn.title = '';
      formStatus.textContent = '';
      formStatus.className = 'form-status';
      yamlPreview.textContent = '';
      deleteBtn.hidden = true;
      return;
    }
    isSystemApp = s.kind === 'system_app';
    saveBtn.disabled = isSystemApp;
    saveBtn.title = isSystemApp
      ? 'System app sources are YAML-only — edit the file directly'
      : '';
    fields.originalName.value = s.name || '';
    fields.name.value = s.name || '';
    fields.desc.value = s.description || '';
    fields.cat.value = s.category || '';
    fields.os.value = s.os || 'any';
    fields.parser.value = s.parser || 'raw_text';
    fields.reqKey.checked = !!s.requires_key;
    fields.keyEnv.value = s.key_env || '';
    fields.keyEnv.disabled = !s.requires_key;
    fields.contact.value = s.contact || 'none';
    fields.logsQueries.checked = !!s.logs_queries;
    fields.toolUrl.value = (s.tool && s.tool.url) || '';
    if (isSystemApp && s.tool && s.tool.binary) {
      var binDesc = s.tool.binary;
      if (s.tool.args && s.tool.args.length) binDesc += ' ' + JSON.stringify(s.tool.args);
      fields.toolUrl.value = '(binary) ' + binDesc;
    }
    fields.toolMethod.value = (s.tool && s.tool.method) || 'GET';
    fields.toolHeaders.value = (s.tool && s.tool.headers && Object.keys(s.tool.headers).length)
      ? JSON.stringify(s.tool.headers, null, 2) : '';
    fields.toolParams.value = (s.tool && s.tool.params && Object.keys(s.tool.params).length)
      ? JSON.stringify(s.tool.params, null, 2) : '';
    fields.toolBody.value = (s.tool && s.tool.body && Object.keys(s.tool.body).length)
      ? JSON.stringify(s.tool.body, null, 2) : '';

    // Pagination
    var pag = s.pagination || {};
    fields.pagStrategy.value = pag.strategy || '';
    fields.pagLimit.value = pag.limit || '';
    fields.pagParam.value = pag.param || '';
    fields.pagCursorPath.value = pag.cursor_path || '';

    setCheckedTags('field-applies-to', s.applies_to);
    setCheckedTags('field-entity-hints', s.entity_hints);

    currentName = s.name;
    isDirty = false;
    formStatus.textContent = '';
    formStatus.className = 'form-status';
    deleteBtn.hidden = false;
    updateYamlPreview();
  }

  /* ─── update YAML preview ─── */
  function updateYamlPreview() {
    try {
      var s = readForm();
      yamlPreview.textContent = JSON.stringify(s, null, 2);
    } catch (e) {
      yamlPreview.textContent = '/* cannot render preview */';
    }
  }

  /* ─── render source list ─── */
  function renderList(filterText) {
    filterText = (filterText || '').toLowerCase();
    var grouped = {};
    sources.forEach(function (s) {
      if (filterText && s.name.indexOf(filterText) === -1 && s.category.toLowerCase().indexOf(filterText) === -1) return;
      if (!grouped[s.category]) grouped[s.category] = [];
      grouped[s.category].push(s);
    });

    var html = '';
    var sortedCats = Object.keys(grouped).sort();
    sortedCats.forEach(function (cat) {
      html += '<div class="src-cat-header">' + escHtml(cat) + ' <span class="field-sub">(' + grouped[cat].length + ')</span></div>';
      grouped[cat].forEach(function (s) {
        var active = s.name === currentName ? ' active' : '';
        var onOff = s.enabled !== false ? 'on' : 'off';
        var keyBadge = s.requires_key ? '<span class="src-item-key-badge">key</span>' : '';
        var sysBadge = s.kind === 'system_app' ? '<span class="src-item-sys-badge">sys</span>' : '';
        html += '<div class="src-item' + active + '" data-name="' + escAttr(s.name) + '">'
          + '<span class="src-item-icon ' + onOff + '"></span>'
          + '<div class="src-item-info">'
          + '<div class="src-item-name">' + escHtml(s.name) + sysBadge + keyBadge + '</div>'
          + '<div class="src-item-cat">' + escHtml(s.description || '') + '</div>'
          + '</div></div>';
      });
    });
    listEl.innerHTML = html || '<div style="padding:20px;text-align:center;color:var(--text-2);font-size:13px;">No sources match filter</div>';
  }

  /* ─── helpers ─── */
  function escHtml(s) { return String(s).replace(/[&<>"]/g, function (m) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[m]; }); }
  function escAttr(s) { return String(s).replace(/"/g, '&quot;'); }

  /* ─── toast ─── */
  function toast(msg, kind) {
    var el = document.createElement('div');
    el.className = 'toast ' + (kind || 'info');
    el.textContent = msg;
    document.getElementById('toast-stack').appendChild(el);
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 4000);
  }

  /* ─── load sources ─── */
  function loadSources() {
    apiFetch('/api/sources/yaml').then(function (data) {
      sources = data.sources || [];
      srcCount.textContent = data.total + ' sources';
      renderList(filterInput.value);
      // If currently selected source still exists, keep it; otherwise clear
      if (currentName && !data.sources.some(function (s) { return s.name === currentName; })) {
        clearEditor();
      }
    }).catch(function (err) {
      toast('Failed to load sources: ' + err.message, 'err');
    });
  }

  /* ─── clear editor ─── */
  function clearEditor() {
    form.hidden = true;
    editorEmpty.hidden = false;
    writeForm(null);
    // Remove active class from all list items
    listEl.querySelectorAll('.src-item.active').forEach(function (el) { el.classList.remove('active'); });
    currentName = null;
  }

  /* ─── select source ─── */
  function selectSource(name) {
    var s = sources.filter(function (s) { return s.name === name; })[0];
    if (!s) return;
    form.hidden = false;
    editorEmpty.hidden = true;
    writeForm(s);
    listEl.querySelectorAll('.src-item.active').forEach(function (el) { el.classList.remove('active'); });
    var item = listEl.querySelector('.src-item[data-name="' + escAttr(name) + '"]');
    if (item) item.classList.add('active');
  }

  /* ─── save source ─── */
  function saveSource() {
    if (isSystemApp) {
      toast('System app sources are YAML-only — edit the file directly', 'err');
      return;
    }
    var data = readForm();
    if (!data.name) { toast('Name is required', 'err'); return; }
    if (!data.tool.url) { toast('Tool URL is required', 'err'); return; }

    formStatus.textContent = 'Saving…';
    formStatus.className = 'form-status';

    var isNew = !currentName || currentName !== data.name;
    var url = isNew ? '/api/sources/yaml' : '/api/sources/yaml/' + encodeURIComponent(currentName);
    var method = isNew ? 'POST' : 'PUT';

    apiFetch(url, { method: method, body: JSON.stringify(data) }).then(function () {
      toast('Source "' + data.name + '" saved', 'ok');
      formStatus.textContent = 'Saved';
      formStatus.className = 'form-status ok';
      loadSources();
      // Re-select the saved source
      selectSource(data.name);
    }).catch(function (err) {
      toast('Save failed: ' + err.message, 'err');
      formStatus.textContent = 'Error: ' + err.message;
      formStatus.className = 'form-status err';
    });
  }

  /* ─── delete source ─── */
  function deleteSource() {
    if (!currentName) return;

    // Show confirmation
    var overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';
    overlay.innerHTML = '<div class="confirm-card">'
      + '<h3>Delete source</h3>'
      + '<p>Are you sure you want to delete <strong>' + escHtml(currentName) + '</strong>? This will remove the YAML file from disk. This action cannot be undone.</p>'
      + '<div class="confirm-actions">'
      + '<button class="ghost" id="confirm-cancel">Cancel</button>'
      + '<button class="primary" id="confirm-delete">Delete</button>'
      + '</div></div>';
    document.body.appendChild(overlay);

    document.getElementById('confirm-delete').addEventListener('click', function () {
      overlay.remove();
      apiFetch('/api/sources/yaml/' + encodeURIComponent(currentName), { method: 'DELETE' }).then(function () {
        toast('Source "' + currentName + '" deleted', 'ok');
        clearEditor();
        loadSources();
      }).catch(function (err) {
        toast('Delete failed: ' + err.message, 'err');
      });
    });
    document.getElementById('confirm-cancel').addEventListener('click', function () { overlay.remove(); });
    overlay.addEventListener('click', function (e) { if (e.target === overlay) overlay.remove(); });
  }

  /* ─── new source ─── */
  function newSource() {
    form.hidden = false;
    editorEmpty.hidden = true;
    writeForm(null);
    // Set sensible defaults
    fields.cat.value = '00. Misc';
    fields.os.value = 'any';
    fields.parser.value = 'raw_text';
    fields.contact.value = 'none';
    fields.toolMethod.value = 'GET';
    setCheckedTags('field-applies-to', ['any']);
    fields.name.focus();
    deleteBtn.hidden = true;
    listEl.querySelectorAll('.src-item.active').forEach(function (el) { el.classList.remove('active'); });
  }

  /* ─── events ─── */

  // Form submission
  form.addEventListener('submit', function (e) { e.preventDefault(); saveSource(); });

  // Delete button
  deleteBtn.addEventListener('click', deleteSource);

  // Cancel button
  $('cancel-btn').addEventListener('click', clearEditor);

  // New source button
  $('new-source-btn').addEventListener('click', newSource);

  // Filter input
  filterInput.addEventListener('input', function () { renderList(this.value); });

  // Source list click (delegation)
  listEl.addEventListener('click', function (e) {
    var item = e.target.closest('.src-item');
    if (item) selectSource(item.getAttribute('data-name'));
  });

  // Req key toggle → enable/disable key_env
  fields.reqKey.addEventListener('change', function () {
    fields.keyEnv.disabled = !this.checked;
    if (!this.checked) fields.keyEnv.value = '';
  });

  // Update YAML preview on any input change
  form.addEventListener('input', function () {
    isDirty = true;
    updateYamlPreview();
  });

  // Suggest button for common headers
  document.querySelectorAll('.suggest-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var targetId = this.getAttribute('data-target');
      var template = this.getAttribute('data-template');
      var target = document.getElementById(targetId);
      if (target && template) {
        target.value = template;
        updateYamlPreview();
      }
    });
  });

  /* ─── init ─── */
  loadSources();
})();
