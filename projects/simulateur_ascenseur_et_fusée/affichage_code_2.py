#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 13:38:44 2024

@author: maxime
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import *
from scipy import stats as st
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
from scipy import optimize as op
from scipy.special import erf
from scipy.optimize import fsolve
from matplotlib.patches import ConnectionPatch
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
import time
import pickle

#donnees numériques
MT=5.9736e24
ML=7.3477e22
RT=6400e3
RL=1735e3
D=385000e3
Cste_G=6.67e-11
m=1e5
#unités
periode=2*np.pi/np.sqrt(Cste_G*(MT+ML))*(np.sqrt(D))**3
vitesse=np.sqrt(Cste_G*(MT+ML)/D)


alpha=ML/(ML+MT) # paramètre du problème à 2 corps
rT=RT/D #rayon de la terre en unités naturelles
rL=RL/D #rayon de la lune en unités naturelles


#premières vitesses cosmiques de la Terre et la Lune en unités naturelles, et périodes associées
v1T=np.sqrt((1-alpha)/rT)
v1L=np.sqrt(alpha/rL)
periodeT=2*np.pi*rT/v1T
periodeL=2*np.pi*rL/v1L



# Charger les données
with open("simulation_results.pkl", "rb") as f:
    data = pickle.load(f)

val_x = data["val_x"]
val_t = data["val_t"]
distance_satelisation_atteint = data["distance_satelisation_atteint"] 

def afficher(k):
    #t_racc=distance_Min_Lune(traj)[0]

    
    taille_graphe=1.57*2.
    espace_entre_graphes=.28
    hauteur=taille_graphe*(2+1*espace_entre_graphes)
    largeur=taille_graphe*(2+1*espace_entre_graphes)

    fig=figure(figsize=(largeur,hauteur))
    graphe1=fig.add_subplot(221)
    graphe2=fig.add_subplot(222)
    graphe3=fig.add_subplot(223)#,projection='polar')
    graphe4=fig.add_subplot(224)

    dist_max=10


   
    beta=1.2


    graphe2.plot(val_x[k][0],val_x[k][1],'g-',label='$v0=${:.4f}')
    graphe3.plot(val_x[k][0],val_x[k][1],'g-',label='$v0=${:.4f}')
    graphe1.plot(val_x[k][0],val_x[k][1],'g-',label='$v0=${:.4f}')


    graphe1.set_aspect('equal', adjustable='box')
    graphe1.set_ylim([-0.5,0.5])

    #graphe1.plot(traj[:,0],traj[:,1],'r-',label='$v0=${:.4f}'.format(v0))
    #graphe1.plot(traj_racc[:,0],traj_racc[:,1],'b-',label='$v0=${:.4f}'.format(v0))
    graphe1.axhline(0,ls='--');graphe1.axvline(0,ls='--')

    graphe1.add_patch(Circle((-alpha,0),RT/D,edgecolor= 'black',fill=False,hatch='//',lw=2.5))
    graphe1.add_patch(Circle((1-alpha,0),RL/D,edgecolor= 'black',fill=False,hatch='//',lw=2.5))
    

    #graphe3.plot(traj[:,0],traj[:,1],'r-',label='$v0=${:.4f}'.format(v0))
    #graphe3.plot(traj_racc[:,0],traj_racc[:,1],'-',label='$v0=${:.4f}'.format(v0))


    graphe3.set_xlim([(1-alpha-dist_max*rL)-0.1,(1-alpha+dist_max*rL)+0.1])
    graphe3.set_ylim([(-dist_max*rL)-0.1,(dist_max*rL)+0.1])
    graphe3.add_patch(Circle((1-alpha,0),RL/D,edgecolor= 'black',fill=False,hatch='//',lw=2.5))
    graphe3.add_patch(Circle((1-alpha,0),10*RL/D,edgecolor= 'black',fill=False,lw=2.5))

    graphe2.set_xlim([-alpha-dist_max*rT,-alpha+dist_max*rT])
    graphe2.set_ylim([-dist_max*rT,-alpha+dist_max*rT])

        
    graphe2.add_patch(Circle((-alpha,0),RT/D,edgecolor= 'black',fill=False,hatch='\\',lw=2.5))
    #graphe4.add_patch(Circle((0,0),1+h0,edgecolor='black',fill=False,lw=.5))

    #graphe4.plot([L3],[0],[U(L3,0)],color='red')


    graphe2.text(-alpha,0,'Terre',ha='center',va='center',bbox=dict(boxstyle="square",ec='red',fc='white',alpha=.8))
    graphe3.text(1-alpha,0,'Lune',ha='center',va='center',bbox=dict(boxstyle="square",ec='red',fc='white',alpha=.8))

    # Ajouter le câble entre la Lune et le point L2 dans le graphique 3
    

   
    #graphe3.legend()

    for ax in fig.axes:
        #ax.legend(loc=3)
        ax.set_xlabel('$X$ (unité : $D$)',fontsize=12)
        ax.set_ylabel('$Y$ (unité : $D$)',fontsize=12)

    fig.tight_layout()


#afficher(distance_satelisation_atteint[0])