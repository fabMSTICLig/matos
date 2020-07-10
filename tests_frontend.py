#!/usr/bin/env python3

import selenium
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time, datetime
from datetime import date

ff_profile_dir="/usr/local/lib/python3.7/dist-packages/selenium/webdriver/firefox/"
ff_profile = selenium.webdriver.FirefoxProfile(profile_directory=ff_profile_dir)
driver = Firefox(ff_profile, service_log_path="/home/lesaulnc/geckodriver.log")

server_url = "http://localhost:8000"

def login(username, password):
    try:
        driver.get(server_url+"/auth/login/")
        driver.find_element(By.CSS_SELECTOR, '[name="username"]').send_keys(username)
        driver.find_element(By.CSS_SELECTOR, '[name="password"]').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
        time.sleep(2)
    except ValueError:
        print("login error")

def loan():
    try:    
        login("user", "cyborg22") # set user's loan 
        driver.get(server_url+"/#/search")
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
                if entity.text == 'ens3':
                    print("ajout")
                    print(add_material[0].text)
                    add_material[0].click()
                    clicked = True
            if clicked:
                break

        driver.get(server_url+"/#/loan")
        time.sleep(2)
        inputs_date =  driver.find_elements(By.CSS_SELECTOR, '[type="date"]')
        inputs_date[0].send_keys("2020-07-08")

        time.sleep(2)
        inputs_date[1].send_keys("2020-07-09")
        action = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
        driver.find_element(By.CSS_SELECTOR,"body").click()
        time.sleep(2)

        user_input = driver.find_element(By.CSS_SELECTOR,".form-control.p-0")
        user_input.find_element(By.CSS_SELECTOR,"input").click()
        user_input.find_element(By.CSS_SELECTOR,"input").send_keys(4)
        time.sleep(4)
        driver.find_element(By.CSS_SELECTOR,"body").click()
        action.click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,".modal-footer .btn.btn-primary").click()
        time.sleep(2)
try:
    """
    test utilisateur rattaché à un pret 
    """
    doLoan()

    # Vérification de l'emprunt enregistré par un manager 
    driver.get(server_url+"/auth/logout")
    time.sleep(3)
    login("primeca", "primeca")
    time.sleep(3)
    # Get loans depending on the entity
    driver.get(server_url+"/#/entities/2/loans")
    time.sleep(1)
    tables = driver.find_elements(By.CSS_SELECTOR,"table")
    table_loans = tables[0].find_elements(By.CSS_SELECTOR,"tbody tr")
    for entries in table_loans:
        col = entries.find_elements(By.TAG_NAME, "td")
        if col[0].text == "user":
            assert( col[1].text == "En Attente" and col[2].text == "2020-07-08" and col[3].text == "2020-07-09")
            break
    """
    test utilisateur d'un emprunt non assignable pour une autre personne
    """
    driver.get(server_url+"/auth/logout")
    time.sleep(3)
    doLoan()
    time.sleep(3)
    driver.get(server_url+"/auth/logout")
    login("supportPrimeca", "primeca19")
    time.sleep(3)
     driver.get(server_url+"/#/entities/2/loans")
    time.sleep(1)
    tables = driver.find_elements(By.CSS_SELECTOR,"table")
    table_loans = tables[0].find_elements(By.CSS_SELECTOR,"tbody tr")
    for entries in table_loans:
        col = entries.find_elements(By.TAG_NAME, "td")
        if col[0].text == "user":
            assert( col[1].text == "En Attente" and col[2].text == "2020-07-08" and col[3].text == "2020-07-09")
            break
finally:
    print('finally')
    driver.quit()