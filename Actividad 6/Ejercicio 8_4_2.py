import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from enum import Enum

class TipoCargo(Enum):
    DIRECTIVO = 1
    ESTRATEGICO = 2
    OPERATIVO = 3

class TipoGenero(Enum):
    MASCULINO = 1
    FEMENINO = 2

class Empleado:
    def __init__(self, nombre, apellidos, cargo, genero, salario_p_d, dias_t,otros_i,pagos_s,aportes_p):
        self._nombre = nombre
        self._apellidos = apellidos
        self._cargo = cargo
        self._genero = genero
        self._salario_p_d = salario_p_d
        self._dias_t = dias_t
        self._otros_i = otros_i
        self._pagos_s = pagos_s
        self._aportes_p = aportes_p

    def calcular_nomina(self):
        return ((self._salario_p_d * self._dias_t) + self._otros_i - self._pagos_s - self._aportes_p)

    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, cadena):
        self._nombre = cadena

    @property
    def apellidos(self):
        return self._apellidos
    @apellidos.setter
    def apellidos(self, cadena):
        self._apellidos = cadena

    @property
    def cargo(self):
        return self._cargo
    @cargo.setter
    def cargo(self, valor):
        self._cargo = valor

    @property
    def genero(self):
        return self._genero
    @genero.setter
    def genero(self, valor):
        self._genero = valor

    @property
    def salario_p_d(self):
        return self._salario_p_d
    @salario_p_d.setter
    def salario_p_d(self, valor):
        self._salario_p_d = valor

    @property
    def dias_t(self):
        return self._dias_t
    @dias_t.setter
    def dias_t(self, valor):
        self._dias_t = valor

    @property
    def otros_i(self):
        return self._otros_i
    @otros_i.setter
    def otros_i(self, valor):
        self._otros_i = valor

    @property
    def pagos_s(self):
        return self._pagos_s
    @pagos_s.setter
    def pagos_s(self, valor):
        self._pagos_s = valor

    @property
    def aportes_p(self):
        return self._aportes_p
    @aportes_p.setter
    def aportes_p(self, valor):
        self._aportes_p = valor

class ListaEmpleados:
    def __init__(self):
        self._lista = []

    def agregar_empleado(self, empleado):
        self._lista.append(empleado)

    def validar_empleado(self,empleado):
        return any(
        e.nombre.lower() == empleado.nombre.lower() and
        e.apellidos.lower() == empleado.apellidos.lower() and
        e.genero == empleado.genero
        for e in self._lista
    )

    def cantidad(self):
        return len(self._lista)

    def obtener_empleado(self, indice):
        return self._lista[indice]

    def todos(self):
        return self._lista

    def calcular_total_nomina(self):
        return sum(e.calcular_nomina() for e in self._lista)

    def obtener_matriz(self):
        return [[e.nombre, e.apellidos, f"{e.calcular_nomina():.2f}"]for e in self._lista]

    def convertir_texto(self):
        partes = []

        for e in self._lista:
            partes.append(
                f"Nombre = {e.nombre}\n"
                f"Apellidos = {e.apellidos}\n"
                f"Cargo = {e.cargo.name}\n"
                f"Género = {e.genero.name}\n"
                f"Salario = ${e.salario_p_d}\n"
                f"Días trabajados = {e.dias_t}\n"
                f"Otros ingresos = ${e.otros_i}\n"
                f"Pagos salud = ${e.pagos_s}\n"
                f"Aportes pensiones = ${e.aportes_p}\n"
                f"---------"
            )

        total = self.calcular_total_nomina()
        partes.append(f"Total nómina = ${total:.2f}")

        return "\n".join(partes)


class Ventana_principal:
    def __init__(self):
        self.lista = ListaEmpleados()
        self.root = tk.Tk()
        self.root.title("Nómina")
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        ancho_ventana = 280
        alto_ventana = 380
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.root.resizable(False, False)

        self.V_e = None
        self.inicio()

        
    def inicio(self):
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)
        
        menu_options = tk.Menu(barra_menu, tearoff=0)
        menu_options.add_command(label="Agregar empleado", command=self.abrir_Ventana_Empleados)
        menu_options.add_command(label="Calcular nómina", command=self.mostrar_nomina)
        menu_options.add_separator()
        menu_options.add_command(label="Guardar archivo", command=self.guardar_archivo)

        barra_menu.add_cascade(label="Menú", menu=menu_options)


    def mostrar_nomina(self):
        if self.lista.cantidad() == 0:
            messagebox.showwarning(
                "Aviso",
                "No hay empleados registrados."
            )
            return

        texto = self.lista.convertir_texto()
        messagebox.showinfo("Nómina de la empresa", texto)


    def guardar_archivo(self):
        if self.lista.cantidad() == 0:
            messagebox.showwarning("Aviso","No hay empleados para guardar.")
            return

        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")]
        )

        if not archivo:
            return

        try:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(self.lista.convertir_texto())

            messagebox.showinfo("Éxito", "Archivo guardado correctamente.")
        except:
            messagebox.showerror(
                "Error",
                "No se pudo guardar el archivo."
            )


    def abrir_Ventana_Empleados(self):
        if self.V_e is None or not self.V_e.modal.winfo_exists():
            self.V_e = Ventana_Empleados(self.root, self.lista)
        else:
            self.V_e.root.deiconify()


    def mostrar(self):
        self.root.mainloop()

class Ventana_Empleados:
    def __init__(self,root,lista):
        self.lista = lista
        self.root = root
        self.modal = tk.Toplevel(self.root)
        self.modal.title("Agregar Empleado")
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        ancho_ventana = 300
        alto_ventana = 400
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.modal.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.modal.resizable(False,False)
        self.modal.grab_set()

        self.inicio()

    def inicio(self):
        self.entradas = {}
        
        campos = ["Nombre:", "Apellidos:", "Cargo:", "Género:","Salario por día:", "Días trabajados al mes:","Otros ingresos:", "Pagos por salud:", "Aportes pensiones:"]

        form = tk.Frame(self.modal)
        form.pack(padx=5, pady=20)

        for fila, texto in enumerate(campos):
            if fila == 2:
                tk.Label(form, text=texto).grid(row=fila, column=0, sticky="e", pady=5)
                self.combo_cargo = ttk.Combobox(form,values=["Directivo", "Estrategico", "Operativo"],state="readonly",width=20)
                self.combo_cargo.grid(row=fila, column=1, padx=15, pady=5)
                self.combo_cargo.current(0)

            elif fila == 3:
                tk.Label(form, text="Género:").grid(row=fila, column=0, sticky="ne", pady=5)
                self.genero_var = tk.StringVar(value="Masculino")

                marco_genero = tk.Frame(form)
                marco_genero.grid(row=fila, column=1, sticky="w")

                tk.Radiobutton(marco_genero, text="Masculino",
                               variable=self.genero_var, value="Masculino").pack(anchor="w")
                tk.Radiobutton(marco_genero, text="Femenino",
                               variable=self.genero_var, value="Femenino").pack(anchor="w")

            elif fila == 5:
                tk.Label(form, text="Días trabajados al mes:").grid(row=fila, column=0, sticky="e", pady=5)

                self.spin_dias = tk.Spinbox(form,from_=0,to=31,width=5)
                self.spin_dias.grid(row=fila, column=1, padx=15, pady=5, sticky="w")

            else:
                tk.Label(form, text=texto).grid(row=fila, column=0,sticky="e", pady=5)

                entrada = tk.Entry(form, width=22)
                entrada.grid(row=fila, column=1,pady=5, padx=10)

                clave = texto.replace(":", "")
                self.entradas[clave] = entrada

        frame_botones = tk.Frame(self.modal)
        frame_botones.pack(pady=15)
        tk.Button(frame_botones, text="Agregar", command=self.Agregar, width=10).grid(row=0, column=0, padx=10)
        tk.Button(frame_botones, text="Limpiar", command=self.limpiar, width=10).grid(row=0, column=1, padx=10)

    def Agregar(self):
        try:
            nombre = self.entradas["Nombre"].get().strip()
            apellidos = self.entradas["Apellidos"].get().strip()
            salario = float(self.entradas["Salario por día"].get())
            dias = int(self.spin_dias.get())
            otros_i = float(self.entradas["Otros ingresos"].get())
            salud = float(self.entradas["Pagos por salud"].get())
            pensiones = float(self.entradas["Aportes pensiones"].get())

            cargo = TipoCargo[self.combo_cargo.get().upper()]
            genero = TipoGenero[self.genero_var.get().upper()]

            empleado = Empleado(nombre,apellidos,cargo,genero,salario,dias,otros_i,salud,pensiones)
        except ValueError:
            messagebox.showerror("Error","Por favor llene todos los campos de manera correcta")
            return

        try:
            validacion = self.lista.validar_empleado(empleado)
            if validacion:
                raise Exception("El empleado ya estaba añadido en la lista.")
            self.lista.agregar_empleado(empleado)
            messagebox.showinfo("Éxito", "Empleado agregado correctamente")
        except Exception as e:
            messagebox.showerror("Error",str(e))



    def limpiar(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.combo_cargo.current(0)
        self.genero_var.set("Masculino")
        self.spin_dias.delete(0, tk.END)
        self.spin_dias.insert(0, "0")

class Principal:
    @staticmethod
    def main():
        app = Ventana_principal()
        app.mostrar()

if __name__ == "__main__":
    Principal.main()
