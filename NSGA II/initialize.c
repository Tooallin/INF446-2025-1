/* Data initializtion routines */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "global.h"
# include "rand.h"

/* Function to initialize a population randomly */
void initialize_pop(population *pop, problem_instance *pi) {
	int i;
	for (i=0; i<popsize; i++) {
		initialize_ind(&(pop->ind[i]), pi);
	}
	return;
}

/* Function to initialize an individual randomly */
void initialize_ind(individual *ind, problem_instance *pi) {
	random_sequence(pi->nPOI, ind->gene);
	split_sequence(pi->nPOI, pi->set_M, ind->gene);
	return;
}