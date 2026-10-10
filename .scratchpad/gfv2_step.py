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
    print("stage html len pre-graph:", d.execute_script("return document.getElementById('gf-stage').innerHTML.length"))
    d.find_element(By.CSS_SELECTOR, '.canvas-tab[data-canvas="graph"]').click()
    time.sleep(3)
    print("stage kids pre-3d:", d.execute_script("return document.getElementById('gf-stage').innerHTML.slice(0,200)"))
    print(d.execute_script("""
const el = document.getElementById('gf-stage');
const ov = document.getElementById('gf-overlay3d');
el.textContent = '';
if (ov) el.appendChild(ov);
return 'after manual preserve: kids=' + el.childElementCount + ' overlay=' + !!document.getElementById('gf-overlay3d');
"""))
    print(d.execute_script("""
const el = document.getElementById('gf-stage');
const g = ForceGraph3D({controlType:'orbit'})(el);
return 'after engine construct: kids=' + el.childElementCount + ' overlay=' + !!document.getElementById('gf-overlay3d');
"""))
finally:
    d.quit()
