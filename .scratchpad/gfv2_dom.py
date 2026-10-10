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
    print("raw html has overlay:", d.execute_script("return document.documentElement.outerHTML.includes('gf-overlay3d')"))
    time.sleep(2)
    try:
        skip = d.find_element(By.ID, "onboarding-skip")
        if skip.is_displayed():
            skip.click(); time.sleep(1)
    except Exception:
        pass
    d.find_element(By.CSS_SELECTOR, '.canvas-tab[data-canvas="graph"]').click()
    time.sleep(2)
    print("pre-3d stage kids:", d.execute_script("return document.getElementById('gf-stage').childElementCount"))
    d.find_element(By.CSS_SELECTOR, '#gf-toolbar [data-engine="3d"]').click()
    time.sleep(12)
    print(d.execute_script("""
const st = document.getElementById('gf-stage');
const kids = [];
st.childNodes.forEach(n => kids.push(n.nodeName + '#' + (n.id||'') + '.' + (n.className && n.className.baseVal !== undefined ? '' : (n.className||''))));
return JSON.stringify({kids, overlay: !!document.getElementById('gf-overlay3d'),
  err: (document.getElementById('gf-engine-error')||{}).textContent});
"""))
finally:
    d.quit()
