# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 11:50:48 2018

@author: David Romero Acosta
"""
from gurobipy import *

m = Model("Ejercicio_3.11_Jhonson_Montgomery")
m.update()


# Crea variables

#nProductos es la cantidad de productos a fabricar
nProductos=2
#nFuentes es la cantidad de fuentes para manufacturar los productos
nFuentes=2
#nMaquinas es la cantidad de máquinas para manufacturar los productos
nMaquinas=4

Dispon_Materia_Prima=[3000,2000]

Costo_Materia_Prima=[20,25]

Precio_de_venta=[60,100]

Costo_hora_maquina=[[20,30],[30,40],[40,50],[50,70]]

Demanda_Minimos=[100,150]
Demanda_Máximos=[float('inf'),250]

#x[i][j] es la cantidad de materia prima del producto i en cada fuente j
x = {}
for i in range(nProductos):
    for j in range(nFuentes):
        x[i,j] = m.addVar(vtype= GRB.CONTINUOUS,obj=-Costo_Materia_Prima[i], name="Materia Prima %d %d" % (i,j))
        
#y[i][j] es la cantidad en unidades del producto terminado i en cada fuente j
y = {}
for i in range(nProductos):
    for j in range(nFuentes):
        y[i,j] = m.addVar(vtype= GRB.CONTINUOUS,obj=Precio_de_venta[i], name="Producto %d %d" % (i,j))

#M[k][j] es la cantidad de horas empleadas en la máquina k en cada fuente j
M = {}
for k in range(nMaquinas):
    for j in range(nFuentes):
        M[k,j] = m.addVar(vtype= GRB.CONTINUOUS,obj=-Costo_hora_maquina[k][j], name="Maquina %d %d" % (k,j))

#Relación de consumos de materia prima para cada producto terminado
#Relación para el producto A
for j in range(nFuentes):
    m.addConstr(y[0,j] == 0.99*0.95*0.98*x[0,j], "Producto A Fuente %d" % j)
#Relación para el producto B
for j in range(nFuentes):
    m.addConstr(y[1,j] == 0.97*0.90*0.98*0.93*x[1,j], "Producto B Fuente %d" % j)
#Horas empleadas en cada Máquina k en cada fuente j
#Máquina 1
for j in range(nFuentes):
    m.addConstr(M[0,j] == 0.03*x[0,j]+0.12*x[1,j]+0.04*0.97*0.90*0.98*x[1,j] , "Maquina 1 Fuente %d" % j)
#Máquina 2
for j in range(nFuentes):
    m.addConstr(M[1,j] == 0.07*0.99*x[0,j], "Maquina 2 Fuente %d" % j)
#Máquina 3
for j in range(nFuentes):
    m.addConstr(M[2,j] == 0.05*0.99*0.95*x[0,j]+0.08*0.97*x[1,j]  , "Maquina 3 Fuente %d" % j)
#Máquina 4
for j in range(nFuentes):
    m.addConstr(M[3,j] ==  0.17*0.97*0.90*x[1,j] , "Maquina 4 Fuente %d" % j)
x
# Agregue restricción de disponibilidad de materia prima

for i in range(nProductos):
    m.addConstr(quicksum(x[i,j] for j in range(nFuentes)) <= Dispon_Materia_Prima[i] , "Materia Prima Prod. %d" %i)
    
# Agregue restricción de demanda máxima de producto

for i in range(nProductos):
    m.addConstr(quicksum(y[i,j] for j in range(nFuentes)) <= Demanda_Máximos[i] , "Demanda Máxima Producto %d" %i)

# Agregue restricción de demanda mínima de producto

for i in range(nProductos):
    m.addConstr(quicksum(y[i,j] for j in range(nFuentes)) >= Demanda_Minimos[i] , "Demanda Mínima Producto %d" %i)

#Restricciones de Límite de Capacidad de máquinas

Capacidad_maquinas=[[400,80],[340,68],[160,0],[300,60]]

for k in range(nMaquinas):
    for j in range(nFuentes):
        m.addConstr(M[k,j]<=Capacidad_maquinas[k][j], "Capacidad Maquina %d Fuente %d" % (k,j) )
        
# Defina la función objetivo, maximización

m.ModelSense = -1

m.optimize()


import numpy as np
Variables = m.getVars()
Var={}
for i in m.getVars():
           Var[i]= (i.varname, i.x)

t={}
for i in range(nProductos): 
       t[i]= quicksum(y[i,j].x for j in range(nFuentes))
       
#Total de unidades de los Productos Terminados
for i in range(len(t)):
    print("Total Unidades Producto %d %g" % (i,t[i].getValue()))

for i in m.getVars():
    print('%s %g' % (i.varname, i.x))

for cs in m.getConstrs(): 
  print ('\n Restriccion %s ' %cs.ConstrName +  '  Holgura : %f' %cs.slack )
