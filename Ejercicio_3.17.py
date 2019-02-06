#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 13:50:58 2018

@author: laufernanda
"""
from gurobipy import *
import numpy as np
m = Model("3.17")
m.update()


#Nombres productos
productos=["Producto 14-5-10","Producto 10-6-4","Producto 8-8-6","Producto 6-8-6"]

# insumos
insumos=["Nitratos","Fosfatos", "Potasa", "Inertes" ]

#Proporciones del insumo j requerido para cada tonelada  del  producto i
A= [[0.14,0.10,0.08,0.06],
    [0.05,0.06,0.08,0.08],
    [0.10,0.04,0.06,0.06],
    [0.71,0.80,0.78,0.80]]
# Toneladas disponibles del insumo j
b=[2000,1000,1500,math.inf]

#Costo de una tonelada del insumo j
costo_insumos=[220,80,130,20]
#Costo constante
c=30

#Precio venta de los productos i
PV=[150,120,90,70]

#Producción mínima en toneladas de los productos i
L=[2000,3000,0,1000]

#Producción máxima en toneladas de los productos i
U=[4000,8000,5000,9000]

# Calcula rentabilidad
R=[0,0,0,0]

for i in range(len(productos)):
    R[i]= PV[i]-np.dot(list(item[i] for item in A),costo_insumos)
    
print(R)
     
# Crea variables con límites y coeficientes de función objetiva
x= {}
for i in range(len(productos)): 
       x[i]  = m.addVar(L[i],U[i], R[i], 
	       GRB.CONTINUOUS, productos[i])

m.update()
       
# Agregue restricción de capacidad

for j in range(len(insumos)):
    #print(list(A[i][j]*x[i] for i in range(4)))
    m.addConstr( quicksum(A[j][i]*x[i] for i in range(len(productos))) <=b[j],insumos[j])
 
m.update()

#Maximizar,  m.ModelSense = -1 
m.ModelSense = -1 

m.optimize()

print('Obj: %g' % m.objVal)

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

# Print solution
archivo = open('salida_Ejercicio_3_17.txt','w')

archivo.write ( '\n RENTABILIDAD TOTAL: %f'  %m.ObjVal)
archivo.write ( '\n SOLUCION:\n' )


for i in range(len(productos)): 
     archivo.write ( productos[i]  + '= %f\n' %x[i].x  )

# Print reduced costs

archivo.write ( '\nshadow prices :')

for cs in m.getConstrs(): 
  archivo.write ('\n Restriccion %s ' %cs.ConstrName + '  Precio sombra : %f' %cs.Pi )

archivo.write ( '\nHolguras de las restricciones :')

for cs in m.getConstrs(): 
  archivo.write ('\n Restriccion  ' + str (cs.ConstrName) + '  Holgura :' +  str(cs.Slack) )

archivo.write ( '\nCosto Reducido de las variables X :\n')

for i in range(len(productos)): 
     archivo.write ( productos[i]  + '= %f\n' %x[i].RC  )


archivo.close()


