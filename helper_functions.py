from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
ADDRESS_XPATH=".//a[@aria-label='Adres']"
DESCRIPTION=".//div[@data-cy='adPageAdDescription']"
PATTERN = r"ul\.\s+[A-ZĄĆĘŁŃÓŚŹŻa-ząćęłńóśźż]+\s*\d*"
class Help:
    def __init__(self,driver,wait):
        self.driver=driver
        self.wait=wait
        self.rentals=pd.DataFrame()


    def extract(self):
        address1=self.driver.find_element(By.XPATH,ADDRESS_XPATH).text
        address2 = \
        re.findall(PATTERN, self.driver.find_element(By.XPATH, ".//div[@data-cy='adPageAdDescription']").text)[
            0] if re.findall(PATTERN, self.driver.find_element(By.XPATH,
                                                               ".//div[@data-cy='adPageAdDescription']").text) else None
        Powierzchnia=self.driver.find_element(By.XPATH,".//div[@aria-label='Powierzchnia']").text
        Czynsz=self.driver.find_element(By.XPATH,".//div[@aria-label='Czynsz']").text
        Liczba_pokoi = self.driver.find_element(By.XPATH, ".//div[@aria-label='Liczba pokoi']").text
        Kaucja = self.driver.find_element(By.XPATH, ".//div[@aria-label='Kaucja']").text
        Piętro = self.driver.find_element(By.XPATH, ".//div[@aria-label='Piętro']").text
        Rodzaj_zabudowy = self.driver.find_element(By.XPATH, ".//div[@aria-label='Rodzaj zabudowy']").text
        Balcon = self.driver.find_element(By.XPATH, ".//div[@aria-label='Balkon / ogród / taras']").text
        Stan_wykończenia = self.driver.find_element(By.XPATH, ".//div[@aria-label='Stan wykończenia']").text
        Dostępne_od = self.driver.find_element(By.XPATH, ".//div[@aria-label='Dostępne od']").text
        Obsługa_zdalna = self.driver.find_element(By.XPATH, ".//div[@aria-label='Obsługa zdalna']").text
        #ADDITIONAL_INFO
        Advertiser_type=self.driver.find_element(By.XPATH,".//div[@aria-label='Typ ogłoszeniodawcy']").text
        rent_to_students=self.driver.find_element(By.XPATH,".//div[@aria-label='Wynajmę również studentom']").text
        Equipment=self.driver.find_element(By.XPATH,".//div[@aria-label='Wyposażenie']").text
        Media=self.driver.find_element(By.XPATH,".//div[@aria-label='Media']").text
        Heating = self.driver.find_element(By.XPATH, ".//div[@aria-label='Ogrzewanie']").text
        Security = self.driver.find_element(By.XPATH, ".//div[@aria-label='Zabezpieczenia']").text
        Windows=self.driver.find_element(By.XPATH, ".//div[@aria-label='Okna']").text
        Elevator=self.driver.find_element(By.XPATH, ".//div[@aria-label='Winda']").text
        Parking=self.driver.find_element(By.XPATH, ".//div[@aria-label='Miejsce parkingowe']").text
        Year_of_construction=self.driver.find_element(By.XPATH, ".//div[@aria-label='Rok budowy']").text
        Building_material=self.driver.find_element(By.XPATH, ".//div[@aria-label='Materiał budynku']").text
        data_dict={'advertiser_type':[Advertiser_type],'rent_to_students':[rent_to_students],'equipment':[Equipment],'media':[Media],'heating':Heating,
               'security':[Security],'windows':[Windows],'elevatot':[Elevator],'parking':[Parking],'year_of_construction':[Year_of_construction],
               'building_material':[Building_material],'address1':[address1],'address2':[address2],'area':[Powierzchnia],'Czynsz':[Czynsz],'Liczba_pokoi':Liczba_pokoi,
              'Kaucja':[Kaucja],'Piętro':[Piętro],'Rodzaj_zabudowy':[Rodzaj_zabudowy],'Balcon':[Balcon],'Stan_wykończenia':[Stan_wykończenia],
              'Dostępne_od':[Dostępne_od],'Obsługa_zdalna':[Obsługa_zdalna]}
        data=pd.DataFrame(data_dict)
        self.rentals=pd.concat([self.rentals,data],ignore_index=True)
    def click(self,link):
        wait = WebDriverWait(self.driver, 10)
        self.driver.execute_script("arguments[0].scrollIntoView();", link)

        # Click on the <a> tag using JavaScript
        self.driver.execute_script("arguments[0].click();", link)

    def collect_links(self):
        container = self.driver.find_element(By.XPATH, "//div[@data-cy='search.listing.organic']")
        list_element = container.find_elements(By.XPATH, ".//ul[@class='css-rqwdxd e127mklk0']")[1]
        # Find the first <a> tag element
        child_con = list_element.find_elements(By.XPATH, ".//div[@data-testid='carousel-container']")
        links = []
        for i in child_con:
            links.append(i.find_elements(By.TAG_NAME, 'a')[0])
        return links
    def save_data(self):
        self.rentals.to_csv('otodom.csv',index=False)

    def next_page(self):
        page_list=self.driver.find_element(By.XPATH,".//ul[@data-testid='frontend.search.base-pagination.nexus-pagination']")
        link=page_list.find_element(By.XPATH,".//*[@title='Go to next Page']")
        self.click(link)





