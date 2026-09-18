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
            if valor != 0: # Si es distinto de 0, hay conexión
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

def main():
    print("=== INGRESO DE DATOS DEL GRAFO ===")
    
    respDirigido = input("¿El grafo es dirigido? (s/n): ").strip().lower()
    esDirigido = True if respDirigido == 's' else False
    
    respPeso = input("¿El grafo es con peso? (s/n): ").strip().lower()
    conPeso = True if respPeso == 's' else False
    
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
                        filaProcesada.append(float(x))
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

    print("\n=== DATOS CAPTURADOS CORRECTAMENTE ===")
    print(f"Tipo de grafo: {'Dirigido' if esDirigido else 'No dirigido'}")
    print(f"Pesos: {'Con peso' if conPeso else 'Sin peso'}")
    print("Matriz ingresada:")
    for fila in matrizAdyacencia:
        print(fila)
        
    mostrarRepresentacionMatematica(n, matrizAdyacencia, esDirigido, conPeso)

if __name__ == "__main__":
    main()