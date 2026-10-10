import time, json
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
const st = window.GF.state;
const byId = {};
st.raw.nodes.forEach(n => byId[n.id] = n);
const com = Object.values(byId).filter(n => n.type==='entity').map(n => n.community);
const uniq = [...new Set(com)];
let diff = 0, nullEnd = 0, same = 0, osint = 0;
st.raw.links.forEach(e => {
  if (e.type === 'member_of' || e.type === 'layered_as') return;
  osint++;
  const a = byId[e.source.id || e.source], b = byId[e.target.id || e.target];
  if (!a || !b || a.community == null || b.community == null) { nullEnd++; return; }
  if (a.community !== b.community) diff++; else same++;
});
return JSON.stringify({entities: com.length, uniqCommunities: uniq, osint, diff, same, nullEnd,
  sampleEnt: JSON.stringify(byId[st.raw.nodes.find(n=>n.type==='entity').id]).slice(0,200)});
"""))
finally:
    d.quit()
