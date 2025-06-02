import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator

def es_dominado(p1, p2):
	return all(x >= y for x, y in zip(p1, p2)) and any(x > y for x, y in zip(p1, p2))

def obtener_no_dominados(puntos):
	no_dominados = []
	for i, p in enumerate(puntos):
		if not any(es_dominado(p, q) for j, q in enumerate(puntos) if i != j):
			no_dominados.append(i)
	return no_dominados

# Carpeta con archivos
carpeta = "./"
archivos = [f for f in os.listdir(carpeta) if f.startswith("points_") and f.endswith(".txt")]

for archivo in archivos:
	df = pd.read_csv(os.path.join(carpeta, archivo), sep="\t")

	# Determinar índices no dominados
	puntos = df[["F1", "F2", "F3"]].values.tolist()
	idx_no_dominados = obtener_no_dominados(puntos)
	df_no_dominados = df.iloc[idx_no_dominados]
	df_dominados = df.drop(index=idx_no_dominados)

	# Preparar figura
	fig = plt.figure(figsize=(8, 7))
	ax = fig.add_subplot(111, projection='3d', facecolor='white')

	# Dibujar dominados con menor alpha y colores claros
	for fuente, color, marker in [('AMPL', '#6495ED', 'o'), ('NSGA-II', '#F08080', 'D')]:
		sub = df_dominados[df_dominados["fuente"] == fuente]
		if not sub.empty:
			ax.scatter(sub["F1"], sub["F2"], sub["F3"],
			           c=color, label=f'{fuente} (dom)', alpha=0.4, s=50, edgecolors='k', marker=marker)

	# Dibujar no dominados con colores oscuros
	for fuente, color, marker in [('AMPL', '#00008B', 'o'), ('NSGA-II', '#8B0000', 'D')]:
		sub = df_no_dominados[df_no_dominados["fuente"] == fuente]
		if not sub.empty:
			ax.scatter(sub["F1"], sub["F2"], sub["F3"],
			           c=color, label=f'{fuente} (no dom)', alpha=1.0, s=50, edgecolors='k', marker=marker)

	# Ejes
	ax.set_xlabel("F1", fontsize=12, labelpad=15, fontweight='bold')
	ax.set_ylabel("F2", fontsize=12, labelpad=15, fontweight='bold')
	ax.set_zlabel("F3", fontsize=12, labelpad=20, fontweight='bold')
	ax.zaxis.set_label_coords(-0.1, 0.5)

	# Título
	titulo = archivo.replace("points_", "").replace(".txt", ".dat").lower()
	ax.set_title(f"Frente Pareto - {titulo}", fontsize=14, pad=20, fontweight='bold')

	# Estilo general
	ax.legend(loc='best', fontsize=10)
	ax.view_init(elev=20, azim=135)
	ax.grid(True)
	ax.tick_params(axis='both', which='major', labelsize=10)

	ax.xaxis.set_major_locator(MaxNLocator(integer=True))
	ax.yaxis.set_major_locator(MaxNLocator(integer=True))
	ax.zaxis.set_major_locator(MaxNLocator(integer=True))

	# Holgura en ejes
	for dim, col in zip([ax.set_xlim, ax.set_ylim, ax.set_zlim], ["F1", "F2", "F3"]):
		min_val = df[col].min()
		max_val = df[col].max()
		margin = 0.05 * (max_val - min_val) if max_val != min_val else 1
		dim(min_val - margin, max_val + margin)

	# Guardar imagen
	nombre_img = f"pareto_front_{archivo.replace('points_', '').replace('.txt', '').lower()}.png"
	plt.savefig(nombre_img, dpi=300)
	plt.close()

	print(f"✅ Gráfico generado: {nombre_img}")
