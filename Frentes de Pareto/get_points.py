import os
import re
from collections import defaultdict

# Carpeta con los archivos
carpeta = "./Outputs"

# Regex para capturar F1 F2 F3 desde .txt de instancia clásica
regex_txt = re.compile(r"^\s*\d+\s+[\d.eE+-]+\s+[\d.eE+-]+\s+[\d.eE+-]+\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)")

# Diccionario por instancia
instancia_datos = defaultdict(list)
puntos_unicos = defaultdict(set)  # clave: instancia, valor: set de (F1,F2,F3)

# Archivos relevantes
archivos = [f for f in os.listdir(carpeta) if (
	f.endswith(".txt") or f.endswith(".out")
) and (any(f"c10{i}" in f for i in range(1, 5)) or f == "juguete.txt")]

for archivo in archivos:
	path = os.path.join(carpeta, archivo)
	with open(path, "r") as f:
		lineas = f.readlines()

	# Caso especial: juguete.txt
	if archivo == "juguete.txt":
		capturar = False
		for linea in lineas:
			if ":=" in linea and "FN1" in linea:
				capturar = True
				continue
			if capturar and linea.strip() == ";":
				break
			if capturar:
				partes = linea.strip().split()
				if len(partes) >= 7:
					try:
						f1 = int(float(partes[4]))
						f2 = int(float(partes[5]))
						f3 = int(float(partes[6]))
						punto = (f1, f2, f3)
						if punto not in puntos_unicos["juguete"]:
							puntos_unicos["juguete"].add(punto)
							instancia_datos["juguete"].append(f"{archivo}\tAMPL\t{f1}\t{f2}\t{f3}")
					except ValueError:
						continue
		continue

	# Determinar la instancia
	instancia_match = re.search(r"(c10\d)", archivo)
	if not instancia_match:
		continue
	instancia = instancia_match.group(1)

	if archivo.endswith(".txt"):
		capturar = False
		seccion = 0
		for linea in lineas:
			if ":=" in linea:
				seccion += 1
				capturar = seccion >= 2
				continue
			if capturar:
				match = regex_txt.match(linea)
				if match:
					f1, f2, f3 = map(int, match.groups())
					punto = (f1, f2, f3)
					if punto not in puntos_unicos[instancia]:
						puntos_unicos[instancia].add(punto)
						instancia_datos[instancia].append(f"{archivo}\tAMPL\t{f1}\t{f2}\t{f3}")

	elif archivo.endswith(".out"):
		for linea in lineas:
			partes = linea.strip().split()
			if len(partes) >= 3:
				try:
					f1 = float(partes[0])
					f2 = float(partes[1])
					f3 = float(partes[2])
					punto = (f1, f2, f3)
					if punto not in puntos_unicos[instancia]:
						puntos_unicos[instancia].add(punto)
						instancia_datos[instancia].append(f"{archivo}\tNSGA-II\t{f1}\t{f2}\t{f3}")
				except ValueError:
					continue

# Guardar por instancia
for instancia, lineas in instancia_datos.items():
	nombre_archivo = f"points_{instancia}.txt"
	with open(nombre_archivo, "w") as f:
		f.write("archivo\tfuente\tF1\tF2\tF3\n")
		for linea in lineas:
			f.write(linea + "\n")
	print(f"✅ Archivo generado (sin duplicados): {nombre_archivo}")
