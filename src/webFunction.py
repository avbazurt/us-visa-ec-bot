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

        print("Begin Login:")
        print(f"User: {user}")
        print(f"Pass: {password}")
        print("")


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
            print("Starting the available date verification process")
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
                print("The calendar is available, validating if there are dates within the next 3 months")
                # Si esta disponible las fechas, valido si estan los dias
                if (self.aviableDate()):
                    return True

            # Si no hay cita me salgo
            self.driver.find_element(By.XPATH, self.xpath["close"]).click()

            print("There are no dates available, start the process again")

            self._delay_random(30)

            # Volvemos a intentar luego
            contador+=1

        return False


    def aviableDate(self) -> bool:
        self.driver.find_element(By.XPATH, self.xpath["fecha"]).click()
        self._delay_random(1)

        # Primero localizo el mes actual
        for i in range(3):
            _div_mes = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-group")
            mes_actual = _div_mes.find_element(By.CLASS_NAME, "ui-datepicker-month").text
            print(f"Starting Scan of the month {mes_actual}")

            calendario = _div_mes.find_element(By.CLASS_NAME, "ui-datepicker-calendar")
            dias = calendario.find_elements(By.TAG_NAME, "td")
            for dia in dias:
                if (dia.text.isdigit()):
                    _status = False
                    _message = "Disabled"

                    if not ("ui-state-disabled" in dia.get_attribute("class")):
                        _message = "Enabled"
                        _status = True

                    print(f"Day: {dia.text}, {_message}")

                    if (_status):
                        return True

            print("")
            self.driver.find_element(By.XPATH, self.xpath["siguiente_mes"]).click()
        
        return False






    def logout(self)->None:
        self.driver.find_element(By.XPATH, self.xpath["actions"]).click()
        self._delay_random(3)
        self.driver.find_element(By.XPATH, self.xpath["output"]).click()
        self._delay_random(3)


    def close(self)->None:
        self.driver.close()
    
