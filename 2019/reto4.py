from datetime import datetime, timedelta, time, date
import json

# Cargar pedidos
pedidos = []
with open("confidential-data/pedidos-AM.json") as f:
	pedidos += json.load(f)
with open("confidential-data/pedidos-EB.json") as f:
	pedidos += json.load(f)
with open("confidential-data/pedidos-HM.json") as f:
	pedidos += json.load(f)
with open("confidential-data/pedidos-JO.json") as f:
	pedidos += json.load(f)
with open("confidential-data/pedidos-MM.json") as f:
	pedidos += json.load(f)
with open("confidential-data/pedidos-ZA.json") as f:
	pedidos += json.load(f)

# Filtramos paquetes de más de 2kg
pedidos = [p for p in pedidos if p["pesoPaqueteGr"] <= 2000]

def hora(t):
	return datetime.strptime(t["horaEntregaDeseada"], "%H:%M") - timedelta(minutes = t["duracionRecorrido"])

pedidos.sort(key = hora) # Ordenar por hora de salida deseada

ultima = datetime.strptime("08:55", "%H:%M") # Hora de última salida realizada
viajelargo = False # Último viaje tenía una duráción de más de 15 minutos
fin = False # Se ha alcanzado el fin del día (21:00)

for p in pedidos:
	# Hora de salida deseada
	salida = hora(p)
	
	# Ajustar tiempos de descanso
	if viajelargo:
		salida = max(salida, ultima + timedelta(minutes = 10))
	else:
		salida = max(salida, ultima + timedelta(minutes = 5))

	hh = salida.hour
	mm = salida.minute
	# Entrega antes de horario
	if hh < 9:
		hh = 9
		mm = 0
	# Entrega después de horario
	if hh == 21 and mm > 0:
		hh = 0
		mm = 0
		fin = True
	# Redondear a múltiplo de 5 superior. Si redondeo a 60, aumentar una hora.
	if mm > 55:
		hh += 1
		mm = 0
	mm = ((mm+4)//5)*5

	salida = salida.replace(hour = hh, minute = mm)
	
	if fin:
		p["horaSalidaReal"] = "Retrasado día siguiente"
	else:
		p["horaSalidaReal"] = salida.strftime("%H:%M")
	ultima = salida
	viajelargo = p["duracionRecorrido"] > 15

def reto4(x):
	reparto = pedidos[x-1]
	print(reparto["id"], reparto["horaSalidaReal"])

reto4(1)
reto4(25)
reto4(115)





















