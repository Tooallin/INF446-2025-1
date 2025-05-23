import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FormatStrFormatter

JUGUETE_POINTS = {
	"1":  (0.891775, 1       , 0.83871  ),
	"2":  (0.891775, 1       , 0.83871  ),
	"3":  (0.87013 , 0.833333, 1        ),
	"4":  (0.891775, 1       , 0.83871  ),
	"5":  (0.87013 , 0.833333, 1        ),
	"6":  (0.87013 , 0.833333, 1        ),
	"7":  (0.891775, 1       , 0.83871  ),
	"8":  (0.87013 , 0.833333, 1        ),
	"9":  (1       , 0.833333, 0.0322581),
	"10": (0.242424, 1       , 0.516129 ),
	"11": (0.264069, 0.833333, 1        ),
}

C101_POINTS = {
	"1":  (1       , 0.9375, 1       ),
	"2":  (0.963009, 1     , 1       ),
	"3":  (1       , 0.875 , 1       ),
	"4":  (1       , 0.9375, 1       ),
	"5":  (0.963009, 1     , 1       ),
	"6":  (1       , 0.9375, 1       ),
	"7":  (1       , 0.9375, 1       ),
	"8":  (1       , 0.9375, 1       ),
	"9":  (1       , 0.9375, 1       ),
	"10": (0.408138, 1     , 0.295775),
	"11": (0.112207, 0.3125, 1       ),
}

def dominates(p, q):
	return all(p_i >= q_i for p_i, q_i in zip(p, q)) and any(p_i > q_i for p_i, q_i in zip(p, q))

def pareto_front(points_dict):
	points = list(points_dict.values())
	pareto = []
	for p in points:
		if not any(dominates(other, p) for other in points if other != p):
			pareto.append(p)
	return pareto

def plot_pareto_front(points_dict):
	all_points = list(points_dict.values())
	pareto = pareto_front(points_dict)
	dominated = [p for p in all_points if p not in pareto]

	fig = plt.figure(figsize=(8, 6))
	ax = fig.add_subplot(111, projection='3d')

	# Puntos dominados en azul
	if dominated:
		x_d, y_d, z_d = zip(*dominated)
		ax.scatter(x_d, y_d, z_d, c='blue', s=40, label='Dominados')

	# Frente de Pareto en rojo
	if pareto:
		x_p, y_p, z_p = zip(*pareto)
		ax.scatter(x_p, y_p, z_p, c='red', s=50, label='Frente de Pareto')

	# Estética
	ax.set_xlabel('FO 1', fontsize=10, labelpad=8)
	ax.set_ylabel('FO 2', fontsize=10, labelpad=8)
	ax.set_zlabel('FO 3', fontsize=10, labelpad=8)
	ax.set_title('Frente de Pareto vs Dominados (Instancia c101.dat)', fontsize=12)
	#ax.set_title('Frente de Pareto vs Dominados (Instancia juguete.dat)', fontsize=12)

	ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
	ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.2f'))
	ax.tick_params(axis='both', which='major', labelsize=8)

	ax.xaxis.set_pane_color((0.95, 0.95, 0.95, 1.0))
	ax.yaxis.set_pane_color((0.95, 0.95, 0.95, 1.0))
	ax.zaxis.set_pane_color((0.95, 0.95, 0.95, 1.0))

	ax.grid(True, linestyle=':', linewidth=0.5)
	ax.legend()
	plt.tight_layout()
	plt.show()

# Ejecutar la función
plot_pareto_front(C101_POINTS)
