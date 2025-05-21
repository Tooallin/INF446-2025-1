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

	/* Evaluate constrain 4 */
	contraint_four(ind, pi);

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
	int i, j, k;
	int temp;
	ind->obj[1] = 0;
	for (i = 0; i < pi->set_Z; i++) {
		k = 0;
		for (j = 1; j < n_routes; j++) {
			temp = 0;
			while (ind->gene[k] != -1) {
				if (pi->set_POI[ind->gene[k]-1].e[i] == 1) temp = 1;
				k++;
			}
			ind->obj[1] -= temp;
			k++;
		}
	}
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
	int temp;
	ind->constr[1] = 0;
	for (i = 1; i < n_routes; i++) {
		temp = 0;
		temp += pi->param_t[pi->param_o.id][ind->gene[j]] + pi->set_POI[ind->gene[j]-1].TT;
		j++;
		while (ind->gene[j] != -1) {
			temp += pi->param_t[ind->gene[j-1]][ind->gene[j]] + pi->set_POI[ind->gene[j]-1].TT;
			j++;
		}
		temp += pi->param_t[ind->gene[j-1]][pi->param_s.id];
		temp -= pi->param_TM;
		if (temp > 0) {
			ind->constr[1] -= temp;
		}
		j++;
	}
	return;
}

/* Routine to evaluate constraint 3 */
void contraint_three(individual *ind, problem_instance *pi) {
	int i, j;
	int temp;
	ind->constr[2] = 0;
	for (i = 1; i < n_routes; i++) {
		temp = 0;
		temp += pi->param_t[pi->param_o.id][ind->gene[j]];
		if (temp < pi->set_POI[ind->gene[j]-1].OT) {
			ind->constr[2] += temp - pi->set_POI[ind->gene[j]-1].OT;
		}
		if (temp > pi->set_POI[ind->gene[j]-1].CT) {
			ind->constr[2] += pi->set_POI[ind->gene[j]-1].CT - temp;
		}
		temp += pi->set_POI[ind->gene[j]-1].TT;
		j++;
		while (ind->gene[j] != -1) {
			temp += pi->param_t[ind->gene[j-1]][ind->gene[j]];
			if (temp < pi->set_POI[ind->gene[j]-1].OT) {
				ind->constr[2] += temp - pi->set_POI[ind->gene[j]-1].OT;
			}
			if (temp > pi->set_POI[ind->gene[j]-1].CT) {
				ind->constr[2] += pi->set_POI[ind->gene[j]-1].CT - temp;
			}
			temp += pi->set_POI[ind->gene[j]-1].TT;
			j++;
		}
		temp += pi->param_t[ind->gene[j-1]][pi->param_s.id];
		if (temp > pi->param_s.CT) {
			ind->constr[2] += pi->param_s.CT - temp;
		}
		j++;
	}
	return;
}

/* Routine to evaluate constraint 4 */
void contraint_four(individual *ind, problem_instance *pi) {
	ind->constr[3] = 0;
	return;
}