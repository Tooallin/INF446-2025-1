import os
import re

def load_solutions(file_list):
	solutions = []
	for file in file_list:
		with open(file, "r") as f:
			for line in f:
				if not line.strip():
					continue
				parts = re.split(r'\s+', line.strip())
				if len(parts) >= 3:
					try:
						objs = tuple(float(x) for x in parts[:3])
						solutions.append(objs)
					except ValueError:
						continue
	return solutions

def is_dominated(a, b):
	"""Retorna True si 'a' es dominado por 'b'"""
	return all(bi <= ai for ai, bi in zip(a, b)) and any(bi < ai for ai, bi in zip(a, b))

def filter_non_dominated(solutions):
	"""Devuelve solo las soluciones no dominadas del conjunto"""
	non_dominated = []
	for i, sol in enumerate(solutions):
		dominated = False
		for j, other in enumerate(solutions):
			if i != j and is_dominated(sol, other):
				dominated = True
				break
		if not dominated:
			non_dominated.append(sol)
	return non_dominated

def write_output(instance_name, solutions):
	with open(f"{instance_name}_data", "w") as out:
		out.write("#\n")
		# Convertir a enteros positivos y eliminar duplicados
		unique_rows = set(tuple(abs(int(x)) for x in sol) for sol in solutions)
		for row in sorted(unique_rows):
			out.write(f"{row[0]} {row[1]} {row[2]}\n")
		out.write("#\n")

# Archivos agrupados por instancia
instances = {
	"c101_nsga2": [
		"Outputs NSGA-II/best_pop_c101.dat_0.123.out",
		"Outputs NSGA-II/best_pop_c101.dat_0.237.out",
		"Outputs NSGA-II/best_pop_c101.dat_0.351.out",
		"Outputs NSGA-II/best_pop_c101.dat_0.468.out",
		"Outputs NSGA-II/best_pop_c101.dat_0.582.out",
		"Outputs NSGA-II/best_pop_c101.dat_0.619.out",
		"Outputs NSGA-II/best_pop_c101.dat_0.703.out",
		"Outputs NSGA-II/best_pop_c101.dat_0.745.out",
		"Outputs NSGA-II/best_pop_c101.dat_0.862.out",
		"Outputs NSGA-II/best_pop_c101.dat_0.974.out"
	],
	"c102_nsga2": [
		"Outputs NSGA-II/best_pop_c102.dat_0.123.out",
		"Outputs NSGA-II/best_pop_c102.dat_0.237.out",
		"Outputs NSGA-II/best_pop_c102.dat_0.351.out",
		"Outputs NSGA-II/best_pop_c102.dat_0.468.out",
		"Outputs NSGA-II/best_pop_c102.dat_0.582.out",
		"Outputs NSGA-II/best_pop_c102.dat_0.619.out",
		"Outputs NSGA-II/best_pop_c102.dat_0.703.out",
		"Outputs NSGA-II/best_pop_c102.dat_0.745.out",
		"Outputs NSGA-II/best_pop_c102.dat_0.862.out",
		"Outputs NSGA-II/best_pop_c102.dat_0.974.out"
	],
	"c103_nsga2": [
		"Outputs NSGA-II/best_pop_c103.dat_0.123.out",
		"Outputs NSGA-II/best_pop_c103.dat_0.237.out",
		"Outputs NSGA-II/best_pop_c103.dat_0.351.out",
		"Outputs NSGA-II/best_pop_c103.dat_0.468.out",
		"Outputs NSGA-II/best_pop_c103.dat_0.582.out",
		"Outputs NSGA-II/best_pop_c103.dat_0.619.out",
		"Outputs NSGA-II/best_pop_c103.dat_0.703.out",
		"Outputs NSGA-II/best_pop_c103.dat_0.745.out",
		"Outputs NSGA-II/best_pop_c103.dat_0.862.out",
		"Outputs NSGA-II/best_pop_c103.dat_0.974.out"
	],
	"c104_nsga2": [
		"Outputs NSGA-II/best_pop_c104.dat_0.123.out",
		"Outputs NSGA-II/best_pop_c104.dat_0.237.out",
		"Outputs NSGA-II/best_pop_c104.dat_0.351.out",
		"Outputs NSGA-II/best_pop_c104.dat_0.468.out",
		"Outputs NSGA-II/best_pop_c104.dat_0.582.out",
		"Outputs NSGA-II/best_pop_c104.dat_0.619.out",
		"Outputs NSGA-II/best_pop_c104.dat_0.703.out",
		"Outputs NSGA-II/best_pop_c104.dat_0.745.out",
		"Outputs NSGA-II/best_pop_c104.dat_0.862.out",
		"Outputs NSGA-II/best_pop_c104.dat_0.974.out"
	]
}

# Procesar cada conjunto
for instance_name, file_list in instances.items():
	all_solutions = load_solutions(file_list)
	nd_solutions = filter_non_dominated(all_solutions)
	write_output(instance_name, nd_solutions)
