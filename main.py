from src.SqLite3 import parametrosApp
from src.UsaVisaBot import VisaAppointment
import logging, time

visaBot = VisaAppointment(logging.DEBUG)

# Credenciales
visaBot.user = ""
visaBot.password = ""
visaBot.periodo = 10 * 5

# Inicializo el servidor
visaBot.begin()

try:
    while (visaBot.isRun()):
        time.sleep(5)
except KeyboardInterrupt:
    visaBot.stop()