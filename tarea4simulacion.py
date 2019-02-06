import random

archivo = open('salida_Markov_simulacion.txt','w')

CP = [0, 100, 200, 400, 550] # Costos de producción para cada nivel de producción desde 0 hasta 5
HH = [0, 30, 40, 100, 150] # Costos de inventario para cada nivel de inventarios desde 0 hasta 5
FF = [0, 1000, 2000, 3000, 3800] # Costos de faltantes para cada nivel de faltantes desde 0 hasta 5
PR = [0.2 , 0.1, 0.4, 0.3, 0] # Probabilidad de que la demanda sea 0, 1, 2, 3,4,5

random.seed()
nIntervalos =len(PR)
nIntervalos

acum = 0
PR_ACUM = []
for i in range(nIntervalos):
    acum += PR[i]
    PR_ACUM.append(acum)
    
PR_ACUM


def demanda():
    u = random.random()
    for i in range(nIntervalos):
        if u <= PR_ACUM[i]:
            demanda = i
            break
    return demanda
    
def produccion(i):
    x = 0
    if i == 0:
        x = 3
    else:
        if i == 1:
            x = 2
        else:
            if i == 2:
                x = 2
            else:
                if i == 3:
                    x = 1
                else:
                    if i == 4:
                        x = 0
    return x
        
n_periodos = 1000
for replicas in range(30):
    costo_total = 0
    costo_producir = 0
    costo_mantener = 0
    costo_faltantes = 0
    Inventario = 0
    #Inventario
    for t in range(n_periodos):
        D= demanda()
        x = produccion(Inventario)
        i_inicial = Inventario
        i_final = Inventario + x - D
        if i_final > 0 :
            Inventario = i_final
            Faltantes = 0
        else:
            Faltantes = -i_final
            Inventario = 0
        costo_total += CP[x] + HH[Inventario] + FF[Faltantes]
        costo_producir += CP[x]
        costo_mantener += HH[Inventario]
        costo_faltantes += FF[Faltantes]
        #print (t, Inventario, Faltantes, x, i_inicial, D)
    
    costo_total = costo_total/float(n_periodos)
    costo_producir = costo_producir/float(n_periodos)
    costo_mantener = costo_mantener/float(n_periodos)
    costo_faltantes = costo_faltantes/float(n_periodos)
    #print ('costo total promedio = ', costo_total)
    #print ('costo producir promedio = ', costo_producir)
    #print ('costo mantener promedio = ', costo_mantener)
    #print ('costo faltantes promedio = ', costo_faltantes)
    
    archivo. write ( '%d' %replicas +  ' %f' %costo_total +  ' %f' %costo_producir +  ' %f' %costo_mantener +  ' %f   \n ' %costo_faltantes)
    
archivo.close()

import numpy as np
import matplotlib.pyplot as plt
matriz_E = np.loadtxt('salida_Markov_simulacion.txt') # Lee la matriz da datos 

# Multiple box plots on one Axes
Nombres_costos = ['Costo Total', 'Costo de Producción', 'Costo de Mantener', 'Costo de Faltantes']

fig, ax = plt.subplots(figsize=(12, 12))
ax.boxplot(matriz_E[:,[1,2,3,4]])
ax.set_xticklabels(Nombres_costos)
ax.set_title('Resultado de la simulación de la política óptima')
ax.set_xlabel('Origen de costos')
ax.set_ylabel('$')
xtickNames = plt.setp(ax, xticklabels=Nombres_costos)
plt.setp(xtickNames, rotation=45, fontsize=10)

fig.savefig('Simulacion.png')
fig.savefig('Simulacion.pdf')
 
# Show graphic
plt.show()

#Cálculo de media e intervalos de confianza
import scipy.stats

def mean_confidence_interval(data, confidence=0.95): # Calcula la media, limite inferior y superior del intervalo de confianza de la media
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

values = np.apply_along_axis(mean_confidence_interval, 0, matriz_E[:,[1,2,3,4]]) # Aplica la función a cada columna de la matriz de datos

import pandas as pd
dataset = pd.DataFrame(values)
dataset.columns = Nombres_costos
dataset.index = ['Media','Límite Inferior','Límite Superior']
print(dataset.to_string()) # imprime el data frame con los límites de confianza

