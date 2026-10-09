# Laboratorio-grafo-optimizacion (Parte 2)
Permite crear grafos (dirigidos o no, con o sin peso) a partir de una matriz de adyacencia
y encontrar la ruta más corta entre dos nodos con Dijkstra y Bellman-Ford.

## Funciones
- Validación de la matriz (tamaño, valores, simetría, nan/inf).
- Representación matemática y gráfica del grafo.
- Nodos adyacentes, caminos y ciclos.
- Ruta más corta con su costo total, resaltada en el grafo.
- Comparación de eficiencia: Bellman-Ford (matriz), Dijkstra (lista y min) y Dijkstra (heap).

## Uso
    pip install -r requirements.txt
    python mainGrafoPart2.py     # versión de consola
    python interfazGrafo.py      # versión con interfaz gráfica

Nota: el valor 0 en la matriz significa "sin arista", por lo que no se pueden usar aristas de peso 0.
