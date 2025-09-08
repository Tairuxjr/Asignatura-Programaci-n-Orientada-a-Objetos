class Calculos:
    @staticmethod
    def x_cuadrado(x):
        x_cuadrado = x**2
        return x_cuadrado
    @staticmethod
    def x_cubo(x):
        x_cubo = x**3
        return x_cubo
    
#Programa principal
x = "A"
while x.isalpha() or x == "" or " " in x:
    x = input("Escriba el valor de X: ")
    if x.isalpha() or x == "" or " " in x:
        print("Por favor ingrese un valor válido para la X.")
x = float(x)
x_cuadrado = Calculos.x_cuadrado(x)
x_cubo = Calculos.x_cubo(x)
print(f"X: {x}")
print(f"X al cuadrado: {x_cuadrado}")
print(f"X al cubo: {x_cubo}")