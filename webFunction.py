# Creator avbazurt@espol.edu.ec

from time import sleep
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from time import sleep
from random import randint

def delay(second):
    a = (second * 100) - 100
    b = (second * 100) + 300
    sleep(randint(a,b)/100)

def openDriver()->webdriver:
    # Creamos el driver
    driver = webdriver.Firefox()

    # Configuramos la pestana
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--disable-popup-blocking")
    driver.maximize_window()
    delay(3)

    return driver

def login(url:str ,driver:webdriver, user:str, password:str, xpath:dict)->None:
    # Abrimos la pagina
    driver.get(url)
    delay(5)

    # Iniciamos seccion
    driver.find_element(By.XPATH, xpath["user"]).send_keys(user)
    driver.find_element(By.XPATH, xpath["password"]).send_keys(password)
    delay(3)
    driver.find_element(By.XPATH, xpath["checkbox"]).click()
    delay(3)
    driver.find_element(By.XPATH, xpath["sign"]).click()
    delay(3)


def aviableAppointment(driver:webdriver, xpath:dict)->bool:
    driver.find_element(By.XPATH, xpath["continue"]).click()
    delay(3)
    driver.find_element(By.XPATH, xpath["reschedule"]).click()
    delay(3)
    driver.find_element(By.XPATH, xpath["appointment"]).click()
    delay(3)

    select = Select(driver.find_element(By.XPATH, xpath["location"]))
    select.select_by_visible_text('Quito')
    delay(3)

    display = driver.find_element(By.XPATH, xpath["date"]).get_property('style')["display"].strip('\n')

    return not(display=="none")

def logout(driver:webdriver, xpath:dict)->None:
    driver.find_element(By.XPATH, xpath["close"]).click()
    delay(3)
    driver.find_element(By.XPATH, xpath["actions"]).click()
    delay(3.5)
    driver.find_element(By.XPATH, xpath["output"]).click()
    delay(3.5)



    
