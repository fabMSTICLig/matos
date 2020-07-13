#!/usr/bin/env python3

import selenium
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import time, datetime
from datetime import date

ff_profile_dir="/usr/local/lib/python3.7/dist-packages/selenium/webdriver/firefox/"
ff_profile = selenium.webdriver.FirefoxProfile(profile_directory=ff_profile_dir)
driver = Firefox(ff_profile, service_log_path="/home/lesaulnc/geckodriver.log")


def check_exists_by_selector(selector):
    el = None
    if len(driver.find_elements(By.CSS_SELECTOR,selector)) > 0:
        el = driver.find_element(By.CSS_SELECTOR,selector)
    return el

class MaterialLoans:
    server_url = "http://localhost:8000"
    user_id = 4

    def login(self,username, password):
        try:
            driver.get(self.server_url+"/auth/login/")
            driver.find_element(By.CSS_SELECTOR, '[name="username"]').send_keys(username)
            driver.find_element(By.CSS_SELECTOR, '[name="password"]').send_keys(password)
            driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
            time.sleep(2)
        except ValueError:
            print("login error")

    def loan(self):
        try:    
            self.login("user", "cyborg22") # set user not manager 
            driver.get(self.server_url+"/#/search")
            time.sleep(1)
            filter_type = driver.find_elements(By.TAG_NAME, 'select')
            select_object = Select(filter_type[0])
            select_object.select_by_index(1)
            materials = driver.find_elements(By.CLASS_NAME, 'list-group-item')
            time.sleep(2)
            clicked = False
            # add material of an entity 
            for e in materials:
                entities = e.find_elements(By.TAG_NAME, 'a') 
                add_material = e.find_elements(By.TAG_NAME, 'button')
                for entity in entities:
                    if entity.text == 'ge2lab':
                        print("ajout")
                        print(add_material[0].text)
                        add_material[0].click()
                        clicked = True
                if clicked:
                    break

            driver.get(self.server_url+"/#/loan")
            time.sleep(2)
            inputs_date =  driver.find_elements(By.CSS_SELECTOR, '[type="date"]')
            inputs_date[0].send_keys("2020-07-08")

            time.sleep(2)
            inputs_date[1].send_keys("2020-07-09")
            action = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
            driver.find_element(By.CSS_SELECTOR,"body").click()
            time.sleep(2)

            user_input = check_exists_by_selector(".form-control.p-0")
            if user_input:
                user_input.find_element(By.CSS_SELECTOR,"input").click()
                user_input.find_element(By.CSS_SELECTOR,"input").send_keys(user_id)
                time.sleep(4)
            driver.find_element(By.CSS_SELECTOR,"body").click()
            action.click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,".modal-footer .btn.btn-primary").click()
            time.sleep(2)
        
        except ValueError:
            print("loan error")

    def update_loan(user, checkout_date, status):
        try:
            tables = driver.find_elements(By.CSS_SELECTOR,"table")
            table_loans = tables[0].find_elements(By.CSS_SELECTOR,"tbody tr")
            for entries in table_loans:
                col = entries.find_elements(By.TAG_NAME, "td")
                if col[0].text == "user":
                    assert( col[1].text == status and col[2].text == "2020-07-08" and col[3].text == "2020-07-09")
                    col[0].click()
                    break
            actions = driver.find_elements(By.CSS_SELECTOR,".btn-group.float-right button")
            actions[0].click()
            time.sleep(1)
            user_input = check_exists_by_selector(".form-control.p-0")
            if user_input:
                user_input.find_element(By.CSS_SELECTOR,"input").click()
                user_input.find_element(By.CSS_SELECTOR,"input").clear()
                user_input.find_element(By.CSS_SELECTOR,"input").send_keys(user)
                time.sleep(2)

            driver.find_element(By.CSS_SELECTOR,"body").click()
            inputs_date =  driver.find_elements(By.CSS_SELECTOR, '[type="date"]')
            inputs_date[0].send_keys(checkout_date)
            action = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
            action.click()
            driver.find_element(By.CSS_SELECTOR,".modal-footer .btn.btn-primary").click()

        except ValueError:
            print('error update loan')

try:
    
    """
    test utilisateur d'un emprunt non assignable pour une autre personne
    """
  
    material_loans = MaterialLoans()
    material_loans.loan()
    time.sleep(3)
    driver.get(material_loans.server_url+"/#/entities/1/loans")
    time.sleep(1)
    MaterialLoans.update_loan(1,"2020-05-08","Demandé")
    time.sleep(1)
    # check if user input is present    
    assert(check_exists_by_selector(".form-control.p-0") is None)

except ValueError as e:
    print(e)
    
finally:
    print('finally')
    #driver.quit()