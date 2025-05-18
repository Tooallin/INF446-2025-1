/* This file contains the variable and function declarations */

# ifndef _GLOBAL_H_
# define _GLOBAL_H_

# define INF 1.0e14
# define EPS 1.0e-14
# define E  2.71828182845905
# define PI 3.14159265358979
# define GNUPLOT_COMMAND "gnuplot -persist"

typedef struct {
	int rank;
	double constr_violation;
	int *gene;
	double *obj;
	double *constr;
	double crowd_dist;
} individual;

typedef struct {
	individual *ind;
} population;

typedef struct lists {
	int index;
	struct lists *parent;
	struct lists *child;
} list;

typedef struct {
	int id;
	int name;
	int *e;
	int SCORE;
	int OT;
	int TT;
	int CT;
} POI;

typedef struct {
	POI param_o;
	POI param_s;
	int param_TM;
	int nPOI;
	POI *set_POI;
	int set_M;
	int set_Z;
	int *param_E;
	double **param_t;
} problem_instance;

extern int gene_length;
extern int n_routes;
extern int nreal;
extern int nbin;
extern int nobj;
extern int ncon;
extern int popsize;
extern double pcross_real;
extern double pcross_bin;
extern double pmut_real;
extern double pmut_bin;
extern double eta_c;
extern double eta_m;
extern int ngen;
extern int nbinmut;
extern int nrealmut;
extern int nbincross;
extern int nrealcross;
extern int *nbits;
extern double *min_realvar;
extern double *max_realvar;
extern double *min_binvar;
extern double *max_binvar;
extern int bitlength;
extern int choice;
extern int obj1;
extern int obj2;
extern int obj3;
extern int angle1;
extern int angle2;

void allocate_memory_pop (population *pop, int size);
void allocate_memory_ind (individual *ind);
void deallocate_memory_pop (population *pop, int size);
void deallocate_memory_ind (individual *ind);

double maximum(double a, double b);
double minimum(double a, double b);

/* Functions from crossover.c */
void crossover(individual *parent1, individual *parent2, individual *child1, individual *child2);
void rbx(individual *parent1, individual *parent2, individual *child1, individual *child2);

/* Functions from mutation.c */
void mutation_pop(population *pop);
void mutation_ind(individual *ind);
void ars(individual *ind);
void ers(individual *ind);

/* Functions from reader.c */
int readInputFile(char* filePath, problem_instance *pi);

/* Functions from crowddist.c */
void assign_crowding_distance_list (population *pop, list *lst, int front_size);
void assign_crowding_distance_indices (population *pop, int c1, int c2);
void assign_crowding_distance (population *pop, int *dist, int **obj_array, int front_size);

/* Functions from decode.c */
void decode_pop (population *pop);
void decode_ind (individual *ind);

void onthefly_display (population *pop, FILE *gp, int ii);

int check_dominance (individual *a, individual *b);

void evaluate_pop (population *pop);
void evaluate_ind (individual *ind);

void fill_nondominated_sort (population *mixed_pop, population *new_pop);
void crowding_fill (population *mixed_pop, population *new_pop, int count, int front_size, list *cur);

void initialize_pop(population *pop, problem_instance *pi);
void initialize_ind(individual *ind, problem_instance *pi);

void insert (list *node, int x);
list* del (list *node);

void merge(population *pop1, population *pop2, population *pop3);
void copy_ind (individual *ind1, individual *ind2);

void test_problem (double *xreal, double *xbin, int **gene, double *obj, double *constr);

void assign_rank_and_crowding_distance (population *new_pop);

void report_pop (population *pop, FILE *fpt);
void report_feasible (population *pop, FILE *fpt);
void report_ind (individual *ind, FILE *fpt);

void quicksort_front_obj(population *pop, int objcount, int obj_array[], int obj_array_size);
void q_sort_front_obj(population *pop, int objcount, int obj_array[], int left, int right);
void quicksort_dist(population *pop, int *dist, int front_size);
void q_sort_dist(population *pop, int *dist, int left, int right);

void selection (population *old_pop, population *new_pop);
individual* tournament (individual *ind1, individual *ind2);

int isAPOI(int name, problem_instance pi);
int getNodeId(int name, problem_instance pi);
void printProblemInstance(problem_instance *pi);

# endif
