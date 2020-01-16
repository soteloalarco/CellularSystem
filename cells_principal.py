#Este script realiza la simulacion M/M tomando como métrica de paro un número tope de arribos
#Importación de librerías
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial
import subprocess
import sys


class Simulacion():
    """Esta clase representa una simulación"""
    a = []
    umbralTopeArribos = 0
    y = []


# Simulacion para un conjunto de valores de a
def simulacion_a(simulacion):
    output = []
    for a1 in simulacion.a:
        output.append(subprocess.check_output('cells.py '+str(a1)+' '+str(simulacion.umbralTopeArribos), shell=True))
        # os.system(".py "+str(p))

    # Conversion del formato de salida
    salida = []
    for i in range(len(simulacion.a)):
        salida.append(output[i].decode(sys.stdout.encoding))
        simulacion.y.append(float(salida[i].rstrip()))



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

    y1 = [B(10, xi) for xi in simulacion.a]
    plt.plot(simulacion.a, y1, 'k', label="FormErlang Teórica 1")

    #Formula Erlang B tomando solamente ultimo estado
    def Pe(s, a, j):
        A=(a**j)/factorial(j)

        sum=0
        for k in range(0, s+1):
            sum=sum+(a**k)/factorial(k)

        return A/sum

    y2 = [Pe(10, xi, 10) for xi in simulacion.a]
    plt.plot(simulacion.a, y2, 'y', label="FormErlang Teórica 2")


    plt.xlabel('a (tráfico ofrecido)')
    plt.ylabel('$P_B$ (probabilidad de bloqueo)')
    plt.title("Simulación Erlang B M/M/"+str(10))
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)

    plt.show()


#Definicion de Parámetros de la simulación

simulacion= Simulacion() #Creación de objeto de clase Simulación
a1 = input('Ingresa el valor inicial de a (a>0):        ')
a2 = input('Ingresa el valor final de a:                ')
a3 = input('Ingresa el número de muestras a generar:    ')
simulacion.a = np.linspace(float(a1), float(a2), int(a3))#(0.01, 22, 100)
simulacion.umbralTopeArribos = int(input('Ingresa el umbral tope de arribos a generar: '))#10000
#os.system('cls')
print("  Simulando  ...")
#Ejecución de funciones
simulacion_a(simulacion)
graficasProbBloq(simulacion)