# from pywebcopy import save_webpage

# url = 'https://www.tutorialspoint.com/internet_technologies/html.htm'
# download_folder = './samp/'    

# kwargs = {'bypass_robots': True, 'project_name': 'recognisable-name'}

# save_webpage(url, download_folder, **kwargs)


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import time
import pyautogui


# Get the current working directory
current_folder = os.getcwd()

# Create a Chrome WebDriver instance
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
br = webdriver.Chrome(options=chrome_options)

# Navigate to the desired URL
br.get('https://fast.com/')

# Simulate the keyboard shortcut for saving (Ctrl + S)
# save_action = ActionChains(br)
# save_action.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()

# Wait for the save dialog to appear (you might need to adjust the timing)
# time.sleep(5)

# Handle the file save dialog
# filename = 'saved_page.html'
# save_path = os.path.join(current_folder, filename)
# save_dialog = br.switch_to.active_element
# save_dialog.send_keys(save_path)
# save_dialog.send_keys(Keys.RETURN)

# Close the browser
# Simulate Ctrl + S keyboard shortcut using pyautogui
pyautogui.hotkey('ctrl', 's')
time.sleep(2)  # Wait for the save dialog to appear

# Type the file name and save

filename = current_folder + "\\" + 'fast.html'
print(filename)
pyautogui.write(filename)
pyautogui.press('enter')

max_wait_time = 300  # Maximum time to wait for the download in seconds
start_time = time.time()

while time.time() - start_time < max_wait_time:
    if os.path.exists(filename):
        print("Download complete!")
        time.sleep(1)
        break
    time.sleep(1)  # Wait for 1 second before checking again
else:
    print("Download didn't complete within the specified time.")

br.quit()
