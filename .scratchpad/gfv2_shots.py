import time, json
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
    d.get("http://127.0.0.1:5050/")
    time.sleep(3)
    try:
        skip = d.find_element(By.ID, "onboarding-skip")
        if skip.is_displayed():
            skip.click()
            time.sleep(1)
    except Exception as e:
        print("onboarding:", e)
    d.find_element(By.CSS_SELECTOR, '.canvas-tab[data-canvas="graph"]').click()
    time.sleep(2)
    # wait for toolbar (graph data present)
    shown = False
    for _ in range(30):
        try:
            tb = d.find_element(By.ID, "gf-toolbar")
            if tb.is_displayed():
                shown = True
                break
        except Exception:
            pass
        time.sleep(1)
    print("toolbar shown:", shown)
    print("graphData:", d.execute_script("return window._graphData ? {n:(window._graphData.nodes||[]).length, e:(window._graphData.edges||[]).length} : null"))
    d.save_screenshot(".scratchpad/gfv2_2d.png")
    if shown:
        d.find_element(By.CSS_SELECTOR, '#gf-toolbar [data-engine="3d"]').click()
        for _ in range(30):
            st = d.execute_script("return window.GF ? window.GF.state.engine : null")
            has3 = d.execute_script("return typeof ForceGraph3D !== 'undefined'")
            if st == "3d" and has3:
                break
            time.sleep(1)
        print("engine:", d.execute_script("return window.GF && window.GF.state.engine"), "has3D:", d.execute_script("return typeof ForceGraph3D !== 'undefined'"))
        time.sleep(9)
        print("nodes3d:", d.execute_script("return (window.GF && window.GF.state.g3) ? window.GF.state.g3.graphData().nodes.length : null"))
        d.save_screenshot(".scratchpad/gfv2_3d.png")
        # click center of stage
        stage = d.find_element(By.ID, "gf-stage")
        d.execute_script("arguments[0].scrollIntoView();", stage)
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(d).move_to_element(stage).click().perform()
        time.sleep(3)
        print("selected:", d.execute_script("return window.GF && window.GF.state.selected"))
        print("inspector:", d.execute_script("return !document.getElementById('graph-inspector').hidden"))
        d.save_screenshot(".scratchpad/gfv2_3d_click.png")
    for e in d.get_log("browser"):
        print("CONSOLE:", e.get("level"), (e.get("message") or "")[:220])
finally:
    d.quit()
