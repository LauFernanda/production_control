# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 19:52:47 2018

@author: David Romero Acosta
"""

#Desde la librería de Gurobi se importan los resultados
from gurobipy import *
#Se define el modelo
m = Model("Ejercicio3.4_Montgomery")
#EL archivo de salidas se define con un nombre de archivo y un tipo de texto,
archivo = open('Ejercicio3.4_Montgomery.txt', 'w')
#Define las matrices o "arrays" 
nProd= 3
nRestr= 5
#Define la matriz A
a= [[0.14, 0.10, 0],
    [0.6, 0.4, 0.2],
    [0.2, 0.2, 0.1],
    [0.04, 0.04, 0.04],
    [0.10, 0.10, 0.12]]
#Define la matriz B
b= [160, 320, 160, 80, 80]
#Define el vector de coeficientes de la función objetivo
r= [42, 40, 36]
#Define los límites inferiores de las variables
import scipy.stats as st

mediaA=200
desvA=10

#Si es límite inferior se lo resto a la media, si es límite superior se los sumo. También puedo sumar  siempre pero calcular la otra cola (0.8)
La=mediaA-desvA*st.norm.ppf(0.2)

Lb=300+(st.norm.ppf(0.5))*15
Lc=0
L= [La,Lb,Lc]
#Define los límites superiores de las variables
import scipy.stats as st
Ua=float('inf')
Ub==Lb
Uc=500+(st.norm.ppf(0.10))*20
U=[Ua,Ub,Uc]
#Define los nombres de las restricciones
nombres_restr=["Departamento 1", "Departamento 2", "Departamento 3", "Inspection", "Shipping"]
#Define los nombres de las variables
nombres_var=["Producto A","Producto B","Producto C"]
#Crea las variables
xx= {}
for i in range(nProd):
    xx[i]= m.addVar(L[i],U[i], r[i], GRB.CONTINUOUS, nombres_var[i])
#Crear las restricciones
for j in range(nRestr):
    m.addConstr(quicksum(a[j][i]*xx[i] for i in range(nProd))<= b[j], 
                nombres_restr[j])
m.update()
m.ModelSense= -1
m.optimize()
#Imprime las variables y su valores óptimos de solución para el problema
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))
#Imprime el valor de la función objetivo
print('Obj: %g' % m.objVal)
#Imprime los nombres de las restricciones y sus precios sombra y las holguras asociadas.
print ('Precios sombra y las holguras de restricciones :')
for i in m.getConstrs():
    print('%s %g %g' % (i.ConstrName, i.Pi, i.Slack))
#Imprime los costos reducidos asociados a las variables.
print('Costos reducidos de las variables:')
for i in m.getVars():
    print('%s %g' % (i.varName, i.RC))

#Aquí el código empieza a generar en el archivo de texto de salida definido al inicio los datos.
archivo.write('SOLUCIÓN AL EJERCICIO 3.4 MODELOS CONTROL DE PRODUCCION')
#Se imprime el valor de la función objetivo en el archivo de salida
archivo.write('\nCosto Total: %f' %m.objVal)
#Se imprime la solución de valores para cada variable del modelo
archivo.write('\nSolución:')

for i in m.getVars():
    archivo.write('\n%s %g' % (i.varName, i.x))
#Se imprimen los precios sombra de las restricciones en el archivo de salida

archivo.close()
