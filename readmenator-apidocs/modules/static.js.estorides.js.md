# `static/js/estorides.js`

> Source: [static/js/estorides.js:1](../../static/js/estorides.js#L1) | language `js` | coverage 25.3% | [API index](../index.md)

Estorides front-end controller

## Contents

- **Classes:** [`to`](#to), [`on`](#on), [`attribute`](#attribute)
- **Functions:** [`setVisible`](#setvisible), [`isLanQueryLocal`](#islanquerylocal), [`t`](#t), [`lanRunFields`](#lanrunfields), [`ensureLanConsent`](#ensurelanconsent), [`safe`](#safe), [`done`](#done), [`onYes`](#onyes), [`onNo`](#onno), [`set`](#set), [`TELEMETRY`](#telemetry), [`detectQueryTypeLocal`](#detectquerytypelocal), [`showToast`](#showtoast), [`updateQueryChip`](#updatequerychip), [`setRunProgress`](#setrunprogress), [`showEmptyState`](#showemptystate), [`summariseObservation`](#summariseobservation), [`buildResultCard`](#buildresultcard), [`toolBinary`](#toolbinary), [`status`](#status), [`requestToolInstall`](#requesttoolinstall), [`pollToolInstall`](#polltoolinstall), [`out`](#out), [`populateCategoryFilter`](#populatecategoryfilter), [`applyResultFilters`](#applyresultfilters), [`text`](#text), [`cat`](#cat), [`status`](#status), [`bindResultFilters`](#bindresultfilters), [`showFriendlyError`](#showfriendlyerror), [`focusGraphNodeByValue`](#focusgraphnodebyvalue), [`switchSidebarTab`](#switchsidebartab), [`switchCanvasTab`](#switchcanvastab), [`clearMap`](#clearmap), [`plotPoints`](#plotpoints), [`replotStreamData`](#replotstreamdata), [`stopRunStream`](#stoprunstream), [`renderLanResults`](#renderlanresults), [`startLanScan`](#startlanscan), [`scope`](#scope), [`msg`](#msg), [`runQuery`](#runquery), [`runQueryBlocking`](#runqueryblocking), [`searchEntity`](#searchentity), [`handleRunStreamEvent`](#handlerunstreamevent), [`appendStreamObservation`](#appendstreamobservation), [`appendStreamEntity`](#appendstreamentity), [`sig`](#sig), [`clearAll`](#clearall), [`setStatus`](#setstatus), [`renderResult`](#renderresult), [`loadAnalysisModels`](#loadanalysismodels), [`renderAnalysisModels`](#renderanalysismodels), [`makeModelPill`](#makemodelpill), [`renderAnalysis`](#renderanalysis), [`renderMarkdownInto`](#rendermarkdowninto), [`setThinkingVisible`](#setthinkingvisible), [`toggleThinking`](#togglethinking), [`reanalyze`](#reanalyze), [`boxQ`](#boxq), [`scheduleRender`](#schedulerender), [`flush`](#flush), [`pump`](#pump), [`analyseEntity`](#analyseentity), [`expandNode`](#expandnode), [`mergeExpansionIntoGraph`](#mergeexpansionintograph), [`k`](#k), [`drawGraphWithExtras`](#drawgraphwithextras), [`pushLink`](#pushlink), [`is3DActive`](#is3dactive), [`CLUSTER_PALETTE`](#cluster_palette), [`resolverTypeFor`](#resolvertypefor), [`saveLevelOverrides`](#saveleveloverrides), [`levelOf`](#levelof), [`clusterColor`](#clustercolor), [`c`](#c), [`safeColor`](#safecolor), [`deriveClusters`](#deriveclusters), [`cid`](#cid), [`hideTooltip`](#hidetooltip), [`purifyHTML`](#purifyhtml), [`setSanitizedHTML`](#setsanitizedhtml), [`showTooltipAt`](#showtooltipat), [`hideContextMenu`](#hidecontextmenu), [`showBridgeTooltip`](#showbridgetooltip), [`labelFor`](#labelfor), [`c`](#c), [`showNodeTooltip`](#shownodetooltip), [`showContextMenu`](#showcontextmenu), [`tr`](#tr), [`setNodeLevel`](#setnodelevel), [`applyLevelStyles`](#applylevelstyles), [`focusNode`](#focusnode), [`barH`](#barh), [`runTransform`](#runtransform), [`runTransformStream`](#runtransformstream), [`flush`](#flush), [`undoGraph`](#undograph), [`k`](#k), [`selectNode`](#selectnode), [`add`](#add), [`addText`](#addtext), [`tr`](#tr), [`renderGraphCore`](#rendergraphcore), [`barH`](#barh), [`drawHulls`](#drawhulls), [`setStatusDot`](#setstatusdot), [`showWorkingIndicator`](#showworkingindicator), [`hideWorkingIndicator`](#hideworkingindicator), [`toggleTierSection`](#toggletiersection), [`renderTieredResults`](#rendertieredresults), [`escapeAttr`](#escapeattr), [`buildMapCoords`](#buildmapcoords), [`validCoord`](#validcoord), [`colorFor`](#colorfor), [`renderEntities`](#renderentities), [`renderGraphSummary`](#rendergraphsummary), [`colorForKind`](#colorforkind), [`renderTimeline`](#rendertimeline), [`obs`](#obs), [`frac`](#frac), [`fmtTime`](#fmttime), [`filterTimeline`](#filtertimeline), [`drawGraph`](#drawgraph), [`loadCases`](#loadcases), [`q`](#q), [`openCaseDetail`](#opencasedetail), [`entities`](#entities), [`obs`](#obs), [`restoreCaseToWorkspace`](#restorecasetoworkspace), [`buildCaseMapCoords`](#buildcasemapcoords), [`renderCaseItem`](#rendercaseitem), [`saved`](#saved), [`debounce`](#debounce), [`escapeHTML`](#escapehtml), [`truncate`](#truncate), [`caseActionSave`](#caseactionsave), [`caseActionDiff`](#caseactiondiff), [`renderCaseDiffPanel`](#rendercasediffpanel), [`rows`](#rows), [`removed`](#removed), [`caseActionReport`](#caseactionreport), [`showReportModal`](#showreportmodal), [`openModal`](#openmodal), [`actions`](#actions), [`close`](#close), [`promptModal`](#promptmodal), [`confirmModal`](#confirmmodal), [`tag`](#tag), [`loadSidebarWidth`](#loadsidebarwidth), [`saveSidebarWidth`](#savesidebarwidth), [`loadSidebarCollapsed`](#loadsidebarcollapsed), [`saveSidebarCollapsed`](#savesidebarcollapsed), [`switchSidebarTab`](#switchsidebartab), [`loadFusionTab`](#loadfusiontab), [`loadFusionStats`](#loadfusionstats), [`loadFusionTopChanged`](#loadfusiontopchanged), [`loadFusionSearch`](#loadfusionsearch), [`doSearch`](#dosearch), [`loadFusionEntityDetail`](#loadfusionentitydetail), [`setStatus`](#setstatus), [`setDiscoverProgress`](#setdiscoverprogress), [`hideDiscoverProgress`](#hidediscoverprogress), [`startDiscover`](#startdiscover), [`stopDiscover`](#stopdiscover), [`handleDiscoverEvent`](#handlediscoverevent), [`addDiscoverEntityToTab`](#adddiscoverentitytotab), [`sig`](#sig), [`escapeHtml`](#escapehtml), [`maybePlotDiscoverEntity`](#maybeplotdiscoverentity), [`flushDiscoverEntities`](#flushdiscoverentities), [`check`](#check)
- **Other Members:** [`setTimeout`](#settimeout), [`fetch`](#fetch)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class to
    class on
    class attribute
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_static_js_estorides_js__lanRunFields(["lanRunFields"])
    n_static_js_estorides_js__isLanQueryLocal(["isLanQueryLocal"])
    n_static_js_estorides_js__ensureLanConsent(["ensureLanConsent"])
    n_static_js_estorides_js__purifyHTML(["purifyHTML"])
    n_static_js_estorides_js__setSanitizedHTML(["setSanitizedHTML"])
    n_static_js_estorides_js__setVisible(["setVisible"])
    n_static_js_estorides_js__done(["done"])
    n_static_js_estorides_js__onYes(["onYes"])
    n_static_js_estorides_js__onNo(["onNo"])
    n_static_js_estorides_js__showToast(["showToast"])
    n_static_js_estorides_js__escapeHTML(["escapeHTML"])
    n_static_js_estorides_js__setRunProgress(["setRunProgress"])
    n_static_js_estorides_js__showEmptyState(["showEmptyState"])
    n_static_js_estorides_js__summariseObservation(["summariseObservation"])
    n_static_js_estorides_js__truncate(["truncate"])
    n_static_js_estorides_js__buildResultCard(["buildResultCard"])
    n_static_js_estorides_js__requestToolInstall(["requestToolInstall"])
    n_static_js_estorides_js__pollToolInstall(["pollToolInstall"])
    n_static_js_estorides_js__showFriendlyError(["showFriendlyError"])
    n_static_js_estorides_js__plotPoints(["plotPoints"])
    n_static_js_estorides_js__clearMap(["clearMap"])
    n_static_js_estorides_js__escapeAttr(["escapeAttr"])
    n_static_js_estorides_js__expandNode(["expandNode"])
    n_static_js_estorides_js__lanRunFields --> n_static_js_estorides_js__isLanQueryLocal
    n_static_js_estorides_js__ensureLanConsent --> n_static_js_estorides_js__isLanQueryLocal
    n_static_js_estorides_js__ensureLanConsent --> n_static_js_estorides_js__purifyHTML
    n_static_js_estorides_js__ensureLanConsent --> n_static_js_estorides_js__setSanitizedHTML
    n_static_js_estorides_js__ensureLanConsent --> n_static_js_estorides_js__setVisible
    n_static_js_estorides_js__done --> n_static_js_estorides_js__setVisible
    n_static_js_estorides_js__onYes --> n_static_js_estorides_js__done
    n_static_js_estorides_js__onNo --> n_static_js_estorides_js__done
    n_static_js_estorides_js__showToast --> n_static_js_estorides_js__escapeHTML
    n_static_js_estorides_js__setRunProgress --> n_static_js_estorides_js__setVisible
    n_static_js_estorides_js__showEmptyState --> n_static_js_estorides_js__setVisible
    n_static_js_estorides_js__summariseObservation --> n_static_js_estorides_js__truncate
    n_static_js_estorides_js__buildResultCard --> n_static_js_estorides_js__escapeHTML
    n_static_js_estorides_js__buildResultCard --> n_static_js_estorides_js__requestToolInstall
    n_static_js_estorides_js__buildResultCard --> n_static_js_estorides_js__summariseObservation
    n_static_js_estorides_js__buildResultCard --> n_static_js_estorides_js__truncate
    n_static_js_estorides_js__requestToolInstall --> n_static_js_estorides_js__pollToolInstall
    n_static_js_estorides_js__requestToolInstall --> n_static_js_estorides_js__showToast
    n_static_js_estorides_js__pollToolInstall --> n_static_js_estorides_js__showToast
    n_static_js_estorides_js__showFriendlyError --> n_static_js_estorides_js__escapeHTML
    n_static_js_estorides_js__plotPoints --> n_static_js_estorides_js__clearMap
    n_static_js_estorides_js__plotPoints --> n_static_js_estorides_js__escapeAttr
    n_static_js_estorides_js__plotPoints --> n_static_js_estorides_js__escapeHTML
    n_static_js_estorides_js__plotPoints --> n_static_js_estorides_js__expandNode
```

## Classes

<a id="to"></a>

### `to`

`class` | [static/js/estorides.js:474](../../static/js/estorides.js#L474)

```javascript
// id is "map", not "map-canvas"), so select by class to stay consistent.
```

Panels are keyed by the `<name>-canvas` class, not by id (the map panel's

---

<a id="on"></a>

### `on`

`class` | [static/js/estorides.js:2178](../../static/js/estorides.js#L2178)

```javascript
// make entities first-class on the map, not just observations.
```

Geolocated entities (parsed.lat / parsed.lon) AND country codes.

Many parsers stash coords on the entity itself (e.g. abuseipdb has a "countryCode" field). The whole point of v1.1 is to

---

<a id="attribute"></a>

### `attribute`

`class` | [static/js/estorides.js:3194](../../static/js/estorides.js#L3194)

```javascript
// Whitelist the intel level before it reaches a class attribute,
```

---

## Functions

<a id="setvisible"></a>

### `setVisible`

`function` | [static/js/estorides.js:12](../../static/js/estorides.js#L12)

```javascript
function setVisible(el, show, display)
```

Show/hide that respects the HTML5 `hidden` attribute.

`[hidden]` is enforced with `!important` (see estorides_ui.css), so toggling inline `style.display` alone can never reveal an element that carries the attribute — the attribute must be cleared too.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `el` |  |  |  |
| `show` |  |  |  |
| `display` |  |  |  |

*Called by:* [`done`](#done), [`ensureLanConsent`](#ensurelanconsent), [`hideContextMenu`](#hidecontextmenu), [`hideTooltip`](#hidetooltip), [`renderTimeline`](#rendertimeline), [`selectNode`](#selectnode), [`setRunProgress`](#setrunprogress), [`showContextMenu`](#showcontextmenu), [`showEmptyState`](#showemptystate), [`showTooltipAt`](#showtooltipat)

---

<a id="islanquerylocal"></a>

### `isLanQueryLocal`

`function` | [static/js/estorides.js:24](../../static/js/estorides.js#L24)

```javascript
function isLanQueryLocal(q)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `q` |  |  |  |

*Called by:* [`ensureLanConsent`](#ensurelanconsent), [`lanRunFields`](#lanrunfields), [`startLanScan`](#startlanscan)

---

<a id="t"></a>

### `t`

`function` `const` | [static/js/estorides.js:25](../../static/js/estorides.js#L25)

```javascript
const t = (q || '').trim();
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `q` |  |  |  |

**Returns:** `cons`

---

<a id="lanrunfields"></a>

### `lanRunFields`

`function` | [static/js/estorides.js:33](../../static/js/estorides.js#L33)

```javascript
function lanRunFields(q)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `q` |  |  |  |

*Calls:* [`isLanQueryLocal`](#islanquerylocal)

*Called by:* [`runQuery`](#runquery), [`runQueryBlocking`](#runqueryblocking), [`searchEntity`](#searchentity)

---

<a id="ensurelanconsent"></a>

### `ensureLanConsent`

`function` | [static/js/estorides.js:46](../../static/js/estorides.js#L46)

```javascript
function ensureLanConsent(q)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `q` |  |  |  |

*Calls:* [`isLanQueryLocal`](#islanquerylocal), [`purifyHTML`](#purifyhtml), [`setSanitizedHTML`](#setsanitizedhtml), [`setVisible`](#setvisible)

*Called by:* [`runQuery`](#runquery), [`searchEntity`](#searchentity), [`startLanScan`](#startlanscan)

---

<a id="safe"></a>

### `safe`

`function` `const` | [static/js/estorides.js:60](../../static/js/estorides.js#L60)

```javascript
const safe = (typeof purifyHTML === 'function')
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `purifyHTML` | `typeof` | `== 'function'` |  |

---

<a id="done"></a>

### `done`

`function` `const` | [static/js/estorides.js:70](../../static/js/estorides.js#L70)

```javascript
const done = (val) =>
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `val` |  |  |  |

*Calls:* [`setVisible`](#setvisible)

*Called by:* [`onNo`](#onno), [`onYes`](#onyes)

---

<a id="onyes"></a>

### `onYes`

`function` `const` | [static/js/estorides.js:77](../../static/js/estorides.js#L77)

```javascript
const onYes = () => done(true);
```

*Calls:* [`done`](#done)

---

<a id="onno"></a>

### `onNo`

`function` `const` | [static/js/estorides.js:78](../../static/js/estorides.js#L78)

```javascript
const onNo = () => done(false);
```

*Calls:* [`done`](#done)

---

<a id="set"></a>

### `set`

`function` `const` | [static/js/estorides.js:105](../../static/js/estorides.js#L105)

```javascript
const set = (k, v) =>
```

Headers may be a Headers instance, an object, or absent.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `k` |  |  |  |
| `v` |  |  |  |

---

<a id="telemetry"></a>

### `TELEMETRY`

`function` `const` | [static/js/estorides.js:114](../../static/js/estorides.js#L114)

```javascript
const TELEMETRY = (function readTelemetry()
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `readTelemetry` | `function ()` |  |  |

---

<a id="detectquerytypelocal"></a>

### `detectQueryTypeLocal`

`function` | [static/js/estorides.js:128](../../static/js/estorides.js#L128)

```javascript
function detectQueryTypeLocal(q)
```

---- UX helpers (v1.4) ----

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `q` |  |  |  |

*Called by:* [`runQuery`](#runquery)

---

<a id="showtoast"></a>

### `showToast`

`function` | [static/js/estorides.js:139](../../static/js/estorides.js#L139)

```javascript
function showToast(type, title, body, duration)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `type` |  |  |  |
| `title` |  |  |  |
| `body` |  |  |  |
| `duration` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml)

*Called by:* [`appendStreamObservation`](#appendstreamobservation), [`caseActionDiff`](#caseactiondiff), [`caseActionReport`](#caseactionreport), [`caseActionSave`](#caseactionsave), [`pollToolInstall`](#polltoolinstall), [`requestToolInstall`](#requesttoolinstall), [`restoreCaseToWorkspace`](#restorecasetoworkspace), [`runQuery`](#runquery), [`runQueryBlocking`](#runqueryblocking), [`searchEntity`](#searchentity), [`startLanScan`](#startlanscan)

---

<a id="updatequerychip"></a>

### `updateQueryChip`

`function` | [static/js/estorides.js:149](../../static/js/estorides.js#L149)

```javascript
function updateQueryChip(type)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `type` |  |  |  |

*Called by:* [`clearAll`](#clearall), [`runQuery`](#runquery)

---

<a id="setrunprogress"></a>

### `setRunProgress`

`function` | [static/js/estorides.js:159](../../static/js/estorides.js#L159)

```javascript
function setRunProgress(current, total)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `current` |  |  |  |
| `total` |  |  |  |

*Calls:* [`setVisible`](#setvisible)

*Called by:* [`appendStreamObservation`](#appendstreamobservation), [`clearAll`](#clearall), [`runQuery`](#runquery), [`runQueryBlocking`](#runqueryblocking)

---

<a id="showemptystate"></a>

### `showEmptyState`

`function` | [static/js/estorides.js:180](../../static/js/estorides.js#L180)

```javascript
function showEmptyState(show)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `show` |  |  |  |

*Calls:* [`setVisible`](#setvisible)

*Called by:* [`clearAll`](#clearall), [`renderLanResults`](#renderlanresults), [`renderResult`](#renderresult), [`restoreCaseToWorkspace`](#restorecasetoworkspace), [`runQuery`](#runquery)

---

<a id="summariseobservation"></a>

### `summariseObservation`

`function` | [static/js/estorides.js:186](../../static/js/estorides.js#L186)

```javascript
function summariseObservation(obs)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `obs` |  |  |  |

*Calls:* [`truncate`](#truncate)

*Called by:* [`buildResultCard`](#buildresultcard)

---

<a id="buildresultcard"></a>

### `buildResultCard`

`function` | [static/js/estorides.js:211](../../static/js/estorides.js#L211)

```javascript
function buildResultCard(obs)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `obs` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml), [`requestToolInstall`](#requesttoolinstall), [`summariseObservation`](#summariseobservation), [`truncate`](#truncate)

*Called by:* [`appendStreamObservation`](#appendstreamobservation), [`renderResult`](#renderresult)

---

<a id="toolbinary"></a>

### `toolBinary`

`function` `const` | [static/js/estorides.js:215](../../static/js/estorides.js#L215)

```javascript
const toolBinary = (obs.meta && obs.meta.tool_binary) || obs.source || '';
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `tool_binary` | `obs.meta && obs.meta.` |  |  |

---

<a id="status"></a>

### `status`

`function` `const` | [static/js/estorides.js:221](../../static/js/estorides.js#L221)

```javascript
const status = (obs.meta && obs.meta.status) || (failed ? 'ERR' : 'OK');
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `status` | `obs.meta && obs.meta.` |  |  |

---

<a id="requesttoolinstall"></a>

### `requestToolInstall`

`function` | [static/js/estorides.js:270](../../static/js/estorides.js#L270)

```javascript
function requestToolInstall(tool, btn)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `tool` |  |  |  |
| `btn` |  |  |  |

*Calls:* [`pollToolInstall`](#polltoolinstall), [`showToast`](#showtoast)

*Called by:* [`buildResultCard`](#buildresultcard)

---

<a id="polltoolinstall"></a>

### `pollToolInstall`

`function` | [static/js/estorides.js:293](../../static/js/estorides.js#L293)

```javascript
function pollToolInstall(tool, btn, tries)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `tool` |  |  |  |
| `btn` |  |  |  |
| `tries` |  |  |  |

*Calls:* [`showToast`](#showtoast)

*Called by:* [`requestToolInstall`](#requesttoolinstall)

---

<a id="out"></a>

### `out`

`function` `const` | [static/js/estorides.js:319](../../static/js/estorides.js#L319)

```javascript
const out = (res.output || '').toString().replace(/\s+/g, ' ').trim().slice(0, 220);
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `output` | `res. \|\| ''` |  |  |

---

<a id="populatecategoryfilter"></a>

### `populateCategoryFilter`

`function` | [static/js/estorides.js:326](../../static/js/estorides.js#L326)

```javascript
function populateCategoryFilter(categories)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `categories` |  |  |  |

*Called by:* [`appendStreamObservation`](#appendstreamobservation), [`renderResult`](#renderresult)

---

<a id="applyresultfilters"></a>

### `applyResultFilters`

`function` | [static/js/estorides.js:332](../../static/js/estorides.js#L332)

```javascript
function applyResultFilters()
```

*Called by:* [`appendStreamObservation`](#appendstreamobservation), [`renderResult`](#renderresult)

---

<a id="text"></a>

### `text`

`function` `const` | [static/js/estorides.js:333](../../static/js/estorides.js#L333)

```javascript
const text = (document.getElementById('result-filter-text') && document.getElementById('result-filter-text').value || '').toLowerCase();
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `document.getElementById('result-filter-text') && document.getElementById('result-filter-text'). \|\| ''` |  |  |

*Called by:* [`renderGraphCore`](#rendergraphcore)

---

<a id="cat"></a>

### `cat`

`function` `const` | [static/js/estorides.js:334](../../static/js/estorides.js#L334)

```javascript
const cat = (document.getElementById('result-filter-cat') && document.getElementById('result-filter-cat').value) || '';
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `document.getElementById('result-filter-cat') && document.getElementById('result-filter-cat').` |  |  |

---

<a id="status"></a>

### `status`

`function` `const` | [static/js/estorides.js:335](../../static/js/estorides.js#L335)

```javascript
const status = (document.getElementById('result-filter-status') && document.getElementById('result-filter-status').value) || '';
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `document.getElementById('result-filter-status') && document.getElementById('result-filter-status').` |  |  |

---

<a id="bindresultfilters"></a>

### `bindResultFilters`

`function` | [static/js/estorides.js:353](../../static/js/estorides.js#L353)

```javascript
function bindResultFilters()
```

*Called by:* [`renderResult`](#renderresult), [`runQuery`](#runquery)

---

<a id="showfriendlyerror"></a>

### `showFriendlyError`

`function` | [static/js/estorides.js:361](../../static/js/estorides.js#L361)

```javascript
function showFriendlyError(message, retryFn)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `message` |  |  |  |
| `retryFn` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml)

*Called by:* [`runQuery`](#runquery), [`runQueryBlocking`](#runqueryblocking), [`startLanScan`](#startlanscan)

---

<a id="focusgraphnodebyvalue"></a>

### `focusGraphNodeByValue`

`function` | [static/js/estorides.js:374](../../static/js/estorides.js#L374)

```javascript
function focusGraphNodeByValue(value)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` |  |  |  |

*Called by:* [`renderEntities`](#renderentities)

---

<a id="switchsidebartab"></a>

### `switchSidebarTab`

`function` | [static/js/estorides.js:383](../../static/js/estorides.js#L383)

```javascript
function switchSidebarTab(index)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `index` |  |  |  |

*Called by:* [`analyseEntity`](#analyseentity), [`openCaseDetail`](#opencasedetail)

---

<a id="switchcanvastab"></a>

### `switchCanvasTab`

`function` | [static/js/estorides.js:387](../../static/js/estorides.js#L387)

```javascript
function switchCanvasTab(name)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` |  |  |  |

---

<a id="clearmap"></a>

### `clearMap`

`function` | [static/js/estorides.js:409](../../static/js/estorides.js#L409)

```javascript
function clearMap()
```

*Called by:* [`clearAll`](#clearall), [`plotPoints`](#plotpoints), [`runQuery`](#runquery)

---

<a id="plotpoints"></a>

### `plotPoints`

`function` | [static/js/estorides.js:414](../../static/js/estorides.js#L414)

```javascript
function plotPoints(coords)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `coords` |  |  |  |

*Calls:* [`clearMap`](#clearmap), [`escapeAttr`](#escapeattr), [`escapeHTML`](#escapehtml), [`expandNode`](#expandnode)

*Called by:* [`renderResult`](#renderresult), [`replotStreamData`](#replotstreamdata), [`restoreCaseToWorkspace`](#restorecasetoworkspace)

---

<a id="replotstreamdata"></a>

### `replotStreamData`

`function` | [static/js/estorides.js:518](../../static/js/estorides.js#L518)

```javascript
function replotStreamData()
```

Rebuild the geospatial + temporal views from everything seen so far. plotPoints clears and redraws from the full coord set, so feeding it the accumulated observations makes the map grow as sources resolve.

*Calls:* [`buildMapCoords`](#buildmapcoords), [`plotPoints`](#plotpoints), [`renderTimeline`](#rendertimeline)

*Called by:* [`appendStreamObservation`](#appendstreamobservation)

---

<a id="stoprunstream"></a>

### `stopRunStream`

`function` | [static/js/estorides.js:530](../../static/js/estorides.js#L530)

```javascript
function stopRunStream()
```

*Called by:* [`clearAll`](#clearall), [`runQuery`](#runquery), [`searchEntity`](#searchentity)

---

<a id="renderlanresults"></a>

### `renderLanResults`

`function` | [static/js/estorides.js:551](../../static/js/estorides.js#L551)

```javascript
function renderLanResults(data)
```

Dedicated LAN entry point: resolves the scope (query box when it looks like LAN, otherwise the auto-detected private network), asks permission through the blocking modal, then runs a real local inventory scan.

The checkbox only widens the ceiling to active; without it the scan still runs passive. Results render below and the graph views refresh from the fed knowledge graph.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` |  |  |  |

*Calls:* [`showEmptyState`](#showemptystate)

*Called by:* [`startLanScan`](#startlanscan)

---

<a id="startlanscan"></a>

### `startLanScan`

`function` `async` | [static/js/estorides.js:620](../../static/js/estorides.js#L620)

```javascript
async function startLanScan()
```

*Calls:* [`drawGraph`](#drawgraph), [`ensureLanConsent`](#ensurelanconsent), [`hideWorkingIndicator`](#hideworkingindicator), [`isLanQueryLocal`](#islanquerylocal), [`renderLanResults`](#renderlanresults), [`setStatus`](#setstatus), [`setStatusDot`](#setstatusdot), [`showFriendlyError`](#showfriendlyerror), [`showToast`](#showtoast), [`showWorkingIndicator`](#showworkingindicator)

---

<a id="scope"></a>

### `scope`

`function` | [static/js/estorides.js:621](../../static/js/estorides.js#L621)

```javascript
let scope = ($('#query').value || '').trim();
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `$('#query'). \|\| ''` |  |  |

---

<a id="msg"></a>

### `msg`

`function` `const` | [static/js/estorides.js:662](../../static/js/estorides.js#L662)

```javascript
const msg = (data && data.message) || (data && data.error) || ('HTTP ' + r.status);
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `message` | `data && data.` |  |  |

---

<a id="runquery"></a>

### `runQuery`

`function` `async` | [static/js/estorides.js:685](../../static/js/estorides.js#L685)

```javascript
async function runQuery()
```

*Calls:* [`bindResultFilters`](#bindresultfilters), [`clearMap`](#clearmap), [`detectQueryTypeLocal`](#detectquerytypelocal), [`ensureLanConsent`](#ensurelanconsent), [`handleRunStreamEvent`](#handlerunstreamevent), [`hideWorkingIndicator`](#hideworkingindicator), [`lanRunFields`](#lanrunfields), [`runQueryBlocking`](#runqueryblocking), [`setRunProgress`](#setrunprogress), [`setStatus`](#setstatus), [`setStatusDot`](#setstatusdot), [`showEmptyState`](#showemptystate) and 5 more

---

<a id="runqueryblocking"></a>

### `runQueryBlocking`

`function` `async` | [static/js/estorides.js:773](../../static/js/estorides.js#L773)

```javascript
async function runQueryBlocking(q)
```

Blocking fallback: the original one-shot render path.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `q` |  |  |  |

*Calls:* [`hideWorkingIndicator`](#hideworkingindicator), [`lanRunFields`](#lanrunfields), [`renderResult`](#renderresult), [`renderTieredResults`](#rendertieredresults), [`setRunProgress`](#setrunprogress), [`setStatus`](#setstatus), [`setStatusDot`](#setstatusdot), [`showFriendlyError`](#showfriendlyerror), [`showToast`](#showtoast), [`showWorkingIndicator`](#showworkingindicator)

*Called by:* [`runQuery`](#runquery)

---

<a id="searchentity"></a>

### `searchEntity`

`function` `async` | [static/js/estorides.js:807](../../static/js/estorides.js#L807)

```javascript
async function searchEntity(entityType, query)
```

Deep-search an entity through the full OSINT pipeline without clearing existing data — appends and merges into current state.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entityType` |  |  |  |
| `query` |  |  |  |

*Calls:* [`ensureLanConsent`](#ensurelanconsent), [`handleRunStreamEvent`](#handlerunstreamevent), [`hideWorkingIndicator`](#hideworkingindicator), [`lanRunFields`](#lanrunfields), [`setStatus`](#setstatus), [`setStatusDot`](#setstatusdot), [`showToast`](#showtoast), [`showWorkingIndicator`](#showworkingindicator), [`stopRunStream`](#stoprunstream)

*Called by:* [`showContextMenu`](#showcontextmenu)

---

<a id="handlerunstreamevent"></a>

### `handleRunStreamEvent`

`function` | [static/js/estorides.js:858](../../static/js/estorides.js#L858)

```javascript
function handleRunStreamEvent(d)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `d` |  |  |  |

*Calls:* [`appendStreamEntity`](#appendstreamentity), [`appendStreamObservation`](#appendstreamobservation), [`loadAnalysisModels`](#loadanalysismodels), [`renderAnalysis`](#renderanalysis), [`renderGraphSummary`](#rendergraphsummary), [`setStatus`](#setstatus), [`setStatusDot`](#setstatusdot)

*Called by:* [`runQuery`](#runquery), [`searchEntity`](#searchentity)

---

<a id="appendstreamobservation"></a>

### `appendStreamObservation`

`function` | [static/js/estorides.js:896](../../static/js/estorides.js#L896)

```javascript
function appendStreamObservation(obs)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `obs` |  |  |  |

*Calls:* [`applyResultFilters`](#applyresultfilters), [`buildResultCard`](#buildresultcard), [`populateCategoryFilter`](#populatecategoryfilter), [`replotStreamData`](#replotstreamdata), [`setRunProgress`](#setrunprogress), [`showToast`](#showtoast)

*Called by:* [`handleRunStreamEvent`](#handlerunstreamevent)

---

<a id="appendstreamentity"></a>

### `appendStreamEntity`

`function` | [static/js/estorides.js:918](../../static/js/estorides.js#L918)

```javascript
function appendStreamEntity(entity, from)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entity` |  |  |  |
| `from` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml)

*Called by:* [`handleRunStreamEvent`](#handlerunstreamevent)

---

<a id="sig"></a>

### `sig`

`function` `const` | [static/js/estorides.js:920](../../static/js/estorides.js#L920)

```javascript
const sig = (entity.type || '') + '|' + (entity.value || '');
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `type` | `entity. \|\| ''` |  |  |

---

<a id="clearall"></a>

### `clearAll`

`function` | [static/js/estorides.js:947](../../static/js/estorides.js#L947)

```javascript
function clearAll()
```

*Calls:* [`clearMap`](#clearmap), [`setRunProgress`](#setrunprogress), [`setStatus`](#setstatus), [`setStatusDot`](#setstatusdot), [`showEmptyState`](#showemptystate), [`stopRunStream`](#stoprunstream), [`updateQueryChip`](#updatequerychip)

---

<a id="setstatus"></a>

### `setStatus`

`function` | [static/js/estorides.js:975](../../static/js/estorides.js#L975)

```javascript
function setStatus(s)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `s` |  |  |  |

*Called by:* [`clearAll`](#clearall), [`expandNode`](#expandnode), [`handleRunStreamEvent`](#handlerunstreamevent), [`runQuery`](#runquery), [`runQueryBlocking`](#runqueryblocking), [`runTransform`](#runtransform), [`runTransformStream`](#runtransformstream), [`searchEntity`](#searchentity), [`startLanScan`](#startlanscan), [`undoGraph`](#undograph)

---

<a id="renderresult"></a>

### `renderResult`

`function` | [static/js/estorides.js:981](../../static/js/estorides.js#L981)

```javascript
function renderResult(data)
```

---- result rendering ----

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` |  |  |  |

*Calls:* [`applyResultFilters`](#applyresultfilters), [`bindResultFilters`](#bindresultfilters), [`buildMapCoords`](#buildmapcoords), [`buildResultCard`](#buildresultcard), [`loadAnalysisModels`](#loadanalysismodels), [`plotPoints`](#plotpoints), [`populateCategoryFilter`](#populatecategoryfilter), [`renderAnalysis`](#renderanalysis), [`renderEntities`](#renderentities), [`renderGraphSummary`](#rendergraphsummary), [`renderTimeline`](#rendertimeline), [`showEmptyState`](#showemptystate)

*Called by:* [`runQueryBlocking`](#runqueryblocking)

---

<a id="loadanalysismodels"></a>

### `loadAnalysisModels`

`function` | [static/js/estorides.js:1029](../../static/js/estorides.js#L1029)

```javascript
function loadAnalysisModels()
```

*Calls:* [`renderAnalysisModels`](#renderanalysismodels)

*Called by:* [`analyseEntity`](#analyseentity), [`handleRunStreamEvent`](#handlerunstreamevent), [`openCaseDetail`](#opencasedetail), [`renderResult`](#renderresult), [`switchSidebarTab`](#switchsidebartab)

---

<a id="renderanalysismodels"></a>

### `renderAnalysisModels`

`function` | [static/js/estorides.js:1036](../../static/js/estorides.js#L1036)

```javascript
function renderAnalysisModels(models)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `models` |  |  |  |

*Calls:* [`makeModelPill`](#makemodelpill)

*Called by:* [`loadAnalysisModels`](#loadanalysismodels)

---

<a id="makemodelpill"></a>

### `makeModelPill`

`function` | [static/js/estorides.js:1048](../../static/js/estorides.js#L1048)

```javascript
function makeModelPill(label, model, active)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `label` |  |  |  |
| `model` |  |  |  |
| `active` |  |  |  |

*Calls:* [`reanalyze`](#reanalyze)

*Called by:* [`renderAnalysisModels`](#renderanalysismodels)

---

<a id="renderanalysis"></a>

### `renderAnalysis`

`function` | [static/js/estorides.js:1061](../../static/js/estorides.js#L1061)

```javascript
function renderAnalysis(a)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `a` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml), [`renderMarkdownInto`](#rendermarkdowninto), [`setThinkingVisible`](#setthinkingvisible)

*Called by:* [`analyseEntity`](#analyseentity), [`handleRunStreamEvent`](#handlerunstreamevent), [`openCaseDetail`](#opencasedetail), [`renderResult`](#renderresult)

---

<a id="rendermarkdowninto"></a>

### `renderMarkdownInto`

`function` | [static/js/estorides.js:1076](../../static/js/estorides.js#L1076)

```javascript
function renderMarkdownInto(el, text)
```

Node-only Markdown renderer (CodeQL #38).

Remote LLM text must never travel as an HTML string into an innerHTML sink: parse, sanitize and append nodes in one step so there is no string round-trip to flag.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `el` |  |  |  |
| `text` |  |  |  |

*Calls:* [`setSanitizedHTML`](#setsanitizedhtml)

*Called by:* [`renderAnalysis`](#renderanalysis), [`scheduleRender`](#schedulerender)

---

<a id="setthinkingvisible"></a>

### `setThinkingVisible`

`function` | [static/js/estorides.js:1091](../../static/js/estorides.js#L1091)

```javascript
function setThinkingVisible(show)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `show` |  |  |  |

*Called by:* [`renderAnalysis`](#renderanalysis)

---

<a id="togglethinking"></a>

### `toggleThinking`

`function` | [static/js/estorides.js:1098](../../static/js/estorides.js#L1098)

```javascript
function toggleThinking()
```

---

<a id="reanalyze"></a>

### `reanalyze`

`function` | [static/js/estorides.js:1103](../../static/js/estorides.js#L1103)

```javascript
function reanalyze()
```

*Calls:* [`pump`](#pump)

*Called by:* [`analyseEntity`](#analyseentity), [`makeModelPill`](#makemodelpill), [`openCaseDetail`](#opencasedetail)

---

<a id="boxq"></a>

### `boxQ`

`function` `const` | [static/js/estorides.js:1122](../../static/js/estorides.js#L1122)

```javascript
const boxQ = ($('#query') ? $('#query').value.trim() : '') || '';
```

The target being assessed = the current query box (if the user typed something) else the last completed run.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `$('#query') ? $('#query').value.trim()` | `''` |  |  |

---

<a id="schedulerender"></a>

### `scheduleRender`

`function` `const` | [static/js/estorides.js:1146](../../static/js/estorides.js#L1146)

```javascript
const scheduleRender = () =>
```

*Calls:* [`renderMarkdownInto`](#rendermarkdowninto), [`requestAnimationFrame`](static.js.graph_force.js.md#requestanimationframe)

*Called by:* [`flush`](#flush)

---

<a id="flush"></a>

### `flush`

`function` `const` | [static/js/estorides.js:1151](../../static/js/estorides.js#L1151)

```javascript
const flush = () =>
```

*Calls:* [`escapeHTML`](#escapehtml), [`scheduleRender`](#schedulerender)

*Called by:* [`pump`](#pump), [`runTransformStream`](#runtransformstream)

---

<a id="pump"></a>

### `pump`

`function` `const` | [static/js/estorides.js:1172](../../static/js/estorides.js#L1172)

```javascript
const pump = () =>
```

*Calls:* [`flush`](#flush)

*Called by:* [`reanalyze`](#reanalyze)

---

<a id="analyseentity"></a>

### `analyseEntity`

`function` | [static/js/estorides.js:1193](../../static/js/estorides.js#L1193)

```javascript
function analyseEntity(value, type, node)
```

Analyse a single graph/fusion entity: seed the analysis context with the entity's own data (kept in the Results context so re-analysis uses it) and stream an assessment into the Analysis tab.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` |  |  |  |
| `type` |  |  |  |
| `node` |  |  |  |

*Calls:* [`loadAnalysisModels`](#loadanalysismodels), [`reanalyze`](#reanalyze), [`renderAnalysis`](#renderanalysis), [`switchSidebarTab`](#switchsidebartab)

*Called by:* [`doSearch`](#dosearch), [`loadFusionTopChanged`](#loadfusiontopchanged), [`showContextMenu`](#showcontextmenu), [`showNodeTooltip`](#shownodetooltip)

---

<a id="expandnode"></a>

### `expandNode`

`function` `async` | [static/js/estorides.js:1226](../../static/js/estorides.js#L1226)

```javascript
async function expandNode(type, value)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `type` |  |  |  |
| `value` |  |  |  |

*Calls:* [`mergeExpansionIntoGraph`](#mergeexpansionintograph), [`setStatus`](#setstatus)

*Called by:* [`plotPoints`](#plotpoints), [`renderEntities`](#renderentities), [`renderGraphCore`](#rendergraphcore), [`showContextMenu`](#showcontextmenu)

---

<a id="mergeexpansionintograph"></a>

### `mergeExpansionIntoGraph`

`function` | [static/js/estorides.js:1256](../../static/js/estorides.js#L1256)

```javascript
function mergeExpansionIntoGraph(payload)
```

Merge a /api/intel/resolve response into the current D3 graph and Leaflet map.

Idempotent: re-clicking the same node won't duplicate edges. Returns {nodes, links} counts of what was actually added. Every merge pushes a batch onto window._graphBatches so Ctrl+Z (window.undoGraph) can pop it and repaint without that batch.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` |  |  |  |

*Calls:* [`drawGraphWithExtras`](#drawgraphwithextras), [`escapeHTML`](#escapehtml), [`validCoord`](#validcoord)

*Called by:* [`expandNode`](#expandnode), [`flush`](#flush), [`runTransform`](#runtransform)

---

<a id="k"></a>

### `k`

`function` `const` | [static/js/estorides.js:1270](../../static/js/estorides.js#L1270)

```javascript
const k = (l.source || '') + '|' + (l.target || '') + '|' + (l.relation || '');
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `source` | `l. \|\| ''` |  |  |

---

<a id="drawgraphwithextras"></a>

### `drawGraphWithExtras`

`function` | [static/js/estorides.js:1320](../../static/js/estorides.js#L1320)

```javascript
function drawGraphWithExtras(extraNodes, extraLinks)
```

Re-draws the D3 graph with the original nodes/edges PLUS any extras passed in (from a /api/intel/resolve call).

The extras are translated to the shape the drawGraph() function already understands (id, label, type, color, size).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `extraNodes` |  |  |  |
| `extraLinks` |  |  |  |

*Calls:* [`deriveClusters`](#deriveclusters), [`is3DActive`](#is3dactive), [`pushLink`](#pushlink), [`renderGraphCore`](#rendergraphcore)

*Called by:* [`mergeExpansionIntoGraph`](#mergeexpansionintograph), [`undoGraph`](#undograph)

---

<a id="pushlink"></a>

### `pushLink`

`function` | [static/js/estorides.js:1344](../../static/js/estorides.js#L1344)

```javascript
function pushLink(src, tgt, rel, inter)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `src` |  |  |  |
| `tgt` |  |  |  |
| `rel` |  |  |  |
| `inter` |  |  |  |

*Called by:* [`drawGraphWithExtras`](#drawgraphwithextras)

---

<a id="is3dactive"></a>

### `is3DActive`

`function` | [static/js/estorides.js:1367](../../static/js/estorides.js#L1367)

```javascript
function is3DActive()
```

True while the force-graph module owns the canvas in 3D mode.

*Called by:* [`drawGraphWithExtras`](#drawgraphwithextras), [`renderGraphCore`](#rendergraphcore)

---

<a id="cluster_palette"></a>

### `CLUSTER_PALETTE`

`function` `const` | [static/js/estorides.js:1388](../../static/js/estorides.js#L1388)

```javascript
const CLUSTER_PALETTE = (TELEMETRY.cluster_palette || [ '#5B8FF9', '#5AD8A6', '#F6BD16', '#E8684A', '#6DC8EC', '#9270CA', '#FF9D4D', '#269A99', '#FF99C3', '#A0D911', '#FF6B6B', '#36CFC9', '#B37FEB', '#FFC53D', '#7CB305', ])
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `CB305` | `TELEMETRY.cluster_palette \|\| [ '#5B8FF9', '#5AD8A6', '#F6BD16', '#E8684A', '#6DC8EC', '#9270CA', '#FF9D4D', '#269A99', '#FF99C3', '#A0D911', '#FF6B6B', '#36CFC9', '#B37FEB', '#FFC53D', '#7 ', ]` |  |  |

---

<a id="resolvertypefor"></a>

### `resolverTypeFor`

`function` | [static/js/estorides.js:1395](../../static/js/estorides.js#L1395)

```javascript
function resolverTypeFor(node)
```

Map a graph node's type/kind onto a resolver/transform entity type.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `node` |  |  |  |

*Called by:* [`renderGraphCore`](#rendergraphcore), [`selectNode`](#selectnode), [`showContextMenu`](#showcontextmenu)

---

<a id="saveleveloverrides"></a>

### `saveLevelOverrides`

`function` | [static/js/estorides.js:1411](../../static/js/estorides.js#L1411)

```javascript
function saveLevelOverrides()
```

*Called by:* [`setNodeLevel`](#setnodelevel)

---

<a id="levelof"></a>

### `levelOf`

`function` | [static/js/estorides.js:1415](../../static/js/estorides.js#L1415)

```javascript
function levelOf(node)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `node` |  |  |  |

*Called by:* [`applyLevelStyles`](#applylevelstyles), [`renderGraphCore`](#rendergraphcore), [`selectNode`](#selectnode), [`showNodeTooltip`](#shownodetooltip)

---

<a id="clustercolor"></a>

### `clusterColor`

`function` | [static/js/estorides.js:1419](../../static/js/estorides.js#L1419)

```javascript
function clusterColor(cid, clusters)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `cid` |  |  |  |
| `clusters` |  |  |  |

*Calls:* [`safeColor`](#safecolor)

*Called by:* [`deriveClusters`](#deriveclusters), [`drawHulls`](#drawhulls), [`showBridgeTooltip`](#showbridgetooltip)

---

<a id="c"></a>

### `c`

`function` `const` | [static/js/estorides.js:1421](../../static/js/estorides.js#L1421)

```javascript
const c = (clusters || []).find((x) => x.id === cid);
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `clusters` |  |  |  |

---

<a id="safecolor"></a>

### `safeColor`

`function` | [static/js/estorides.js:1429](../../static/js/estorides.js#L1429)

```javascript
function safeColor(v)
```

Cluster colors come from remote data (TELEMETRY.cluster_palette and per-cluster `color`).

Treat them as hostile: only accept a CSS-safe hex or rgb() colour, else fall back to a neutral grey. This keeps a tampered value from ever carrying CSS/HTML into the graph overlays.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `v` |  |  |  |

*Called by:* [`clusterColor`](#clustercolor), [`deriveClusters`](#deriveclusters), [`renderGraphCore`](#rendergraphcore)

---

<a id="deriveclusters"></a>

### `deriveClusters`

`function` | [static/js/estorides.js:1438](../../static/js/estorides.js#L1438)

```javascript
function deriveClusters(nodes)
```

Build a clusters[] summary from a flat node list (used after a merge when the server-side clusters array isn't carried along).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `nodes` |  |  |  |

*Calls:* [`clusterColor`](#clustercolor), [`safeColor`](#safecolor)

*Called by:* [`drawGraphWithExtras`](#drawgraphwithextras)

---

<a id="cid"></a>

### `cid`

`function` `const` | [static/js/estorides.js:1441](../../static/js/estorides.js#L1441)

```javascript
const cid = (n.cluster == null) ? -1 : n.cluster;
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `cluster` | `n.` | `= null` |  |

---

<a id="hidetooltip"></a>

### `hideTooltip`

`function` | [static/js/estorides.js:1451](../../static/js/estorides.js#L1451)

```javascript
function hideTooltip()
```

---- floating overlays (tooltip + context menu) ----

*Calls:* [`setVisible`](#setvisible)

*Called by:* [`renderGraphCore`](#rendergraphcore), [`showNodeTooltip`](#shownodetooltip)

---

<a id="purifyhtml"></a>

### `purifyHTML`

`function` | [static/js/estorides.js:1465](../../static/js/estorides.js#L1465)

```javascript
function purifyHTML(html)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `html` |  |  |  |

*Called by:* [`ensureLanConsent`](#ensurelanconsent), [`setSanitizedHTML`](#setsanitizedhtml)

---

<a id="setsanitizedhtml"></a>

### `setSanitizedHTML`

`function` | [static/js/estorides.js:1476](../../static/js/estorides.js#L1476)

```javascript
function setSanitizedHTML(el, html)
```

Append hostile markup: sanitize with DOMPurify, assign once.

When the library is missing, fall back to inert plain text (fail-closed).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `el` |  |  |  |
| `html` |  |  |  |

*Calls:* [`purifyHTML`](#purifyhtml)

*Called by:* [`ensureLanConsent`](#ensurelanconsent), [`renderMarkdownInto`](#rendermarkdowninto), [`showTooltipAt`](#showtooltipat)

---

<a id="showtooltipat"></a>

### `showTooltipAt`

`function` | [static/js/estorides.js:1485](../../static/js/estorides.js#L1485)

```javascript
function showTooltipAt(ev, html, paint)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ev` |  |  |  |
| `html` |  |  |  |
| `paint` |  |  |  |

*Calls:* [`setSanitizedHTML`](#setsanitizedhtml), [`setVisible`](#setvisible)

*Called by:* [`showBridgeTooltip`](#showbridgetooltip), [`showNodeTooltip`](#shownodetooltip)

---

<a id="hidecontextmenu"></a>

### `hideContextMenu`

`function` | [static/js/estorides.js:1495](../../static/js/estorides.js#L1495)

```javascript
function hideContextMenu()
```

*Calls:* [`setVisible`](#setvisible)

*Called by:* [`renderGraphCore`](#rendergraphcore), [`showContextMenu`](#showcontextmenu)

---

<a id="showbridgetooltip"></a>

### `showBridgeTooltip`

`function` | [static/js/estorides.js:1500](../../static/js/estorides.js#L1500)

```javascript
function showBridgeTooltip(ev, d, clusters)
```

Cross-referenced tooltip for an inter-cluster (bridge) link.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ev` |  |  |  |
| `d` |  |  |  |
| `clusters` |  |  |  |

*Calls:* [`clusterColor`](#clustercolor), [`escapeHTML`](#escapehtml), [`labelFor`](#labelfor), [`showTooltipAt`](#showtooltipat)

*Called by:* [`renderGraphCore`](#rendergraphcore)

---

<a id="labelfor"></a>

### `labelFor`

`function` `const` | [static/js/estorides.js:1503](../../static/js/estorides.js#L1503)

```javascript
const labelFor = (cid) =>
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `cid` |  |  |  |

*Called by:* [`showBridgeTooltip`](#showbridgetooltip)

---

<a id="c"></a>

### `c`

`function` `const` | [static/js/estorides.js:1504](../../static/js/estorides.js#L1504)

```javascript
const c = (clusters || []).find((x) => x.id === cid);
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `clusters` |  |  |  |

---

<a id="shownodetooltip"></a>

### `showNodeTooltip`

`function` | [static/js/estorides.js:1529](../../static/js/estorides.js#L1529)

```javascript
function showNodeTooltip(ev, d)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ev` |  |  |  |
| `d` |  |  |  |

*Calls:* [`analyseEntity`](#analyseentity), [`escapeHTML`](#escapehtml), [`hideTooltip`](#hidetooltip), [`levelOf`](#levelof), [`showTooltipAt`](#showtooltipat)

*Called by:* [`renderGraphCore`](#rendergraphcore)

---

<a id="showcontextmenu"></a>

### `showContextMenu`

`function` | [static/js/estorides.js:1548](../../static/js/estorides.js#L1548)

```javascript
function showContextMenu(ev, d)
```

---- context menu: transforms grouped by intel tier ----

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ev` |  |  |  |
| `d` |  |  |  |

*Calls:* [`analyseEntity`](#analyseentity), [`escapeHTML`](#escapehtml), [`expandNode`](#expandnode), [`focusNode`](#focusnode), [`hideContextMenu`](#hidecontextmenu), [`resolverTypeFor`](#resolvertypefor), [`runTransform`](#runtransform), [`runTransformStream`](#runtransformstream), [`searchEntity`](#searchentity), [`setNodeLevel`](#setnodelevel), [`setVisible`](#setvisible)

*Called by:* [`renderGraphCore`](#rendergraphcore)

---

<a id="tr"></a>

### `tr`

`function` `const` | [static/js/estorides.js:1598](../../static/js/estorides.js#L1598)

```javascript
const tr = (j && j.transforms) || [];
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `transforms` | `j && j.` |  |  |

---

<a id="setnodelevel"></a>

### `setNodeLevel`

`function` | [static/js/estorides.js:1623](../../static/js/estorides.js#L1623)

```javascript
function setNodeLevel(d, level)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `d` |  |  |  |
| `level` |  |  |  |

*Calls:* [`applyLevelStyles`](#applylevelstyles), [`saveLevelOverrides`](#saveleveloverrides), [`selectNode`](#selectnode)

*Called by:* [`selectNode`](#selectnode), [`showContextMenu`](#showcontextmenu)

---

<a id="applylevelstyles"></a>

### `applyLevelStyles`

`function` | [static/js/estorides.js:1632](../../static/js/estorides.js#L1632)

```javascript
function applyLevelStyles()
```

Re-apply level rings to every rendered node circle.

*Calls:* [`levelOf`](#levelof)

*Called by:* [`setNodeLevel`](#setnodelevel)

---

<a id="focusnode"></a>

### `focusNode`

`function` | [static/js/estorides.js:1640](../../static/js/estorides.js#L1640)

```javascript
function focusNode(d)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `d` |  |  |  |

*Called by:* [`renderGraphCore`](#rendergraphcore), [`showContextMenu`](#showcontextmenu)

---

<a id="barh"></a>

### `barH`

`function` `const` | [static/js/estorides.js:1644](../../static/js/estorides.js#L1644)

```javascript
const barH = (bar && !bar.hidden) ? bar.offsetHeight : 0;
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `hidden` | `bar && !bar.` |  |  |

---

<a id="runtransform"></a>

### `runTransform`

`function` `async` | [static/js/estorides.js:1654](../../static/js/estorides.js#L1654)

```javascript
async function runTransform(transformId, type, value)
```

Run a graph pivot transform and merge the result into the graph+map.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `transformId` |  |  |  |
| `type` |  |  |  |
| `value` |  |  |  |

*Calls:* [`mergeExpansionIntoGraph`](#mergeexpansionintograph), [`setStatus`](#setstatus), [`links`](static.js.graph_force.js.md#links)

*Called by:* [`selectNode`](#selectnode), [`showContextMenu`](#showcontextmenu)

---

<a id="runtransformstream"></a>

### `runTransformStream`

`function` `async` | [static/js/estorides.js:1675](../../static/js/estorides.js#L1675)

```javascript
async function runTransformStream(transformId, type, value)
```

Stream a transform over SSE so the graph "explodes" progressively.

Shift+click on a context-menu transform uses this path; plain click keeps the single-POST path above. Both merge through the same dedupe (_expansionSeen) and history (_graphBatches) machinery.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `transformId` |  |  |  |
| `type` |  |  |  |
| `value` |  |  |  |

*Calls:* [`flush`](#flush), [`setStatus`](#setstatus)

*Called by:* [`selectNode`](#selectnode), [`showContextMenu`](#showcontextmenu)

---

<a id="flush"></a>

### `flush`

`function` `const` | [static/js/estorides.js:1681](../../static/js/estorides.js#L1681)

```javascript
const flush = () =>
```

*Calls:* [`mergeExpansionIntoGraph`](#mergeexpansionintograph)

---

<a id="undograph"></a>

### `undoGraph`

`function` | [static/js/estorides.js:1735](../../static/js/estorides.js#L1735)

```javascript
function undoGraph()
```

Undo the last graph expansion (transform / resolve).

Rebuilds the dedupe set from the surviving batches and repaints the base graph plus those extras — the popped batch vanishes from the canvas.

*Calls:* [`drawGraphWithExtras`](#drawgraphwithextras), [`setStatus`](#setstatus)

---

<a id="k"></a>

### `k`

`function` `const` | [static/js/estorides.js:1748](../../static/js/estorides.js#L1748)

```javascript
const k = (l.source || '') + '|' + (l.target || '') + '|' + (l.relation || '');
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `source` | `l. \|\| ''` |  |  |

---

<a id="selectnode"></a>

### `selectNode`

`function` | [static/js/estorides.js:1770](../../static/js/estorides.js#L1770)

```javascript
function selectNode(d)
```

---- side inspector panel ----

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `d` |  |  |  |

*Calls:* [`add`](#add), [`addText`](#addtext), [`levelOf`](#levelof), [`resolverTypeFor`](#resolvertypefor), [`runTransform`](#runtransform), [`runTransformStream`](#runtransformstream), [`setNodeLevel`](#setnodelevel), [`setVisible`](#setvisible)

*Called by:* [`renderGraphCore`](#rendergraphcore), [`setNodeLevel`](#setnodelevel)

---

<a id="add"></a>

### `add`

`function` | [static/js/estorides.js:1781](../../static/js/estorides.js#L1781)

```javascript
function add(container, tag, className)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `container` |  |  |  |
| `tag` |  |  |  |
| `className` |  |  |  |

*Called by:* [`addText`](#addtext), [`selectNode`](#selectnode)

---

<a id="addtext"></a>

### `addText`

`function` | [static/js/estorides.js:1787](../../static/js/estorides.js#L1787)

```javascript
function addText(container, tag, className, text)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `container` |  |  |  |
| `tag` |  |  |  |
| `className` |  |  |  |
| `text` |  |  |  |

*Calls:* [`add`](#add)

*Called by:* [`selectNode`](#selectnode)

---

<a id="tr"></a>

### `tr`

`function` `const` | [static/js/estorides.js:1838](../../static/js/estorides.js#L1838)

```javascript
const tr = (j && j.transforms) || [];
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `transforms` | `j && j.` |  |  |

---

<a id="rendergraphcore"></a>

### `renderGraphCore`

`function` | [static/js/estorides.js:1874](../../static/js/estorides.js#L1874)

```javascript
function renderGraphCore(nodes, edges, clusters)
```

---- unified force-graph renderer (clusters + rings + interactions) ----

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `nodes` |  |  |  |
| `edges` |  |  |  |
| `clusters` |  |  |  |

*Calls:* [`drawHulls`](#drawhulls), [`expandNode`](#expandnode), [`focusNode`](#focusnode), [`hideContextMenu`](#hidecontextmenu), [`hideTooltip`](#hidetooltip), [`is3DActive`](#is3dactive), [`levelOf`](#levelof), [`on`](#on), [`resolverTypeFor`](#resolvertypefor), [`safeColor`](#safecolor), [`selectNode`](#selectnode), [`showBridgeTooltip`](#showbridgetooltip) and 4 more

*Called by:* [`drawGraph`](#drawgraph), [`drawGraphWithExtras`](#drawgraphwithextras)

---

<a id="barh"></a>

### `barH`

`function` `const` | [static/js/estorides.js:1893](../../static/js/estorides.js#L1893)

```javascript
const barH = (bar && !bar.hidden) ? bar.offsetHeight : 0;
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `hidden` | `bar && !bar.` |  |  |

---

<a id="drawhulls"></a>

### `drawHulls`

`function` | [static/js/estorides.js:1962](../../static/js/estorides.js#L1962)

```javascript
function drawHulls()
```

*Calls:* [`merge`](estorides_core.entity_extraction.py.md#merge), [`clusterColor`](#clustercolor)

*Called by:* [`renderGraphCore`](#rendergraphcore)

---

<a id="setstatusdot"></a>

### `setStatusDot`

`function` | [static/js/estorides.js:1999](../../static/js/estorides.js#L1999)

```javascript
function setStatusDot(state)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `state` |  |  |  |

*Called by:* [`clearAll`](#clearall), [`handleRunStreamEvent`](#handlerunstreamevent), [`hideWorkingIndicator`](#hideworkingindicator), [`runQuery`](#runquery), [`runQueryBlocking`](#runqueryblocking), [`searchEntity`](#searchentity), [`showWorkingIndicator`](#showworkingindicator), [`startLanScan`](#startlanscan)

---

<a id="showworkingindicator"></a>

### `showWorkingIndicator`

`function` | [static/js/estorides.js:2005](../../static/js/estorides.js#L2005)

```javascript
function showWorkingIndicator()
```

*Calls:* [`setStatusDot`](#setstatusdot)

*Called by:* [`runQuery`](#runquery), [`runQueryBlocking`](#runqueryblocking), [`searchEntity`](#searchentity), [`startLanScan`](#startlanscan)

---

<a id="hideworkingindicator"></a>

### `hideWorkingIndicator`

`function` | [static/js/estorides.js:2010](../../static/js/estorides.js#L2010)

```javascript
function hideWorkingIndicator()
```

*Calls:* [`setStatusDot`](#setstatusdot)

*Called by:* [`runQuery`](#runquery), [`runQueryBlocking`](#runqueryblocking), [`searchEntity`](#searchentity), [`startLanScan`](#startlanscan)

---

<a id="toggletiersection"></a>

### `toggleTierSection`

`function` | [static/js/estorides.js:2015](../../static/js/estorides.js#L2015)

```javascript
function toggleTierSection(key, header)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `key` |  |  |  |
| `header` |  |  |  |

*Called by:* [`renderTieredResults`](#rendertieredresults)

---

<a id="rendertieredresults"></a>

### `renderTieredResults`

`function` | [static/js/estorides.js:2023](../../static/js/estorides.js#L2023)

```javascript
function renderTieredResults(data)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml), [`toggleTierSection`](#toggletiersection)

*Called by:* [`runQueryBlocking`](#runqueryblocking)

---

<a id="escapeattr"></a>

### `escapeAttr`

`function` | [static/js/estorides.js:2089](../../static/js/estorides.js#L2089)

```javascript
function escapeAttr(s)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `s` |  |  |  |

*Called by:* [`doSearch`](#dosearch), [`loadFusionTopChanged`](#loadfusiontopchanged), [`plotPoints`](#plotpoints)

---

<a id="buildmapcoords"></a>

### `buildMapCoords`

`function` | [static/js/estorides.js:2125](../../static/js/estorides.js#L2125)

```javascript
function buildMapCoords(data)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` |  |  |  |

*Calls:* [`colorFor`](#colorfor), [`colorForKind`](#colorforkind), [`validCoord`](#validcoord)

*Called by:* [`renderResult`](#renderresult), [`replotStreamData`](#replotstreamdata)

---

<a id="validcoord"></a>

### `validCoord`

`function` | [static/js/estorides.js:2221](../../static/js/estorides.js#L2221)

```javascript
function validCoord(lat, lon)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `lat` |  |  |  |
| `lon` |  |  |  |

*Called by:* [`buildCaseMapCoords`](#buildcasemapcoords), [`buildMapCoords`](#buildmapcoords), [`mergeExpansionIntoGraph`](#mergeexpansionintograph)

---

<a id="colorfor"></a>

### `colorFor`

`function` | [static/js/estorides.js:2225](../../static/js/estorides.js#L2225)

```javascript
function colorFor(category)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `category` |  |  |  |

*Called by:* [`buildMapCoords`](#buildmapcoords)

---

<a id="renderentities"></a>

### `renderEntities`

`function` | [static/js/estorides.js:2244](../../static/js/estorides.js#L2244)

```javascript
function renderEntities(entities)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entities` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml), [`expandNode`](#expandnode), [`focusGraphNodeByValue`](#focusgraphnodebyvalue)

*Called by:* [`renderResult`](#renderresult), [`restoreCaseToWorkspace`](#restorecasetoworkspace)

---

<a id="rendergraphsummary"></a>

### `renderGraphSummary`

`function` | [static/js/estorides.js:2296](../../static/js/estorides.js#L2296)

```javascript
function renderGraphSummary(g)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `g` |  |  |  |

*Calls:* [`colorForKind`](#colorforkind), [`entities`](#entities)

*Called by:* [`handleRunStreamEvent`](#handlerunstreamevent), [`renderResult`](#renderresult), [`restoreCaseToWorkspace`](#restorecasetoworkspace)

---

<a id="colorforkind"></a>

### `colorForKind`

`function` | [static/js/estorides.js:2325](../../static/js/estorides.js#L2325)

```javascript
function colorForKind(k)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `k` |  |  |  |

*Called by:* [`buildCaseMapCoords`](#buildcasemapcoords), [`buildMapCoords`](#buildmapcoords), [`renderGraphSummary`](#rendergraphsummary)

---

<a id="rendertimeline"></a>

### `renderTimeline`

`function` | [static/js/estorides.js:2333](../../static/js/estorides.js#L2333)

```javascript
function renderTimeline(data)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml), [`filterTimeline`](#filtertimeline), [`fmtTime`](#fmttime), [`setVisible`](#setvisible), [`truncate`](#truncate)

*Called by:* [`renderResult`](#renderresult), [`replotStreamData`](#replotstreamdata), [`restoreCaseToWorkspace`](#restorecasetoworkspace)

---

<a id="obs"></a>

### `obs`

`function` | [static/js/estorides.js:2337](../../static/js/estorides.js#L2337)

```javascript
var obs = (data.observations || []).slice();
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `observations` | `data. \|\| []` |  |  |

---

<a id="frac"></a>

### `frac`

`function` | [static/js/estorides.js:2370](../../static/js/estorides.js#L2370)

```javascript
var frac = ((ts - minTs) / range);
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `range` | `(ts - minTs) /` |  |  |

---

<a id="fmttime"></a>

### `fmtTime`

`function` | [static/js/estorides.js:2383](../../static/js/estorides.js#L2383)

```javascript
function fmtTime(ts)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ts` |  |  |  |

*Called by:* [`renderTimeline`](#rendertimeline)

---

<a id="filtertimeline"></a>

### `filterTimeline`

`function` | [static/js/estorides.js:2394](../../static/js/estorides.js#L2394)

```javascript
function filterTimeline(fracVal)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `fracVal` |  |  |  |

*Called by:* [`renderTimeline`](#rendertimeline)

---

<a id="drawgraph"></a>

### `drawGraph`

`function` `async` | [static/js/estorides.js:2443](../../static/js/estorides.js#L2443)

```javascript
async function drawGraph()
```

---- D3 graph view ----

*Calls:* [`renderGraphCore`](#rendergraphcore)

*Called by:* [`startLanScan`](#startlanscan)

---

<a id="loadcases"></a>

### `loadCases`

`function` | [static/js/estorides.js:2473](../../static/js/estorides.js#L2473)

```javascript
function loadCases()
```

*Calls:* [`openCaseDetail`](#opencasedetail)

*Called by:* [`caseActionSave`](#caseactionsave)

---

<a id="q"></a>

### `q`

`function` `const` | [static/js/estorides.js:2474](../../static/js/estorides.js#L2474)

```javascript
const q = (caseSearch && caseSearch.value) || '';
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `caseSearch && caseSearch.` |  |  |

---

<a id="opencasedetail"></a>

### `openCaseDetail`

`function` | [static/js/estorides.js:2499](../../static/js/estorides.js#L2499)

```javascript
function openCaseDetail(c)
```

Rich case modal: loads the saved DB record (query, entities, observations) and offers Analyse (re-run on the case data) and "Load in workspace" (restore entities into the tabs).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `c` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml), [`loadAnalysisModels`](#loadanalysismodels), [`openModal`](#openmodal), [`reanalyze`](#reanalyze), [`renderAnalysis`](#renderanalysis), [`restoreCaseToWorkspace`](#restorecasetoworkspace), [`switchSidebarTab`](#switchsidebartab)

*Called by:* [`loadCases`](#loadcases)

---

<a id="entities"></a>

### `entities`

`function` `const` | [static/js/estorides.js:2500](../../static/js/estorides.js#L2500)

```javascript
const entities = (c.entities || []).slice(0, 40);
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entities` | `c. \|\| []` |  |  |

*Called by:* [`renderGraphSummary`](#rendergraphsummary)

---

<a id="obs"></a>

### `obs`

`function` `const` | [static/js/estorides.js:2501](../../static/js/estorides.js#L2501)

```javascript
const obs = (c.observations || []).slice(0, 30);
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `observations` | `c. \|\| []` |  |  |

---

<a id="restorecasetoworkspace"></a>

### `restoreCaseToWorkspace`

`function` | [static/js/estorides.js:2554](../../static/js/estorides.js#L2554)

```javascript
function restoreCaseToWorkspace(c)
```

Restore a case's saved entities into the workspace tabs (entities list, graph summary, map, timeline) without re-running collection.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `c` |  |  |  |

*Calls:* [`buildCaseMapCoords`](#buildcasemapcoords), [`plotPoints`](#plotpoints), [`renderEntities`](#renderentities), [`renderGraphSummary`](#rendergraphsummary), [`renderTimeline`](#rendertimeline), [`showEmptyState`](#showemptystate), [`showToast`](#showtoast)

*Called by:* [`openCaseDetail`](#opencasedetail)

---

<a id="buildcasemapcoords"></a>

### `buildCaseMapCoords`

`function` | [static/js/estorides.js:2575](../../static/js/estorides.js#L2575)

```javascript
function buildCaseMapCoords(entities)
```

Build map coords from a case's saved entities, reusing the same latitude/longitude resolution and country-centroid fallback as the normal run renderer so a case without explicit lat/lon still drops pins.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entities` |  |  |  |

*Calls:* [`colorForKind`](#colorforkind), [`validCoord`](#validcoord)

*Called by:* [`restoreCaseToWorkspace`](#restorecasetoworkspace)

---

<a id="rendercaseitem"></a>

### `renderCaseItem`

`function` | [static/js/estorides.js:2593](../../static/js/estorides.js#L2593)

```javascript
function renderCaseItem(c)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `c` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml), [`truncate`](#truncate)

---

<a id="saved"></a>

### `saved`

`function` `const` | [static/js/estorides.js:2597](../../static/js/estorides.js#L2597)

```javascript
const saved = (c.notes || '').indexOf('[saved]') === 0;
```

Saved cases get a visible bookmark pill so the operator can scan the list for "things I came back to" at a glance.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `notes` | `c. \|\| ''` |  |  |

---

<a id="debounce"></a>

### `debounce`

`function` | [static/js/estorides.js:2619](../../static/js/estorides.js#L2619)

```javascript
function debounce(fn, ms)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `fn` |  |  |  |
| `ms` |  |  |  |

---

<a id="escapehtml"></a>

### `escapeHTML`

`function` | [static/js/estorides.js:2669](../../static/js/estorides.js#L2669)

```javascript
function escapeHTML(s)
```

---- utils ----

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `s` |  |  |  |

*Called by:* [`appendStreamEntity`](#appendstreamentity), [`buildResultCard`](#buildresultcard), [`confirmModal`](#confirmmodal), [`doSearch`](#dosearch), [`flush`](#flush), [`loadFusionEntityDetail`](#loadfusionentitydetail), [`loadFusionStats`](#loadfusionstats), [`loadFusionTopChanged`](#loadfusiontopchanged), [`mergeExpansionIntoGraph`](#mergeexpansionintograph), [`openCaseDetail`](#opencasedetail), [`openModal`](#openmodal), [`plotPoints`](#plotpoints) and 13 more

---

<a id="truncate"></a>

### `truncate`

`function` | [static/js/estorides.js:2674](../../static/js/estorides.js#L2674)

```javascript
function truncate(s, n)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `s` |  |  |  |
| `n` |  |  |  |

*Called by:* [`buildResultCard`](#buildresultcard), [`renderCaseItem`](#rendercaseitem), [`renderTimeline`](#rendertimeline), [`summariseObservation`](#summariseobservation)

---

<a id="caseactionsave"></a>

### `caseActionSave`

`function` | [static/js/estorides.js:2697](../../static/js/estorides.js#L2697)

```javascript
function caseActionSave(id, btn)
```

Bookmark a case.

The endpoint prefixes the notes column with "[saved]" so the bookmarked case surfaces in the list at a glance.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `id` |  |  |  |
| `btn` |  |  |  |

*Calls:* [`loadCases`](#loadcases), [`promptModal`](#promptmodal), [`showToast`](#showtoast)

---

<a id="caseactiondiff"></a>

### `caseActionDiff`

`function` | [static/js/estorides.js:2718](../../static/js/estorides.js#L2718)

```javascript
function caseActionDiff(id)
```

Compare this case to another.

The user picks the baseline; the response is rendered inline in a diff panel under the case.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `id` |  |  |  |

*Calls:* [`promptModal`](#promptmodal), [`renderCaseDiffPanel`](#rendercasediffpanel), [`showToast`](#showtoast)

---

<a id="rendercasediffpanel"></a>

### `renderCaseDiffPanel`

`function` | [static/js/estorides.js:2738](../../static/js/estorides.js#L2738)

```javascript
function renderCaseDiffPanel(caseId, diff)
```

Render the diff result below the case.

The panel survives until the user reloads the cases list (or opens another diff).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `caseId` |  |  |  |
| `diff` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml)

*Called by:* [`caseActionDiff`](#caseactiondiff)

---

<a id="rows"></a>

### `rows`

`function` `const` | [static/js/estorides.js:2746](../../static/js/estorides.js#L2746)

```javascript
const rows = (diff.added || []).slice(0, 25).map((e) =>
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `added` | `diff. \|\| []` |  |  |

*Called by:* [`GraphRagIndex.from_dict`](estorides_core.graph_rag_search.py.md#graphragindex-from_dict)

---

<a id="removed"></a>

### `removed`

`function` `const` | [static/js/estorides.js:2749](../../static/js/estorides.js#L2749)

```javascript
const removed = (diff.removed || []).slice(0, 10).map((e) =>
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `removed` | `diff. \|\| []` |  |  |

---

<a id="caseactionreport"></a>

### `caseActionReport`

`function` | [static/js/estorides.js:2779](../../static/js/estorides.js#L2779)

```javascript
function caseActionReport(id)
```

Render the Markdown report.

We just dump the text into a modal overlay — keeping it in-browser is enough; the CLI command produces a file copy for sharing.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `id` |  |  |  |

*Calls:* [`showReportModal`](#showreportmodal), [`showToast`](#showtoast)

---

<a id="showreportmodal"></a>

### `showReportModal`

`function` | [static/js/estorides.js:2815](../../static/js/estorides.js#L2815)

```javascript
function showReportModal(text)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `text` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml)

*Called by:* [`caseActionReport`](#caseactionreport)

---

<a id="openmodal"></a>

### `openModal`

`function` | [static/js/estorides.js:2843](../../static/js/estorides.js#L2843)

```javascript
function openModal(opts)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `opts` |  |  |  |

*Calls:* [`close`](#close), [`escapeHTML`](#escapehtml)

*Called by:* [`confirmModal`](#confirmmodal), [`openCaseDetail`](#opencasedetail), [`promptModal`](#promptmodal)

---

<a id="actions"></a>

### `actions`

`function` `const` | [static/js/estorides.js:2849](../../static/js/estorides.js#L2849)

```javascript
const actions = (opts.actions || []).map((a, i) =>
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `actions` | `opts. \|\| []` |  |  |

---

<a id="close"></a>

### `close`

`function` `const` | [static/js/estorides.js:2863](../../static/js/estorides.js#L2863)

```javascript
const close = () => { modal.remove(); if (opts.onClose) opts.onClose(); };
```

*Called by:* [`openModal`](#openmodal)

---

<a id="promptmodal"></a>

### `promptModal`

`function` | [static/js/estorides.js:2878](../../static/js/estorides.js#L2878)

```javascript
function promptModal(opts)
```

Promise-style text prompt.

Resolves with a sanitized string or null.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `opts` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml), [`openModal`](#openmodal)

*Called by:* [`caseActionDiff`](#caseactiondiff), [`caseActionSave`](#caseactionsave)

---

<a id="confirmmodal"></a>

### `confirmModal`

`function` | [static/js/estorides.js:2902](../../static/js/estorides.js#L2902)

```javascript
function confirmModal(opts)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `opts` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml), [`openModal`](#openmodal)

---

<a id="tag"></a>

### `tag`

`function` `const` | [static/js/estorides.js:2964](../../static/js/estorides.js#L2964)

```javascript
const tag = (ev.target && ev.target.tagName) || '';
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `tagName` | `ev.target && ev.target.` |  |  |

---

<a id="loadsidebarwidth"></a>

### `loadSidebarWidth`

`function` | [static/js/estorides.js:2994](../../static/js/estorides.js#L2994)

```javascript
function loadSidebarWidth()
```

Responsive sidebar toggle + resizable divider.

---

<a id="savesidebarwidth"></a>

### `saveSidebarWidth`

`function` | [static/js/estorides.js:3005](../../static/js/estorides.js#L3005)

```javascript
function saveSidebarWidth(w)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `w` |  |  |  |

---

<a id="loadsidebarcollapsed"></a>

### `loadSidebarCollapsed`

`function` | [static/js/estorides.js:3008](../../static/js/estorides.js#L3008)

```javascript
function loadSidebarCollapsed()
```

---

<a id="savesidebarcollapsed"></a>

### `saveSidebarCollapsed`

`function` | [static/js/estorides.js:3016](../../static/js/estorides.js#L3016)

```javascript
function saveSidebarCollapsed(v)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `v` |  |  |  |

---

<a id="switchsidebartab"></a>

### `switchSidebarTab`

`function` | [static/js/estorides.js:3074](../../static/js/estorides.js#L3074)

```javascript
function switchSidebarTab(idx)
```

---- Fusion tab ----

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `idx` |  |  |  |

*Calls:* [`loadAnalysisModels`](#loadanalysismodels), [`loadFusionTab`](#loadfusiontab)

---

<a id="loadfusiontab"></a>

### `loadFusionTab`

`function` | [static/js/estorides.js:3087](../../static/js/estorides.js#L3087)

```javascript
function loadFusionTab()
```

*Calls:* [`loadFusionSearch`](#loadfusionsearch), [`loadFusionStats`](#loadfusionstats), [`loadFusionTopChanged`](#loadfusiontopchanged)

*Called by:* [`switchSidebarTab`](#switchsidebartab)

---

<a id="loadfusionstats"></a>

### `loadFusionStats`

`function` | [static/js/estorides.js:3093](../../static/js/estorides.js#L3093)

```javascript
function loadFusionStats()
```

*Calls:* [`escapeHTML`](#escapehtml)

*Called by:* [`loadFusionTab`](#loadfusiontab)

---

<a id="loadfusiontopchanged"></a>

### `loadFusionTopChanged`

`function` | [static/js/estorides.js:3112](../../static/js/estorides.js#L3112)

```javascript
function loadFusionTopChanged()
```

*Calls:* [`analyseEntity`](#analyseentity), [`escapeAttr`](#escapeattr), [`escapeHTML`](#escapehtml), [`loadFusionEntityDetail`](#loadfusionentitydetail)

*Called by:* [`loadFusionTab`](#loadfusiontab)

---

<a id="loadfusionsearch"></a>

### `loadFusionSearch`

`function` | [static/js/estorides.js:3141](../../static/js/estorides.js#L3141)

```javascript
function loadFusionSearch()
```

*Calls:* [`doSearch`](#dosearch)

*Called by:* [`loadFusionTab`](#loadfusiontab)

---

<a id="dosearch"></a>

### `doSearch`

`function` | [static/js/estorides.js:3148](../../static/js/estorides.js#L3148)

```javascript
function doSearch()
```

*Calls:* [`analyseEntity`](#analyseentity), [`escapeAttr`](#escapeattr), [`escapeHTML`](#escapehtml), [`loadFusionEntityDetail`](#loadfusionentitydetail)

*Called by:* [`loadFusionSearch`](#loadfusionsearch)

---

<a id="loadfusionentitydetail"></a>

### `loadFusionEntityDetail`

`function` | [static/js/estorides.js:3186](../../static/js/estorides.js#L3186)

```javascript
function loadFusionEntityDetail(eid)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `eid` |  |  |  |

*Calls:* [`escapeHTML`](#escapehtml)

*Called by:* [`doSearch`](#dosearch), [`loadFusionTopChanged`](#loadfusiontopchanged)

---

<a id="setstatus"></a>

### `setStatus`

`function` | [static/js/estorides.js:3283](../../static/js/estorides.js#L3283)

```javascript
function setStatus(text)
```

The discoverer code lives outside the IIFE, so the module-private setStatus is not in scope here.

Provide a global one that writes to the same footer element, guarded so a missing node can never throw.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `text` |  |  |  |

---

<a id="setdiscoverprogress"></a>

### `setDiscoverProgress`

`function` | [static/js/estorides.js:3290](../../static/js/estorides.js#L3290)

```javascript
function setDiscoverProgress(step, found, max)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `step` |  |  |  |
| `found` |  |  |  |
| `max` |  |  |  |

---

<a id="hidediscoverprogress"></a>

### `hideDiscoverProgress`

`function` | [static/js/estorides.js:3302](../../static/js/estorides.js#L3302)

```javascript
function hideDiscoverProgress()
```

---

<a id="startdiscover"></a>

### `startDiscover`

`function` `async` | [static/js/estorides.js:3307](../../static/js/estorides.js#L3307)

```javascript
async function startDiscover()
```

---

<a id="stopdiscover"></a>

### `stopDiscover`

`function` | [static/js/estorides.js:3391](../../static/js/estorides.js#L3391)

```javascript
function stopDiscover()
```

---

<a id="handlediscoverevent"></a>

### `handleDiscoverEvent`

`function` | [static/js/estorides.js:3408](../../static/js/estorides.js#L3408)

```javascript
function handleDiscoverEvent(ev)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ev` |  |  |  |

---

<a id="adddiscoverentitytotab"></a>

### `addDiscoverEntityToTab`

`function` | [static/js/estorides.js:3447](../../static/js/estorides.js#L3447)

```javascript
function addDiscoverEntityToTab(entity, from)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entity` |  |  |  |
| `from` |  |  |  |

---

<a id="sig"></a>

### `sig`

`function` `const` | [static/js/estorides.js:3451](../../static/js/estorides.js#L3451)

```javascript
const sig = (entity.type || '') + '|' + (entity.value || '');
```

Avoid duplicates with the simple in-memory check.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `type` | `entity. \|\| ''` |  |  |

---

<a id="escapehtml"></a>

### `escapeHtml`

`function` | [static/js/estorides.js:3475](../../static/js/estorides.js#L3475)

```javascript
function escapeHtml(s)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `s` |  |  |  |

---

<a id="maybeplotdiscoverentity"></a>

### `maybePlotDiscoverEntity`

`function` | [static/js/estorides.js:3480](../../static/js/estorides.js#L3480)

```javascript
function maybePlotDiscoverEntity(entity)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `entity` |  |  |  |

---

<a id="flushdiscoverentities"></a>

### `flushDiscoverEntities`

`function` | [static/js/estorides.js:3487](../../static/js/estorides.js#L3487)

```javascript
function flushDiscoverEntities()
```

---

<a id="check"></a>

### `check`

`function` | [static/js/estorides.js:3505](../../static/js/estorides.js#L3505)

```javascript
function check()
```

---

## Other Members

<a id="settimeout"></a>

### `setTimeout`

`method` | [static/js/estorides.js:2942](../../static/js/estorides.js#L2942)

```javascript
setTimeout(function() { splash.classList.add('hidden'); }, 1500);
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `hidden` | `function() { splash.classList.add(' '); }` |  |  |
| `1500` |  |  |  |

---

<a id="fetch"></a>

### `fetch`

`method` | [static/js/estorides.js:3326](../../static/js/estorides.js#L3326)

```javascript
fetch('/api/discover/start', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(Object.assign({ value: q, type: 'auto', max_depth: 2, max_steps: 30, max_entities: 1000, deadline_s: 20, parallel: 4, }, (window.EstoridesLan ? window.EstoridesLan.lanRunFields(q) :
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `start` | `'/api/discover/ '` |  |  |
| `{ method` | `'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(Object.assign({ value: q, type: 'auto', max_depth: 2, max_steps: 30, max_entities: 1000, deadline_s: 20, parallel: 4, }, (window.EstoridesLan ? window.EstoridesLan.lanRunFields(q) :` |  |  |

---
