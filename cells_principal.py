#Este script realiza la simulacion M/M tomando como métrica de paro un número tope de arribos
#Importación de librerías
import os
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial
import subprocess
import sys
import re
import multiprocessing as mp
import math as mth



# Simulacion para un conjunto de valores de a
class Simulacion():
    """Esta clase representa una simulación"""
    a = []
    y = []
    numceldas = 0
    numMetricas = []
    Metricas = {}

# Simulacion para un conjunto de valores de a
def simulacion_a(a1, umbralTopeArribos=3000):
    #Conversion del formato de salida
    output = subprocess.check_output('cells.py '+str(a1)+' '+str(umbralTopeArribos), shell=True)
    output1 = output.decode(sys.stdout.encoding)
    output2 = str((re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', output1)).rstrip()).split(" , ")
    output3 = np.array(output2, float)
    return output3


def creacionDiccionarios(simulacion):
    for x in range(0,simulacion.numMetricas):
        simulacion.Metricas["Metrica"+str(x)] = []


# Graficas de Probabilidad de Bloqueo
def graficasProbBloq(simulacion):

    for i in range(0, simulacion.numMetricas):
        plt.figure(i)
        simulacion.y=np.array(simulacion.Metricas['Metrica' + str(i)][0])
        Ncc = [1, 3, 4, 7]
        y = []

        apd = 4
        for i in range(0,len(Ncc)):
            rcc = mth.sqrt(3 * Ncc[i])
            #CI = 1 / ((2 * (rcc - 1) ** -apd) + (2 * (rcc) ** -apd) + ((2 * rcc + 1) ** -apd))
            CI=(16/6)*((rcc)**apd)
            y.append(10 * mth.log10(CI))

        plt.plot(Ncc, y, 'y', label="Fórmula Teorica SIR")
        plt.plot(Ncc, simulacion.y, 'r', label="Fórmula Simulada SIR")

        if  i==0:
            plt.ylabel('probabilidad_Outage')


        elif i==1:
            plt.ylabel('SIR promedio')


        plt.xlabel('Ncc Factor de reuso')
        # plt.title("")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)
        plt.show()





if __name__ == '__main__':
    # Definicion de Parámetros de la simulación
    capacidad = 0
    output = []
    z = []
    Z = []
    simulacion = Simulacion()  # Creación de objeto de clase Simulación
    simulacion.numceldas=7
    simulacion.numMetricas = 2
    #a1 = input('Ingresa el valor inicial de a (a>0):        ')
    #a2 = input('Ingresa el valor final de a:                ')
    #a3 = input('Ingresa el número de muestras a generar:    ')
    #simulacion.a = np.linspace(float(a1), float(a2), int(a3))  # (0.01, 22, 100)
    simulacion.a = [1, 3, 4, 7]

    inicio = timer()
    print("  Simulando  ...")
    # Multiprocesamiento

    pool = mp.Pool(mp.cpu_count())

    results = pool.map(simulacion_a, [a1 for a1 in simulacion.a])

    pool.close()

    creacionDiccionarios(simulacion)
    for i in range(0, simulacion.numMetricas):
        Z=[]
        for j in range(0, len(results)):
            Z.append(results[j][i])
        simulacion.Metricas['Metrica' + str(i)].append(Z)

    graficasProbBloq(simulacion)


    fin = timer()
    tiempo_TotalSimulacion = fin - inicio
    print('Tiempo total de simulacion en segundos: ', tiempo_TotalSimulacion, '  en minutos: ', tiempo_TotalSimulacion/60, '  y en horas: ', tiempo_TotalSimulacion/60/60)

