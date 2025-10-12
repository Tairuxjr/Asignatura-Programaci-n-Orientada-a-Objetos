import tkinter as tk
from tkinter import messagebox
import statistics as stats

class Notas:
    def __init__(self):
        self.lista_notas = [0.0] * 5

    def calcular_promedio(self):
        return sum(self.lista_notas) / len(self.lista_notas)

    def calcular_desviacion(self):
        return stats.pstdev(self.lista_notas)

    def calcular_mayor(self):
        return max(self.lista_notas)

    def calcular_menor(self):
        return min(self.lista_notas)

class VentanaPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Notas")
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        ancho_ventana = 200
        alto_ventana = 200
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.root.resizable(False, False)

        self.notas = Notas()
        self.inicio()

    def inicio(self):
        tk.Label(self.root, text="Ingrese las 5 notas del estudiante:").pack(pady=5)

        self.entradas = []
        for i in range(5):
            frame = tk.Frame(self.root)
            frame.pack()
            tk.Label(frame, text=f"Nota {i+1}:").pack(side=tk.LEFT)
            entrada = tk.Entry(frame, width=10)
            entrada.pack(side=tk.RIGHT)
            self.entradas.append(entrada)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        tk.Button(frame_botones, text="Calcular", command=self.calcular).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Limpiar", command=self.limpiar).pack(side=tk.RIGHT, padx=5)

        self.resultado = tk.StringVar()
        tk.Label(self.root, textvariable=self.resultado, justify="left").pack(pady=10)

    def calcular(self):
        try:
            self.notas.lista_notas = [float(e.get()) for e in self.entradas]
            promedio = self.notas.calcular_promedio()
            desv = self.notas.calcular_desviacion()
            mayor = self.notas.calcular_mayor()
            menor = self.notas.calcular_menor()

            self.resultado.set(f"Promedio: {promedio:.2f}\n"+f"Desviación estándar: {desv:.2f}\n"+f"Mayor nota: {mayor:.2f}\n"+f"Menor nota: {menor:.2f}")
            self.root.geometry("200x300")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese notas válidas")

    def limpiar(self):
        for e in self.entradas:
            e.delete(0, tk.END)
        self.resultado.set("")
        self.root.geometry("200x200")

    def mostrar(self):
        self.root.mainloop()

class Principal:
    @staticmethod
    def main():
        app = VentanaPrincipal()
        app.mostrar()

#Ejecución del programa
if __name__ == "__main__":
    Principal.main()

