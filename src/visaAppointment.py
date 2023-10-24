import json
from src.webFunction import visaServer
from selenium.common.exceptions import WebDriverException
from playsound import playsound
from time import sleep
import traceback
from src import AppLog

class visaAppointment():
    def __init__(self) -> None:
        self.visaServer = visaServer()

        self.user = None
        self.password = None

        self.periodo = None


    def loop(self)->None:
        while True:
            try:
                # Iniciamos el Server
                self.visaServer.login(self.user, self.password)

                # Abrimos el Appointment
                avaible = self.visaServer.aviableAppointment()

                if (avaible):
                    AppLog.error("Date found")
                    try:
                        while(True):
                            NOMBRE_ARCHIVO = "alarm-clock.mp3"
                            playsound(NOMBRE_ARCHIVO)
                            sleep(10)
                    except KeyboardInterrupt:
                        input("Presiona enter para cerrar el proceso")
                        break
                        quit()
                    except Exception as err:
                        AppLog.error(err, exc_info=True)
                        input("Presiona enter para cerrar el proceso")

                        
                else:
                    AppLog.error("Could not find available dates, log out and wait to log back in")

                # Esperamos un rato
                self.visaServer.logout()

                sleep(self.periodo)

            except KeyboardInterrupt:
                break

            except WebDriverException as err:
                AppLog.error(f"{err}\n se reinicia el proceso")
                sleep(60)

            except Exception as err:
                AppLog.error(f"Unexpected {err=}, {type(err)=}", exc_info=True)
                sleep(60)



        self.visaServer.close()
        input("Programa finalizado, presiona enter para cerrar")
            

        

