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
    time.sleep(4)
    print("2D svg present:", d.execute_script("return document.querySelectorAll('#graph-canvas > svg').length"))
    d.save_screenshot(".scratchpad/gfv2_2d.png")
    d.find_element(By.CSS_SELECTOR, '#gf-toolbar [data-engine="3d"]').click()
    time.sleep(12)
    print("links before bridges:", d.execute_script("return window.GF.state.g3.graphData().links.length"))
    d.find_element(By.ID, "gf-bridges").click()
    time.sleep(2)
    print("links bridges-only:", d.execute_script("return window.GF.state.g3.graphData().links.length"))
    d.find_element(By.ID, "gf-bridges").click()
    time.sleep(2)
    d.find_element(By.ID, "gf-orbit").click()
    time.sleep(1)
    print("orbit:", d.execute_script("return [window.GF.state.orbit, window.GF.state.g3.controls().autoRotate]"))
    d.find_element(By.ID, "gf-orbit").click()
    # back to 2D
    d.find_element(By.CSS_SELECTOR, '#gf-toolbar [data-engine="2d"]').click()
    time.sleep(3)
    print(d.execute_script("""
return JSON.stringify({
  engine: window.GF.state.engine,
  stageHidden: document.getElementById('gf-stage').hidden,
  svgVisible: Array.from(document.querySelectorAll('#graph-canvas > svg')).map(s => !s.classList.contains('gf-hide')),
  overlayCleared: (function(){const c=document.getElementById('gf-overlay3d');return c ? c.width : 'gone';})()
});"""))
    d.save_screenshot(".scratchpad/gfv2_back2d.png")
    errs = [e.get("message","")[:160] for e in d.get_log("browser") if e.get("level")=="SEVERE" and "Content Security" not in e.get("message","")]
    print("severe(non-csp):", errs if errs else "none")
finally:
    d.quit()
