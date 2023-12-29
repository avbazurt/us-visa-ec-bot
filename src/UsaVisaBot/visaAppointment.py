import json, traceback, logging, threading
from .webFunction import visaServer
from selenium.common.exceptions import WebDriverException
from playsound import playsound
from time import sleep

from threading import Thread, Event


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

class VisaAppointment():
    def __init__(self, log_level:int = logging.CRITICAL) -> None:
        # Seteo primero el log
        AppLog.setLevel(log_level)
    
        # Obtengo mi server
        self.visaServer = None

        # Parametros importantes
        self.user = None
        self.password = None
        self.periodo = None
        
        # Variables para control de thread
        self._eventThread:Event = Event()

    def isRun(self) -> bool:
        return not self._eventThread.is_set()

    def begin(self)->None:
        # Inicializo el server
        self.visaServer = visaServer()
        Thread(target=self._loop, daemon=True).start()

    def stop(self) -> None:
        # Detengo el servidor
        self._eventThread.set()
        self.visaServer.close()

    def _loop(self)->None:
        while self.isRun:
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
            

        

