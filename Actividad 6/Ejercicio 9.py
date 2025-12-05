import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Contacto:
    nombres: str
    apellidos: str
    fecha_nacimiento: str
    direccion: str
    telefono: str
    correo: str


class ListaContactos:
    def __init__(self):
        self.lista: List[Contacto] = []

    def agregar_contacto(self, contacto: Contacto):
        self.lista.append(contacto)

class VentanaContacto:
    def __init__(self):
        self.lista_contactos = ListaContactos()

        self.root = tk.Tk()
        self.root.title("Detalles del contacto")
        self.root.resizable(False, False)

        self.grid = ttk.Frame(self.root, padding=10)
        self.grid.grid(row=0, column=0)

        self.grid.configure(borderwidth=2, relief="solid")

        ttk.Label(self.grid, text="Nombres:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        ttk.Label(self.grid, text="Apellidos:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
        ttk.Label(self.grid, text="Fecha nacimiento (AAAA-MM-DD):").grid(row=2, column=0, sticky="e", padx=5, pady=3)
        ttk.Label(self.grid, text="Dirección:").grid(row=3, column=0, sticky="e", padx=5, pady=3)
        ttk.Label(self.grid, text="Teléfono:").grid(row=4, column=0, sticky="e", padx=5, pady=3)
        ttk.Label(self.grid, text="Correo:").grid(row=5, column=0, sticky="e", padx=5, pady=3)

        self.campo_nombres = ttk.Entry(self.grid)
        self.campo_apellidos = ttk.Entry(self.grid)
        self.campo_fecha = ttk.Entry(self.grid)   # ahora es texto normal
        self.campo_direccion = ttk.Entry(self.grid)
        self.campo_telefono = ttk.Entry(self.grid)
        self.campo_correo = ttk.Entry(self.grid)

        # Ubicación en grid (columna 1)
        self.campo_nombres.grid(row=0, column=1, padx=5, pady=3)
        self.campo_apellidos.grid(row=1, column=1, padx=5, pady=3)
        self.campo_fecha.grid(row=2, column=1, padx=5, pady=3)
        self.campo_direccion.grid(row=3, column=1, padx=5, pady=3)
        self.campo_telefono.grid(row=4, column=1, padx=5, pady=3)
        self.campo_correo.grid(row=5, column=1, padx=5, pady=3)

        self.lista_grafica = tk.Listbox(self.grid, width=35, height=12)
        self.lista_grafica.grid(row=0, column=2, rowspan=7, padx=10, pady=5)

        # Botón agregar
        self.boton_agregar = ttk.Button(self.grid, text="Agregar", command=self.mostrar_datos)
        self.boton_agregar.grid(row=6, column=0, columnspan=1, sticky="ew", padx=5, pady=10)
        self.boton_agregar.configure(width=20)

        self.root.mainloop()

    def mostrar_datos(self):
        # Capturar datos
        a = self.campo_nombres.get().strip()
        b = self.campo_apellidos.get().strip()
        c = self.campo_fecha.get().strip()
        d = self.campo_direccion.get().strip()
        e = self.campo_telefono.get().strip()
        f = self.campo_correo.get().strip()

        # Validación de vacíos
        if a == "" or b == "" or c == "" or d == "" or e == "" or f == "":
            messagebox.showinfo(
                "Mensaje",
                "Error en ingreso de datos\nNo se permiten campos vacíos"
            )
            return

        # Validar fecha AAAA-MM-DD
        try:
            datetime.strptime(c, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Error",
                "La fecha debe tener formato AAAA-MM-DD"
            )
            return

        # Crear contacto
        contacto = Contacto(a, b, c, d, e, f)

        # Agregar a la lista interna
        self.lista_contactos.agregar_contacto(contacto)

        # Mostrar en la lista gráfica
        data = f"{a} - {b} - {c} - {d} - {e} - {f}"
        self.lista_grafica.insert(tk.END, data)

        # Limpiar campos
        self.campo_nombres.delete(0, tk.END)
        self.campo_apellidos.delete(0, tk.END)
        self.campo_fecha.delete(0, tk.END)
        self.campo_direccion.delete(0, tk.END)
        self.campo_telefono.delete(0, tk.END)
        self.campo_correo.delete(0, tk.END)


if __name__ == "__main__":
    VentanaContacto()
