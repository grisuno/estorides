import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
opts = webdriver.ChromeOptions()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1600,900")
opts.add_argument("--no-sandbox")
opts.add_argument("--enable-unsafe-swiftshader")
d = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=opts)
d.set_page_load_timeout(60)
try:
    d.get("http://127.0.0.1:5050/")
    time.sleep(2)
    try:
        skip = d.find_element(By.ID, "onboarding-skip")
        if skip.is_displayed():
            skip.click(); time.sleep(1)
    except Exception:
        pass
    d.find_element(By.CSS_SELECTOR, '.canvas-tab[data-canvas="graph"]').click()
    time.sleep(3)
    print(d.execute_script("""
const gd = window._graphData || {};
const types = {};
(egd(gd) || []).forEach(e => types[e.type || e.relation || '?'] = (types[e.type || e.relation || '?'] || 0) + 1);
function egd(g) { return (g.force && g.force.edges) || g.edges || []; }
const rtypes = {};
((window.GF && window.GF.state.raw && window.GF.state.raw.links) || []).forEach(e => rtypes[e.type] = (rtypes[e.type] || 0) + 1);
return JSON.stringify({
  gdKeys: Object.keys(gd),
  hasForce: !!(gd.force && gd.force.nodes),
  forceNodes: gd.force ? gd.force.nodes.length : null,
  forceEdges: gd.force ? gd.force.edges.length : null,
  gdEdges: (gd.edges || []).length,
  edgeTypes: types,
  rawLinkTypes: rtypes,
  sampleEdge: JSON.stringify((egd(gd)[0] || null)).slice(0,200)
});
"""))
finally:
    d.quit()
