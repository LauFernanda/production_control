

"""
Created on Wed Aug 16 16:36:24 2017

@author: ftorres
"""

from gurobipy import *

mL = Model("Ejercicio mezclas")

mL.update()

Nombres_recursos = ["Estampado Regular","Estampado Subcontratado",
                     "Perforado Regular","Perforado Subcontratado",
                     "Terminado regular","Terminado Extras",
                     "Ensamble Regular","Empaque regular"]
print(type(Nombres_recursos))

# Cada recurso se usa en varias fuentes

Fuentes_recursos = [[0,1], [2,3],[0,1],[2,3],[0,2],[1,3],[0,1,2,3],[0,1,2,3]]

#EStampado Regular se usa en las fuentes 0 y 1, 
#EStampado subcontratado se usa en las fuentes 2 y 3, etc

# Cada recurso tiene una capacidad 
Capacidad_fuentes = [400, 1e100,400, 1e100,450,100,500,400]

# Cada recurso se usa en un proceso productivo : 
# 0 : Estampado, 1 : Perforado, 2 : Ensamblado, 3: Terminado, 4 : Empaque
secuencia_recursos = [0,0,1,1,3,3,2,4]

# horas[p][i] son horas invertidas en la produccción de una unidad del producto i
# en cada proceso proceso productivo p
# i = 0,1,2,3    p = 0,1,2,3,4

horas_unidad = [[0.03,0.15,0.05, 0.10],
                 [0.06,0.12,0.0,0.10],
                 [0.05,0.10,0.05,0.12],
                 [0.04,0.2,0.03,0.12],
                 [0.02,0.06,0.02,0.05]]


nRecursos =len(Fuentes_recursos)

demandas = [3000,500,1000,2000]
nProductos = len(demandas)

# costos_unitarios[i][j] es el costo unitario de producir una unidad del
# producto i en cada fuente j TOCA CALCULARLO
costos_unitarios = [[6,6.2,7.2,7.4],
                    [15,15.4,18,18.4],
                    [11,11.2,13.2,13.4],
                    [14,14.3,16.8,17.1]]

nFuentes = len(costos_unitarios[0])

a = {}
for k in range(nRecursos):
    for i in range(nProductos):
        for j in Fuentes_recursos[k]:
            a[i,j,k] = horas_unidad[secuencia_recursos[k]][i]

x = {}
for i in range(nProductos):
    for j in range(nFuentes):
        x[i,j] = mL.addVar(0, GRB.INFINITY, costos_unitarios[i][j] , GRB.CONTINUOUS, "Produccion %d %d" % (i,j))  
    
for i in range(nProductos):
    mL.addConstr(quicksum(x[i,j] for j in range(nFuentes)) == demandas[i], "Demanda producto %d" %i)


for k in range(nRecursos):
        mL.addConstr(quicksum(a[i,j,k]*x[i,j] 
                          for i in range(nProductos) for j in Fuentes_recursos[k]) <= Capacidad_fuentes[k] ,
                          Nombres_recursos[k])
"""

for k in range(nRecursos):
     ptot = LinExpr()
     for i in range(nProductos):
        for j in Fuentes_recursos[k]:
               ptot.addTerms(a[i,j,k], x[i,j])
     mL.addConstr(ptot<= Capacidad_fuentes[k], Nombres_recursos[k])
    
"""   
# las hojas intervienen en los productos 2 y 4 en las fuentes 1 y 2

mL.addConstr(2.0*(x[1,0]+x[1,1])+ 1.2*(x[3,0]+x[3,1]) <= 2000, "HOJAS")

# La función objetiva es MINIMIZAR
mL.ModelSense = 1

mL.update()

# Solve
mL.optimize()

print ('\n Valor Objetivo = %f' %mL.objVal )

for v in mL.getVars(): 
  print ('\n Variable %s ' %v.varName + '  Valor : %f' %v.x + ' Reduced Cost : %f' %v.RC )

for cs in mL.getConstrs(): 
  print ('\n Restriccion %s ' %cs.ConstrName + '  Precio sombra : %f' %cs.Pi + '  Holgura : %f' %cs.Slack )
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  