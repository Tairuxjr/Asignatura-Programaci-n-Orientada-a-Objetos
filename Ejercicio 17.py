import math
class Calculos:
    @staticmethod
    def area_circulo(r):
        area_circulo = math.pi*(r**2)
        return area_circulo
    @staticmethod
    def perimetro_circulo(r):
        perimetro_circulo = 2*(math.pi)*r
        return perimetro_circulo

#Programa principal

while True:
    try:
        r=float(input("Escriba el valor del radio del círculo: "))
        break
    except ValueError:
        print("Por favor ingrese un valor válido para el radio")
area_circulo = Calculos.area_circulo(r)
perimetro_circulo = Calculos.perimetro_circulo(r)
print(f"Área del círculo: {area_circulo}")
print(f"Longitud de círcunferencia: {perimetro_circulo}")