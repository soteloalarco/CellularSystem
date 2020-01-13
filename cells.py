import numpy as np
import math as mth
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import random


cluster_size = 4
r_cell = 5
sec = 1
# Ubicación de las estaciones base (La célula central se encuentra en x=0 y y=0)

# Ubicación angular de la cécula central de cada cluster de tier 1
theta_N = [0, mth.pi/6, 0, mth.pi/6, mth.asin(1/(2*mth.sqrt(7)))]
# distancia angular entre el centro de las 6 células de tier 1
aux1= np.arange(0, 6, 1)
theta = (mth.pi/3)*aux1
aux2= [0, 1, 0, 2, 3, 0, 0, 4]
ind=aux2[cluster_size]

#Ubicación [x,y] de las células centro de todos los clusters de tier 1
bs_position = []

for i in range(0, len(theta)):
    bs_position.append([(mth.sqrt(3*cluster_size)*r_cell*np.cos(theta[i] + theta_N[ind])), (mth.sqrt(3*cluster_size)*r_cell*np.sin(theta[i] + theta_N[ind]))])
    #bs_position.append(mth.sqrt(3*cluster_size)*r_cell*np.cos(theta[i] + theta_N[ind]))
    #bs_position.append(mth.sqrt(3*cluster_size)*r_cell*np.sin(theta[i] + theta_N[ind]))

fig, ax = plt.subplots(1)
ax.set_aspect('equal')
#Agregamos los hexagonos
for j in range(0,len(aux1)):
    hex = RegularPolygon((bs_position[j][0], bs_position[j][1]), numVertices=6, radius=r_cell, orientation=np.radians(30),facecolor="red", alpha=0.2, edgecolor='k')

    ax.add_patch(hex)
    ax.scatter(bs_position[j][0], bs_position[j][1], c='k', alpha=0.5)

hex = RegularPolygon((0, 0), numVertices=6, radius=r_cell, orientation=np.radians(30),facecolor="blue", alpha=0.2, edgecolor='g')
ax.scatter(0, 0, c='k', alpha=0.5)
ax.add_patch(hex)

for j in range(0, len(aux1)):
    hex = RegularPolygon((bs_position[j][0]/2, bs_position[j][1]/2), numVertices=6, radius=r_cell, orientation=np.radians(30),facecolor="blue", alpha=0.2, edgecolor='g')

    ax.add_patch(hex)
    ax.scatter(bs_position[j][0]/2, bs_position[j][1]/2, c='k', alpha=0.5)

plt.show()

#% Determination of the sector to simulated in this snapshot
#% --- Select (randomly) a sector ---
num_sectors = [6, 3, 1]
auxpi3 = mth.pi/3
phi_BW = [1*auxpi3, 2*auxpi3, 6*auxpi3]
sector = random.randint(1, num_sectors[sec-1])
phi_center =[ [-mth.pi, -(2/3)*mth.pi, -mth.pi/3, 0, mth.pi/3, (2/3)*mth.pi], [-mth.pi, -mth.pi/3, mth.pi/3, 0, 0, 0],[0, 0, 0, 0, 0, 0]]

#% --- Place the desired mobile within the select sector ---
des_user_beta = np.random.uniform(0, 1)*phi_BW[sec-1] + phi_center[sec-1][sector-1]
des_user_r = mth.sqrt(np.random.uniform(0, 1)*(r_cell**2))

#% --- Place co-channel mobiles within the selected sector of
#% co-channel cells---
co_ch_user_beta = np.random.uniform(0, 1, 6)*phi_BW[sec-1] + phi_center[sec-1][sector-1]
co_ch_user_r = np.sqrt(np.random.uniform(0, 1, 6))*r_cell

des_user_position = [np.cos(des_user_beta)*des_user_r, np.sin(des_user_beta)*des_user_r]
ax.scatter(des_user_position[0], des_user_position[1], c='b', alpha=0.3)

co_ch_user_position=[]
for j in range(0, len(co_ch_user_r)):
    co_ch_user_position.append([co_ch_user_r[j]*np.cos(co_ch_user_beta[j]) + bs_position[j][0], co_ch_user_r[j]*np.sin(co_ch_user_beta[j]) + bs_position[j][1]])
    ax.scatter(co_ch_user_position[j][0], co_ch_user_position[j][1], c='b', alpha=0.3)
plt.show()