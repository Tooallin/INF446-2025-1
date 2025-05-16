/* Conjuntos */
param o; set O := {o}; # nodo inicial
param s; set S := {s}; # nodo final
set POI;               # conjunto de POIs

set N := O union POI union S;      # conjunto de nodos
set A := {i in N, j in N: i != j}; # conjunto de arcos
set M;                             # conjunto de rutas
set Z;                             # conjunto de categorias

/* Parametros */
param e{N,Z};            # valor del nodo para cada categoria
param SCORE{N};          # score por visitar el nodo
param OT{N};             # tiempo de apertura del nodo
param TT{N};             # tiempo de atencion del nodo
param CT{N};             # tiempo de cierre del nodo
param t{A};              # tiempo de desplazarse por un arco
param BIG default 10000; # numero muy grande
set objetivos := {1}; # conjunto de objetivos del problema

/* Variables */
var x{A,M} binary;        # 1 si el nodo j es visitado despues del nodo i en la ruta m
var y{N,M} binary;        # 1 si el nodo i es visitado en la ruta m
var tt{N,M};              # tiempo en el que comienza la visita al nodo i en la ruta m
var P{M} integer;         # puntaje del tour m
var E{Z} integer;         # cuota para la categoria z
var EE{M,Z} integer;      # cuota para la categoria z en la ruta m
var TM integer default 0; # tiempo maximo para las rutas
var F{objetivos} >= 0;    # funciones objetivo del problema

/* Funcion Objetivo */
maximize FO1 : F[1];

/* Restricciones */
subject to

/* Objetivos */
O1 : F[1] = sum {m in M, i in N} SCORE[i] * y[i,m]; # Maximizar el puntaje sumado entre todos los tours

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

/* Visitar un POI dentro de su ventana de tiempo */
R5 {i in N, m in M} : OT[i] <= tt[i,m] <= CT[i];

/* Fijar el puntaje del tour */
R6 {m in M} : P[m] = sum {i in N} SCORE[i] * y[i,m];

/* Fijar la categoria acumulada del tour */
R7 {m in M, z in Z} : EE[m,z] = sum {i in N} e[i,z] * y[i,m];

/* Fijar la categoria acumulada de la instancia */
R8 {z in Z} : E[z] = sum {i in N, m in M} e[i,z] * y[i,m];

/* Fijar el tiempo maximo del tour */
R9 {m in M} : TM >= tt[s,m];