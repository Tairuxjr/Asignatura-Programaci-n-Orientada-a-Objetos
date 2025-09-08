class Calculos:
    @staticmethod
    def calcular_suma(suma,x,y):
        suma = 0
        print(f"Suma: {suma}")
        x = 20
        print(f"X: {x}")
        suma = suma + x
        print(f"Suma: {suma}")
        y = 40
        print(f"Y: {y}")
        x = x + y**2
        print(f"X: {x}")
        suma += x/y
        return suma

#Programa principal
suma = 0
x = 0
y = 0
suma = Calculos.calcular_suma(suma,x,y)
print(f"El valor de la suma es: {suma}")