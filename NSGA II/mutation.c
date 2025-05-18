/* Mutation routines */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "global.h"
# include "rand.h"

/* Function to perform mutation in a population */
void mutation_pop(population *pop) {
	int i;
	for (i = 0; i < popsize; i++) {
		mutation_ind(&(pop->ind[i]));
	}
	return;
}

/* Function to perform mutation of an individual */
void mutation_ind(individual *ind) {
	int choice;
	choice = rnd(1,2);
	if (choice == 1) {
		ars(ind);
	} else {
		ers(ind);
	}
	return;
}

/* Routine for intra route swap mutation */
void ars(individual *ind) {
	int start, end;
	int poi1, poi2, temp;
	int count, route;
	route = rnd(1, n_routes);
	start = 0; count = 1;
	while (count < route) {
		if (ind->gene[start] == -1) {
			count++;
		}
		start++;
	}
	end = 0; count = 1;
	while (count < route + 1) {
		if (ind->gene[end] == -1) {
			count++;
		}
		end++;
	}
	poi1 = rnd(start, end - 1);
	poi2 = rnd(start, end - 1);
	temp = ind->gene[poi1];
	ind->gene[poi1] = ind->gene[poi2];
	ind->gene[poi2] = temp;
	return;
}

/* Routine for inter route swap mutation */
void ers(individual *ind) {
	int start1, end1;
	int start2, end2;
	int poi1, poi2, temp;
	int count, route1, route2;
	route1 = rnd(1, n_routes);
	start1 = 0; count = 1;
	while (count < route1) {
		if (ind->gene[start1] == -1) {
			count++;
		}
		start1++;
	}
	end1 = 0; count = 1;
	while (count < route1 + 1) {
		if (ind->gene[end1] == -1) {
			count++;
		}
		end1++;
	}
	route2 = rnd(1, n_routes);
	start2 = 0; count = 1;
	while (count < route2) {
		if (ind->gene[start2] == -1) {
			count++;
		}
		start2++;
	}
	end2 = 0; count = 1;
	while (count < route2 + 1) {
		if (ind->gene[end2] == -1) {
			count++;
		}
		end2++;
	}
	poi1 = rnd(start1, end1 - 1);
	poi2 = rnd(start2, end2 - 1);
	temp = ind->gene[poi1];
	ind->gene[poi1] = ind->gene[poi2];
	ind->gene[poi2] = temp;
	return;
}