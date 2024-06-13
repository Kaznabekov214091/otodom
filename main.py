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

def click_links_and_return(link_click_limit=36):
    links_clicked=0
    while links_clicked<link_click_limit:
        links=help.collect_links()
        if links_clicked>=len(links):
            break
        link=links[links_clicked]
        link_href=link.get_attribute('href')

        driver.execute_script("window.open(arguments[0]);", link_href)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)

        help.extract()

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        links_clicked+=1
        time.sleep(1)

while True:
    click_links_and_return()
    try:
        # Wait for the "Next Page" button to be clickable and click it
        page_list = driver.find_element(By.XPATH, ".//ul[@data-cy='frontend.search.base-pagination.nexus-pagination']")
        link = page_list.find_element(By.XPATH, ".//*[@title='Go to next Page']")
        help.click(link)

        time.sleep(2)  # Adjust if necessary
    except Exception as e:
        print("No more pages or an error occurred:", e)
        break
help.save_data()
