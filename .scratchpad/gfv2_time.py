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
    for t in (2, 5, 9, 14):
        time.sleep(t - (0 if t == 2 else (2, 5, 9)[(2,5,9,14).index(t)-1]))
        print(t, d.execute_script("""
const st = document.getElementById('gf-stage');
const kids = [];
st.children.forEach ? null : null;
for (const n of st.children) kids.push(n.tagName + '#' + n.id);
return JSON.stringify({kids, g3: !!(window.GF && window.GF.state.g3),
  err: document.getElementById('gf-engine-error').textContent.slice(0,120)});
"""))
finally:
    d.quit()
