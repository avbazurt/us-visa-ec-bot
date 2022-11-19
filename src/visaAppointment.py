import json
from src.webFunction import visaServer
from playsound import playsound
from time import sleep


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
                print(f"Fecha disponible: {avaible}")

                # Si existe se procede a encender la alarma
                if (avaible):
                    try:
                        while(True):
                            NOMBRE_ARCHIVO = "alarm-clock.mp3"
                            playsound(NOMBRE_ARCHIVO)
                            sleep(10)
                    except KeyboardInterrupt:
                        self.visaServer.close()
                        quit()

                # Esperamos un rato
                self.visaServer.logout()

                try:
                    # Esperamos el periodo
                    sleep(self.periodo)
                except:
                    self.visaServer.close()


        except:
            self.visaServer.close()
        

        

