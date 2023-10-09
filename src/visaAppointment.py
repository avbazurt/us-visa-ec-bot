import json
from src.webFunction import visaServer
from playsound import playsound
from time import sleep
import traceback

class visaAppointment():
    def __init__(self) -> None:
        self.visaServer = visaServer()

        self.user = None
        self.password = None

        self.periodo = None


    def loop(self)->None:
        try:
            while True:
                # Iniciamos el Server
                self.visaServer.login(self.user, self.password)

                # Abrimos el Appointment
                avaible = self.visaServer.aviableAppointment()

                if (avaible):
                    print("Date found")
                    try:
                        while(True):
                            NOMBRE_ARCHIVO = "alarm-clock.mp3"
                            playsound(NOMBRE_ARCHIVO)
                            sleep(10)
                    except KeyboardInterrupt:
                        input("Presiona enter para cerrar el proceso")
                        self.visaServer.close()
                        quit()
                        
                else:
                    print("Could not find available dates, log out and wait to log back in")

                # Esperamos un rato
                self.visaServer.logout()

                try:
                    # Esperamos el periodo
                    sleep(self.periodo)
                except:
                    self.visaServer.close()


        except Exception as err:
            traceback.print_exc()
            self.visaServer.close()

        except KeyboardInterrupt:
            pass
        

        

