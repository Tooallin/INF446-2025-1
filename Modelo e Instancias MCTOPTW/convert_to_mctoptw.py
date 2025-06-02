import os
from pathlib import Path

INSTANCE_PARAMS = {
	"c101.dat": (1180, 26, 20, 8, 3, 4),
	"c102.dat": (1236, 21, 16, 8, 2, 1),
	"c103.dat": (1236, 25, 19, 7, 3, 1),
	"c104.dat": (1236, 23, 13, 11, 3, 3),
	"c105.dat": (1208, 24, 19, 7, 3, 4),
	"c106.dat": (1173, 26, 17, 9, 3, 4),
	"c107.dat": (1223, 25, 17, 8, 2, 3),
	"c108.dat": (1229, 21, 17, 8, 4, 3),
	"c109.dat": (1229, 23, 19, 8, 3, 1),
	"c201.dat": (3373, 81, 58, 29, 7, 5),
	"c202.dat": (3359, 56, 41, 18, 6, 5),
	"c203.dat": (1180, 26, 20, 8, 3, 4), #ESTA DIO INFACTIBLE CON 5 MIN
	"c204.dat": (1180, 26, 20, 8, 3, 4), #ESTA DIO INFACTIBLE CON 5 MIN
	"c205.dat": (3366, 73, 56, 28, 7, 6),
	"c206.dat": (3362, 66, 51, 26, 6, 5),
	"c207.dat": (3302, 69, 52, 24, 6, 5),
	"c208.dat": (3153, 41, 29, 14, 3, 4),
	"r101.dat": (229, 18, 9, 7, 1, 3),
	"r102.dat": (219, 5, 8, 3, 1, 1),
	"r103.dat": (1180, 26, 20, 8, 3, 4), #ESTA DIO INFACTIBLE CON 5 MIN
	"r104.dat": (1180, 26, 20, 8, 3, 4), #ESTA DIO INFACTIBLE CON 5 MIN
	"r105.dat": (229, 25, 15, 11, 2, 2),
	"r106.dat": (230, 11, 9, 6, 1, 1),
	"r107.dat": (1180, 26, 20, 8, 3, 4), #ESTA DIO INFACTIBLE CON 5 MIN
	"r108.dat": (1180, 26, 20, 8, 3, 4), #ESTA DIO INFACTIBLE CON 5 MIN
	"r109.dat": (227, 21, 15, 9, 0, 2),
	"r110.dat": (221, 18, 8, 9, 3, 0),
	"r111.dat": (220, 13, 7, 6, 1, 2),
	"r112.dat": (220, 13, 7, 6, 1, 2), #ESTA DIO INFACTIBLE CON 5 MIN
	"r201.dat": (992, 70, 49, 24, 6, 5),
	"r202.dat": (1000, 29, 21, 11, 3, 2),
	"r203.dat": (997, 50, 32, 20, 3, 4),
	"r204.dat": (1180, 26, 20, 8, 3, 4), #ESTA DIO INFACTIBLE CON 5 MIN
	"r205.dat": (989, 36, 30, 13, 4, 2),
	"r206.dat": (1180, 26, 20, 8, 3, 4), #ESTA DIO INFACTIBLE CON 5 MIN
	"r207.dat": (1180, 26, 20, 8, 3, 4), #Falta de aqui pa abajo
	"r208.dat": (1180, 26, 20, 8, 3, 4),
	"r209.dat": (1180, 26, 20, 8, 3, 4),
	"r210.dat": (1180, 26, 20, 8, 3, 4),
	"r211.dat": (1180, 26, 20, 8, 3, 4),
	"rc101.dat": (1180, 26, 20, 8, 3, 4),
	"rc102.dat": (1180, 26, 20, 8, 3, 4),
	"rc103.dat": (1180, 26, 20, 8, 3, 4),
	"rc104.dat": (1180, 26, 20, 8, 3, 4),
	"rc105.dat": (1180, 26, 20, 8, 3, 4),
	"rc106.dat": (1180, 26, 20, 8, 3, 4),
	"rc107.dat": (1180, 26, 20, 8, 3, 4),
	"rc108.dat": (1180, 26, 20, 8, 3, 4),
	"rc201.dat": (1180, 26, 20, 8, 3, 4),
	"rc202.dat": (1180, 26, 20, 8, 3, 4),
	"rc203.dat": (1180, 26, 20, 8, 3, 4),
	"rc204.dat": (1180, 26, 20, 8, 3, 4),
	"rc205.dat": (1180, 26, 20, 8, 3, 4),
	"rc206.dat": (1180, 26, 20, 8, 3, 4),
	"rc207.dat": (1180, 26, 20, 8, 3, 4),
	"rc208.dat": (1180, 26, 20, 8, 3, 4),
}

def modify_dat(input_path, output_path):
	TM, E1, E2, E3, E4, E5 = INSTANCE_PARAMS[os.path.basename(input_path)]
	with open(input_path, 'r') as f:
		lines = f.readlines()
	new_params = [
		f"param TM := {TM};\n\n",
		"param E :=\n",
		f"1 {E1}\n",
		f"2 {E2}\n",
		f"3 {E3}\n",
		f"4 {E4}\n",
		f"5 {E5}\n",
		";\n"
	]
	lines[7:7] = new_params
	with open(output_path, 'w') as f:
		f.writelines(lines)

def batch_modify_dat(input_directory, output_directory):
	os.makedirs(output_directory, exist_ok=True)
	for filename in os.listdir(input_directory):
		if filename.endswith(".dat"):
			input_path = os.path.join(input_directory, filename)
			output_name = filename  # o Path(filename).stem + "_mod.dat" si quieres renombrarlos
			output_path = os.path.join(output_directory, output_name)
			modify_dat(input_path, output_path)

batch_modify_dat("Instancias Iniciales", "Instancias Finales")