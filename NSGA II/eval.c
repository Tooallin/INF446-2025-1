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
	int i, j, k;
	int min, max;
	int temp;

	/* Evaluate objective function 1 */
	ind->obj[0] = 0;
	for (i = 1; i < n_routes; i++) {
		while (ind->gene[j] != -1) {
			ind->obj[0] += pi->set_POI[ind->gene[j]-1].SCORE;
			j++;
		}
		j++;
	}

	/* Evaluate objective function 2 */
	ind->obj[1] = 0;
	for (i = 0; i < pi->set_Z; i++) {
		k = 0;
		for (j = 1; i < n_routes; i++) {
			temp = 0;
			while (ind->gene[k] != -1) {
				if (pi->set_POI[ind->gene[k]-1].e[i] == 1) temp = 1;
				k++;
			}
			ind->obj[1] += temp;
			k++;
		}
	}

	/* Evaluate objective function 3 */
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

	/* Evaluate constrains */
	if (ncon == 0) {
		ind->constr_violation = 0.0;
	} else {
		ind->constr_violation = 0.0;
		for (j = 0; j < ncon; j++) {
			if (ind->constr[j] < 0.0) {
				ind->constr_violation += ind->constr[j];
			}
		}
	}

	return;
}
