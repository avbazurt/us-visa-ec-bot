# Creator avbazurt@espol.edu.ec
from time import sleep
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from time import sleep
from random import randint
import json, logging

try:
    from src.PyLog import Log
    AppLog = Log(__name__)
except Exception as ex:
    AppLog = logging.getLogger(__name__)
    AppLog.setLevel(logging.DEBUG)
    stramHandler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')    
    stramHandler.setFormatter(formatter)
    AppLog.addHandler(stramHandler)



class visaServer():
    def __init__(self, log_level:int = logging.CRITICAL) -> None:
        # Seteo primero el log
        AppLog.setLevel(log_level)

        # Creamos el _driver
        self._driver = webdriver.Firefox()

        self.url = "https://ais.usvisa-info.com/en-ec/niv/users/sign_in"
        self.xpath = json.load(open("src/UsaVisaBot/xpath.json")) 
        
        # Configuramos la pestana
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--disable-popup-blocking")
        self._driver.maximize_window()

        self.calidadInternet = 1 

    def _delay_random(self, second:int)->None:
        gain = 0.5
        second = int(second)
        a = (second * 100) - 100
        b = (second * 100) + 300

        delay = gain * (randint(a,b)/100)

        if (delay<= 0):
            delay = 0.5

        sleep(delay)


    def _get_element(self, type:By, element:str) -> WebElement:
        self._delay_random(1)
        element_present = EC.presence_of_element_located((type, element))
        return WebDriverWait(self._driver, 30).until(element_present)
        

    def login(self, user:str, password:str)->None:
        AppLog.info("Begin Login:")
        AppLog.info(f"User: {user}")
        AppLog.info(f"Pass: {password}")

        # Abrimos la pagina
        self._driver.get(self.url)
        self._delay_random(5)

        # Iniciamos seccion
        self._get_element(By.XPATH, self.xpath["user"]).send_keys(user)
        self._get_element(By.XPATH, self.xpath["password"]).send_keys(password)
        self._get_element(By.XPATH, self.xpath["checkbox"]).click()
        self._get_element(By.XPATH, self.xpath["sign"]).click()

    def aviableAppointment(self)->bool:
        contador = 0
        max_intentos = randint(2,4)

        # Procedo a repetir las veces que sean necesarias
        while (contador<max_intentos):
            AppLog.info("Starting the available date verification process")
            self._get_element(By.XPATH, self.xpath["continue"]).click()
            self._get_element(By.XPATH, self.xpath["reschedule"]).click()
            self._get_element(By.XPATH, self.xpath["appointment"]).click()

            select = Select(self._get_element(By.XPATH, self.xpath["location"]))
            select.select_by_visible_text('Quito')

            # Valido si existe cita
            display = self._get_element(By.XPATH, self.xpath["date"]).get_property('style')["display"].strip('\n')
            if (not(display=="none")):
                AppLog.info("The calendar is available, validating if there are dates within the next 3 months")
                # Si esta disponible las fechas, valido si estan los dias
                if (self.aviableDate()):
                    return True

            # Si no hay cita me salgo
            self._get_element(By.XPATH, self.xpath["close"]).click()
            AppLog.info("There are no dates available, start the process again")

            self._delay_random(30)

            # Volvemos a intentar luego
            contador+=1

        return False

    def aviableDate(self) -> bool:
        self._get_element(By.XPATH, self.xpath["fecha"]).click()
        self._delay_random(1)

        # Primero localizo el mes actual
        for i in range(2):
            _div_mes = self._get_element(By.CLASS_NAME, "ui-datepicker-group")
            mes_actual = _div_mes.find_element(By.CLASS_NAME, "ui-datepicker-month").text
            AppLog.info(f"Starting Scan of the month {mes_actual}")

            calendario = _div_mes.find_element(By.CLASS_NAME, "ui-datepicker-calendar")
            dias = calendario.find_elements(By.TAG_NAME, "td")
            for dia in dias:
                if (dia.text.isdigit()):
                    _status = False
                    _message = "Disabled"

                    if not ("ui-state-disabled" in dia.get_attribute("class")):
                        _message = "Enabled"
                        _status = True

                    AppLog.info(f"Day: {dia.text}, {_message}")

                    if (_status):
                        return True

            self._get_element(By.XPATH, self.xpath["siguiente_mes"]).click()
        return False

    def logout(self)->None:
        self._get_element(By.XPATH, self.xpath["actions"]).click()
        self._get_element(By.XPATH, self.xpath["output"]).click()

    def close(self)->None:
        try:
            self._driver.close()
        except:
            pass
