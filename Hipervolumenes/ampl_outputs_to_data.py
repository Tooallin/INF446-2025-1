import os
import re

# Función de dominancia (minimización)
def is_dominated(a, b):
	return all(bi <= ai for ai, bi in zip(a, b)) and any(bi < ai for ai, bi in zip(a, b))

def filter_non_dominated(solutions):
	non_dominated = []
	for i, sol in enumerate(solutions):
		if not any(is_dominated(sol, other) for j, other in enumerate(solutions) if i != j):
			non_dominated.append(sol)
	return non_dominated

# Extraer F1, F2, F3 desde sección final
def extract_f123_from_block(text):
	matches = re.findall(r':\s+FN1.+?TCPU2\s+:=\s*(.*?)\s*;', text, re.DOTALL)
	if not matches:
		return []

	lines = matches[-1].strip().split('\n')
	solutions = []
	for line in lines[:11]:  # solo filas 1 a 11
		parts = re.split(r'\s+', line.strip())
		if len(parts) >= 7:
			try:
				f1, f2, f3 = float(parts[4]), float(parts[5]), float(parts[6])
				solutions.append((f1, f2, f3))
			except ValueError:
				continue
	return solutions

# Archivos por instancia
instances = {
	"c101_ampl": [
		"Outputs AMPL/c101_123.txt", "Outputs AMPL/c101_237.txt", "Outputs AMPL/c101_351.txt", "Outputs AMPL/c101_468.txt", "Outputs AMPL/c101_582.txt",
		"Outputs AMPL/c101_619.txt", "Outputs AMPL/c101_703.txt", "Outputs AMPL/c101_745.txt", "Outputs AMPL/c101_862.txt", "Outputs AMPL/c101_974.txt"
	],
	"c102_ampl": [
		"Outputs AMPL/c102_123.txt", "Outputs AMPL/c102_237.txt", "Outputs AMPL/c102_351.txt", "Outputs AMPL/c102_468.txt", "Outputs AMPL/c102_582.txt",
		"Outputs AMPL/c102_619.txt", "Outputs AMPL/c102_703.txt", "Outputs AMPL/c102_745.txt", "Outputs AMPL/c102_862.txt", "Outputs AMPL/c102_974.txt"
	],
	"c103_ampl": [
		"Outputs AMPL/c103_123.txt", "Outputs AMPL/c103_237.txt", "Outputs AMPL/c103_351.txt", "Outputs AMPL/c103_468.txt", "Outputs AMPL/c103_582.txt",
		"Outputs AMPL/c103_619.txt", "Outputs AMPL/c103_703.txt", "Outputs AMPL/c103_745.txt", "Outputs AMPL/c103_862.txt", "Outputs AMPL/c103_974.txt"
	],
	"c104_ampl": [
		"Outputs AMPL/c104_123.txt", "Outputs AMPL/c104_237.txt", "Outputs AMPL/c104_351.txt", "Outputs AMPL/c104_468.txt", "Outputs AMPL/c104_582.txt",
		"Outputs AMPL/c104_619.txt", "Outputs AMPL/c104_703.txt", "Outputs AMPL/c104_745.txt", "Outputs AMPL/c104_862.txt", "Outputs AMPL/c104_974.txt"
	]
}

for instance, file_list in instances.items():
	all_solutions = []

	for filename in file_list:
		with open(filename, "r", encoding="utf-8") as f:
			text = f.read()
			all_solutions.extend(extract_f123_from_block(text))

	# Eliminar dominadas
	nd_solutions = filter_non_dominated(all_solutions)

	# Convertir a enteros positivos y eliminar duplicados
	unique_rows = sorted(set((abs(int(f1)), abs(int(f2)), abs(int(f3))) for f1, f2, f3 in nd_solutions))

	# Escribir salida
	with open(f"{instance}_data", "w") as out:
		out.write("#\n")
		for row in unique_rows:
			out.write(f"{row[0]} {row[1]} {row[2]}\n")
		out.write("#\n")
