
"""
Created on Tue Aug 15 00:24:47 2017

@author: Fidel
"""

from gurobipy import *
m = Model("Mezclas")
m.update()


#costos de producción unitario c[i][j] i producto, j proceso o fuente
c = [[6, 6.2, 7.2, 7.4],
     [15, 15.4, 18, 18.4],
     [11, 11.2, 13.2, 13.4],
     [14, 14.3, 16.8, 17.1]]
     
print (type(c))    

U= [6000,500, 3000,1000 ] #Límite superior ventas productos
L=[1000,0,500,100] #Límite inferior ventas productos
r=[10,25,16,20] #Precio de venta productos

b = [400, 400, 500, 450, 400] #capacidad por cada proceso regular L = 0,...4

nombresProcesos =["Estampado", "Perforado", "Ensamblado", "Terminado", "Empaque"]

#horas por unidad a[L][i] en cada proceso L por producto i
a = [[0.03, 0.15, 0.05, 0.10],
     [0.06, 0.12, 0.00, 0.10],
     [0.05, 0.10, 0.05, 0.12],
     [0.04, 0.20, 0.03, 0.12],
     [0.02, 0.06, 0.02, 0.05]]

jj = [2, 2, 4, 0, 4] # en regular el departamento 0 (Estampado) es utilizado por dos procesos. range(2) representa los procesos 0 y 1
                     # en regular el departamento 1 (Perforado) es utilizado tambien dos procesos. range(2) representa de nuevo los procesos 0 y 1
                     # en regular los departamentos 2 y 4 (Ensamble y Empaque)  utilizan todos los procesos. range(4) representa los procesos 0, 1 , 2,3
D = [3000, 500, 1000, 2000]

nProd = 4
nProc = 4
nDepart = 5

nombresProductos=[]
for i in range(nProd):
    nombresProductos.append("Producto"+str(i))
print(nombresProductos)

nombresFuentes=[]
for i in range(nProc):
    nombresFuentes.append("Fuente"+str(i))
print(nombresFuentes)
    
xx = {} #esto es un diccionario de Python
for i in range(nProd): 
  for j in range(nProc):
       xx[i,j]  = m.addVar(obj=r[i]-c[i][j], name="PRODUCCION  del %s de la  %s" % (nombresProductos[i], nombresFuentes[j]))  

# Resources constraints

for k in range(nDepart):
  if k!=3:
     ptot = LinExpr()
     for i in range(nProd):
        for j in range(jj[k]):
               ptot.addTerms(a[k][i], xx[i,j])
     m.addConstr(ptot<= b[k], "BALANCE DE RECURSOS DEPARTAMENTO %s EN HORAS REGULARES " % nombresProcesos[k])


#Horas regulares en Terminado
m.addConstr(   0.04* (xx[0,0]+xx[0,2]) + 
                0.20* (xx[1,0]+xx[1,2]) +
                0.03* (xx[2,0]+xx[2,2]) +
                0.12* (xx[3,0]+xx[3,2]) 
                <= b[3], "BALANCE DE RECURSOS DEPARTAMENTO TERMINADO EN HORAS REGULARES")

#Horas extras en Terminado
m.addConstr(   0.04* (xx[0,1]+xx[0,3]) + 
                0.20* (xx[1,1]+xx[1,3]) +
                0.03* (xx[2,1]+xx[2,3]) +
                0.12* (xx[3,1]+xx[3,3]) 
                <= 100, "BALANCE DE RECURSOS DEPARTAMENTO TERMINADO EN HORAS EXTRAS")

# Disponibilidad para hojas de productos 2 y 4

m.addConstr(2* (xx[1,0]+xx[1,1]) + 
             1.2* (xx[3,0]+xx[3,1])
             <= 2000, "BALANCE DE RECURSOS DISPONIBILIDAD HOJAS 2 y 4")


for i in range(nProd): 
  ptot = LinExpr()
  for j in range(nProc):
     ptot.addTerms(1, xx[i,j])
  m.addConstr(ptot, GRB.LESS_EQUAL, U[i], "DEMANDA SUPERIOR%d" % i)

for i in range(nProd): 
  ptot = LinExpr()
  for j in range(nProc):
     ptot.addTerms(1, xx[i,j])
  m.addConstr(ptot, GRB.GREATER_EQUAL, L[i], "DEMANDA INFERIOR%d" % i)

"""
for i in range(nProd): 
  ptot = LinExpr()
  for j in range(nProc):
    ptot.addTerms(1, xx[i,j])
  m.addConstr(ptot, GRB.EQUAL, D[i], "DEMANDA supeRIOR%d" % i)
"""

#maximizar rentabilidad
m.ModelSense = -1;
m.update()

print(m)

m.optimize()

print('\nVariables y Costos Reducidos :\n')
for v in m.getVars():
    print(v.varName, v.x, v.RC)

print('Obj: ' ,m.objVal)

print('\nPrecios sombra y holguras de restricciones :\n')
for c in m.getConstrs():
    print(c.ConstrName, c.Pi, c.Slack)

