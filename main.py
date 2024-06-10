from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import sys
import re
from tqdm import tqdm
import helper_functions


PATH = "C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

# Create a new Chrome driver instance
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa/warszawa/warszawa')
wait = WebDriverWait(driver, 10)
help=helper_functions.Help(driver,wait)
for i in tqdm(range(189)):
    links = help.collect_links()
    for link in links:
        link.click()
        WebDriverWait(driver, 10).until(EC.url_changes)
        #help.extract()
        # Go back to the previous page
        driver.execute_script("window.history.go(-1)")
        wait = WebDriverWait(driver, 10)
    help.next_page()
    WebDriverWait(driver, 15)

# Save data outside the loop
help.save_data()

