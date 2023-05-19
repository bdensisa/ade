# Import
from time import sleep
from json import load
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

# Icon used to find export button
export_icon = 'iVBORw0KGgoAAAANSUhEUgAAACMAAAAjCAYAAAAe2bNZAAACJUlEQVR42u2WTWsTQRjHC+pVv4IXPXkQPHhQwdqLIoh+By+iB0E/QL+CB79EKyqlUFoK9Q2krBgUX0jTommTNI3ZxriZ2c3OzD4+/2RSKkZ33V1BcB/4EXb2mX9+M7sDOzFRVFFF/Y9FRHdpWFMxfRdt362/KXPT/sm5mL5J23cjb4GzzEvmHnON8ZiTzAJTHsM8c8r2XWHu2/lnsopcZxp2lQ5znDnBHGNcGl8te3/UV7LjNeRlkVmnfGs9i0w7Z5l2apnQRDt9E1Fg8XVE8g9A/2gucpCXWqbTN54bGPIUXeiGdDotPUVTyEFeapmWr8WOr7G9BzMehEPIQd7ervOJNMbcThzS5MkNqXFsDmeR2dilI8hp7pNRSp3XxpCOohWWPRobUpda1BLKYKUIHovWz6UyxOjRGO9KaSAzpBO7S5s9Jar8wCtuvIwyZnpfeDpY8pd/8JllPnnJZHj1V7OK/PZxbXhKVL4lk4l7Z5CDvJ/emSSPCFXxQlHms5mHzCCH836QiaJHiV5e1MduKD7kJIMc5KUOed8Ng3dfs8u8YhnkIC91yNtO332z26c8PkWQg7z0K3KDO6vtoPOiFbx+2vSdFWZ523eWtqWz1JDOIrMA6sNfXGMc99GHfszj+aXVtu8iL7XMDNGBZ1+Cy8sNf22xLuV8Tcq5LSEfbwr5kHlQFXK22tsD1xjH/bmaGPRjHouVn7SCS8grPt6LKqqof6W+Ay+dK1+43l/5AAAAAElFTkSuQmCC'

# Create a browser element
def init_browser():
    options = webdriver.FirefoxOptions()
    options.headless = True # Allows to run without a window, useful for server
    browser = webdriver.Firefox(options=options)
    browser.get('https://www.emploisdutemps.uha.fr/direct/')
    return browser

# Quit the browser
def clear_browser(browser):
    browser.quit()
    pass

# Function to get the URL of a user
def load_user(browser, name):
    # Login if needed
    if browser.current_url.startswith('https://cas.uha.fr/cas/login'):
        # Read username and password from json file
        file = open('credentials.json')
        credentials = load(file)
        browser.find_element('id', 'username').send_keys(credentials['username'])
        browser.find_element('id', 'password').send_keys(credentials['password'])
        browser.find_element('id', 'password').submit()
        file.close()

    # Grab field and enter name
    WebDriverWait(browser, 5).until(visibility_of_element_located((By.ID, 'x-auto-33-input')))
    browser.find_element('id', 'x-auto-33-input').send_keys(name)
    browser.find_element('id', 'x-auto-33-input').send_keys(Keys.ENTER)
    urlText = None # Default value if user not found
    sleep(3)
    try:
        # Check that planning is loaded (and by the way that user exists)
        WebDriverWait(browser, 5).until(visibility_of_element_located((By.ID, 'Planning')))
        # Click on export
        WebDriverWait(browser, 5).until(visibility_of_element_located((By.XPATH, "//img[contains(@style, '" + export_icon + "')]"))).click()
        # Click on Generate URL
        WebDriverWait(browser, 5).until(visibility_of_element_located((By.XPATH, "//button[contains(text(), 'URL')]"))).click()
        # Get generated URL
        urlText = WebDriverWait(browser, 5).until(visibility_of_element_located((By.ID, 'logdetail'))).text
        # Close popups
        WebDriverWait(browser, 5).until(visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Close') or contains(text(), 'Fermer')]"))).click()
        WebDriverWait(browser, 5).until(visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Cancel') or contains(text(), 'Annuler')]"))).click()
    except:
        # User not found
        pass
    
    # Clear name
    for _ in range(len(name)):
        browser.find_element('id', 'x-auto-33-input').send_keys(Keys.BACKSPACE)
    return urlText
