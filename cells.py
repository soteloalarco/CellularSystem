import numpy as np
import math as mth
import simpy
import matplotlib.pyplot as plt
# Librería para dibujar hexagonos
from matplotlib.patches import RegularPolygon
import random



class Usuario(object):
    """Esta clase representa a un usuario"""

    # Definición de constructor
    def __init__(self, entorno, Lambda, Mu):
        self.entorno = entorno
        self.Lambda = Lambda
        self.Mu = Mu

    # Definicion de Métodos
    def procesarLlegada(self, Lambda):
        return random.expovariate(Lambda)
        # return np.random.exponential(1 / Lambda)

    def procesarSalida(self, Mu):
        return random.expovariate(1 / Mu)
        # return np.random.exponential(Mu)

class Simulacion(object):

    """Esta clase representa a una Simulación"""
    contadorLlegadas = 0
    contadorSalidas = 0
    umbralArribos = 0
    # Lista de eventos de las llegadas de usuarios
    Llegadas= []
    # Lista de eventos de las salidas de usuarios
    Salidas= []

def simulacionEventosDiscretos(entorno, usuario, simulacion, terminarSimulacion):

    # Tamaño del cluster
    cluster_size = 4
    # Radio de la celda
    r_cell = 5
    #  Sectorización (1 -> 60 grados, 2 -> 120 grados, 3 -> omnidireccional)
    sec = 3

    # Ubicación de las estaciones base (la celda central se encuentra en x=0 y y=0)
    # Ubicación angular de la cécula central de cada cluster del primer anillo de interferencia
    theta_N = [0, mth.pi / 6, 0, mth.pi / 6, mth.asin(1 / (2 * mth.sqrt(7)))]

    # Distancia angular entre el centro de las 6 células del primer anillo de interferencia
    aux1 = np.arange(0, 6, 1)
    theta = (mth.pi / 3) * aux1
    aux2 = [0, 1, 0, 2, 3, 0, 0, 4]
    ind = aux2[cluster_size]

    # Ubicación [x,y] de las celdas centrales de todos los clusters para el primer anillo de interferencia
    bs_position = []

    for i in range(0, len(theta)):
        bs_position.append([(mth.sqrt(3 * cluster_size) * r_cell * np.cos(theta[i] + theta_N[ind])),
                            (mth.sqrt(3 * cluster_size) * r_cell * np.sin(theta[i] + theta_N[ind]))])
        # bs_position.append(mth.sqrt(3*cluster_size)*r_cell*np.cos(theta[i] + theta_N[ind]))
        # bs_position.append(mth.sqrt(3*cluster_size)*r_cell*np.sin(theta[i] + theta_N[ind]))
        # ¿Qué significan esos comentarios ??

    # Creación de figura a plotear
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')

    # CREACIÓN DE HEXÁGONOS
    # Se forma y dibuja el hexágono central en x=0, y=0 en color azul
    hex = RegularPolygon((0, 0), numVertices=6, radius=r_cell, orientation=np.radians(30), facecolor="blue", alpha=0.2,
                         edgecolor='g')
    ax.add_patch(hex)
    # Se dibuja un punto negro representando a la estación base
    ax.scatter(0, 0, c='k', alpha=0.5)

    for j in range(0, len(aux1)):
        # Se forman y dibujan los hexágonos del primer anillo de interferencia en color rojo
        hex = RegularPolygon((bs_position[j][0], bs_position[j][1]), numVertices=6, radius=r_cell,
                             orientation=np.radians(30), facecolor="red", alpha=0.2, edgecolor='k')
        ax.add_patch(hex)
        # Se dibuja un punto negro representando a la estación base en cada celda
        ax.scatter(bs_position[j][0], bs_position[j][1], c='k', alpha=0.5)

    for j in range(0, len(aux1)):
        # Se forman y dibujan los demás hexágonos en color verde
        hex = RegularPolygon((bs_position[j][0] / 2, bs_position[j][1] / 2), numVertices=6, radius=r_cell,
                             orientation=np.radians(30), facecolor="green", alpha=0.2, edgecolor='g')
        ax.add_patch(hex)
        # Se dibuja un punto negro representando a la estación base en cada celda
        ax.scatter(bs_position[j][0] / 2, bs_position[j][1] / 2, c='k', alpha=0.5)

    # Ploteo de figura
    plt.show()

    while True:
        # Se calendariza la llegada de un usuario
        tiempoLlegada = entorno.timeout(usuario.procesarLlegada(usuario.Lambda), simulacion.contadorLlegadas)
        simulacion.Llegadas.append(tiempoLlegada)
        simulacion.contadorLlegadas = simulacion.contadorLlegadas + 1
        condiciondeParo(terminarSimulacion, simulacion)

        yield tiempoLlegada
        if simpy.events.AnyOf(entorno, simulacion.Llegadas):
            for i in range(0, len(simulacion.Llegadas)):
                if simulacion.Llegadas[i].processed:
                    print(entorno.now, " Llegada de usuario", simulacion.Llegadas[i].value)
                    # Posicionar usuario
                    del simulacion.Llegadas[i]
                    break

        entorno.process(calendarizarSalida(entorno, usuario, simulacion, terminarSimulacion))


def calendarizarSalida(entorno, usuario, simulacion, terminarSimulacion):
    tiempoSalida = entorno.timeout(usuario.procesarSalida(usuario.Mu), simulacion.contadorSalidas)
    simulacion.Salidas.append(tiempoSalida)
    simulacion.contadorSalidas = simulacion.contadorSalidas + 1

    yield tiempoSalida
    if simpy.events.AnyOf(entorno, simulacion.Salidas):
        for i in range(0, len(simulacion.Salidas)):
            if simulacion.Salidas[i].processed:
                print(entorno.now, " Salida de usuario", simulacion.Salidas[i].value)
                # Quitar usuario del plano
                del simulacion.Salidas[i]
                break

def condiciondeParo(terminarSimulacion, simulacion):
   if simulacion.contadorLlegadas == simulacion.umbralArribos:
      terminarSimulacion.succeed()



# Determinación del sector a simular en el snapshot
num_sectors = [6, 3, 1]
auxpi3 = mth.pi/3
phi_BW = [1*auxpi3, 2*auxpi3, 6*auxpi3]

# Se selecciona un sector aleatoriamente
sector = random.randint(1, num_sectors[sec-1])
phi_center =[ [-mth.pi, -(2/3)*mth.pi, -mth.pi/3, 0, mth.pi/3, (2/3)*mth.pi], [-mth.pi, -mth.pi/3, mth.pi/3, 0, 0, 0],[0, 0, 0, 0, 0, 0]]

num_celdas = 7

# Determinación de la celda para la llegada del usuario
celda_a_posicionar = random.randint(1, num_celdas)

if celda_a_posicionar==1:
    # Llegará a la celda central
    # y se establecen los moviles dentro del sector seleccionado
    des_user_beta = np.random.uniform(0, 1) * phi_BW[sec - 1] + phi_center[sec - 1][sector - 1]
    des_user_r = mth.sqrt(np.random.uniform(0, 1) * (r_cell ** 2))

    # Ubicacion [X,Y] del móvil en la celda central
    des_user_position = [np.cos(des_user_beta) * des_user_r, np.sin(des_user_beta) * des_user_r]
    ax.scatter(des_user_position[0], des_user_position[1], c='b', alpha=0.3)

else:
    # Llegará a cualquiera de las 6 celdas co canal interferentes
    # Se establecen los moviles co canal dentro del sector seleccionado de las celdas co canal
    co_ch_user_beta = np.random.uniform(0, 1, 6) * phi_BW[sec - 1] + phi_center[sec - 1][sector - 1]
    co_ch_user_r = np.sqrt(np.random.uniform(0, 1, 6)) * r_cell

    # Ubicacion [X,Y] de los móviles en las celdas co canal
    co_ch_user_position = []
    for j in range(0, len(co_ch_user_r)):
        co_ch_user_position.append([co_ch_user_r[j] * np.cos(co_ch_user_beta[j]) + bs_position[j][0],
                                    co_ch_user_r[j] * np.sin(co_ch_user_beta[j]) + bs_position[j][1]])
        ax.scatter(co_ch_user_position[j][0], co_ch_user_position[j][1], c='b', alpha=0.3)




# Inicialización de la simulación
entorno = simpy.Environment()
Lambda = 2
Mu = 1
# Creacion de objeto clase Usuario
usuario = Usuario(entorno, Lambda, Mu)
# Creacion de objeto clase Simulación
simulacion = Simulacion()
simulacion.umbralArribos = 50

terminarSimulacion = simpy.events.Event(entorno)

entorno.process(simulacionEventosDiscretos(entorno, usuario, simulacion, terminarSimulacion))
entorno.run(until=terminarSimulacion)