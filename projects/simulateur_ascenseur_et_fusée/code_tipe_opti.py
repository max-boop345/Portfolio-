#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 21:31:04 2024

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

#on définit la fonction pour intégrer les mouvements de la fusée
def rhs2(t,x):
    """ force vectorialisée"""
    G1x=-(1-alpha)*(x[0]+alpha)/((x[0]+alpha)**2+x[1]**2)**(3/2)
    G1y=-(1-alpha)*x[1]/((x[0]+alpha)**2+x[1]**2)**(3/2)
    G2x=-alpha*(x[0]-1+alpha)/((x[0]-1+alpha)**2+x[1]**2)**(3/2)
    G2y=-alpha*x[1]/((x[0]-1+alpha)**2+x[1]**2)**(3/2)
    Ficx=2*x[3]
    Ficy=-2*x[2]
    Fiex=x[0]
    Fiey=x[1]
    return  np.array([x[2],x[3],G1x+G2x+Fiex+Ficx,G1y+G2y+Fiey+Ficy])


# On définit les événements
def distance_satelisation(t, x):
    return ((-x[0] + 1 - alpha)**2 + x[1]**2)**0.5 - (10 * RL / D)
distance_satelisation.terminal = False       
distance_satelisation.direction = 0          

def est_dans_la_lune(t,x):
    return ((-x[0] + 1 - alpha)**2 + x[1]**2)**0.5 - (RL / D)
est_dans_la_lune.terminal = True
    
def est_parr_a_TL_dans_le_sens_plus_ux(t, x):
    return x[3]
est_parr_a_TL_dans_le_sens_plus_ux.terminal = True
est_parr_a_TL_dans_le_sens_plus_ux.direction = -1

def est_parr_a_TL_dans_le_sens_moins_ux(t, x):
    return x[3]
est_parr_a_TL_dans_le_sens_moins_ux.terminal = True
est_parr_a_TL_dans_le_sens_moins_ux.direction = 1

def est_trop_loin(t,x):
    return ((-x[0] + 1 - alpha)**2 + x[1]**2)**0.5 - 2*(1-alpha)
est_trop_loin.terminal = True
est_trop_loin.direction = 0 

def est_proche_de_la_lune(t,x):
    return ((-x[0] + 1 - alpha)**2 + x[1]**2)**0.5 - (20 * RL / D)
est_proche_de_la_lune.terminal = False
est_proche_de_la_lune.direction = 0

#on définit les fonctions liée au événements (modif CI)

def parra_plus(traj3):
    #création du nouveau domaine temporel
    t_event = traj3.t_events[0][0]
    n=round(t_event/delta_t)
    t_eval=np.linspace(t_event,TMAX,N-n)
    
    #création des nouvelles CI
    etat_event = traj3.sol(t_event)
    v_event=etat_event[2:]
    delta_v=-np.linalg.norm(v_event)*(1-np.sqrt(2/(1+r0/r_perigee)))
    deltaV[-1]+=delta_v
    etat_event[2:]= v_event*(1-np.sqrt(2/(1+r0/r_perigee)))
    return etat_event, t_eval, n

def parra_moin(traj3):
    #création du nouveau domaine temporel
    t_event = traj3.t_events[1][0]
    n=round(t_event/delta_t)
    t_eval=np.linspace(t_event,TMAX,N-n)

    #création des nouvelles CI
    etat_event = traj3.sol(t_event)
    v_event=etat_event[2:]
    direction = v_event/np.linalg.norm(v_event)
    v_lib=np.sqrt(2*(1-alpha)/r_perigee + np.linalg.norm(v_event)**2) * impulsion
    deltaV[-1]+= abs(v_lib - np.linalg.norm(v_event))

    etat_event[2:]= direction*v_lib
    return etat_event, t_eval, n

def satelisation(traj3):
    # Calcul des distances pour toutes les positions
    distances = np.sqrt((trajectoire_initiale_x[0, :] - (1 - alpha))**2 + trajectoire_initiale_x[1, :]**2)
    
    # Trouver la distance minimale et son indice
    dMin = np.min(distances)          # Distance minimale
    n = np.argmin(distances)       # Indice correspondant
    # Trouver n correspondant
    etat_min = trajectoire_initiale_x[:,n]
    normeV = np.sqrt(alpha / dMin)  # Vitesse pour une orbite circulaire à dMin
    v_min=etat_min[2:]
    direction = v_min/np.linalg.norm(v_min)
    #on rajoute le deltaV du à la maneuvre
    deltaV[-1] += abs( np.linalg.norm(v_min) - normeV) 
    etat_min[2:] = direction * normeV
    # Mise à jour de t_start et CI pour l'orbite circulaire
    t_start = trajectoire_initiale_t[n]
    t_eval = np.linspace(t_start, TMAX, N-n)
    return etat_min, t_eval, n

def integrate(CI, t_eval):      #pour satelisé en 2 temps
    t_start = t_eval[0]
    traj3 = solve_ivp(rhs2, 
                      (t_start, TMAX), 
                      CI, 
                      method='RK45', 
                      t_eval=t_eval, 
                      rtol=1.49012e-12, 
                      atol=1.49012e-12, 
                      events=[est_parr_a_TL_dans_le_sens_plus_ux,
                              est_parr_a_TL_dans_le_sens_moins_ux,
                              distance_satelisation,
                              est_dans_la_lune,
                              est_trop_loin],
                      dense_output=True)
    return traj3

def integrate2(CI, t_eval):     #pour aller vers la lune
    t_start = t_eval[0]
    traj3 = solve_ivp(rhs2, 
                      (t_start, TMAX), 
                      CI, 
                      method='RK45',
                      max_step = 1e-3,
                      t_eval=t_eval, 
                      rtol=1.49012e-12, 
                      atol=1.49012e-12, 
                      events=[distance_satelisation,
                              est_dans_la_lune,
                              est_trop_loin,
                               est_proche_de_la_lune],
                      dense_output=True)
    return traj3

def integrate3(CI, t_eval):     #pour intégrer de manière précise
    t_start = t_eval[0]
    traj3 = solve_ivp(rhs2, 
                      (t_start, TMAX), 
                      CI, 
                      method='DOP853',
                      #max_step = 1e-3,
                      t_eval=t_eval, 
                      rtol=1.49012e-12, 
                      atol=1.49012e-12, 
                      events=[distance_satelisation,
                              est_dans_la_lune,
                              est_trop_loin],
                      dense_output=True)
    return traj3

def concat_res(traj3,n,trajectoire_initiale_x, trajectoire_initiale_t):
    valeur_x, valeur_t = [], []  
    # Stocker uniquement les résultats de la trajectoire circulaire
    valeur_x.append(traj3.y)
    valeur_t.append(traj3.t)
    valeur_x = np.hstack(valeur_x)
    valeur_t = np.hstack(valeur_t)
    
    valeur_x = np.hstack([trajectoire_initiale_x[:,:n], valeur_x])
    valeur_t = np.hstack([trajectoire_initiale_t[:n], valeur_t])
    return valeur_x, valeur_t
    
start_time =time.time()

#paramétre à faire varier
theta0 = - np.pi/2
r0=10*rT
impulsion_T= 1
r_perigee = 1.5*rT
nbre_impulsion=2

p,q,r,s = 1,5,5,5

theta0_values = np.linspace(theta0, theta0, p)
r0_values = np.linspace(r0*0.8, r0 *1.2, q)
impulsion_T_values = np.linspace(impulsion_T*0.9, impulsion_T*1.5, r)
r_perigee_values = np.linspace(r0*0.8, r0 *1.2, s)

# Créer une grille 3D
x, y, z, t = np.meshgrid(theta0_values, r0_values, impulsion_T_values, r_perigee_values)

# Combiner les valeurs dans un tableau de points 3D
points = np.vstack([x.ravel(), y.ravel(), z.ravel(), t.ravel()]).T

TMAX= 1
# Variables pour stocker résultats
val_x=[]
val_t=[]
deltaV=[]
distance_satelisation_atteint=[]

for i in points:
    theta = i[0]
    r_ini = i[1]
    impulsion = i[2]
    r_peri = i[3]
    
    valeur_x= []
    valeur_t= []
    deltaV.append(0)
    
    v0= np.sqrt((1-alpha)/r_ini)
        
    x0,y0=-alpha+r_ini*np.cos(theta),r_ini*np.sin(theta)
    vx0,vy0=-v0*np.sin(theta),v0*np.cos(theta)

    # Variables pour stocker les résultats
    N = 1500                   # Nombre total de points souhaités
    point_utilise = 0             # Compteur de points déjà utilisés
    n = 0
    temps_event = []              # Liste pour stocker les temps où l'événement est détecté
    t_start=0
    t_origine = np.linspace(0, TMAX, N)
    t_eval = np.linspace(0, TMAX, N)  # Discrétisation initiale de t_eval en N points
    delta_t = (TMAX - t_start) / (N - 1) #utile pour retrouver le n associé à un t

    # Conditions initiales
    CI = [x0, y0, vx0, vy0]

    traj3=integrate(CI, t_eval)
    valeur_x.append(traj3.y)
    valeur_t.append(traj3.t)
    if traj3.t_events[0].size>0:
        # Stocker la trajectoire avant l'ajustement circulaire
        trajectoire_initiale_x = np.hstack(valeur_x)  # Sauvegarde la première partie
        trajectoire_initiale_t = np.hstack(valeur_t)
        
        CI, t_eval, n = parra_plus(traj3)
        

        #nouvelle intégration avec les nouvelles CI et domaine temp
        traj3=integrate(CI, t_eval)
       
        valeur_x, valeur_t = [], []  
        valeur_x, valeur_t = concat_res(traj3,n,trajectoire_initiale_x, trajectoire_initiale_t)
        
    if traj3.t_events[1].size>0:

        # Stocker la trajectoire avant l'ajustement circulaire
        trajectoire_initiale_x = np.copy(valeur_x)  # Sauvegarde la première partie
        trajectoire_initiale_t = np.copy(valeur_t)
             
        CI, t_eval, n = parra_moin(traj3)
        #nouvelle intégration avec les nouvelles CI et domaine temp
        traj3=integrate2(CI, t_eval)
        
        valeur_x, valeur_t = [], []     
        valeur_x, valeur_t = concat_res(traj3,n,trajectoire_initiale_x, trajectoire_initiale_t)

    if traj3.t_events[3].size>0:
        # Stocker la trajectoire avant l'ajustement circulaire
        trajectoire_initiale_x = np.copy(valeur_x)  # Sauvegarde la première partie
        trajectoire_initiale_t = np.copy(valeur_t)
        
        t_event = traj3.t_events[3][0]
        n=round(t_event/delta_t)
        t_eval=np.linspace(t_event,TMAX,N-n)

        CI = traj3.sol(t_event)
        traj3 = integrate3(CI, t_eval)

    if traj3.t_events[0].size>1:        #attention, ici les events ont été modifié : parra+ et parra- ont été enlevé

        # Stocker la trajectoire avant l'ajustement circulaire
        trajectoire_initiale_x = np.copy(valeur_x)  # Sauvegarde la première partie
        trajectoire_initiale_t = np.copy(valeur_t)
        
        CI, t_eval, n = satelisation(traj3)

        #nouvelle intégration avec les nouvelles CI et domaine temp
        traj3=integrate3(CI, t_eval)
        
        valeur_x, valeur_t = [], []  
        valeur_x, valeur_t = concat_res(traj3,n,trajectoire_initiale_x, trajectoire_initiale_t)
        
        distance_satelisation_atteint.append(len(deltaV))
        
    val_x.append(valeur_x)
    val_t.append(valeur_t)
    
     
    
end_time = time.time()   
temps_passé = - start_time + end_time  
print(temps_passé) 
    
    
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


    graphe3.plot(val_x[k][0],val_x[k][1],'g-',label='$v0=${:.4f}'.format(v0))
    graphe2.plot(val_x[k][0],val_x[k][1],'g-',label='$v0=${:.4f}'.format(v0))
    graphe1.plot(val_x[k][0],val_x[k][1],'g-',label='$v0=${:.4f}'.format(v0))


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
    

   
    graphe3.legend()

    for ax in fig.axes:
        #ax.legend(loc=3)
        ax.set_xlabel('$X$ (unité : $D$)',fontsize=12)
        ax.set_ylabel('$Y$ (unité : $D$)',fontsize=12)

    fig.tight_layout()

afficher(distance_satelisation_atteint[0])