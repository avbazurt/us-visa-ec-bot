from webFunction import openDriver, login, aviableAppointment, logout, delay
from playsound import playsound
import json
from random import randint

# Credenciales
user = ""
password = ""

# Extraemos todas los XPATH
url = "https://ais.usvisa-info.com/en-ec/niv/users/sign_in"
xpath = json.load(open("xpath.json"))

# Creamos el driver
driver = openDriver()

while True:
    login(url, driver, user, password, xpath)

    # Abrimos el Appointment
    avaible = aviableAppointment(driver, xpath)
    print(f"Fecha disponible: {avaible}")

    if (avaible):
        try:
            while(True):
                NOMBRE_ARCHIVO = "alarm-clock.mp3"
                playsound(NOMBRE_ARCHIVO)
                delay(10)


        except KeyboardInterrupt:
            quit()

    # Esperamos un rato para salir
    delay(5)
    logout(driver,xpath)

    # Un tiempo de espera para volver a intentar
    delay(randint(10, 14)*60)


