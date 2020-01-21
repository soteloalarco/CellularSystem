#Este script realiza la simulacion M/M tomando como métrica de paro un número tope de arribos
#Importación de librerías
import os
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial
import subprocess
import sys
import multiprocessing as mp



# Simulacion para un conjunto de valores de a
class Simulacion():
    """Esta clase representa una simulación"""
    a = []
    y = []
    numceldas = 0

# Simulacion para un conjunto de valores de a
def simulacion_a(a1, umbralTopeArribos=15000):
    output = subprocess.check_output('cells.py '+str(a1)+' '+str(umbralTopeArribos), shell=True)
    output = output.decode(sys.stdout.encoding)
    return output.rstrip()



# Graficas de Probabilidad de Bloqueo
def graficasProbBloq(simulacion):
    plt.figure(100)
    plt.plot(simulacion.a, simulacion.y, 'g', label="FormErlang Simulada")
    #Formula Erlang B Recursiva
    def B(s, a):
        if s==0:
            return 1
        else:
            return (B(s - 1, a)) / ((s/a) + B(s - 1, a))

    # Se hace la compensación de a de acuerdo a el numero de celdas establecidas
    y1 = [B(10, xi/simulacion.numceldas) for xi in simulacion.a]
    plt.plot(simulacion.a, y1, 'k', label="FormErlang Teórica")

    plt.xlabel('a (tráfico ofrecido)')
    plt.ylabel('$P_B$ (probabilidad de bloqueo)')
    plt.title("Simulación Erlang B M/M/"+str(10))
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)

    plt.show()



if __name__ == '__main__':
    # Definicion de Parámetros de la simulación
    capacidad = 0
    umbralTopeArribos = 0
    output = []

    simulacion = Simulacion()  # Creación de objeto de clase Simulación
    simulacion.numceldas=7
    a1 = input('Ingresa el valor inicial de a (a>0):        ')
    a2 = input('Ingresa el valor final de a:                ')
    a3 = input('Ingresa el número de muestras a generar:    ')
    simulacion.a = np.linspace(float(a1), float(a2), int(a3))  # (0.01, 22, 100)


    inicio = timer()
    print("  Simulando  ...")
    # Multiprocesamiento

    pool = mp.Pool(mp.cpu_count())

    results = pool.map(simulacion_a, [a1 for a1 in simulacion.a])

    pool.close()

    #Conversion del formato de salida

    for i in range(len(results)):
       simulacion.y.append(float(results[i]))

    graficasProbBloq(simulacion)


    fin = timer()
    tiempo_TotalSimulacion = fin - inicio
    print('Tiempo total de simulacion en segundos: ', tiempo_TotalSimulacion, '  en minutos: ', tiempo_TotalSimulacion/60, '  y en horas: ', tiempo_TotalSimulacion/60/60)

