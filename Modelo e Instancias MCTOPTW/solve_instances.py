import subprocess
import os

# Configuración
run_file = "mctoptw-multi.run"  # Este archivo NO debe tener model/data/randseed
seeds = [123, 237, 351, 468, 582, 619, 703, 745, 862, 974]
data_files = ['MCTOPTW/c101.dat', 'MCTOPTW/c102.dat', 'MCTOPTW/c103.dat', 'MCTOPTW/c104.dat']

# Carpeta de salida
output_folder = "Outputs"
os.makedirs(output_folder, exist_ok=True)

# Iterar sobre instancias y semillas
for data_file in data_files:
	for seed in seeds:
		data_name = os.path.splitext(os.path.basename(data_file))[0]
		output_file = os.path.join(output_folder, f"{data_name}_{seed}.txt")

		print(f"Solving {data_file} with seed={seed}")

		# Crear contenido completo para AMPL
		ampl_commands = f"""
		reset;
		option randseed {seed};
		model mctoptw-multi.mod;
		data {data_file};
		include {run_file};
		"""

		# Ejecutar y guardar salida
		with open(output_file, "w") as out:
			subprocess.run(["ampl"], input=ampl_commands.encode(), stdout=out, stderr=subprocess.STDOUT)
