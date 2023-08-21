import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_fullpage_screenshot(device=2):
    # please note that we MUST use headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("https://www.youtube.com/watch?v=jakpo7tj7Qw&list=RDMM&index=5")
    time.sleep(2)

    height = driver.execute_script('return document.documentElement.scrollHeight')
    width  = 1080
    if (device == 0):
        width = 480
    elif (device == 1):
        width = 800
    else:
        width = 1080
    driver.set_window_size(width, height)  # the trick
    
    time.sleep(2)
    driver.save_screenshot("screenshot1.png")
    driver.quit()

test_fullpage_screenshot()