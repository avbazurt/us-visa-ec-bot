# Creator avbazurt@espol.edu.ec
from time import sleep
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from time import sleep
from random import randint
import json

class visaServer():
    def __init__(self) -> None:
        # Creamos el driver
        self.driver = webdriver.Firefox()

        self.url = "https://ais.usvisa-info.com/en-ec/niv/users/sign_in"
        self.xpath = json.load(open("src/xpath.json")) 
        
        # Configuramos la pestana
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--disable-popup-blocking")
        self.driver.maximize_window()
        sleep(3)

        self.calidadInternet = 1 


    def _delay_random(self, second:int)->None:
        gain = 0.5 * (self.calidadInternet) + 0.5
        second = int(second)
        a = (second * 100) - 100
        b = (second * 100) + 300
        sleep(gain * (randint(a,b)/100))
        

    def login(self, user:str, password:str)->None:
        # Abrimos la pagina
        self.driver.get(self.url)
        self._delay_random(5)

        # Iniciamos seccion
        self.driver.find_element(By.XPATH, self.xpath["user"]).send_keys(user)
        self.driver.find_element(By.XPATH, self.xpath["password"]).send_keys(password)
        self._delay_random(3)
        self.driver.find_element(By.XPATH, self.xpath["checkbox"]).click()
        self._delay_random(3)
        self.driver.find_element(By.XPATH, self.xpath["sign"]).click()
        self._delay_random(3)


    def aviableAppointment(self)->bool:
        contador = 0
        max_intentos = randint(2,4)

        # Procedo a repetir las veces que sean necesarias
        while (contador<max_intentos):
            self.driver.find_element(By.XPATH, self.xpath["continue"]).click()
            self._delay_random(3)
            self.driver.find_element(By.XPATH, self.xpath["reschedule"]).click()
            self._delay_random(3)
            self.driver.find_element(By.XPATH, self.xpath["appointment"]).click()
            self._delay_random(3)

            select = Select(self.driver.find_element(By.XPATH, self.xpath["location"]))
            select.select_by_visible_text('Quito')
            self._delay_random(3)

            # Valido si existe cita
            display = self.driver.find_element(By.XPATH, self.xpath["date"]).get_property('style')["display"].strip('\n')
            if (not(display=="none")):
                return True

            # Si no hay cita me salgo
            self.driver.find_element(By.XPATH, self.xpath["close"]).click()
            self._delay_random(30)

            # Volvemos a intentar luego
            contador+=1

        return False

    def logout(self)->None:
        self.driver.find_element(By.XPATH, self.xpath["actions"]).click()
        self._delay_random(3)
        self.driver.find_element(By.XPATH, self.xpath["output"]).click()
        self._delay_random(3)


    def close(self)->None:
        self.driver.close()
    
