# INF446-2025-1
Proyecto para el curso INF446 (Algoritmos Multiobjetivo), implementacion del problema MCTOPTW en AMPL y NSGA II.

## Estructura repositorio
+ 📁 Modelo e Instancias MCTOPTW: Implementacion del problema MCTOPTW en AMPL, junto a instancias para el MCTOPTW junto a su version original para el TOPTW en formato .DAT, `convert_to_mctoptw.py` es el Script de Python que modifica las instancias originalmente para ser llevadas al MCTOPTW.
+ 📁 Modelo e Instancias TOPTW: Implementacion del problema TOPTW en AMPL, junto a instancias para el TOPTW en formato .CSV y .DAT, `convert_to_dat.py` es el Script de Python que lee las instancias en formato .CSV para ser llevadas al formato .DAT.
+ 📁 Modelo e Instancias NSGA II: Implementacion del algoritmo evolutivo NSGA II en C, modificado para resolver el MCTOPTW.