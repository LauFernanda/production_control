# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 21:19:01 2018

@author: David Romero Acosta
"""
from gurobipy import *

m = Model("Ejercicio_3.18_Jhonson_Montgomery")
m.update()

#Materiales 
materiales=["Grano 1","Grano 2","Grano 3","Grano 4"]

#Productos 
Productos=["Marca A","Marca B","Marca C"]

#Mínimos por tipo de grano
L=[[0,0.10,0.40,0.0],
   [0.2,0.3,0.0,0.0],
   [0.4,0.0,0.0,0.0]]

#Máximo por tipo de grano
U=[[0.0,1.0,0.7,0.8],
    [0.4,0.7,0.0,0.1],
    [1.0,0.6,0.1,0.0]]

#Demanda de marca de cafè
a=[5000,10000,3000]

#Disponibilidad de tipo de grano
b=[4000,6000,2500,8000]

#Costo por tipo de grano i
p=[0.23,0.20,0.15,0.10]

#x[i][j] es la fracción de materiales i en cada producto j
x = {}
for i in range(len(materiales)):
    for j in range(len(Productos)):
        x[i,j] = m.addVar(L[j][i],U[j][i],vtype= GRB.CONTINUOUS, name="Materia Prima %s %s" % (materiales[i],Productos[j]))
        
#y[i] es la cantidad total de grano i usada en la producción

y={}
for i in range(len(materiales)):
    y[i]=m.addVar(obj=p[i],vtype= GRB.CONTINUOUS, name="Total Grano %s" % (materiales[i]))
        
#Restricción de balance en mezcla, la suma de todas las fracciones de un producto debe sumar 1.

for j in range(len(Productos)):
    m.addConstr(quicksum(x[i,j] for i in range(len(materiales))) == 1, "Mezcla %s" % (Productos[j]))

#Restricción de disponibilidad de grano

for i in range(len(materiales)):
    m.addConstr(quicksum(a[j]*x[i,j] for j in range(len(Productos))) <= b[i] , "Disponibilidad %s" %materiales[i])

#Restricción de disponibilidad de grano

for i in range(len(materiales)):
    m.addConstr(y[i]==quicksum(a[j]*x[i,j] for j in range(len(Productos))), "Consumo Total de Grano %s" %materiales[i])
  

#Función Objetivo Minimización

m.ModelSense = 1

m.optimize()

#Impresión de resultados de las variables

for i in m.getVars():
    print('%s %g' % (i.varname, i.x))

#imprimir el valor de la función objetivo
    
print('Función Objetivo: %g' % (m.objVal))

#Impresión de resultados de las variables


for cs in m.getConstrs(): 
  print ('\n Restriccion %s ' %cs.ConstrName +  '  Holgura : %f' %cs.Slack)

