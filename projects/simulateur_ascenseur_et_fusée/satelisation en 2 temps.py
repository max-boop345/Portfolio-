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
import datetime

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





# Événement : parallèle à l'axe T-L
def est_parr_a_TL_dans_le_sens_plus_ux(t, x):
    return x[3]
est_parr_a_TL_dans_le_sens_plus_ux.terminal = False
est_parr_a_TL_dans_le_sens_plus_ux.direction = -1

def est_parr_a_TL_dans_le_sens_moins_ux(t, x):
    return x[3]
est_parr_a_TL_dans_le_sens_moins_ux.terminal = False
est_parr_a_TL_dans_le_sens_moins_ux.direction = 1

TMAX=5
valeur_x= []
valeur_t= []
deltaV=[]

theta0= - np.pi/4

r0=rT*10.5
r_perigee=1.5*rT
v0= np.sqrt((1-alpha)/r0)
e= (r0-r_perigee)/(r0+r_perigee)
    
x0,y0=-alpha+r0*np.cos(theta0),r0*np.sin(theta0)
vx0,vy0=-v0*np.sin(theta0),v0*np.cos(theta0)

# Variables pour stocker les résultats
N = 1000                 # Nombre total de points souhaités
point_utilise = 0             # Compteur de points déjà utilisés
n = 0
temps_event = []              # Liste pour stocker les temps où l'événement est détecté
t_start=0
t_origine = np.linspace(0, TMAX, N)
t_eval = np.linspace(0, TMAX, N)  # Discrétisation initiale de t_eval en N points

delta_t = (TMAX - t_start) / (N - 1) #utile pour retrouver le n associé à un t

# Conditions initiales
CI = [x0, y0, vx0, vy0]

traj3 = solve_ivp(rhs2, 
                  (t_start, TMAX), 
                  CI, 
                  method='RK45', 
                  t_eval=t_eval, 
                  rtol=1.49012e-12, 
                  atol=1.49012e-12, 
                  events=[est_parr_a_TL_dans_le_sens_plus_ux, est_parr_a_TL_dans_le_sens_moins_ux],
                  dense_output=True)

valeur_x.append(traj3.y)
valeur_t.append(traj3.t)

if traj3.t_events[0].size>0:
    # Stocker la trajectoire avant l'ajustement circulaire
    trajectoire_initiale_x = np.hstack(valeur_x)  # Sauvegarde la première partie
    trajectoire_initiale_t = np.hstack(valeur_t)
    #création du nouveau domaine temporel
    t_event = traj3.t_events[0][0]
    n=round(t_event/delta_t)
    t_eval=np.linspace(t_event,TMAX,N-n)
    
    #création des nouvelles CI
    etat_event = traj3.sol(t_event)
    v_event=etat_event[2:]
    #v_new = (2+(1-alpha)/(r0*(1+r0/r_perigee)))**1/2
    #v_new = (2+(1-alpha)/(r_perigee*(1+r_perigee/r0)))**1/2 #np.linalg.norm(v_event)*((2/(1+r0/r_perigee))**1/2)
    delta_v=-np.linalg.norm(v_event)*(1-np.sqrt(2/(1+r0/r_perigee)))
    direction = v_event/np.linalg.norm(v_event)
    etat_event[2:]= v_event*(1-np.sqrt(2/(1+r0/r_perigee)))
    CI = etat_event
    
    #nouvelle intégration avec les nouvelles CI et domaine temp
    traj3=solve_ivp(rhs2, 
                      (t_event, TMAX), 
                      CI, 
                      method='RK45', 
                      t_eval=t_eval, 
                      rtol=1.49012e-12, 
                      atol=1.49012e-12, 
                      events=[est_parr_a_TL_dans_le_sens_plus_ux, est_parr_a_TL_dans_le_sens_moins_ux],
                      dense_output=True)
   
    
    #concaténation des résultats 
    valeur_x = []
    valeur_t = []
    # Stocker uniquement les résultats de la trajectoire circulaire
    valeur_x.append(traj3.y)
    valeur_t.append(traj3.t)
    valeur_x = np.hstack(valeur_x)
    valeur_t = np.hstack(valeur_t)
    
    valeur_x = np.hstack([trajectoire_initiale_x[:,:n], valeur_x])
    valeur_t = np.hstack([trajectoire_initiale_t[:n], valeur_t])
    
if traj3.t_events[1].size>0:
    # Stocker la trajectoire avant l'ajustement circulaire
    trajectoire_initiale_x = np.copy(valeur_x)  # Sauvegarde la première partie
    trajectoire_initiale_t = np.copy(valeur_t)
     
    #création du nouveau domaine temporel
    t_event = traj3.t_events[1][0]
    n=round(t_event/delta_t)
    t_eval=np.linspace(t_event,TMAX,N-n)
     
    #création des nouvelles CI
    etat_event = traj3.sol(t_event)
    v_event=etat_event[2:]
    direction = v_event/np.linalg.norm(v_event)
    v_lib=np.sqrt(2*(1-alpha)/r_perigee + np.linalg.norm(v_event)**2)*1.05
    etat_event[2:]= direction*v_lib
    CI = etat_event
     
    #nouvelle intégration avec les nouvelles CI et domaine temp
    traj3=solve_ivp(rhs2, 
                      (t_event, TMAX), 
                       CI, 
                       method='RK45', 
                       t_eval=t_eval, 
                       rtol=1.49012e-12, 
                       atol=1.49012e-12, 
                       events=[est_parr_a_TL_dans_le_sens_plus_ux, est_parr_a_TL_dans_le_sens_moins_ux],
                       dense_output=True)
    
     
    #concaténation des résultats 
    valeur_x = []
    valeur_t = []
    # Stocker uniquement les résultats de la trajectoire circulaire
    valeur_x.append(traj3.y)
    valeur_t.append(traj3.t)
    valeur_x = np.hstack(valeur_x)
    valeur_t = np.hstack(valeur_t)
     
    valeur_x = np.hstack([trajectoire_initiale_x[:,:n], valeur_x])
    valeur_t = np.hstack([trajectoire_initiale_t[:n], valeur_t]) 
    
if True:
    # Stocker la trajectoire avant l'ajustement circulaire
    trajectoire_initiale_x = np.copy(valeur_x)  # Sauvegarde la première partie
    trajectoire_initiale_t = np.copy(valeur_t)
    
    distance_lune=((-valeur_x[0]+1-alpha)**2 + valeur_x[1]**2)**0.5
    dMin = np.min(distance_lune)
    n = np.argmin(distance_lune)
    t_event= valeur_t[n]
    t_eval=np.linspace(t_event,TMAX,N-n)
    
    v_circ = np.sqrt(alpha / dMin)  # Vitesse pour une orbite circulaire à dMin   
    #création des nouvelles CI
    etat_event = traj3.sol(t_event)
    v_event=etat_event[2:]
    x_Min = etat_event[0]
    y_Min = etat_event[1]
    
    #on crée un vecteur directeur dirigée dans le bon sens et tangeant au cercle de rayon dMin
    LM = [x_Min-1+alpha ,y_Min]
    LM_perpandiculaire = [-y_Min,x_Min-1+alpha]
    if np.dot(LM_perpandiculaire,v_event)<0:
        LM_perpandiculaire = [y_Min,-x_Min+1-alpha]
        
    direction = LM_perpandiculaire/np.linalg.norm(LM_perpandiculaire)
    
    coeff_correcteur = r_perigee/rT * 0.552 + 0.390
    etat_event[2:]= direction*v_circ*coeff_correcteur
    CI = etat_event
    
    #nouvelle intégration avec les nouvelles CI et domaine temp
    traj3=solve_ivp(rhs2, 
                      (t_event, TMAX), 
                       CI, 
                       method='RK45', 
                       t_eval=t_eval, 
                       rtol=1.49012e-12, 
                       atol=1.49012e-12, 
                       events=[est_parr_a_TL_dans_le_sens_plus_ux, est_parr_a_TL_dans_le_sens_moins_ux],
                       dense_output=True)
    #concaténation des résultats 
    valeur_x = []
    valeur_t = []
    # Stocker uniquement les résultats de la trajectoire circulaire
    valeur_x.append(traj3.y)
    valeur_t.append(traj3.t)
    valeur_x = np.hstack(valeur_x)
    valeur_t = np.hstack(valeur_t)
     
    valeur_x = np.hstack([trajectoire_initiale_x[:,:n], valeur_x])
    valeur_t = np.hstack([trajectoire_initiale_t[:n], valeur_t]) 
    
    
#calcul des forces le long du trajet : 
val_G1x=-(1-alpha)*(valeur_x[0]+alpha)/((valeur_x[0]+alpha)**2+valeur_x[1]**2)**(3/2)
val_G1y=-(1-alpha)*valeur_x[1]/((valeur_x[0]+alpha)**2+valeur_x[1]**2)**(3/2)
val_G2x=-alpha*(valeur_x[0]-1+alpha)/((valeur_x[0]-1+alpha)**2+valeur_x[1]**2)**(3/2)
val_G2y=-alpha*valeur_x[1]/((valeur_x[0]-1+alpha)**2+valeur_x[1]**2)**(3/2)
val_Ficx=2*valeur_x[3]
val_Ficy=-2*valeur_x[2]
val_Fiex=valeur_x[0]
val_Fiey=valeur_x[1] 

val_G1= np.sqrt(val_G1x**2 + val_G1y**2)
val_G2= np.sqrt(val_G2x**2 + val_G2y**2)
val_Fic= np.sqrt(val_Ficx**2 + val_Ficy**2)
val_Fie= np.sqrt(val_Fiex**2 + val_Fiey**2)

#calcul de l'énergie le long du trajet
Ep1=-(1-alpha)/((valeur_x[0]+alpha)**2+valeur_x[1]**2)**(1/2)
Ep2=-alpha/((valeur_x[0]-1+alpha)**2+valeur_x[1]**2)**(1/2)
Ep3=-.5*(valeur_x[0]**2+valeur_x[1]**2)

Ep= Ep1 +Ep2+ Ep3
Ec=1/2 * D * m /(Cste_G*(MT+ML)) * np.sqrt(valeur_x[2]**2 + valeur_x[3]**2)

Em= Ep + Ec



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


xmax=np.max(valeur_x[:,0]);xmin=np.min(valeur_x[:,0]);xmoy=(xmin+xmax)/2;dx=(xmax-xmin)/2
ymax=np.max(valeur_x[:,1]);ymin=np.min(valeur_x[:,1]);ymoy=(ymin+ymax)/2;dy=(ymax-ymin)/2
beta=1.2
XM=xmoy+dx*beta;Xm=xmoy-dx*beta
Ym=ymoy-dy*beta;YM=ymoy+dy*beta

graphe3.plot(valeur_x[0,:],valeur_x[1,:],'g-',label='$v0=${:.4f}'.format(v0))
graphe2.plot(valeur_x[0,:],valeur_x[1,:],'g-',label='$v0=${:.4f}'.format(v0))
graphe1.plot(valeur_x[0,:],valeur_x[1,:],'g-',label='$v0=${:.4f}'.format(v0))


graphe1.axhline(0,ls='--');graphe1.axvline(0,ls='--')

#graphe1.set_xlim([-0.10,0.10])
#graphe1.set_ylim([-1,1])
#graphe1.set_ylim([ymin-.05*dy,ymax+.05*dy])

graphe1.add_patch(Circle((-alpha,0),RT/D,edgecolor= 'black',fill=False,hatch='//',lw=2.5))
graphe1.add_patch(Circle((1-alpha,0),RL/D,edgecolor= 'black',fill=False,hatch='//',lw=2.5))




graphe3.set_xlim([(1-alpha-dist_max*rL)-0.1,(1-alpha+dist_max*rL)+0.1])
graphe3.set_ylim([(-dist_max*rL)-0.1,(dist_max*rL)+0.1])
graphe3.add_patch(Circle((1-alpha,0),RL/D,edgecolor= 'black',fill=False,hatch='//',lw=2.5))
graphe3.add_patch(Circle((1-alpha,0),10*RL/D,edgecolor= 'black',fill=False,lw=2.5))






graphe2.set_xlim([-alpha-dist_max*rT,-alpha+dist_max*rT])
graphe2.set_ylim([-dist_max*rT,-alpha+dist_max*rT])
graphe2.add_patch(Circle((-alpha,0),RT/D,edgecolor= 'black',fill=False,hatch='\\',lw=2.5))



graphe2.text(-alpha,0,'Terre',ha='center',va='center',bbox=dict(boxstyle="square",ec='red',fc='white',alpha=.8))
graphe3.text(1-alpha,0,'Lune',ha='center',va='center',bbox=dict(boxstyle="square",ec='red',fc='white',alpha=.8))

graphe1.set_aspect('equal', adjustable='box')


graphe4.plot(val_G1,'b-')
graphe4.plot(val_G2,'g-')
graphe4.plot(val_Fic,'r-')
graphe4.plot(val_Fie,'y-')
graphe4.set_ylim([-0.5,10])

























