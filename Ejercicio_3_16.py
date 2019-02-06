# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 15:50:59 2018

@author: David Romero Acosta
"""

from gurobipy import *

m = Model("Ejercicio_3.16_Jhonson_Montgomery")
m.update()

#Materiales: Mineral del tipo i
materiales=["Mineral 1","Mineral 2","Mineral 3","Mineral 4", "Mineral 5", "Mineral 6"]

#Productos: Metales del tipo j
Productos=["Metal A","Metal B","Metal C", "Metal D"]

#Costo Materiales: costo/ton del material i
r=[23,20,18,10,27,12]

#Fracción de impureza en el material i
Imp=[0.3,0.3,0.4,0.6,0.2,0.6]

#Fracción obtenible del Producto j en el material i 
a=[[0.25,0.10,0.10,0.25],
   [0.40,0.0,0.0,0.30],
   [0.20,0.10,0.0,0.30],
   [0.0,0.15,0.05,0.20],
   [0.20,0.20,0.0,0.40],
   [0.08,0.05,0.10,0.17]]

#Demanda de la aleación obtenible en la mezcla
Demanda=4000

#Disponibilidad de material i

Disp=[2500,2200,800,3000,1000,1600]

#Requerimientos de metales

Minimo=[0.23,0.0,0.0,0.35]

Maximo=[1.0,0.15,0.04,0.65]

#Variables

x={}
for i in range(len(materiales)):
    x[i]=m.addVar(obj=r[i],vtype= GRB.CONTINUOUS, name="Total %s" % (materiales[i]))
    
#Restricción de balance de demanda

m.addConstr(quicksum((1-Imp[i])*x[i] for i in range(len(materiales))) == Demanda, "Demanda")

#Restricción de disponibilidad de materiales
for i in range(len(materiales)):
    m.addConstr(x[i]<= Disp[i], "Disponibilidad %s" % materiales[i])

#Restricción de minimos de mezcla

for j in range(len(Productos)):
    m.addConstr(quicksum(a[i][j]*x[i] for i in range(len(materiales))) >= Minimo[j]*Demanda , "Minimos %s" %Productos[j])

#Restricción de maximos de mezcla

for j in range(len(Productos)):
    m.addConstr(quicksum(a[i][j]*x[i] for i in range(len(materiales))) <= Maximo[j]*Demanda , "Maximos %s" %Productos[j])

#Función Objetivo

m.ModelSense = 1

m.optimize()

#Impresión de resultados de las variables

for i in m.getVars():
    print('%s %g %g' % (i.varname, i.x, i.RC))

#imprimir el valor de la función objetivo
    
print('Función Objetivo: %g' % (m.objVal))

#Impresión de resultados de las variables


for cs in m.getConstrs(): 
  print ('\n Restriccion %s ' %cs.ConstrName +  '  Holgura : %f' %cs.Slack + '  Precio Sombra : %f' %cs.Pi)

