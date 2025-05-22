/* Crossover routines */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "global.h"
# include "rand.h"

/* Function to cross two individuals */
void crossover(individual *parent1, individual *parent2, individual *child1, individual *child2) {
	rbx(parent1, parent2, child1, child2);
	return;
}

/* Routine for route based crossover */
void rbx(individual *parent1, individual *parent2, individual *child1, individual *child2) {
	int used1[1000] = {0};
	int used2[1000] = {0};
	int i, j, route, count;
	route = rnd(1, n_routes);

	/* RBX for first child */
	count = 1;
	j = 0;
	for (i = 0; i < gene_length; i++) {
		if (parent1->gene[i] == -1) {
			count++;
			continue;
		}
		if (count == route) {
			used1[parent1->gene[i]] = 1;
			child1->gene[j++] = parent1->gene[i];
		} 
	}
	child1->gene[j++] = -1;
	count = 1;
	for (i = 0; i < gene_length; i++) {
		if (parent2->gene[i] == -1) {
			if (count != route) {
				child1->gene[j++] = -1;
			}
			count++;
			continue;
		}
		if (count != route && used1[parent2->gene[i]] != 1) {
			used1[parent2->gene[i]] = 1;
			child1->gene[j++] = parent2->gene[i];
		}
	}
	count = 1;
	for (i = 0; i < gene_length; i++) {
		if (parent2->gene[i] == -1) {
			count++;
			continue;
		}
		if (count == route && used1[parent2->gene[i]] != 1) {
			used1[parent2->gene[i]] = 1;
			child1->gene[j++] = parent2->gene[i];
		}
	}

	/* RBX for second child */
	count = 1;
	j = 0;
	for (i = 0; i < gene_length; i++) {
		if (parent2->gene[i] == -1) {
			count++;
			continue;
		}
		if (count == route) {
			used2[parent2->gene[i]] = 1;
			child2->gene[j++] = parent2->gene[i];
		} 
	}
	child2->gene[j++] = -1;
	count = 1;
	for (i = 0; i < gene_length; i++) {
		if (parent1->gene[i] == -1) {
			if (count != route) {
				child2->gene[j++] = -1;
			}
			count++;
			continue;
		}
		if (count != route && used2[parent1->gene[i]] != 1) {
			used2[parent1->gene[i]] = 1;
			child2->gene[j++] = parent1->gene[i];
		}
	}
	count = 1;
	for (i = 0; i < gene_length; i++) {
		if (parent1->gene[i] == -1) {
			count++;
			continue;
		}
		if (count == route && used2[parent1->gene[i]] != 1) {
			used2[parent1->gene[i]] = 1;
			child2->gene[j++] = parent1->gene[i];
		}
	}

	return;
}

/* Routine for order crossover */
void ox(individual *parent1, individual *parent2, individual *child1, individual *child2) {
	return;
}