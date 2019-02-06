# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 10:07:18 2018

@author: David Romero Acosta
"""

from gurobipy import *

m = Model("Ejercicio 3.2 Montgomery")

#Primer paso, crear las variables.
#Variables de materia prima
x1 = m.addVar(vtype= GRB.CONTINUOUS, name="Materiales A")
x2 = m.addVar(vtype= GRB.CONTINUOUS, name="Materiales B")
#Variables de producto terminado
y1 = m.addVar(vtype= GRB.CONTINUOUS, name="Producto A")
y2 = m.addVar(vtype= GRB.CONTINUOUS, name="Producto B")

M1 = m.addVar(vtype= GRB.CONTINUOUS, name="Horas Maquina 1")
M2 = m.addVar(vtype= GRB.CONTINUOUS, name="Horas Maquina 2")
M3 = m.addVar(vtype= GRB.CONTINUOUS, name="Horas Maquina 3")
M4 = m.addVar(vtype= GRB.CONTINUOUS, name="Horas Maquina 4")
#Parámetros
m.addConstr(M1 == 0.03*x1+0.12*x2+0.04*0.856*x2, "Maquina 1")
m.addConstr(M2 == 0.07*0.99*x1, "Maquina 2")
m.addConstr(M3 == 0.05*0.941*x1+0.08*0.97*x2, "Maquina 3")
m.addConstr(M4 == 0.17*0.873*x2, "Maquina 4")

#Restricciones de Límite de Capacidad
m.addConstr(M1 <= 480, "Cap. Maquina 1")
m.addConstr(M2 <= 340+68, "Cap. Maquina 2")
m.addConstr(M3 <= 160+0, "Cap. Maquina 3")
m.addConstr(M4 <= 360, "Cap. Maquina 4")

m.addConstr(y2 == 0.97*0.90*0.98*0.93*x2, "Consumo Materiales A")
m.addConstr(y1 == 0.99*0.95*0.98*x1, "Consumo Materiales B")

#Restricciones de Límite de Capacidad
m.addConstr(y1 <=3000, "Minimo Producto A")

m.addConstr(y2 <=2000, "Maximo Producto B")
#m.addConstr(y2 >=150, "Minimo Producto B")

#Optimizar el Modelo

#Definir la funciòn objetivo
#setObjective(funcion, maximizar o minimizar)

m.setObjective((60*y1+100*y2)-(20*M1+30*M2+40*M3+50*M4)-(20*x1+25*x2), GRB.MAXIMIZE)

m.optimize()

#imprimir el nombre de cada variable y el valor óptimo de cada una.

for i in m.getVars():
    print('%s %g %g' % (i.varname, i.x, i.RC))
    
#imprimir el valor de la función objetivo
    
print('Función Objetivo: %g' % (m.objVal))

#imprimir los precios sombra y las holguras para cada variable
print('\nPrecios Sombra y Holguras de restricciones: \n')
for i in m.getConstrs():
    print('%s %g %g' % (i.ConstrName, i.Pi, i.Slack))
    
