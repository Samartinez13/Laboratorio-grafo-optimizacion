from collections import deque
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
            if valor != 0:  # Si es distinto de 0, hay conexión
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
    """
    En un grafo NO dirigido, la matriz de adyacencia debe ser
    simétrica: matriz[i][j] debe ser igual a matriz[j][i].
    Devuelve (True, None) si es válida, o (False, (i, j)) si
    encuentra una inconsistencia.
    """
    for i in range(n):
        for j in range(n):
            if matriz[i][j] != matriz[j][i]:
                return False, (i, j)
    return True, None


def avisarSiHayLazos(n, matriz):
    lazos = [f"v{i+1}" for i in range(n) if matriz[i][i] != 0]
    if lazos:
        print(f"Aviso: se detectaron lazos (auto-conexiones) en: {', '.join(lazos)}")

def mostrarRepresentacionGrafica(n, matriz, esDirigido, conPeso):
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

    # El parámetro "arrowsize" solo aplica cuando el grafo es dirigido,
    # por eso se agrega únicamente en ese caso (evita un warning de networkx).
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

    plt.title("Representación Gráfica del Grafo")
    plt.show()

def obtenerNodosAdyacentes(nodo, n, matriz, esDirigido):
    adyacentesSalida = [f"v{j+1}" for j in range(n) if matriz[nodo][j] != 0]

    if esDirigido:
        adyacentesEntrada = [f"v{i+1}" for i in range(n) if matriz[i][nodo] != 0]
        return adyacentesSalida, adyacentesEntrada

    return adyacentesSalida, None

def encontrarCamino(origen, destino, n, matriz):
    visitados = [False] * n
    padres = [-1] * n
    cola = deque([origen])
    visitados[origen] = True

    while cola:
        actual = cola.popleft()
        if actual == destino:
            break
        for vecino in range(n):
            if matriz[actual][vecino] != 0 and not visitados[vecino]:
                visitados[vecino] = True
                padres[vecino] = actual
                cola.append(vecino)

    if not visitados[destino]:
        return None

    camino = []
    nodo = destino
    while nodo != -1:
        camino.append(nodo)
        nodo = padres[nodo]
    camino.reverse()
    return camino

def detectarCicloDirigido(n, matriz):
    colores = [0] * n  # 0 = blanco, 1 = gris (en proceso), 2 = negro (terminado)
    padre = [-1] * n

    def dfs(u):
        colores[u] = 1
        for v in range(n):
            if matriz[u][v] != 0:
                if colores[v] == 1:
                    # Se encontró un ciclo: reconstruirlo desde u hasta v
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
                    continue  # No contar la arista de regreso al padre
                if visitados[v]:
                    # Se encontró un ciclo: reconstruirlo desde u hasta v
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


def menuConceptos(n, matriz, esDirigido):
    while True:
        print("\n=== EVIDENCIA DE CONCEPTOS ===")
        print("1. Ver nodos adyacentes de un nodo")
        print("2. Buscar un camino entre dos nodos")
        print("3. Detectar un ciclo en el grafo")
        print("4. Salir")
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
            camino = encontrarCamino(origen, destino, n, matriz)

            if camino:
                caminoTexto = " -> ".join([f"v{nodo+1}" for nodo in camino])
                print(f"\nCamino encontrado: {caminoTexto}")
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
            print("Fin del programa. ¡Hasta luego!")
            break

        else:
            print("Opción inválida, intente nuevamente.")


def pedirRespuestaSiNo(mensaje):
    """
    Pide una respuesta al usuario y no continúa hasta que sea
    's' (sí) o 'n' (no). Devuelve True si respondió 's'.
    """
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

    # Se repite todo el ingreso de la matriz hasta que pase las validaciones
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
                            numero = float(x)
                            if numero < 0:
                                print(f"Error: '{x}' no puede ser negativo.")
                                filaValida = False
                                break
                            filaProcesada.append(numero)
                        except ValueError:
                            print(f"Error: '{x}' no es un número válido.")
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

        # Validación: si el grafo NO es dirigido, la matriz debe ser simétrica
        if not esDirigido:
            esValida, posicion = validarMatrizSimetrica(n, matrizAdyacencia)
            if not esValida:
                i, j = posicion
                print(f"\nError: la matriz no es simétrica en la posición [{i+1}][{j+1}]"
                      f" ({matrizAdyacencia[i][j]} != {matrizAdyacencia[j][i]}).")
                print("En un grafo NO dirigido, la matriz de adyacencia debe ser simétrica.")
                print("Vuelva a ingresar la matriz completa.\n")
                continue  # Vuelve a pedir toda la matriz

        break  # La matriz es válida, se continúa con el programa

    print("\n=== DATOS CAPTURADOS CORRECTAMENTE ===")
    print(f"Tipo de grafo: {'Dirigido' if esDirigido else 'No dirigido'}")
    print(f"Pesos: {'Con peso' if conPeso else 'Sin peso'}")
    print("Matriz ingresada:")
    for fila in matrizAdyacencia:
        print(fila)

    avisarSiHayLazos(n, matrizAdyacencia)

    mostrarRepresentacionMatematica(n, matrizAdyacencia, esDirigido, conPeso)
    mostrarRepresentacionGrafica(n, matrizAdyacencia, esDirigido, conPeso)
    menuConceptos(n, matrizAdyacencia, esDirigido)


if __name__ == "__main__":
    main()