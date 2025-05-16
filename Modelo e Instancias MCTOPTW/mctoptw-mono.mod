/* Conjuntos */
param o; set O := {o}; # nodo inicial
param s; set S := {s}; # nodo final
set POI;               # conjunto de POIs

set N := O union POI union S;                    # conjunto de nodos
set A := {i in N, j in N: i != j};               # conjunto de arcos
set M;                                           # conjunto de rutas
set Z;                                           # conjunto de categorias

/* Parametros */
param TM;                # tiempo maximo de las rutas
param E{Z};              # cuota maxima por categoria de nodo
param e{N,Z};            # valor del nodo para cada categoria
param SCORE{N};          # score por visitar el nodo
param OT{N};             # tiempo de apertura del nodo
param TT{N};             # tiempo de atencion del nodo
param CT{N};             # tiempo de cierre del nodo
param t{A};              # tiempo de desplazarse por un arco
param BIG default 10000; # numero muy grande
set objetivos := {1..3}; # conjunto de objetivos del problema

/* Variables */
var x{A,M} binary;     # 1 si el nodo j es visitado despues del nodo i en la ruta m
var y{N,M} binary;     # 1 si el nodo i es visitado en la ruta m
var u{M,Z} binary;     # 1 si la ruta m visita al menos un nodo de la categoria z
var tt{N,M} integer;   # tiempo en el que comienza la visita al nodo i en la ruta m
var P{M} integer;      # puntaje del tour m
var P_max integer;     # mayor puntaje encontrado
var P_min integer;     # menor puntaje encontrado
var F{objetivos} >= 0; # funciones objetivo del problema

/* Funcion Objetivo */
maximize FO1 : F[1];
#minimize FO1 : F[2];
#maximize FO1 : F[3];

/* Restricciones */
subject to

/* Objetivos */
O1 : F[1] = sum {m in M, i in N} SCORE[i] * y[i,m]; # Maximizar el puntaje sumado entre todos los tours
O2 : F[2] = P_max - P_min;                          # Minimizar la diferencia de puntaje entre el tour con mayor puntaje y el de menor puntaje
O3 : F[3] = sum {m in M, z in Z} u[m,z];            # Maximizar el numero de categorias distintas visitadas en los distintos tours

/* Tours comenzando en el primer nodo y terminando en el ultimo */
R1a : sum {(i,j) in A, m in M: i = o and i != j} x[i,j,m] = card(M);
R1b : sum {(i,j) in A, m in M: i != j and j = s} x[i,j,m] = card(M);

/* Conectividad de los tours */
R2a {k in POI, m in M} : sum {i in N: i != s and i != k} x[i,k,m] = y[k,m];
R2b {k in POI, m in M} : sum {j in N: j != o and j != k} x[k,j,m] = y[k,m];

/* No permitir que hayan tiempos de espera */
R3 {(i,j) in A, m in M} : x[i,j,m] = 1 ==> tt[j,m] = tt[i,m] + TT[i] + t[i,j];

/* Asegurarse que un nodo es visitado solo una vez */
R4 {i in POI} : sum {m in M} y[i,m] <= 1;

/* No superar la cuota maxima por categoria */
R5 {z in Z} : sum {m in M, i in N} e[i,z] * y[i,m] <= E[z];

/* Visitar un POI dentro de su ventana de tiempo */
R6 {i in N, m in M} : OT[i] <= tt[i,m] <= CT[i];

/* Respetar la duracion maxima para las rutas */
R7 {m in M} : sum {i in N: i != s} ( TT[i] * y[i,m] + sum {j in N: j != o and j != i} t[i,j] * x[i,j,m] ) <= TM;

/* Forzar el valor de las variables u[m,z] */
R8a {m in M, z in Z} : u[m,z] <= sum {i in N} e[i,z] * y[i,m];
R8b {m in M, z in Z} : BIG * u[m,z] >= sum {i in N} e[i,z] * y[i,m];

/* Fijar el puntaje del tour */
R9 {m in M} : P[m] = sum {i in N} SCORE[i] * y[i,m];

/* Fijar el puntaje maximo encontrado */
R10 {m in M} : P_max >= P[m];

/* Fijar el puntaje minimo encontrado */
R11 {m in M} : P_min <= P[m];

/* No permitir que el tour se termine de inmediato */
R12 {m in M} : x[o,s,m] != 1;