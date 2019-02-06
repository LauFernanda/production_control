# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 20:26:03 2018

@author: David Romero Acosta
"""

#Desde la librería de Gurobi se importan los resultados
from gurobipy import *
#Se define el modelo
m = Model("Ejercicio3.3_Montgomery")
#EL archivo de salidas se define con un nombre de archivo y un tipo de texto,
archivo = open('Ejercicio3.3_Montgomery.txt', 'w')
#Define las matrices o "arrays" 
nProd= 3
nRestr= 4
#Define el vector A
a= [
    [1/20, 1/30, 1/60],
    [1/40, 1/25, 0],
    [0, 1/10, 1/20],
    [0, 1/22, 1/5],
    ]
             
#Define la matriz B
b= [150, 160, 130, 100]
#Define un vector C de minimos para cada restriccion
c= [100, 100, 0, 0]
#Define el vector de coeficientes de la función objetivo
r= [3.10,2.05,6.17]
#Define los límites inferiores de las variables
L= [1000,0,0]
#Define los límites superiores de las variables
U=[float('inf'),float('inf'),float('inf')]
#Define los nombres de las restricciones
nombres_restr=["Departamento 1", "Departamento 2", "Departamento 3", "Shipping"]
#Define los nombres de las variables
nombres_var=["Producto 1","Producto 2","Producto 3"]
#Crea las variables
xx= {}
for i in range(nProd):
    xx[i]= m.addVar(L[i],U[i], r[i], GRB.CONTINUOUS, nombres_var[i])
#Crear las restricciones
#Restriccion de producto escaso
m.addConstr( 2.0* xx[0]  + 3.0*xx[2] <= 3500,"Recurso Escaso")
#Restricciones de máxima capacidad disponible en Departamentos
for k in range(nRestr):
    m.addConstr(quicksum(a[k][i]*xx[i] for i in range(nProd))<= b[k], 
               "Máximo %s" %nombres_restr[k])
#Restricciones de mínima capacidad a emplear en Departamentos
for k in range(nRestr):
   m.addConstr(quicksum(a[k][i]*xx[i] for i in range(nProd))>= c[k], 
               "Mínimo %s" %nombres_restr[k])

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
