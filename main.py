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

def close_popups():
    try:
        # Wait for and close the overlay if present
        overlay = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.onetrust-close-btn-handler, .ot-close-icon'))
        )
        overlay.click()
        print("Overlay closed.")
    except Exception as e:
        print(f"No overlay or unable to close overlay: {e}")

def click_next_button():
    while True:
        try:
            # Wait for the "Next Page" button to be clickable
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, ".//*[@title='Go to next Page']"))
            )
            # Scroll the button into view and click it
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            next_button.click()
            time.sleep(2)  # Adjust if necessary
            break  # Break the loop if click is successful
        except Exception as e:
            print(f"Click intercepted, retrying: {e}")
            close_popups()
            time.sleep(2)  # Wait before retrying

def click_links_and_return(link_click_limit=36):
    links_clicked = 0
    while links_clicked < link_click_limit:
        try:
            # Re-find the <a> tags on the page within the loop to avoid stale elements
            links = help.collect_links()
            if links_clicked >= len(links):
                break

            link = links[links_clicked]
            link_href = link.get_attribute('href')

            driver.execute_script("window.open(arguments[0]);", link_href)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)  # Adjust as needed

            # Perform any necessary actions on the new page
            # Example: help.extract() function call
            help.extract()

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            links_clicked += 1
            time.sleep(1)  # Small delay to ensure proper loading
        except Exception as e:
            print(f"An error occurred while clicking links: {e}")
            break


for i in range(189):
    click_links_and_return()
    page_list = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, ".//ul[@data-cy='frontend.search.base-pagination.nexus-pagination']"))
    )
    link = page_list.find_element(By.XPATH, ".//*[@title='Go to next Page']")
    driver.execute_script("arguments[0].scrollIntoView(true);", link)
    help.click(link)
    time.sleep(2)  # Adjust if necessary

help.save_data()
