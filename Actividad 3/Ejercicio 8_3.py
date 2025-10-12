import math
import tkinter as tk
from tkinter import messagebox

class Figuras_Geometricas:
    def __init__(self, volumen, superficie):
        self._volumen = volumen
        self._superficie = superficie
        
    @property
    def volumen(self):
        return self._volumen

    @volumen.setter
    def volumen(self, valor):
        self._volumen = valor

    @property
    def superficie(self):
        return self._superficie

    @superficie.setter
    def superficie(self, valor):
        self._superficie = valor
    
class Cilindro(Figuras_Geometricas):

    def __init__(self,radio,altura):
        super().__init__(0,0)
        self.radio=radio
        self.altura=altura
    def calcular_volumen(self):
        self.volumen = math.pi*(self.radio**2)*self.altura

    def calcular_superficie(self):
        self.superficie = (2*math.pi*self.radio*self.altura)+(2*math.pi*(self.radio**2))

class Esfera(Figuras_Geometricas):
    def __init__(self,radio):
        super().__init__(0,0)
        self.radio = radio
    def calcular_volumen(self):
        self.volumen = (4/3)*math.pi*(self.radio**3)
    def calcular_superficie(self):
        self.superficie = 4*math.pi*(self.radio**2)

class Piramide(Figuras_Geometricas):
    def __init__(self, base, altura, apotema):
        super().__init__(0, 0)
        self.base = base
        self.altura = altura
        self.apotema = apotema

    def calcular_volumen(self):
        area_base = self.base ** 2
        self.volumen = (area_base * self.altura) / 3

    def calcular_superficie(self):
        area_base = self.base ** 2
        self.superficie = area_base + 2 * self.base * self.apotema


class Ventana_principal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Figuras Geométricas")
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        ancho_ventana = 400
        alto_ventana = 100
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.root.resizable(False, False)

        self.V_c = None
        self.V_e = None
        self.V_p = None
        self.inicio()

    def inicio(self):
        frame_izq = tk.Frame(self.root)
        frame_centro = tk.Frame(self.root)
        frame_der = tk.Frame(self.root)

        frame_izq.pack(side=tk.LEFT, expand=True)
        frame_centro.pack(side=tk.LEFT, expand=True)
        frame_der.pack(side=tk.LEFT, expand=True)

        tk.Button(frame_izq, text="Cilindro", command=self.abrir_cilindro).pack()
        tk.Button(frame_centro, text="Esfera",command=self.abrir_esfera).pack()
        tk.Button(frame_der, text="Pirámide",command=self.abrir_piramide).pack()

    def abrir_cilindro(self):
        if self.V_c is None or not tk.Toplevel.winfo_exists(self.V_c.root):
            self.V_c = Ventana_cilindro()
        else:
            self.V_c.root.deiconify()

    def abrir_esfera(self):
        if self.V_e is None or not tk.Toplevel.winfo_exists(self.V_e.root):
            self.V_e = Ventana_esfera()
        else:
            self.V_e.root.deiconify()

    def abrir_piramide(self):
        if self.V_p is None or not tk.Toplevel.winfo_exists(self.V_p.root):
            self.V_p = Ventana_piramide()
        else:
            self.V_p.root.deiconify()

    def mostrar(self):
        self.root.mainloop()

class Ventana_cilindro:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Cilindro")
        self.root.geometry("250x160")
        self.root.resizable(False, False)

        self.cilindro = Cilindro(0, 0)
        self.inicio()

    def inicio(self):
        self.entradas = []
        for i, texto in enumerate(["Radio (cm):", "Altura (cm):"]):
            frame = tk.Frame(self.root)
            frame.pack(pady=3)
            tk.Label(frame, text=texto).pack(side=tk.LEFT)
            entrada = tk.Entry(frame, width=10)
            entrada.pack(side=tk.RIGHT)
            self.entradas.append(entrada)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        tk.Button(frame_botones, text="Calcular", command=self.calcular).pack(side=tk.RIGHT, padx=5)

        self.resultado = tk.StringVar()
        tk.Label(self.root, textvariable=self.resultado, justify="left", font=("Arial", 10)).pack(pady=10)

    def calcular(self):
        try:
            radio = float(self.entradas[0].get())
            altura = float(self.entradas[1].get())

            self.cilindro.radio = radio
            self.cilindro.altura = altura

            self.cilindro.calcular_volumen()
            self.cilindro.calcular_superficie()

            self.resultado.set(
                f"Volumen (cm³): {self.cilindro.volumen:.2f}\n"
                f"Superficie (cm²): {self.cilindro.superficie:.2f}"
            )
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")

class Ventana_esfera:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Esfera")
        self.root.geometry("250x140")
        self.root.resizable(False, False)

        self.esfera = Esfera(0)
        self.inicio()

    def inicio(self):
        self.entradas = []
        for i, texto in enumerate(["Radio (cm):"]):
            frame = tk.Frame(self.root)
            frame.pack(pady=3)
            tk.Label(frame, text=texto).pack(side=tk.LEFT)
            entrada = tk.Entry(frame, width=10)
            entrada.pack(side=tk.RIGHT)
            self.entradas.append(entrada)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        tk.Button(frame_botones, text="Calcular", command=self.calcular).pack(side=tk.RIGHT, padx=5)

        self.resultado = tk.StringVar()
        tk.Label(self.root, textvariable=self.resultado, justify="left", font=("Arial", 10)).pack(pady=10)
    def calcular(self):
        try:
            radio = float(self.entradas[0].get())

            self.esfera.radio = radio

            self.esfera.calcular_volumen()
            self.esfera.calcular_superficie()

            self.resultado.set(
                f"Volumen (cm³): {self.esfera.volumen:.2f}\n"
                f"Superficie (cm²): {self.esfera.superficie:.2f}"
            )
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")

class Ventana_piramide:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Piramide")
        self.root.geometry("250x200")
        self.root.resizable(False,False)
        self.piramide = Piramide(0,0,0)
        self.inicio()
    
    def inicio(self):
        self.entradas = []
        for i, texto in enumerate(["Base (cm):","Altura (cm):","Apotema (cm):"]):
            frame = tk.Frame(self.root)
            frame.pack(pady=3)
            tk.Label(frame, text=texto).pack(side=tk.LEFT)
            entrada = tk.Entry(frame, width=10)
            entrada.pack(side=tk.RIGHT)
            self.entradas.append(entrada)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        tk.Button(frame_botones, text="Calcular", command=self.calcular).pack(side=tk.RIGHT, padx=5)

        self.resultado = tk.StringVar()
        tk.Label(self.root, textvariable=self.resultado, justify="left", font=("Arial", 10)).pack(pady=10)

    def calcular(self):
        try:
            base = float(self.entradas[0].get())
            altura = float(self.entradas[1].get())
            apotema = float(self.entradas[2].get())

            self.piramide.base = base
            self.piramide.altura = altura
            self.piramide.apotema = apotema

            self.piramide.calcular_volumen()
            self.piramide.calcular_superficie()

            self.resultado.set(
                f"Volumen (cm³): {self.piramide.volumen:.2f}\n"
                f"Superficie (cm²): {self.piramide.superficie:.2f}"
            )
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")

class Principal:
    @staticmethod
    def main():
        app = Ventana_principal()
        app.mostrar()

#Ejecución del programa
if __name__ == "__main__":
    Principal.main()