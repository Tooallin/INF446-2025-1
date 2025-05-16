import pandas as pd
import numpy as np
import os
from pathlib import Path

def asignar_categorias_binarias(df, categorias, probabilidades):
	poi_indices = df[(df['ID'] != 0) & (df['ID'] != df['ID'].max())].index
	for cat, prob in zip(categorias, probabilidades):
		valores = np.random.binomial(1, prob, size=len(poi_indices))
		df.loc[poi_indices, cat] = valores
	return df

def generate_dat(input_csv_path, output_dat_path, seed=2021735410):
	np.random.seed(seed)
	df = pd.read_csv(input_csv_path)

	df['ei1'] = 0
	df['ei2'] = 0
	df['ei3'] = 0
	df['ei4'] = 0
	df['ei5'] = 0

	probs = [0.85, 0.65, 0.35, 0.15, 0.05]
	df = asignar_categorias_binarias(df, ['ei1', 'ei2', 'ei3', 'ei4', 'ei5'], probs)

	# Agregar nodo final
	last_id = df['ID'].max() + 1
	depot = df[df['ID'] == 0].iloc[0]
	due_date_max = df['DUE_DATE'].max()

	last_node = {
			'ID': last_id,
			'X': depot['X'],
			'Y': depot['Y'],
			'SERVICE_TIME': 0,
			'READY_TIME': 0,
			'DUE_DATE': due_date_max,
			'PRIZE': 0,
			'ei1': 0,
			'ei2': 0,
			'ei3': 0,
			'ei4': 0,
			'ei5': 0,
	}

	df = pd.concat([df, pd.DataFrame([last_node])], ignore_index=True)
	df = df.sort_values(by='ID').reset_index(drop=True)

	node_ids = df['ID'].tolist()
	start_node = node_ids[0]
	end_node = node_ids[-1]
	poi_ids = [i for i in node_ids if i != start_node and i != end_node]

	coords = df.set_index('ID')[['X', 'Y']].to_dict('index')
	distances = {
		(i, j): round(np.hypot(coords[i]['X'] - coords[j]['X'], coords[i]['Y'] - coords[j]['Y']), 2)
		for i in node_ids for j in node_ids if i != j
	}

	lines = []
	lines.append(f"param o := {start_node};")
	lines.append(f"param s := {end_node};\n")
	lines.append(f"set POI := {' '.join(map(str, poi_ids))};")
	lines.append("set M := 1 2 3;")
	lines.append("set Z := 1 2 3 4 5;\n")

	lines.append("\nparam e :=")
	for _, row in df.iterrows():
		lines.append(f"{int(row['ID'])} 1 {int(row['ei1'])} {int(row['ID'])} 2 {int(row['ei2'])} {int(row['ID'])} 3 {int(row['ei3'])} {int(row['ID'])} 4 {int(row['ei4'])} {int(row['ID'])} 5 {int(row['ei5'])}")
	lines.append(";")

	for param, col in zip(["SCORE", "OT", "TT", "CT"], ["PRIZE", "READY_TIME", "SERVICE_TIME", "DUE_DATE"]):
		lines.append(f"\nparam {param} :=")
		for _, row in df.iterrows():
				lines.append(f"{int(row['ID'])} {int(row[col])}")
		lines.append(";")

	lines.append("\nparam t :=")
	for (i, j), d in distances.items():
		lines.append(f"{i} {j} {d}")
	lines.append(";")

	with open(output_dat_path, 'w') as f:
		f.write("\n".join(lines))

	print(f"✅ Archivo generado: {output_dat_path}")

def batch_generate(csv_directory, output_directory):
	os.makedirs(output_directory, exist_ok=True)
	for filename in os.listdir(csv_directory):
		if filename.endswith(".csv"):
			input_path = os.path.join(csv_directory, filename)
			output_name = Path(filename).stem + ".dat"
			output_path = os.path.join(output_directory, output_name)
			generate_dat(input_path, output_path)

batch_generate("Instancias CSV", "Instancias DAT")