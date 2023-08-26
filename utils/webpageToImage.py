import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_fullpage_screenshot(url, filename):
    
    device = 2 # Laptop/PC

    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')

        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        time.sleep(2)

        height = driver.execute_script('return document.documentElement.scrollHeight')
        print(height)
        width  = 1080
        if (device == 0):
            width = 480
        elif (device == 1):
            width = 800
        else:
            width = 1080
        driver.set_window_size(width, height)  # the trick

        time.sleep(2)
        driver.save_screenshot(filename)
        driver.quit()
        return {"success" : True }
    except Exception as e:
        return {"success" : False, "error" : e }

# asas = take_fullpage_screenshot("https://stackoverflow.com/questions/5998245/how-do-i-get-the-current-time-in-milliseconds-in-python", "sdsd.png")
# print(asas)