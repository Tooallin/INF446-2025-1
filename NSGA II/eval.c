/* Routine for evaluating population members  */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "global.h"
# include "rand.h"

/* Routine to evaluate objective function values and constraints for a population */
void evaluate_pop(population *pop, problem_instance *pi) {
	int i;
	for (i = 0; i < popsize; i++) {
		evaluate_ind(&(pop->ind[i]), pi);
	}
	return;
}

/* Routine to evaluate objective function values and constraints for an individual */
void evaluate_ind(individual *ind, problem_instance *pi) {
	int i;

	/* Evaluate objective function 1 */
	objective_function_one(ind, pi);

	/* Evaluate objective function 2 */
	objective_function_two(ind, pi);

	/* Evaluate objective function 3 */
	objective_function_three(ind, pi);

	/* Evaluate constrain 1 */
	contraint_one(ind, pi);

	/* Evaluate constrain 2 */
	contraint_two(ind, pi);

	/* Evaluate constrain 3 */
	contraint_three(ind, pi);

	/* Evaluate constrains */
	ind->constr_violation = 0.0;
	for (i = 0; i < n_constraints; i++) {
		if (ind->constr[i] < 0.0) {
			ind->constr_violation += ind->constr[i];
		}
	}

	return;
}

/* Routine to evaluate objective function 1 */
void objective_function_one(individual *ind, problem_instance *pi) {
	int i, j;
	ind->obj[0] = 0;
	j = 0;
	for (i = 1; i < n_routes; i++) {
		while (ind->gene[j] != -1) {
			ind->obj[0] -= pi->set_POI[ind->gene[j]-1].SCORE;
			j++;
		}
		j++;
	}
	return;
}

/* Routine to evaluate objective function 2 */
void objective_function_two(individual *ind, problem_instance *pi) {
	int i, j, z;
	int **categoria_visitada;
	int total = 0;

	categoria_visitada = (int **)malloc(n_routes * sizeof(int *));
	for (i = 0; i < n_routes; i++) {
		categoria_visitada[i] = (int *)calloc(pi->set_Z, sizeof(int));
	}

	j = 0;
	for (i = 0; i < n_routes; i++) {
		while (j < gene_length && ind->gene[j] != -1) {
			int id_poi = ind->gene[j] - 1;
			for (z = 0; z < pi->set_Z; z++) {
				if (pi->set_POI[id_poi].e[z] == 1) {
					categoria_visitada[i][z] = 1;
				}
			}
			j++;
		}
		j++;
	}

	for (i = 0; i < n_routes; i++) {
		for (z = 0; z < pi->set_Z; z++) {
			total += categoria_visitada[i][z];
		}
	}

	ind->obj[1] = -total;

	for (i = 0; i < n_routes; i++) {
		free(categoria_visitada[i]);
	}
	free(categoria_visitada);
	return;
}

/* Routine to evaluate objective function 3 */
void objective_function_three(individual *ind, problem_instance *pi) {
	int i, j;
	int min, max;
	int temp;
	min = 10000;
	max = -10000;
	j = 0;
	for (i = 1; i < n_routes; i++) {
		temp = 0;
		while (ind->gene[j] != -1) {
			temp += pi->set_POI[ind->gene[j]-1].SCORE;
			j++;
		}
		j++;
		if (temp >= max) {
			max = temp;
		}
		if (temp <= min) {
			min = temp;
		}
	}
	ind->obj[2] = abs(max - min);
	return;
}

/* Routine to evaluate constraint 1 */
void contraint_one(individual *ind, problem_instance *pi) {
	int i, j, k;
	int temp;
	ind->constr[0] = 0;
	for (i = 0; i < pi->set_Z; i++) {
		temp = 0;
		k = 0;
		for (j = 1; j < n_routes; j++) {
			while (ind->gene[k] != -1) {
				temp += pi->set_POI[ind->gene[k]-1].e[i];
				k++;
			}
			k++;
		}
		temp -= pi->param_E[i];
		if (temp < 0) {
			ind->constr[0] += temp;
		}
	}
	return;
}

/* Routine to evaluate constraint 2 */
void contraint_two(individual *ind, problem_instance *pi) {
	int i, j;
	double temp;
	int poi_actual, poi_anterior;

	ind->constr[1] = 0.0;
	j = 0;

	for (i = 1; i < n_routes; i++) {
		temp = 0.0;

		if (ind->gene[j] == -1) {
			j++;
			continue;
		}

		poi_actual = ind->gene[j];
		temp += pi->param_t[pi->param_o.id][poi_actual] + pi->set_POI[poi_actual - 1].TT;
		poi_anterior = poi_actual;
		j++;

		while (ind->gene[j] != -1 && j < gene_length) {
			poi_actual = ind->gene[j];
			temp += pi->param_t[poi_anterior][poi_actual] + pi->set_POI[poi_actual - 1].TT;
			poi_anterior = poi_actual;
			j++;
		}

		if (j > 0 && ind->gene[j - 1] != -1) {
			temp += pi->param_t[poi_anterior][pi->param_s.id];
		}

		if (temp > pi->param_TM) {
			ind->constr[1] += pi->param_TM - temp;
		}

		j++;
	}
	return;
}

/* Routine to evaluate constraint 3 */
void contraint_three(individual *ind, problem_instance *pi) {
	int i, j;
	double temp;
	int poi_actual, poi_anterior;

	ind->constr[2] = 0.0;
	j = 0;

	for (i = 1; i < n_routes; i++) {
		if (ind->gene[j] == -1) {
			j++;
			continue;
		}

		poi_actual = ind->gene[j];
		temp = pi->param_t[pi->param_o.id][poi_actual];

		if (temp < pi->set_POI[poi_actual - 1].OT) {
			ind->constr[2] += temp - pi->set_POI[poi_actual - 1].OT;
			temp = pi->set_POI[poi_actual - 1].OT;
		} else if (temp > pi->set_POI[poi_actual - 1].CT) {
			ind->constr[2] += pi->set_POI[poi_actual - 1].CT - temp;
		}
		temp += pi->set_POI[poi_actual - 1].TT;
		poi_anterior = poi_actual;
		j++;

		while (ind->gene[j] != -1 && j < gene_length) {
			poi_actual = ind->gene[j];
			temp += pi->param_t[poi_anterior][poi_actual];

			if (temp < pi->set_POI[poi_actual - 1].OT) {
				ind->constr[2] += temp - pi->set_POI[poi_actual - 1].OT;
				temp = pi->set_POI[poi_actual - 1].OT;
			} else if (temp > pi->set_POI[poi_actual - 1].CT) {
				ind->constr[2] += pi->set_POI[poi_actual - 1].CT - temp;
			}
			temp += pi->set_POI[poi_actual - 1].TT;
			poi_anterior = poi_actual;
			j++;
		}

		if (j > 0 && ind->gene[j - 1] != -1) {
			temp += pi->param_t[poi_anterior][pi->param_s.id];
			if (temp > pi->param_s.CT) {
				ind->constr[2] += pi->param_s.CT - temp;
			}
		}

		j++;
	}
	return;
}