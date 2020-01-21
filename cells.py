#Autores: Fernando Salazar y Rolando Sotelo enero 2020
import sys
import numpy as np
import math as mth
import cmath as cmth
import simpy
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon # Librería para dibujar los hexagonos
import random

class EstacionBase(object):
    """Esta clase representa a una estación base"""

    def __init__(self,entorno,capacidad):
        self.entorno =entorno
        self.capacidad = capacidad
        self.Resource=simpy.Resource(entorno, capacidad)

    def obtenerusuariosconectados(self):
        return self.Resource.count

    def estadisticas(self):
        print('%d de %d canales están asignados.' % (self.Resource.count, self.Resource.capacity))

    # Lista de estaciones base
    # ListaEstacionesBase = [ID, posicion, contador_UE, [CH0,CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9]]
    #donde CH lista anidada [Tipo, distancia a UE]
    ListaEstacionesBase = []


class Usuario(object):
    """Esta clase representa a un usuario (dispositivo celular)"""

    # Definición de constructor
    def __init__(self, entorno, Lambda, Mu):
        self.entorno = entorno
        self.Lambda = Lambda # tasa deseada a la que aparecen nuevos dispositivos, distribución exponencial
        self.Mu = Mu # media promedio de duración del servicio prestado

    # Definicion de Métodos
    def procesarLlegada(self, Lambda): # Llegada o nacimiento de una petición
        return random.expovariate(Lambda) # Distribución exponencial


    def procesarSalida(self, Mu): # Duración del servicio prestado a cada dispositivo
        return random.expovariate(1 / Mu) # Distribución exponencial
    #ListausuariosMoviles=[Id, posicion, BS, M]
    ListaUsuariosMoviles=[]
    capacidadRecurso = 10

class Simulacion(object):

    """Esta clase representa a una Simulación de eventos discretos"""
    contadorLlegadas = 0
    countLlegadas = np.zeros(7)
    contadorSalidas = 0
    contadorBloqueoXRecurso = np.zeros(7)
    umbralArribos = 0 # Número de arribos a simular (CONDICIÓN DE PARO)
    # Lista de eventos de las llegadas de usuarios
    Llegadas= []
    # Lista de eventos de las salidas de usuarios
    Salidas= []
    probabilidad_Bloqueo = 0


def simulacionEventosDiscretos(entorno, usuario, simulacion, estacionesbase, terminarSimulacion):

    # Tamaño del cluster
    cluster_size = 4 # 1, 3, 4 o 7 celdas
    # Radio de la celda
    r_cell = 1000
    r_cell_plot= r_cell/200
    #  Sectorización (1 -> 60 grados, 2 -> 120 grados, 3 -> omnidireccional)
    sec = 3
    num_celdas = 6  # Tomando en cuenta el cero

    # Ubicación de las estaciones base (la celda central se encuentra en x=0 y y=0)
    # Ubicación (angular) de la célda co-canal de cada cluster del primer anillo de interferencia
    theta_N = [0, mth.pi / 6, 0, mth.pi / 6, mth.asin(1 / (2 * mth.sqrt(7)))]

    # Distancia angular entre el centro de las 6 células del primer anillo de interferencia
    aux1 = np.arange(0, 6, 1)
    theta = (mth.pi / 3) * aux1
    aux2 = [0, 1, 0, 2, 3, 0, 0, 4]
    ind = aux2[cluster_size]

    # Ubicación [x,y] de las celdas centrales de todos los clusters para el primer anillo de interferencia
    bs_position = []

    for i in range(0, len(theta)): # calculamos las coordenadas cartesianas de cada célula del primer anillo
                                   # a partir del tamaño del cluster y el radio de cada célula
        bs_position.append([(mth.sqrt(3 * cluster_size) * r_cell * np.cos(theta[i] + theta_N[ind])),
                            (mth.sqrt(3 * cluster_size) * r_cell * np.sin(theta[i] + theta_N[ind]))])

    estacionesbase.ListaEstacionesBase.append([0, [0, 0], 0, [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]])
    for i in range (0, num_celdas):
        estacionesbase.ListaEstacionesBase.append([i, bs_position[i], 0, [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]])

    # Creación de figura a plotear
    #fig, ax = plt.subplots(1)
    #ax.set_aspect('equal')
#
    ## CREACIÓN DE HEXÁGONOS
    ## Se forma y dibuja el hexágono central en x=0, y=0 en color azul, esta es la célula a analizar
    #hex = RegularPolygon((0, 0), numVertices=6, radius=r_cell, orientation=np.radians(30), facecolor="blue", alpha=0.2,
    #                     edgecolor='k')
    #ax.add_patch(hex) # se dibuja el hexagono
    ## Se dibuja un punto negro representando a la estación base
    #ax.scatter(0, 0, c='k', alpha=0.5)
#
    #for j in range(0, len(aux1)):
    #    # Se forman y dibujan los hexágonos del primer anillo de interferencia en color rojo
    #    hex = RegularPolygon((bs_position[j][0], bs_position[j][1]), numVertices=6, radius=r_cell,
    #                         orientation=np.radians(30), facecolor="red", alpha=0.2, edgecolor='k')
    #    ax.add_patch(hex)
    #    # Se dibuja un punto negro representando a la estación base en cada celda
    #    ax.scatter(bs_position[j][0], bs_position[j][1], c='k', alpha=0.5)
#
    #for j in range(0, len(aux1)):
    #    # Se forman y dibujan los hexágonos que rodean al anillo central a manera de referencia en color verde
    #    hex = RegularPolygon((bs_position[j][0] / 2, bs_position[j][1]/2), numVertices=6, radius=r_cell,
    #                         orientation=np.radians(30), facecolor="green", alpha=0.1, edgecolor='g')
    #    ax.add_patch(hex)
    #    # Se dibuja un punto negro representando a la estación base en cada celda
    #    #ax.scatter(bs_position[j][0] / 2, bs_position[j][1] / 2, c='k', alpha=0.5)
#
    ## Ploteo de figura
    ##plt.show()

    while True:
        # Se calendariza la llegada de un usuario, que es equivalente a su petición de servicio
        tiempoLlegada = entorno.timeout(usuario.procesarLlegada(usuario.Lambda), simulacion.contadorLlegadas)
        simulacion.Llegadas.append(tiempoLlegada)
        simulacion.contadorLlegadas = simulacion.contadorLlegadas + 1
        condiciondeParo(terminarSimulacion, simulacion)

        yield tiempoLlegada
        if simpy.events.AnyOf(entorno, simulacion.Llegadas):
            for i in range(0, len(simulacion.Llegadas)):
                if simulacion.Llegadas[i].processed:
                    #print(entorno.now, " Llegada de usuario", simulacion.Llegadas[i].value)

                    # Posicionar usuario

                    # Determinación del sector a simular en el snapshot
                    num_sectors = [6, 3, 1]
                    auxpi3 = mth.pi / 3
                    phi_BW = [1 * auxpi3, 2 * auxpi3, 6 * auxpi3]

                    # Se selecciona un sector aleatoriamente
                    sector = random.randint(1, num_sectors[sec - 1])
                    phi_center = [[-mth.pi, -(2 / 3) * mth.pi, -mth.pi / 3, 0, mth.pi / 3, (2 / 3) * mth.pi],
                                  [-mth.pi, -mth.pi / 3, mth.pi / 3, 0, 0, 0], [0, 0, 0, 0, 0, 0]]


                    # Determinación de la celda para la llegada del usuario
                    celda_a_posicionar = random.randint(0, num_celdas)

                    if celda_a_posicionar == 0:
                        simulacion.countLlegadas[celda_a_posicionar]=simulacion.countLlegadas[celda_a_posicionar]+1
                        # Llegará a la celda central
                        # y se establecen los moviles dentro del sector seleccionado
                        des_user_beta = np.random.uniform(0, 1) * phi_BW[sec - 1] + phi_center[sec - 1][sector - 1]
                        # Distancia de la estación base al usuario
                        des_user_r = mth.sqrt(np.random.uniform(0, 1) * (r_cell ** 2))

                        # Ubicacion [X,Y] del móvil en la celda central
                        des_user_position = [np.cos(des_user_beta) * des_user_r, np.sin(des_user_beta) * des_user_r]
                        #ax.scatter(des_user_position[0], des_user_position[1], c='b', alpha=0.3)

                        usuario.ListaUsuariosMoviles.append([simulacion.Llegadas[i].value, 0, des_user_position, False])
                        # Verificar si hay disponibilidad
                        if estacionesbase.ListaEstacionesBase[celda_a_posicionar][2] < usuario.capacidadRecurso:

                            #print("SI hay recursos, se asignará recurso a ", simulacion.Llegadas[i].value)
                            for j in range(0, usuario.capacidadRecurso):
                                # estacion base 0 / lista recursos 3 / recurso i
                                if estacionesbase.ListaEstacionesBase[0][3][j] == [0, 0]:
                                    #asignar conexion
                                    estacionesbase.ListaEstacionesBase[0][3][j] = [simulacion.Llegadas[i].value, des_user_r]
                                    #aumentar contador
                                    estacionesbase.ListaEstacionesBase[0][2] = estacionesbase.ListaEstacionesBase[0][2]+1
                                    break

                        elif estacionesbase.ListaEstacionesBase[celda_a_posicionar][2] == usuario.capacidadRecurso:
                            #print("No hay suficientes recursos")
                            simulacion.contadorBloqueoXRecurso[celda_a_posicionar] = simulacion.contadorBloqueoXRecurso[celda_a_posicionar] + 1


                    else:
                        # Llegará a cualquiera de las 6 celdas co canal interferentes
                        simulacion.countLlegadas[celda_a_posicionar] = simulacion.countLlegadas[celda_a_posicionar] + 1
                        # Se establecen los moviles co canal dentro del sector seleccionado de las celdas co canal
                        co_ch_user_beta = np.random.uniform(0, 1) * phi_BW[sec - 1] + phi_center[sec - 1][sector - 1]
                        # Distancia de la estación base al usuario
                        co_ch_user_r = np.sqrt(np.random.uniform(0, 1)) * r_cell
                        # Ubicacion [X,Y] de los móviles en las celdas co canal
                        co_ch_user_position = [co_ch_user_r * np.cos(co_ch_user_beta) + bs_position[celda_a_posicionar - 1][0], co_ch_user_r * np.sin(co_ch_user_beta) + bs_position[celda_a_posicionar - 1][1]]
                        aux_01=complex(co_ch_user_position[0], co_ch_user_position[1])
                        beta_fwd= cmth.polar(aux_01)[1]
                        d_I_fwd= cmth.polar(aux_01)[0]  # estas son las distancias de los dispositivos a la estación base, aunque
                        #ax.scatter(co_ch_user_position[0], co_ch_user_position[1], c='r', alpha=0.3)
                        usuario.ListaUsuariosMoviles.append([simulacion.Llegadas[i].value, celda_a_posicionar, co_ch_user_position, False])
                        # Verificar si hay disponibilidad
                        if estacionesbase.ListaEstacionesBase[celda_a_posicionar][2] < usuario.capacidadRecurso:
                            #print("SI hay recursos, se asignará recurso a ", simulacion.Llegadas[i].value)
                            for j in range(0, usuario.capacidadRecurso):
                                # estacion base 0 / lista recursos 3 / recurso i
                                if estacionesbase.ListaEstacionesBase[celda_a_posicionar][3][j] == [0, 0]:
                                    # asignar conexion
                                    estacionesbase.ListaEstacionesBase[celda_a_posicionar][3][j] = [simulacion.Llegadas[i].value, d_I_fwd]
                                    # aumentar contador
                                    estacionesbase.ListaEstacionesBase[celda_a_posicionar][2] = estacionesbase.ListaEstacionesBase[celda_a_posicionar][2] + 1
                                    break
                        elif estacionesbase.ListaEstacionesBase[celda_a_posicionar][2] == usuario.capacidadRecurso:
                            #print("No hay suficientes recursos")
                            simulacion.contadorBloqueoXRecurso[celda_a_posicionar] = simulacion.contadorBloqueoXRecurso[celda_a_posicionar] + 1


                    del simulacion.Llegadas[i]
                    break

        entorno.process(calendarizarSalida(entorno, usuario, simulacion))



def calendarizarSalida(entorno, usuario, simulacion):
    tiempoSalida = entorno.timeout(usuario.procesarSalida(usuario.Mu), simulacion.contadorSalidas)
    simulacion.Salidas.append(tiempoSalida)
    simulacion.contadorSalidas = simulacion.contadorSalidas + 1

    yield tiempoSalida
    if simpy.events.AnyOf(entorno, simulacion.Salidas):
        for i in range(0, len(simulacion.Salidas)):
            if simulacion.Salidas[i].processed:
                #print(entorno.now, " Salida de usuario", simulacion.Salidas[i].value)
                # Quitar usuario del plano
                # Identificar a usuario como muerto
                usuario.ListaUsuariosMoviles[simulacion.Salidas[i].value][3] = True
                # Liberar recursos
                for j in range (0, usuario.capacidadRecurso):
                    # buscar conexion usuario
                    if estacionesbase.ListaEstacionesBase[usuario.ListaUsuariosMoviles[simulacion.Salidas[i].value][1]][3][j][0] == simulacion.Salidas[i].value:
                        # reiniciarla con 0
                        estacionesbase.ListaEstacionesBase[usuario.ListaUsuariosMoviles[simulacion.Salidas[i].value][1]][3][j] = [0, 0]
                        # bajar contador
                        estacionesbase.ListaEstacionesBase[usuario.ListaUsuariosMoviles[simulacion.Salidas[i].value][1]][2] = estacionesbase.ListaEstacionesBase[usuario.ListaUsuariosMoviles[simulacion.Salidas[i].value][1]][2] - 1
                        break
                #Limpiar lista de usuario que salio del sistema
                for k in range(0, len(usuario.ListaUsuariosMoviles)):
                    if usuario.ListaUsuariosMoviles[k]:
                        if usuario.ListaUsuariosMoviles[k][0]==simulacion.Salidas[i].value:
                            usuario.ListaUsuariosMoviles[k].clear()
                            break


                del simulacion.Salidas[i]
                break

def condiciondeParo(terminarSimulacion, simulacion):
   if simulacion.contadorLlegadas == simulacion.umbralArribos:
      terminarSimulacion.succeed()



# Inicialización de la simulación
entorno = simpy.Environment()
Lambda = float(sys.argv[1])
#Lambda = 22

Mu = 1
# Creacion de objeto clase Usuario
usuario = Usuario(entorno, Lambda, Mu)
# Creación de objetos Estaciones Base, tanto la central como el primer anillo de interferencia
estacionesbase = EstacionBase(entorno, 70)

# Creacion de objeto clase Simulación
simulacion = Simulacion()
simulacion.umbralArribos = int(sys.argv[2])
#simulacion.umbralArribos = 15000

terminarSimulacion = simpy.events.Event(entorno)

entorno.process(simulacionEventosDiscretos(entorno, usuario, simulacion, estacionesbase, terminarSimulacion))
entorno.run(until=terminarSimulacion)

simulacion.probabilidad_Bloqueo = simulacion.contadorBloqueoXRecurso[0] / simulacion.countLlegadas[0]
print(simulacion.probabilidad_Bloqueo)