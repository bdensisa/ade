# Import
from time import sleep
from json import load
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

def load_user(name):
    # Create browser
    options = webdriver.FirefoxOptions()
    options.headless = True # Allows to run without a window, useful for server
    browser = webdriver.Firefox(options=options)

    # Load page
    browser.get('https://www.emploisdutemps.uha.fr/direct/')
    sleep(1)

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
    try:
        # Check that planning is loaded (and by the way that user exists)
        WebDriverWait(browser, 5).until(visibility_of_element_located((By.ID, 'Planning')))
        # Click on export
        WebDriverWait(browser, 5).until(visibility_of_element_located((By.ID, 'x-auto-29'))).click()
        # Click on Generate URL
        WebDriverWait(browser, 5).until(visibility_of_element_located((By.XPATH, "//*[contains(text(), 'URL')]"))).click()
        # Get generated URL
        urlText = WebDriverWait(browser, 5).until(visibility_of_element_located((By.ID, 'logdetail'))).text
    except:
        # User not found
        pass
    
    # Close browser and return result
    browser.quit()
    return urlText
