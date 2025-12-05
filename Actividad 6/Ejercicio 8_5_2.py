import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"


@dataclass
class Huesped:
    nombres: str
    apellidos: str
    documento: int
    fecha_ingreso: Optional[date] = None
    fecha_salida: Optional[date] = None

    def obtener_dias(self):
        if self.fecha_ingreso and self.fecha_salida:
            return (self.fecha_salida - self.fecha_ingreso).days
        return None


@dataclass
class Habitacion:
    numero: int
    disponible: bool = True
    precio_por_dia: int = 0
    huesped: Optional[Huesped] = None

    def reservar(self, huesped: Huesped):
        self.huesped = huesped
        self.disponible = False

    def liberar(self):
        self.huesped = None
        self.disponible = True


@dataclass
class Hotel:
    habitaciones: List[Habitacion] = field(default_factory=list)

    def buscar(self, numero: int) -> Optional[Habitacion]:
        for h in self.habitaciones:
            if h.numero == numero:
                return h
        return None

    def reservar(self, numero: int, huesped: Huesped):
        hab = self.buscar(numero)
        if hab and hab.disponible:
            hab.reservar(huesped)
            return True
        return False

    def liberar(self, numero: int, fecha_salida: date) -> Optional[Huesped]:
        hab = self.buscar(numero)
        if hab and not hab.disponible and hab.huesped:
            hab.huesped.fecha_salida = fecha_salida
            h = hab.huesped
            hab.liberar()
            return h
        return None


class VentanaPrincipal:
    def __init__(self, hotel: Hotel):
        self.hotel = hotel
        self.root = tk.Tk()
        self.root.title("Hotel")

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        w, h = 260, 160
        x = (ancho_pantalla // 2) - (w // 2)
        y = (alto_pantalla // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.resizable(False, False)

        self.inicio()

    def inicio(self):
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)

        opciones = tk.Menu(barra_menu, tearoff=0)
        opciones.add_command(label="Consultar habitaciones", command=self.abrir_consultar)
        opciones.add_command(label="Salida de huéspedes", command=self.menu_salida)
        barra_menu.add_cascade(label="Menú", menu=opciones)

    def abrir_consultar(self):
        VentanaHabitaciones(self.root, self.hotel)

    def menu_salida(self):
        num = simpledialog.askinteger("Salida de huésped",
                                      "Ingrese número de habitación",
                                      parent=self.root,
                                      minvalue=1)

        if num is None:
            return

        hab = self.hotel.buscar(num)
        if hab is None:
            messagebox.showerror("Error", "La habitación no existe.", parent=self.root)
            return
        if hab.disponible or hab.huesped is None:
            messagebox.showerror("Error", "La habitación no está ocupada.", parent=self.root)
            return

        VentanaSalida(self.root, self.hotel, num)

    def mostrar(self):
        self.root.mainloop()


class VentanaHabitaciones(tk.Toplevel):
    def __init__(self, master, hotel: Hotel):
        super().__init__(master)
        self.hotel = hotel
        self.title("Habitaciones")
        self.resizable(False, False)

        self._crear_componentes()

        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def _crear_componentes(self):
        cont = ttk.Frame(self, padding=10)
        cont.grid(row=0, column=0)

        # Grid 2 filas x 5 columnas
        for i, hab in enumerate(self.hotel.habitaciones):
            r = i // 5
            c = i % 5

            frame = ttk.Frame(cont, borderwidth=1, relief="solid", padding=4)
            frame.grid(row=r, column=c, padx=4, pady=4)

            ttk.Label(frame, text=f"Habitación {hab.numero}",
                      font=("Arial", 8, "bold")).pack()

            estado = "Disponible" if hab.disponible else "No disponible"
            ttk.Label(frame, text=estado).pack()

        # Selección inferior
        control = ttk.Frame(self, padding=10)
        control.grid(row=1, column=0)

        ttk.Label(control, text="Habitación a reservar:").grid(row=0, column=0, padx=6, pady=6)
        self.spin = tk.Spinbox(control, from_=1, to=len(self.hotel.habitaciones), width=5)
        self.spin.grid(row=0, column=1, padx=6)
        ttk.Button(control, text="Aceptar", command=self.ingreso).grid(row=0, column=2, padx=6)

    def ingreso(self):
        try:
            num = int(self.spin.get())
        except ValueError:
            messagebox.showerror("Error", "Número inválido", parent=self)
            return

        hab = self.hotel.buscar(num)
        if not hab:
            messagebox.showerror("Error", "La habitación no existe", parent=self)
            return
        if not hab.disponible:
            messagebox.showerror("Error", "No está disponible", parent=self)
            return

        VentanaIngreso(self, self.hotel, num)
        self.destroy()

class VentanaIngreso(tk.Toplevel):
    def __init__(self, master, hotel: Hotel, num):
        super().__init__(master)
        self.hotel = hotel
        self.num = num
        self.title("Ingreso")
        self.resizable(False, False)

        self._crear()

        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def _crear(self):
        pad = {"padx": 6, "pady": 4}
        frm = ttk.Frame(self, padding=10)
        frm.grid(row=0, column=0)

        ttk.Label(frm, text=f"Habitación: {self.num}").grid(row=0, column=0, columnspan=2, **pad)

        ttk.Label(frm, text=f"Fecha ({DATE_FORMAT}):").grid(row=1, column=0, sticky="e", **pad)
        self.entry_fecha = ttk.Entry(frm)
        self.entry_fecha.insert(0, datetime.now().strftime(DATE_FORMAT))
        self.entry_fecha.grid(row=1, column=1, **pad)

        ttk.Label(frm, text="Nombre:").grid(row=2, column=0, sticky="e", **pad)
        self.entry_nom = ttk.Entry(frm)
        self.entry_nom.grid(row=2, column=1, **pad)

        ttk.Label(frm, text="Apellidos:").grid(row=3, column=0, sticky="e", **pad)
        self.entry_ape = ttk.Entry(frm)
        self.entry_ape.grid(row=3, column=1, **pad)

        ttk.Label(frm, text="Doc. Identidad:").grid(row=4, column=0, sticky="e", **pad)
        self.entry_doc = ttk.Entry(frm)
        self.entry_doc.grid(row=4, column=1, **pad)

        btns = ttk.Frame(frm)
        btns.grid(row=5, column=0, columnspan=2, pady=8)
        ttk.Button(btns, text="Aceptar", command=self.aceptar).grid(row=0, column=0, padx=6)
        ttk.Button(btns, text="Cancelar", command=self.destroy).grid(row=0, column=1, padx=6)

    def aceptar(self):
        nom = self.entry_nom.get().strip()
        ape = self.entry_ape.get().strip()
        doc = self.entry_doc.get().strip()
        fecha = self.entry_fecha.get().strip()

        if not (nom and ape and doc and fecha):
            messagebox.showerror("Error", "Campos incompletos", parent=self)
            return

        try:
            documento = int(doc)
            fecha_ing = datetime.strptime(fecha, DATE_FORMAT).date()
        except:
            messagebox.showerror("Error", "Documento o fecha inválidos", parent=self)
            return

        hab = self.hotel.buscar(self.num)
        if not hab.disponible:
            messagebox.showerror("Error", "Habitación no disponible", parent=self)
            return

        huésped = Huesped(nom, ape, documento, fecha_ing)
        self.hotel.reservar(self.num, huésped)

        messagebox.showinfo("Mensaje", "El huésped ha sido registrado", parent=self)
        self.destroy()


class VentanaSalida(tk.Toplevel):
    def __init__(self, master, hotel: Hotel, num):
        super().__init__(master)
        self.hotel = hotel
        self.num = num
        self.title("Salida de huéspedes")
        self.resizable(False, False)

        self._crear()

        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def _crear(self):
        pad = {"padx": 6, "pady": 4}
        frm = ttk.Frame(self, padding=10)
        frm.grid(row=0, column=0)

        hab = self.hotel.buscar(self.num)

        ttk.Label(frm, text=f"Habitación: {self.num}").grid(row=0, column=0, columnspan=2, **pad)

        ttk.Label(frm, text="Fecha de ingreso:").grid(row=1, column=0, sticky="e", **pad)
        ttk.Label(frm, text=hab.huesped.fecha_ingreso.strftime(DATE_FORMAT)).grid(row=1, column=1, **pad)

        ttk.Label(frm, text=f"Fecha de salida ({DATE_FORMAT}):").grid(row=2, column=0, sticky="e", **pad)
        self.entry_sal = ttk.Entry(frm)
        self.entry_sal.insert(0, datetime.now().strftime(DATE_FORMAT))
        self.entry_sal.grid(row=2, column=1, **pad)

        ttk.Button(frm, text="Calcular", command=self.calcular).grid(row=3, column=0, columnspan=2, pady=6)

        self.lbl_dias = ttk.Label(frm, text="Cantidad de días: ")
        self.lbl_dias.grid(row=4, column=0, columnspan=2, **pad)

        self.lbl_total = ttk.Label(frm, text="Total: ")
        self.lbl_total.grid(row=5, column=0, columnspan=2, **pad)

        self.boton_registrar = ttk.Button(frm, text="RegistrarSalida", state="disabled", command=self.registrar)
        self.boton_registrar.grid(row=6, column=0, columnspan=2, pady=(6, 0))

    def calcular(self):
        fecha_s = self.entry_sal.get().strip()
        try:
            fecha_salida = datetime.strptime(fecha_s, DATE_FORMAT).date()
        except:
            messagebox.showerror("Error", "Fecha inválida", parent=self)
            return

        hab = self.hotel.buscar(self.num)
        if fecha_salida < hab.huesped.fecha_ingreso:
            messagebox.showerror("Error", "Fecha no válida", parent=self)
            return

        dias = (fecha_salida - hab.huesped.fecha_ingreso).days
        total = dias * hab.precio_por_dia

        self._datos = (fecha_salida, dias, total)

        self.lbl_dias.config(text=f"Cantidad de días: {dias}")
        self.lbl_total.config(text=f"Total: ${total}")
        self.boton_registrar.config(state="normal")

    def registrar(self):
        fecha_salida, dias, total = self._datos
        huesped = self.hotel.liberar(self.num, fecha_salida)
        messagebox.showinfo("Salida",
                            f"Huésped {huesped.nombres} {huesped.apellidos}\n"
                            f"Días: {dias}\nTotal: ${total}", parent=self)
        self.destroy()

# Inicializar
def crear_hotel():
    hotel = Hotel()
    precios = {i: 120000 for i in range(1, 6)}
    precios.update({i: 160000 for i in range(6, 11)})
    for i in range(1, 11):
        hotel.habitaciones.append(Habitacion(i, True, precios[i]))
    return hotel

class Principal:
    @staticmethod
    def main():
        hotel = crear_hotel()
        app = VentanaPrincipal(hotel)
        app.mostrar()


if __name__ == "__main__":
    Principal.main()

