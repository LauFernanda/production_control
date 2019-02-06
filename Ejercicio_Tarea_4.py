# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 18:13:12 2018

@author: David Romero Acosta
"""

from gurobipy import *

archivo = open('salida_Markov.txt','w')

nIntervals = 5 # 5 valores para los niveles de inventario y producción

CP = [0, 100, 200, 400, 550] # Costos de producción para cada nivel de producción desde 0 hasta 5
HH = [0, 30, 40, 100, 150] # Costos de inventario para cada nivel de inventarios desde 0 hasta 5
SS = [0, 1000, 2000, 3000, 3800] # Costos de faltantes para cada nivel de faltantes desde 0 hasta 5
PR = [0.2 , 0.1, 0.4, 0.3, 0] # Probabilidad de que la demanda sea 0, 1, 2, 3,4,5

# Para este ejemplo el nivel máximo de inventario es 5

CT = {} # CT[i,x] es el el costo total si el nivel de inventario es i y
                                                                  # el nivel de producción es x

q = {}
                                                                  # q[ip,i,x] es la probabilidad de que el inventario final del período sea ip, dado
                                                                  # que el inventario inicial del período sea i y el nivek de producción del
                                                                  # periodo es x
                                                                  
Demanda_maxima_mas= len(PR) # Es la demanda máxima más uno

archivo.write ( '\n ')
archivo.write ( '\n Demanda máxima más uno = %d '%Demanda_maxima_mas)

for i in range(nIntervals):
    for x in range(nIntervals):
        suma = 0
        if (i+x <=Demanda_maxima_mas-1): # El nivel máximo de inventario solo puede ser 5 en este ejemplo
            suma = CP[x]+HH[i]  # Costos de producción e inventario para cada nivel de inventario y de producción x
            for d in range(i+x,Demanda_maxima_mas): # Si demanda es mayor o igual a i+x se generan faltantes
                suma=suma+PR[d]*SS[d-i-x] # Acumula el cálculo del valor esperado del costo de faltantes
        CT[i,x] = suma # El costo total de producción e inventarios
CT

q ={}
for i in range(nIntervals):
    for x in range(nIntervals):
        for ip in range(nIntervals):
            if ip > 0: # Si no hay  faltantes
                if (i+x-ip <=Demanda_maxima_mas-1) and (i+x-ip >=0): # Cuanda la demanda i+x-ip es mayor e igual que 0 y menor igual a la demanda máxima
                    q[ip,i,x]=PR[i+x-ip]
                else:
                    q[ip,i,x]=0
            else:
                suma=0  # Si hay faltantes
                if i+x <=Demanda_maxima_mas-1: # Cuando la demanda es mayoro igual a i+x
                    for k in range(i+x,Demanda_maxima_mas):
                        suma=suma+PR[k]
                q[ip,i,x]=suma
q


archivo.write ( '\n ')
archivo.write ( '\n COSTOS ')
for i in range(nIntervals):
    for x in range(nIntervals):
        archivo.write ('\n Inventario  %d' %i + ' Produccion  %d' %x + ' costo total = %f ' %CT[i,x] )

archivo.write ( '\n \n PROBABILIDADES DE TRANSICION q(ip|i, x) ')
for i in range(nIntervals):
    for x in range(nIntervals):
        for ip in range(nIntervals):
            archivo.write ('\n Inventario ip = %d' %ip + ' Produccion x =  %d' %x + ' Inventario i =  %d' %i +' q(ip dado i, x)  = %f ' %q[ip,i,x] )


mL = Model("Markoviano")

# Assignment decision variables: pp[i,x] == probabilidad de tener inventario en  i y producir x

pp= {}
for i in range(nIntervals):
    for x in range(nIntervals):
        pp[i,x] = mL.addVar(0, 1, CT[i,x], GRB.CONTINUOUS, "xx%d. %d" % (i, x))


# The objective is to minimize the total assignment costs
mL.ModelSense = 1;

# Update model to integrate new variables
mL.update()

# Suma de probabilidades es 1.0
mL.addConstr(quicksum(pp[i,x] for i in range(nIntervals) for x in range(nIntervals)) == 1.0, "suma 1")

for ip in range(nIntervals):
    mL.addConstr(quicksum(pp[ip,x] for x in range(nIntervals)) == quicksum(pp[i,x]*q[ip,i,x] for i in range(nIntervals) for x in range(nIntervals)), "Recurso %d" %ip)

mL.update()

# Solve
mL.optimize()

archivo.write ( '\n ')

costo_op = mL.ObjVal

archivo. write ( '\n  Costo optimo = %f' %costo_op)
archivo.write ( '\n \n Probabilidades estado estable : ')
for i in range(nIntervals):
  for x in range(nIntervals):
      if pp[i,x].x>0:
          archivo.write ('\n Inventario  %d' %i + ' Produccion  %d' %x + ' probabilidad = %f ' %pp[i,x].x )

archivo.write ( '\n \n Probabilidades condicionales : ')

for i in range(nIntervals):
  suma=0
  for x in range(nIntervals):
     suma=suma+pp[i,x].x
  for x in range(nIntervals):
      p_c = pp[i,x].x/suma
      if p_c>0:
          archivo.write ('\n La probabilidad condicional dado un nivel de inventario %d' %i +' de tomar la decisión de producir %d '%x + ' es : %f ' %p_c )

suma=0
for i in range(nIntervals):
  for x in range(nIntervals):
     suma=suma+CP[x]*pp[i,x].x

archivo.write ( '\n ' )

archivo.write ( '\n Costo promedio de producir = %f' %suma)

costo_totaL=suma
suma=0
for i in range(nIntervals):
  for x in range(nIntervals):
     suma=suma+HH[i]*pp[i,x].x

costo_totaL=costo_totaL+suma

archivo.write ( '\n Costo promedio de mantener inventario = %f' %suma)

suma=0
for i in range(nIntervals):
    for x in range(nIntervals):
        suma_a = 0
        if i+x < Demanda_maxima_mas-1:
            for d in range(i+x,Demanda_maxima_mas):
                suma_a=suma_a+PR[d]*SS[d-i-x]
        suma=suma+suma_a*pp[i,x].x

costo_totaL=costo_totaL+suma

archivo.write ( '\n Costo promedio de faltantes = %f' %suma)
archivo.write ( '\n Costo total = %f' %costo_totaL)

archivo.close()
