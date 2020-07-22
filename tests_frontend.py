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


user1 = "user"
password_user1 = "cyborg22"

# manager of other entity than user1's loan entity
user2 = "lesaulnc"
password_user2 = "montAiguille2020"

# name of entity
entity1 = "ge2lab"

def check_exists_by_selector(selector):
    el = None
    if len(driver.find_elements(By.CSS_SELECTOR,selector)) > 0:
        el = driver.find_element(By.CSS_SELECTOR,selector)
    return el

def check_values_by_selector(value, selector, target):
    for l in selector:
        loan = l.find_elements(By.TAG_NAME, target) 
        if loan[0].text != value:
            return False
            break
    print('all values match' + value)
    return True

def find_table_selector():
    selector = driver.find_element(By.CSS_SELECTOR,".row").find_elements(By.CSS_SELECTOR, ".card")[0]
    table_selector = selector.find_elements(By.CSS_SELECTOR,"table tbody tr")
    return table_selector

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

    def loan(self, target):
        try:    
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
                    print()
                    if entity.text == target:
                        add_material[0].click()
                        clicked = True
                if clicked:
                    break
            time.sleep(4)
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
            time.sleep(3)
            for entries in table_loans:
                col = entries.find_elements(By.TAG_NAME, "td")
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
    test emprunt non assignable pour une autre personne
    """
    material_loans = MaterialLoans()
    material_loans.login(user1, password_user1)
    material_loans.loan(entity1)
    time.sleep(2)
    driver.get(material_loans.server_url+"/#/entities/1/loans")
    time.sleep(1)
    MaterialLoans.update_loan(4,"2020-05-09","Accepté")
    time.sleep(1)
    status =  driver.find_element(By.CSS_SELECTOR, 'select')
    assert(status.get_attribute("disabled") == "true")
    # check if user input is present    
    assert(check_exists_by_selector(".form-control.p-0") is None)

    """
    test accès restreint des prêts aux utilisateur non manager d'une entité
    """

    driver.get(material_loans.server_url+"/#/entities/1/loans")
    time.sleep(1)
    table_selector = find_table_selector()
    assert(check_values_by_selector(user1,table_selector, "td") is False)
    time.sleep(1)
    driver.get(material_loans.server_url+'/auth/logout')
    time.sleep(1)

    # check user manager of other entity
    material_loans.login(user2, password_user2)
    time.sleep(2)
    driver.get(material_loans.server_url+"/#/entities/1/loans")
    time.sleep(1)
    table_selector = find_table_selector()
    assert(check_values_by_selector(user2,table_selector, "td") is True)

except ValueError as e:
    print(e)
    
finally:
    print('finally')
    driver.quit()