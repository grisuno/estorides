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
    d.find_element(By.CSS_SELECTOR, '#gf-toolbar [data-engine="3d"]').click()
    time.sleep(12)
    print("total links:", d.execute_script("return window.GF.state.g3.graphData().links.length"))
    d.find_element(By.ID, "gf-bridges").click()
    time.sleep(2)
    print("bridges-only links:", d.execute_script("return window.GF.state.g3.graphData().links.length"))
    print("hud:", d.execute_script("return document.getElementById('gf-hud').textContent"))
    d.save_screenshot(".scratchpad/gfv2_bridges.png")
finally:
    d.quit()
