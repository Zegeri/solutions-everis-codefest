import json

# Escribe aquí la localización del archivo json con las posiciones del tablero
juego = "data/jugada2.json"

# Objeto global que guardará las posiciones del tablero
pos = {}

def check(x,y,eq):
	""" Devuelve 1 si hay una pieza del mismo equipo en la posición (x,y) del tablero,
	    2 si es del otro equipo y 0 si no hay pieza
	"""
	global pos
	if (x,y) not in pos:
		return 0
	elif pos[x,y][1] == eq:
		return 1
	elif pos[x,y][1] != eq:
		return 2

def checkdie(x,y,eq):
	""" Mata una pieza enemiga en (x,y). Devuelve True sii había una pieza en esa posición,
	    incluso si era una pieza amiga
	"""
	c = check(x,y,eq)
	if c == 2:
		# Marcar pieza como muerta
		pos[x,y] = (pos[x,y][0], pos[x,y][1], 1)
	return c != 0

with open(juego) as f:
	# Cargar tablero
	t = json.load(f)
	ancho = 2*int(t['juego']['ancho'])+1
	alto = 2*int(t['juego']['alto'])+1
	tamaño = max(ancho,alto)
	pos = {}
	# Guardamos las posiciones en un diccionario global y las marcamos como vivas
	for x in t['juego']['posiciones']:
		pos[x['x'],x['y']] = (x['piece'], x['side'], 0)

	# Vamos pieza por pieza y marcamos las piezas que puede matar
	for xx,yy in pos:
		p,eq,status = pos[xx,yy]
		
		# Spiderman o Ironman (movimiento alfil)
		if p == "S" or p == "I":
			for r in range(1,tamaño):
				if checkdie(xx+r,yy+r,eq):
					break
			for r in range(1,tamaño):
				if checkdie(xx-r,yy+r,eq):
					break
			for r in range(1,tamaño):
				if checkdie(xx-r,yy-r,eq):
					break
			for r in range(1,tamaño):
				if checkdie(xx+r,yy-r,eq):
					break

		# Capitán América (movimiento caballo)
		if p == "C":
			checkdie(xx+3,yy+1,eq)
			checkdie(xx+3,yy-1,eq)
			checkdie(xx-3,yy+1,eq)
			checkdie(xx-3,yy-1,eq)

			checkdie(xx+1,yy+3,eq)
			checkdie(xx-1,yy+3,eq)
			checkdie(xx+1,yy-3,eq)
			checkdie(xx-1,yy-3,eq)

		# Hulk o Ironman (movimiento torre)
		if p == "H" or p == "I":
			for r in range(1,tamaño):
				if checkdie(xx+r,yy,eq):
					break
			for r in range(1,tamaño):
				if checkdie(xx-r,yy,eq):
					break
			for r in range(1,tamaño):
				if checkdie(xx,yy+r,eq):
					break
			for r in range(1,tamaño):
				if checkdie(xx,yy-r,eq):
					break

		# Doctor Strange (posiciones adyacentes)
		if p == "D":
			checkdie(xx+1,yy,  eq)
			checkdie(xx+1,yy+1,eq)
			checkdie(xx+1,yy-1,eq)
			checkdie(xx,  yy-1,eq)
			checkdie(xx-1,yy-1,eq)
			checkdie(xx-1,yy,  eq)
			checkdie(xx-1,yy+1,eq)
			checkdie(xx,  yy+1,eq)

		# Groot (posiciones adyacentes diagonales)
		if p == "G":
			checkdie(xx+1,yy+1,eq)
			checkdie(xx+1,yy-1,eq)
			checkdie(xx-1,yy+1,eq)
			checkdie(xx-1,yy-1,eq)


	# Calcular puntos de piezas muertas
	puntos = {'C':3,'H':2,'S':4,'D':9,'I':7,'G':1}
	ptsrojos = 0
	ptsazules = 0
	for xx,yy in pos:
		p,eq,status = pos[xx,yy]
		if status == 1: # Pieza muerta
			if eq == "ROJO":
				ptsazules += puntos[p]
			else:
				ptsrojos += puntos[p]

	# Mostrar equipo ganador
	if (ptsrojos > ptsazules):
		print("Rojas {}d".format(ptsrojos))
	if (ptsazules > ptsrojos):
		print("Azules {}d".format(ptsazules))
	if (ptsazules == ptsrojos):
		print("Empate {}d".format(ptsrojos))
