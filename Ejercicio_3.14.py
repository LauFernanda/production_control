# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 15:34:47 2018

@author: d.restrepoj
"""

from gurobipy import *
m = Model("Ejercicio 3.14")
m.update
# Variables
pA1 = m.addVar(vtype=GRB.CONTINUOUS, name="PA R1")
pA2 = m.addVar(vtype=GRB.CONTINUOUS, name="PA R2")
pB1 = m.addVar(vtype=GRB.CONTINUOUS, name="PB R1")
pB2 = m.addVar(vtype=GRB.CONTINUOUS, name="PB R2")
pB3 = m.addVar(vtype=GRB.CONTINUOUS, name="PB R3")
pC1 = m.addVar(vtype=GRB.CONTINUOUS, name="PC R1")
# Función objetivo
m.setObjective(6.00*pA1 + 5.90*pA2 + 10.00*pB1 + 11.50*pB2 + 9.70*pB3 + 8.50*pC1, GRB.MAXIMIZE)
# Restricción de capacidad
m.addConstr(0.21*pA1 + 0.21*pA2 + 1.30*pB1 + 1.30*pB2 + 1.30*pB3 + 0.00*pC1 <= 160, "Departamento 1")
m.addConstr(1.15*pA1 + 1.15*pA2 + 2.19*pB1 + 0.00*pB2 + 0.00*pB3 + 4.00*pC1 <= 140, "Departamento 2")
m.addConstr(3.20*pA1 + 0.00*pA2 + 0.00*pB1 + 1.60*pB2 + 0.00*pB3 + 2.60*pC1 <= 150, "Departamento 3")
m.addConstr(0.00*pA1 + 2.75*pA2 + 0.00*pB1 + 0.00*pB2 + 2.40*pB3 + 1.00*pC1 <= 120, "Departamento 4")
# Producción mínima
m.addConstr(pB1 + pB2 + pB3 >= 10, "Mínimo 10 Unidades de B deben producirse")
# Producción máxima
m.addConstr(pC1 <= 40, "Máximo 40 Unidades de C deben producirse")
m.optimize()


print ('\n Valor Objetivo = %f' %m.objVal )

for v in m.getVars(): 
  print ('\n Variable %s ' %v.varName + '  Valor : %f' %v.x + ' Reduced Cost : %f' %v.RC )

for cs in m.getConstrs(): 
  print ('\n Restriccion %s ' %cs.ConstrName + '  Precio sombra : %f' %cs.Pi + '  Holgura : %f' %cs.Slack )

import matplotlib.pyplot as plt
import numpy as np

#############ANALISIS SENSIBILIDAD##################

##DEPARTAMENTO1
cc = m.getConstrByName("Departamento 1")

x = np.linspace(1,200, 200) # de 1 a 200 y 200 números de tipo ndarrray
y =[]
for B in x:
    cc.RHS=B #Lado derecho de la restricción
    print("B = ", B)
    m.update() # Actualiza la restricción
    m.optimize() # Re-optimiza
    if m.status == GRB.Status.OPTIMAL:
        print(B, m.objVal, " OPTIMO")
        y.append(m.objVal)
    else:
        y.append(0)
        print(B, " No Factible o INFINITO")
        
f1 = plt.figure()
plt.plot(x, y)
plt.title("Análisis de Sensibilidad")
plt.xlabel("Capacidad Departamento de Distribución")
plt.ylabel("Rentabilidad Total (US $)")
f1.savefig('Sensibilidad.png')
f1.savefig('Sensibilidad.pdf')
plt.show()

##DEPARTAMENTO2

cc = m.getConstrByName("Departamento 2")

x = np.linspace(1,200, 200) # de 1 a 200 y 200 números de tipo ndarrray
y =[]
for B in x:
    cc.RHS=B #Lado derecho de la restricción
    print("B = ", B)
    m.update() # Actualiza la restricción
    m.optimize() # Re-optimiza
    if m.status == GRB.Status.OPTIMAL:
        print(B, m.objVal, " OPTIMO")
        y.append(m.objVal)
    else:
        y.append(0)
        print(B, " No Factible o INFINITO")
        
f1 = plt.figure()
plt.plot(x, y)
plt.title("Análisis de Sensibilidad")
plt.xlabel("Capacidad Departamento de Distribución")
plt.ylabel("Rentabilidad Total (US $)")
f1.savefig('Sensibilidad.png')
f1.savefig('Sensibilidad.pdf')
plt.show()


##DEPARTAMENTO3

cc = m.getConstrByName("Departamento 3")

x = np.linspace(1,200, 200) # de 1 a 200 y 200 números de tipo ndarrray
y =[]
for B in x:
    cc.RHS=B #Lado derecho de la restricción
    print("B = ", B)
    m.update() # Actualiza la restricción
    m.optimize() # Re-optimiza
    if m.status == GRB.Status.OPTIMAL:
        print(B, m.objVal, " OPTIMO")
        y.append(m.objVal)
    else:
        y.append(0)
        print(B, " No Factible o INFINITO")
        
f1 = plt.figure()
plt.plot(x, y)
plt.title("Análisis de Sensibilidad")
plt.xlabel("Capacidad Departamento de Distribución")
plt.ylabel("Rentabilidad Total (US $)")
f1.savefig('Sensibilidad.png')
f1.savefig('Sensibilidad.pdf')
plt.show()

##DEPARTAMENTO4

cc = m.getConstrByName("Departamento 4")

x = np.linspace(1,200, 200) # de 1 a 200 y 200 números de tipo ndarrray
y =[]
for B in x:
    cc.RHS=B #Lado derecho de la restricción
    print("B = ", B)
    m.update() # Actualiza la restricción
    m.optimize() # Re-optimiza
    if m.status == GRB.Status.OPTIMAL:
        print(B, m.objVal, " OPTIMO")
        y.append(m.objVal)
    else:
        y.append(0)
        print(B, " No Factible o INFINITO")
        
f1 = plt.figure()
plt.plot(x, y)
plt.title("Análisis de Sensibilidad")
plt.xlabel("Capacidad Departamento de Distribución")
plt.ylabel("Rentabilidad Total (US $)")
f1.savefig('Sensibilidad.png')
f1.savefig('Sensibilidad.pdf')
plt.show()





