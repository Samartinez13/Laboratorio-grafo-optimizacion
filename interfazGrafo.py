import io
import contextlib
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

from mainGrafoPart2 import (
    mostrarRepresentacionMatematica,
    validarMatrizSimetrica,
    avisarSiHayLazos,
    mostrarRepresentacionGrafica,
    obtenerNodosAdyacentes,
    encontrarCaminoBellman,
    encontrarCaminoDijkstra,
    encontrarCaminoDijkstraHeap,
    calcularCostoCamino,
    compararEficiencia,
    convertirAPeso,
    tienePesosNegativos,
    detectarCicloDirigido,
    detectarCicloNoDirigido,
)
class AppGrafo:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Interfaz de Grafos")

        self.n = 0
        self.matrizEntradas = []
        self.matrizActual = None

        self.esDirigido = tk.BooleanVar()
        self.conPeso = tk.BooleanVar()
        self.algoritmo = tk.StringVar(value="dijkstra")

        self.crearInterfazInicial()

    def crearInterfazInicial(self):
        frameConfig = tk.Frame(self.ventana, padx=10, pady=10)
        frameConfig.pack(fill="x")

        tk.Checkbutton(frameConfig, text="¿Grafo dirigido?", variable=self.esDirigido).grid(
            row=0, column=0, sticky="w")
        tk.Checkbutton(frameConfig, text="¿Grafo con peso?", variable=self.conPeso).grid(
            row=1, column=0, sticky="w")
        tk.Label(frameConfig, text="Algoritmo de camino:").grid(row=0, column=2, padx=(20, 0), sticky="w")
        tk.Radiobutton(frameConfig, text="Dijkstra", variable=self.algoritmo,
                       value="dijkstra").grid(row=1, column=2, padx=(20, 0), sticky="w")
        tk.Radiobutton(frameConfig, text="Dijkstra (heap)", variable=self.algoritmo,
                       value="dijkstraHeap").grid(row=2, column=2, padx=(20, 0), sticky="w")
        tk.Radiobutton(frameConfig, text="Bellman-Ford", variable=self.algoritmo,
                       value="bellman").grid(row=3, column=2, padx=(20, 0), sticky="w")

        tk.Label(frameConfig, text="Número de nodos:").grid(row=2, column=0, sticky="w")
        self.entradaN = tk.Entry(frameConfig, width=5)
        self.entradaN.grid(row=2, column=1, sticky="w")

        tk.Button(frameConfig, text="Generar matriz", command=self.generarMatriz).grid(
            row=3, column=0, columnspan=2, pady=5)
        self.frameMatriz = tk.Frame(self.ventana, padx=10, pady=10)
        self.frameMatriz.pack()

        frameBotones = tk.Frame(self.ventana, padx=10, pady=5)
        frameBotones.pack(fill="x")

        tk.Button(frameBotones, text="Procesar grafo", command=self.procesarGrafo).grid(
            row=0, column=0, padx=5)
        tk.Button(frameBotones, text="Ver gráfica", command=self.verGrafica).grid(
            row=0, column=1, padx=5)
        tk.Button(frameBotones, text="Nodos adyacentes", command=self.verAdyacentes).grid(
            row=0, column=2, padx=5)
        tk.Button(frameBotones, text="Buscar camino", command=self.buscarCaminoGUI).grid(
            row=0, column=3, padx=5)
        tk.Button(frameBotones, text="Detectar ciclo", command=self.detectarCicloGUI).grid(
            row=0, column=4, padx=5)
        tk.Button(frameBotones, text="Comparar eficiencia", command=self.compararEficienciaGUI).grid(
            row=0, column=5, padx=5)

        self.areaResultados = scrolledtext.ScrolledText(self.ventana, width=90, height=22)
        self.areaResultados.pack(padx=10, pady=10)

    def generarMatriz(self):
        try:
            self.n = int(self.entradaN.get())
            if self.n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número de nodos válido (mayor a 0).")
            return
        for widget in self.frameMatriz.winfo_children():
            widget.destroy()
        self.matrizEntradas = []
        for i in range(self.n):
            filaEntradas = []
            for j in range(self.n):
                entrada = tk.Entry(self.frameMatriz, width=5, justify="center")
                entrada.insert(0, "0")
                entrada.grid(row=i, column=j, padx=2, pady=2)
                filaEntradas.append(entrada)
            self.matrizEntradas.append(filaEntradas)

    def leerMatrizDesdeEntradas(self):
        matriz = []
        for i in range(self.n):
            fila = []
            for j in range(self.n):
                texto = self.matrizEntradas[i][j].get().strip()
                try:
                    if self.conPeso.get():
                        valor = convertirAPeso(texto)
                    else:
                        if texto.upper() not in ["0", "1", "T"]:
                            raise ValueError
                        valor = 1 if texto.upper() in ["1", "T"] else 0
                except ValueError:
                    raise ValueError(f"Valor inválido en la posición [{i+1}][{j+1}]: '{texto}'")
                fila.append(valor)
            matriz.append(fila)
        return matriz

    def procesarGrafo(self):
        if self.n == 0:
            messagebox.showwarning("Aviso", "Primero genere la matriz.")
            return

        try:
            matriz = self.leerMatrizDesdeEntradas()
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return
        if not self.esDirigido.get():
            esValida, posicion = validarMatrizSimetrica(self.n, matriz)
            if not esValida:
                i, j = posicion
                messagebox.showerror(
                    "Error",
                    f"La matriz no es simétrica en [{i+1}][{j+1}] "
                    f"({matriz[i][j]} != {matriz[j][i]}). "
                    "En un grafo no dirigido debe ser simétrica."
                )
                return

        self.matrizActual = matriz
        salidaCapturada = io.StringIO()
        with contextlib.redirect_stdout(salidaCapturada):
            avisarSiHayLazos(self.n, matriz)
            mostrarRepresentacionMatematica(self.n, matriz, self.esDirigido.get(), self.conPeso.get())

        self.mostrarEnArea(salidaCapturada.getvalue())

    def verGrafica(self):
        if self.matrizActual is None:
            messagebox.showwarning("Aviso", "Primero procese el grafo.")
            return
        mostrarRepresentacionGrafica(self.n, self.matrizActual, self.esDirigido.get(), self.conPeso.get())

    def verAdyacentes(self):
        if self.matrizActual is None:
            messagebox.showwarning("Aviso", "Primero procese el grafo.")
            return
        nodo = simpledialog.askinteger("Nodo", f"Ingrese el nodo (1 a {self.n}):")
        if nodo is None or not (1 <= nodo <= self.n):
            messagebox.showerror("Error", "Nodo inválido.")
            return
        nodoIndice = nodo - 1
        adySalida, adyEntrada = obtenerNodosAdyacentes(
            nodoIndice, self.n, self.matrizActual, self.esDirigido.get())
        texto = f"\nNodos adyacentes de v{nodo}:\n"
        if self.esDirigido.get():
            textoSalida = ', '.join(adySalida) if adySalida else "Ninguno"
            textoEntrada = ', '.join(adyEntrada) if adyEntrada else "Ninguno"
            texto += f" - Adyacentes de salida: {textoSalida}\n"
            texto += f" - Adyacentes de entrada: {textoEntrada}\n"
        else:
            textoAdy = ', '.join(adySalida) if adySalida else "Ninguno"
            texto += f" - Nodos adyacentes: {textoAdy}\n"
        self.mostrarEnArea(texto)

    def buscarCaminoGUI(self):
        if self.matrizActual is None:
            messagebox.showwarning("Aviso", "Primero procese el grafo.")
            return
        origen = simpledialog.askinteger("Origen", f"Nodo de origen (1 a {self.n}):")
        if origen is None:
            return
        self.ventana.update()
        destino = simpledialog.askinteger("Destino", f"Nodo de destino (1 a {self.n}):")
        if destino is None:
            return
        if not (1 <= origen <= self.n) or not (1 <= destino <= self.n):
            messagebox.showerror("Error", "Nodos inválidos.")
            return
        if self.algoritmo.get() == "bellman":
            camino = encontrarCaminoBellman(origen - 1, destino - 1, self.n, self.matrizActual)
        else:
            if tienePesosNegativos(self.n, self.matrizActual):
                messagebox.showinfo(
                    "Aviso",
                    "La matriz tiene pesos negativos, Dijkstra no es válido.\n"
                    "Se resolverá con Bellman-Ford."
                )
                camino = encontrarCaminoBellman(origen - 1, destino - 1, self.n, self.matrizActual)
            elif self.algoritmo.get() == "dijkstraHeap":
                camino = encontrarCaminoDijkstraHeap(origen - 1, destino - 1, self.n, self.matrizActual)
            else:
                camino = encontrarCaminoDijkstra(origen - 1, destino - 1, self.n, self.matrizActual)
        if camino:
            textoCamino = " -> ".join([f"v{nodoIndice+1}" for nodoIndice in camino])
            costoTotal = calcularCostoCamino(camino, self.matrizActual)
            self.mostrarEnArea(f"\nCamino encontrado: {textoCamino}")
            self.mostrarEnArea(f"Costo total del camino: {costoTotal}\n")

            # Preguntamos si quiere ver el camino resaltado en la gráfica
            if messagebox.askyesno("Ver gráfica", "¿Deseas ver el camino resaltado en el grafo?"):
                mostrarRepresentacionGrafica(
                    self.n, self.matrizActual, self.esDirigido.get(), self.conPeso.get(),
                    caminoResaltar=camino
                )
        else:
            self.mostrarEnArea(f"\nNo existe un camino entre v{origen} y v{destino}.\n")
    def detectarCicloGUI(self):
        if self.matrizActual is None:
            messagebox.showwarning("Aviso", "Primero procese el grafo.")
            return

        if self.esDirigido.get():
            ciclo = detectarCicloDirigido(self.n, self.matrizActual)
        else:
            ciclo = detectarCicloNoDirigido(self.n, self.matrizActual)

        if ciclo:
            cicloTexto = " -> ".join([f"v{nodoIndice+1}" for nodoIndice in ciclo])
            self.mostrarEnArea(f"\nSe encontró un ciclo: {cicloTexto}\n")
        else:
            self.mostrarEnArea("\nNo se encontró ningún ciclo en el grafo.\n")

    def compararEficienciaGUI(self):
        if self.matrizActual is None:
            messagebox.showwarning("Aviso", "Primero procese el grafo.")
            return
        origen = simpledialog.askinteger("Origen", f"Nodo de origen (1 a {self.n}):")
        if origen is None:
            return
        destino = simpledialog.askinteger("Destino", f"Nodo de destino (1 a {self.n}):")
        if destino is None:
            return
        if not (1 <= origen <= self.n) or not (1 <= destino <= self.n):
            messagebox.showerror("Error", "Nodos inválidos.")
            return
        salidaCapturada = io.StringIO()
        with contextlib.redirect_stdout(salidaCapturada):
            compararEficiencia(origen - 1, destino - 1, self.n, self.matrizActual)
        self.mostrarEnArea(salidaCapturada.getvalue())
    def mostrarEnArea(self, texto):
        self.areaResultados.insert(tk.END, texto + "\n")
        self.areaResultados.see(tk.END)
def main():
    ventana = tk.Tk()
    AppGrafo(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()