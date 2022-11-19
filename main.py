from src.visaAppointment import visaAppointment

visaAppointment = visaAppointment()

# Credenciales
visaAppointment.user = ""
visaAppointment.password = ""
visaAppointment.periodo = 5 * 60

# Loop
visaAppointment.loop()