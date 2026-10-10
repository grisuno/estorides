import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

opts = webdriver.ChromeOptions()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1600,900")
opts.add_argument("--no-sandbox")
opts.add_argument("--enable-unsafe-swiftshader")
opts.add_argument("--use-gl=angle")
opts.add_argument("--use-angle=swiftshader")
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
    time.sleep(2)
    d.find_element(By.CSS_SELECTOR, '#gf-toolbar [data-engine="3d"]').click()
    time.sleep(12)
    print(d.execute_script("""
const g = window.GF && window.GF.state.g3;
const cv = document.getElementById('gf-overlay3d');
const stage = document.getElementById('gf-stage');
if (!g) return 'NO_G3';
const data = g.graphData();
const withPos = data.nodes.filter(n => n.x != null).length;
let s = null, camInfo = null;
try {
  const n0 = data.nodes.find(n => n.x != null);
  s = n0 ? g.graph2ScreenCoords(n0.x, n0.y, n0.z || 0) : 'no-nodes-with-pos';
} catch (e) { s = 'ERR:' + e.message; }
try {
  const cam = g.camera();
  camInfo = cam ? {fov: cam.fov, pos: [cam.position.x, cam.position.y, cam.position.z].map(Math.round)} : 'no-cam';
} catch (e) { camInfo = 'ERR:' + e.message; }
return JSON.stringify({
  nodes: data.nodes.length, withPos,
  sample: s, cam: camInfo,
  ovSize: cv ? [cv.width, cv.height] : null,
  stageSize: stage ? [stage.clientWidth, stage.clientHeight] : null,
  ovCss: cv ? getComputedStyle(cv).cssText.slice(0,120) : null,
});
"""))
finally:
    d.quit()
