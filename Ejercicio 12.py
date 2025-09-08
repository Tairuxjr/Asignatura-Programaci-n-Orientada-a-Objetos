class Calculos:
    @staticmethod
    def salario_bruto():
        salario_bruto = 48*5000
        return salario_bruto
    @staticmethod
    def porcentaje_retencion(salario_bruto):
        porcentaje_retencion = salario_bruto*0.125
        return porcentaje_retencion
    @staticmethod
    def salario_neto(salario_bruto,porcentaje_retencion):
        salario_neto = salario_bruto-porcentaje_retencion
        return salario_neto

#Programa Principal
salario_bruto = Calculos.salario_bruto()
porcentaje_retencion = Calculos.porcentaje_retencion(salario_bruto)
salario_neto = Calculos.salario_neto(salario_bruto,porcentaje_retencion)

print(f"Salario bruto: ${salario_bruto}")
print(f"Porcentaje de retención en la fuente: ${porcentaje_retencion}")
print(f"Salario neto: ${salario_neto}")