import subprocess

comandos = [
	"./hv -r \"-126 -9 22\" c101_ampl_data",
	"./hv -r \"-126 -9 22\" c101_nsga2_data",
	"./hv -r \"-621 -9.9 66\" c102_ampl_data",
	"./hv -r \"-621 -9.9 66\" c102_nsga2_data",
	"./hv -r \"-270 -9 132\" c103_ampl_data",
	"./hv -r \"-270 -9 132\" c103_nsga2_data",
	"./hv -r \"-279 -12.6 44\" c104_ampl_data",
	"./hv -r \"-279 -12.6 44\" c104_nsga2_data",
]

for cmd in comandos:
	subprocess.run(cmd, shell=True)
