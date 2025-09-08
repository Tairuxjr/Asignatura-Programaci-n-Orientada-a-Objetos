class Calculos:
    @staticmethod
    def calcular_edad_ana(ed_juan):
        ed_ana = (4*ed_juan)/3
        return ed_ana

    @staticmethod
    def calcular_edad_alberto(ed_juan):
        ed_alberto = (2*ed_juan)/3
        return ed_alberto

    @staticmethod
    def calcular_edad_mama(ed_juan,ed_alberto,ed_ana):
        ed_mama = ed_alberto + ed_ana + ed_juan
        return ed_mama


#Programa principal
ed_juan = "A"
while ed_juan.isalpha() or " " in ed_juan or ed_juan == "":
    ed_juan = input("Edad de Juan: ")
    print(ed_juan)
    if ed_juan.isalpha() or " " in ed_juan or ed_juan == "":
        print("Por favor ingresar una edad válida")
ed_juan = float(ed_juan)
ed_alberto = Calculos.calcular_edad_alberto(ed_juan)
ed_ana = Calculos.calcular_edad_ana(ed_juan)
ed_mama = Calculos.calcular_edad_mama(ed_juan,ed_alberto,ed_ana)
print("Las edades son:")
print(f"Juan = {ed_juan}")
print(f"Alberto = {ed_alberto}")
print(f"Ana = {ed_ana}")
print(f"Mamá = {ed_mama}")
