import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

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
    d.get("http://127.0.0.1:5051/")
    time.sleep(4)
    try:
        skip = d.find_element(By.ID, "onboarding-skip")
        if skip.is_displayed():
            skip.click()
            time.sleep(1)
    except Exception as e:
        print("onboarding:", e)
    d.find_element(By.CSS_SELECTOR, '.canvas-tab[data-canvas="bundles"]').click()
    shown = False
    for _ in range(30):
        try:
            st = d.find_element(By.ID, "gb-stage")
            if st.is_displayed() and st.size["width"] > 10:
                shown = True
                break
        except Exception:
            pass
        time.sleep(1)
    print("stage shown:", shown)
    time.sleep(6)
    print("bundle:", d.execute_script(
        "return window.EstoridesBundles ? 'api-ok' : 'no-api'"))
    print("counts:", d.execute_script(
        "return (window._graphData && window._graphData.bundle) ?"
        " {n: window._graphData.bundle.nodes.length,"
        " g: window._graphData.bundle.groups.length,"
        " e: window._graphData.bundle.edges.length} : null"))
    d.save_screenshot(".scratchpad/gb_circle.png")
    d.find_element(By.CSS_SELECTOR, '#bundles-canvas [data-view="3d"]').click()
    time.sleep(4)
    d.save_screenshot(".scratchpad/gb_sphere.png")
    print("done")
finally:
    d.quit()
