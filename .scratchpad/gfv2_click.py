import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
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
    d.find_element(By.CSS_SELECTOR, '#gf-toolbar [data-engine="3d"]').click()
    time.sleep(12)
    # pick highest-rank entity, get its screen coords, click exactly there
    pt = d.execute_script("""
const g = window.GF.state.g3;
const data = g.graphData();
const ents = data.nodes.filter(n => n.type === 'entity' && n.x != null)
  .sort((a,b) => (b.rank||0) - (a.rank||0));
const n = ents[0];
const s = g.graph2ScreenCoords(n.x, n.y, n.z || 0);
return {id: n.id, label: n.label, sx: Math.round(s.x), sy: Math.round(s.y)};
""")
    print("target:", pt)
    stage = d.find_element(By.ID, "gf-stage")
    sz = d.execute_script("const r = document.getElementById('gf-stage').getBoundingClientRect(); return [r.width, r.height]")
    dx, dy = pt["sx"] - sz[0] / 2, pt["sy"] - sz[1] / 2
    print("offset from center:", round(dx), round(dy))
    ActionChains(d).move_to_element_with_offset(stage, dx, dy).click().perform()
    time.sleep(2)
    print("selected:", d.execute_script("return window.GF.state.selected"))
    print("inspector open:", d.execute_script("return !document.getElementById('graph-inspector').hidden"))
    print("title:", d.execute_script("return document.getElementById('inspector-title').textContent"))
    print("hud:", d.execute_script("return document.getElementById('gf-hud').textContent"))
    d.save_screenshot(".scratchpad/gfv2_3d_click.png")
finally:
    d.quit()
