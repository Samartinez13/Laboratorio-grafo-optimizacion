import math
import time
import heapq
import networkx as nx
import matplotlib.pyplot as plt

def mostrarRepresentacionMatematica(n, matriz, esDirigido, conPeso):
    print("\n=== REPRESENTACIÓN MATEMÁTICA DEL GRAFO ===")
    # Conjunto de Vértices
    V = [f"v{i+1}" for i in range(n)]
    print(f"V = {{ {', '.join(V)} }}")
    E = []
    for i in range(n):
        inicioJ = 0 if esDirigido else i
        for j in range(inicioJ, n):
            valor = matriz[i][j]
            if valor != 0:  
                if conPeso:
                    if esDirigido:
                        E.append(f"(v{i+1}, v{j+1}, {valor})")
                    else:
                        E.append(f"{{v{i+1}, v{j+1}, {valor}}}")
                else:
                    if esDirigido:
                        E.append(f"(v{i+1}, v{j+1})")
                    else:
                        E.append(f"{{v{i+1}, v{j+1}}}")

    print(f"E = {{ {', '.join(E)} }}")
    print("G = (V, E)")
def validarMatrizSimetrica(n, matriz):
    for i in range(n):
        for j in range(n):
            if matriz[i][j] != matriz[j][i]:
                return False, (i, j)
    return True, None
def avisarSiHayLazos(n, matriz):
    lazos = [f"v{i+1}" for i in range(n) if matriz[i][i] != 0]
    if lazos:
        print(f"Aviso: se detectaron lazos (auto-conexiones) en: {', '.join(lazos)}")
def mostrarRepresentacionGrafica(n, matriz, esDirigido, conPeso, caminoResaltar=None):
    print("\nGenerando representación gráfica... (se abrirá una ventana con el dibujo)")

    grafo = nx.DiGraph() if esDirigido else nx.Graph()
    for i in range(n):
        grafo.add_node(f"v{i+1}")

    for i in range(n):
        rango = range(n) if esDirigido else range(i, n)
        for j in rango:
            valor = matriz[i][j]
            if valor != 0:
                if conPeso:
                    grafo.add_edge(f"v{i+1}", f"v{j+1}", weight=valor)
                else:
                    grafo.add_edge(f"v{i+1}", f"v{j+1}")

    posiciones = nx.spring_layout(grafo, seed=42)
    plt.figure(figsize=(7, 6))

    argumentosDibujo = {
        "with_labels": True,
        "node_color": "skyblue",
        "node_size": 1500,
        "font_size": 12,
        "font_weight": "bold",
    }
    if esDirigido:
        argumentosDibujo["arrows"] = True
        argumentosDibujo["arrowsize"] = 20
    nx.draw(grafo, posiciones, **argumentosDibujo)
    if conPeso:
        etiquetasPeso = nx.get_edge_attributes(grafo, "weight")
        nx.draw_networkx_edge_labels(grafo, posiciones, edge_labels=etiquetasPeso)
    if caminoResaltar:
        nodosCamino = [f"v{indice+1}" for indice in caminoResaltar]
        aristasCamino = [
            (nodosCamino[i], nodosCamino[i + 1])
            for i in range(len(nodosCamino) - 1)
        ]

        nx.draw_networkx_nodes(
            grafo, posiciones, nodelist=nodosCamino,
            node_color="orange", node_size=1500
        )
        nx.draw_networkx_edges(
            grafo, posiciones, edgelist=aristasCamino,
            edge_color="red", width=3
        )
    plt.title("Representación Gráfica del Grafo")
    plt.show()

def obtenerNodosAdyacentes(nodo, n, matriz, esDirigido):
    adyacentesSalida = [f"v{j+1}" for j in range(n) if matriz[nodo][j] != 0]

    if esDirigido:
        adyacentesEntrada = [f"v{i+1}" for i in range(n) if matriz[i][nodo] != 0]
        return adyacentesSalida, adyacentesEntrada
    return adyacentesSalida, None

def encontrarCaminoBellman(origen, destino, n, matriz):  # Bellman-Ford
    costo = [float('inf')] * n
    costo[origen] = 0
    predecesor = [-1] * n
    for _ in range(n - 1):          
        for i in range(n):          
            for j in range(n):      
                if matriz[i][j] != 0:
                    pesoArista = matriz[i][j]
                    if costo[i] != float('inf') and (costo[i] + pesoArista) < costo[j]:
                        costo[j] = costo[i] + pesoArista
                        predecesor[j] = i
    for i in range(n):
        for j in range(n):
            if matriz[i][j] != 0:
                pesoArista = matriz[i][j]
                if costo[i] != float('inf') and (costo[i] + pesoArista) < costo[j]:
                    print("Aviso: se detectó un ciclo de peso negativo. "
                          "El camino más corto no está definido.")
                    return None

    if costo[destino] == float('inf'):
        return None
    camino = []
    actual = destino
    while True:
        camino.append(actual)
        if actual == origen:
            break
        actual = predecesor[actual]
    camino.reverse()
    return camino

def encontrarCaminoDijkstra(origen, destino, n, matriz):

    distancia=[float('inf')] * n
    distancia[origen]=0
    nodoAnterior= [-1] * n
    colaPrioridad= list(range(n))

    while colaPrioridad:
        nodoMenorDistancia=min(colaPrioridad, key=lambda v: distancia[v])
        colaPrioridad.remove(nodoMenorDistancia)
        if distancia[nodoMenorDistancia]==float("inf") or nodoMenorDistancia==destino:
            break
        for j in range(n):
            if matriz[nodoMenorDistancia][j]!=0 and j in colaPrioridad:
                nuevaDist=distancia[nodoMenorDistancia]+matriz[nodoMenorDistancia][j]
                if nuevaDist<distancia[j]:
                    distancia[j]=nuevaDist
                    nodoAnterior[j]=nodoMenorDistancia

    if distancia[destino] == float('inf'):
        return None
    camino=[]
    actual=destino
    while True:
        camino.append(actual)
        if actual==origen:
            break
        actual=nodoAnterior[actual]
    camino.reverse()
    return camino

def construirListaAdyacencia(n, matriz):
    listaAdyacencia = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if matriz[i][j] != 0:
                listaAdyacencia[i].append((j, matriz[i][j]))
    return listaAdyacencia

def encontrarCaminoDijkstraHeap(origen, destino, n, matriz):
    # Dijkstra con lista de adyacencia y cola de prioridad (heapq)
    listaAdyacencia = construirListaAdyacencia(n, matriz)
    distancia = [float('inf')] * n
    distancia[origen] = 0
    nodoAnterior = [-1] * n
    colaPrioridad = [(0, origen)]

    while colaPrioridad:
        distanciaActual, nodoActual = heapq.heappop(colaPrioridad)
        if distanciaActual > distancia[nodoActual]:
            continue
        if nodoActual == destino:
            break
        for vecino, peso in listaAdyacencia[nodoActual]:
            nuevaDist = distanciaActual + peso
            if nuevaDist < distancia[vecino]:
                distancia[vecino] = nuevaDist
                nodoAnterior[vecino] = nodoActual
                heapq.heappush(colaPrioridad, (nuevaDist, vecino))

    if distancia[destino] == float('inf'):
        return None
    camino = []
    actual = destino
    while True:
        camino.append(actual)
        if actual == origen:
            break
        actual = nodoAnterior[actual]
    camino.reverse()
    return camino

def calcularCostoCamino(camino, matriz):
    costoTotal = 0
    for i in range(len(camino) - 1):
        costoTotal += matriz[camino[i]][camino[i + 1]]
    return costoTotal

def mostrarResultadoCamino(camino, matriz):
    caminoTexto = " -> ".join([f"v{nodo+1}" for nodo in camino])
    costoTotal = calcularCostoCamino(camino, matriz)
    print(f"\nCamino encontrado: {caminoTexto}")
    print(f"Costo total del camino: {costoTotal}")

def compararEficiencia(origen, destino, n, matriz, repeticiones=1000):
    print(f"\n=== COMPARACIÓN DE EFICIENCIA ({repeticiones} repeticiones) ===")
    algoritmos = [("Bellman-Ford (matriz)", encontrarCaminoBellman)]

    if tienePesosNegativos(n, matriz):
        print("Aviso: hay pesos negativos, Dijkstra no se puede aplicar.")
    else:
        algoritmos.append(("Dijkstra (lista y min)", encontrarCaminoDijkstra))
        algoritmos.append(("Dijkstra (heap)", encontrarCaminoDijkstraHeap))

    for nombre, funcion in algoritmos:
        inicio = time.perf_counter()
        for _ in range(repeticiones):
            camino = funcion(origen, destino, n, matriz)
        fin = time.perf_counter()
        tiempoTotal = fin - inicio
        tiempoPromedio = tiempoTotal / repeticiones * 1000
        if camino:
            costo = calcularCostoCamino(camino, matriz)
        else:
            costo = "sin camino"
        print(f"{nombre}: {tiempoPromedio:.5f} ms por ejecución | costo = {costo}")

    print("\nComplejidad teórica:")
    print(" - Bellman-Ford con matriz: O(V^3)")
    print(" - Dijkstra con lista y min(): O(V^2)")
    print(" - Dijkstra con heap y lista de adyacencia: O((V + E) log V)")

def convertirAPeso(texto):
    numero = float(texto)
    if math.isnan(numero) or math.isinf(numero):
        raise ValueError
    return numero

def pedirAlgoritmo():
    while True:
        opn = input("Que algoritmo desea utilizar para resolver el camino\n(1)Bellman-Ford\n(2)Dijkstra\n").strip()
        if opn in ['1', '2']:
            return opn
        print("Error: elija 1 o 2.")

def detectarCicloDirigido(n, matriz):
    colores = [0] * n  
    padre = [-1] * n

    def dfs(u):
        colores[u] = 1
        for v in range(n):
            if matriz[u][v] != 0:
                if colores[v] == 1:
                    # Se encontró un ciclo
                    ciclo = [v]
                    actual = u
                    while actual != v:
                        ciclo.append(actual)
                        actual = padre[actual]
                    ciclo.append(v)
                    ciclo.reverse()
                    return ciclo
                if colores[v] == 0:
                    padre[v] = u
                    resultado = dfs(v)
                    if resultado:
                        return resultado
        colores[u] = 2
        return None
    for nodoInicio in range(n):
        if colores[nodoInicio] == 0:
            resultado = dfs(nodoInicio)
            if resultado:
                return resultado
    return None
def detectarCicloNoDirigido(n, matriz):
    visitados = [False] * n
    padres = [-1] * n

    def dfs(u, padre):
        visitados[u] = True
        padres[u] = padre
        for v in range(n):
            if matriz[u][v] != 0:
                if v == padre:
                    continue  
                if visitados[v]:
                    ciclo = [v]
                    actual = u
                    while actual != v and actual != -1:
                        ciclo.append(actual)
                        actual = padres[actual]
                    ciclo.append(v)
                    ciclo.reverse()
                    return ciclo
                resultado = dfs(v, u)
                if resultado:
                    return resultado
        return None
    for nodoInicio in range(n):
        if not visitados[nodoInicio]:
            resultado = dfs(nodoInicio, -1)
            if resultado:
                return resultado
    return None
def pedirNodoValido(n, tipo=""):
    while True:
        try:
            if tipo:
                texto = f"Ingrese el nodo {tipo} (1 a {n}): "
            else:
                texto = f"Ingrese el número de nodo (1 a {n}): "
            nodo = int(input(texto))
            if 1 <= nodo <= n:
                return nodo - 1
            print(f"Error: el nodo debe estar entre 1 y {n}.")
        except ValueError:
            print("Error: ingrese un número entero válido.")

def tienePesosNegativos(n,matriz):
    for i in range(n):
        for j in range(n):
            if matriz[i][j] < 0:
                return True
    return False
def menuConceptos(n, matriz, esDirigido, conPeso):
    while True:
        print("\n=== EVIDENCIA DE CONCEPTOS ===")
        print("1. Ver nodos adyacentes de un nodo")
        print("2. Buscar un camino entre dos nodos")
        print("3. Detectar un ciclo en el grafo")
        print("4. Comparar eficiencia de los algoritmos")
        print("5. Salir")
        opcion = input("Elija una opción: ").strip()
        
        if opcion == '1':
            nodo = pedirNodoValido(n)
            adySalida, adyEntrada = obtenerNodosAdyacentes(nodo, n, matriz, esDirigido)

            print(f"\nNodos adyacentes de v{nodo+1}:")
            if esDirigido:
                textoSalida = ', '.join(adySalida) if adySalida else "Ninguno"
                textoEntrada = ', '.join(adyEntrada) if adyEntrada else "Ninguno"
                print(f" - Adyacentes de salida (v{nodo+1} -> x): {textoSalida}")
                print(f" - Adyacentes de entrada (x -> v{nodo+1}): {textoEntrada}")
            else:
                textoAdy = ', '.join(adySalida) if adySalida else "Ninguno"
                print(f" - Nodos adyacentes: {textoAdy}")

        elif opcion == '2':
            origen = pedirNodoValido(n, "de origen")
            destino = pedirNodoValido(n, "de destino")
            opn = pedirAlgoritmo()
            if opn == '1':
                camino = encontrarCaminoBellman(origen, destino, n, matriz)
            else:
                if tienePesosNegativos(n, matriz):
                    print("Su matriz tiene pesos negativos, se resolvera con Bellman-Ford")
                    camino = encontrarCaminoBellman(origen, destino, n, matriz)
                else:
                    camino = encontrarCaminoDijkstra(origen, destino, n, matriz)

            if camino:
                mostrarResultadoCamino(camino, matriz)
                if pedirRespuestaSiNo("¿Desea ver el camino resaltado en el grafo? (s/n): "):
                    mostrarRepresentacionGrafica(n, matriz, esDirigido, conPeso, caminoResaltar=camino)
            else:
                print(f"\nNo existe un camino entre v{origen+1} y v{destino+1}.")
        elif opcion == '3':
            if esDirigido:
                ciclo = detectarCicloDirigido(n, matriz)
            else:
                ciclo = detectarCicloNoDirigido(n, matriz)
            if ciclo:
                esLazo = len(ciclo) == 2 and ciclo[0] == ciclo[1]
                if esLazo:
                    print(f"\nSe encontró un ciclo: es un lazo en v{ciclo[0]+1} (v{ciclo[0]+1} -> v{ciclo[0]+1}).")
                else:
                    cicloTexto = " -> ".join([f"v{nodo+1}" for nodo in ciclo])
                    print(f"\nSe encontró un ciclo: {cicloTexto}")
                print("(Nota: se muestra un solo ejemplo de ciclo; el grafo puede tener más de uno.)")
            else:
                print("\nNo se encontró ningún ciclo en el grafo.")

        elif opcion == '4':
            origen = pedirNodoValido(n, "de origen")
            destino = pedirNodoValido(n, "de destino")
            compararEficiencia(origen, destino, n, matriz)

        elif opcion == '5':
            print("Fin del programa. ¡Hasta luego!")
            break

        else:
            print("Opción inválida, intente nuevamente.")
def pedirRespuestaSiNo(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ['s', 'n']:
            return respuesta == 's'
        print("Error: responda solamente con 's' (sí) o 'n' (no).")
def main():
    print("=== INGRESO DE DATOS DEL GRAFO ===")

    esDirigido = pedirRespuestaSiNo("¿El grafo es dirigido? (s/n): ")
    conPeso = pedirRespuestaSiNo("¿El grafo es con peso? (s/n): ")

    while True:
        try:
            n = int(input("\nIngrese el número de nodos (tamaño de la matriz NxN): "))
            if n > 0:
                break
            print("Error: El número de nodos debe ser mayor a 0.")
        except ValueError:
            print("Error: Por favor, ingrese un número entero válido.")
    print(f"\nIngrese la matriz de adyacencia ({n} filas de {n} valores).")
    if conPeso:
        print("Separe los números con espacios (ejemplo: 0 1.5 5 0):")
    else:
        print("Al ser sin peso, ingrese solo 0, 1 o T (ejemplo: 0 1 T 0):")
    while True:
        matrizAdyacencia = []
        for i in range(n):
            while True:
                filaInput = input(f"Fila {i + 1}: ").strip()
                valores = filaInput.split()
                if len(valores) != n:
                    print(f"Error: Debe ingresar exactamente {n} valores. Ha ingresado {len(valores)}.")
                    continue
                filaProcesada = []
                filaValida = True
                for x in valores:
                    if conPeso:
                        try:
                            numero = convertirAPeso(x)
                            filaProcesada.append(numero)
                        except ValueError:
                            print(f"Error: '{x}' no es un número válido (no se permite nan ni inf).")
                            filaValida = False
                            break
                    else:
                        if x.upper() in ['0', '1', 'T']:
                            valor = 1 if x.upper() in ['1', 'T'] else 0
                            filaProcesada.append(valor)
                        else:
                            print(f"Error: '{x}' no es válido. Para grafos sin peso ingrese solo 0, 1 o T.")
                            filaValida = False
                            break
                if filaValida:
                    matrizAdyacencia.append(filaProcesada)
                    break
        if not esDirigido:
            esValida, posicion = validarMatrizSimetrica(n, matrizAdyacencia)
            if not esValida:
                i, j = posicion
                print(f"\nError: la matriz no es simétrica en la posición [{i+1}][{j+1}]"
                      f" ({matrizAdyacencia[i][j]} != {matrizAdyacencia[j][i]}).")
                print("En un grafo NO dirigido, la matriz de adyacencia debe ser simétrica.")
                print("Vuelva a ingresar la matriz completa.\n")
                continue  # Vuelve a pedir toda la matriz

        break  
    print("\n=== DATOS CAPTURADOS CORRECTAMENTE ===")
    print(f"Tipo de grafo: {'Dirigido' if esDirigido else 'No dirigido'}")
    print(f"Pesos: {'Con peso' if conPeso else 'Sin peso'}")
    print("Matriz ingresada:")
    for fila in matrizAdyacencia:
        print(fila)
    avisarSiHayLazos(n, matrizAdyacencia)
    mostrarRepresentacionMatematica(n, matrizAdyacencia, esDirigido, conPeso)
    mostrarRepresentacionGrafica(n, matrizAdyacencia, esDirigido, conPeso)
    menuConceptos(n, matrizAdyacencia, esDirigido, conPeso)

if __name__ == "__main__":
    main()