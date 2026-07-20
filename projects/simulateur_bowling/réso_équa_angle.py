import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.integrate import odeint
from scipy.optimize import fsolve
from math import *

# On définit les ci:
M = 7
R = 0.20
J = 0.4 * M * (R**2)
coef_frottement_dynamique = 1
coef_frottement_statique = 0.5
g = 9.81


# On définit les fonctions:
phi = 0
thêta = pi*1/2
psi = 0
thêta_point = 0
psi_point = 0
phi_point = 1
xo = 0
yo = 0
zo = 0
xo_point = 0
yo_point = -1

# Constantes d'adimensionnement
#vo= (xo_point ** 2 + yo_point ** 2 ) ** (1 / 2)
#if vo==0:
#    vo=1
#Oméga_o=vo / R
#tau= R / vo 


#on définit les costante d'intégration:
A = (tau ** 1 ) * (thêta_point * sin(psi) - phi_point * sin(thêta) * cos(psi)) + xo_point * M * tau / J
B = (tau ** 1 ) * (thêta_point * cos(psi) + phi_point * sin(thêta) * sin(psi)) - yo_point * M * tau / J
C = (tau ** 1 ) * (psi_point + phi_point * cos(thêta))
#on introduit des constante de calcul:
Ro=R+J*M/R
#on définit les vitesses de glissements a t=0
#Vgxo=xo_point * k / vo - A * R
#Vgyo=yo_point * k / vo + B * R


def rhs(x, t):
  Vgx = J*M*A/R - x[1]*Ro*sin(x[4])+Ro*x[3]*sin(x[0])*cos(x[4])
  Vgy = -J*M*B/R + x[1]*Ro*cos(x[4])+Ro*x[3]*sin(x[0])*sin(x[4])
  L1=(J/R)*(x[1]*x[5]*cos(x[4])-x[3]*x[1]*cos(x[0])*cos(x[4])+x[3]*x[5]*sin(x[0])*sin(x[4]))-(coef_frottement_dynamique*M*g/((Vgx**2 + Vgy**2)**(0.5)))*(J*(1/M*R)*A-Ro*x[1]*sin(x[4])+Ro*x[3]*sin(x[0])*cos(x[4]))
  L2=(J/R)*(x[1]*x[5]*sin(x[4])-x[3]*x[1]*cos(x[0])*sin(x[4])-x[3]*x[5]*sin(x[0])*cos(x[4]))-(coef_frottement_dynamique*M*g/((Vgx**2 + Vgy**2)**(0.5)))*(-J*(1/M*R)*B+Ro*x[1]*cos(x[4])+Ro*x[3]*sin(x[0])*sin(x[4]))
  thêta_pointpoint=(R/(J*sin(x[0])))*(sin(x[0])*sin(x[4])*L1+sin(x[0])*cos(x[4])*L2)
  phi_pointpoint = (R/(J*sin(x[0])))*(-cos(x[4])*L1-sin(x[4])*L2)
  psi_pointpoint = -x[3]*cos(x[0])+x[3]*x[1]*sin(x[0])
  if abs(thêta)<10**(-2):
      return [0,0,0,0,0,0]
  #if abs(Vgx)<= 10**(-5) and abs(Vgy)<=10**(-5):
  #    return [R * A / k ,0 ,- R * B / k, 0]
  #if abs(x[0])>5 or x[2]>100 or x[2]<0:
  #    return 
  return [x[1], thêta_pointpoint, x[3], phi_pointpoint,x[5],psi_pointpoint]

TMAX = 1  # durée max de l'intégration exprimée en unité naturelle
N = 600  #nombre de points à calculer
t = np.linspace(0, TMAX, N)  # intervalle de temps d'intégration

CI = [thêta, thêta_point, phi, phi_point,psi, psi_point]  # condition initiale : hauteur=1

traj = odeint(rhs, CI, t)  #on stocke dans la matrice traj[i,j]=y_j(t_i) le resultat de l'integration
taille_graphe = 1.57 * 2
espace_entre_graphes = .28
hauteur = taille_graphe * (2 + 1 * espace_entre_graphes)
largeur = taille_graphe * (2 + 1 * espace_entre_graphes)
fig = figure(figsize=(largeur, hauteur))
graphe1 = fig.add_subplot(221)
graphe2 = fig.add_subplot(222)
graphe3 = fig.add_subplot(223)
graphe4 = fig.add_subplot(224)

graphe1.plot(t, traj[:, 0], 'r-', label="$O(T)$")
graphe1.plot(t, traj[:, 2], 'b-', label="$phi(T)$")
graphe1.plot(t, traj[:, 4], 'g-', label="$psi(T)$")
graphe1.set_xlabel('$T$')
graphe1.set_ylabel('$X$')
#graphe1.set_xlim([0,2]);graphe1.set_ylim([0,.6])
graphe1.axhline(0, ls='--')
graphe1.axvline(0, ls='--')
#liste_x_point=[[t[i],J/(M*R)*(A+traj[i,3]*sin(traj[i,0])*cos(traj[i,4])-traj[:,1]*sin(traj[i,4]))] for i in range(N)]
#graphe2.plot(t, liste_x_point, 'r-', label='$\dot{X}(T)$')
graphe2.set_xlabel('$T$')
graphe2.set_ylabel('$\dot{Z}$')
#graphe2.set_xlim([0,2]);graphe2.set_ylim([-1,1.1])
graphe2.axhline(0, ls='--')
graphe2.axvline(0, ls='--')

graphe3.plot(t, traj[:, 1], 'r-', label="$Vgx$")
graphe3.set_xlabel('$T$')
graphe1.set_ylabel('$Y$')
#graphe1.set_xlim([0,2]);
#graphe3.set_ylim([-.5, .5])
graphe3.axhline(0, ls='--')
graphe1.axvline(0, ls='--')
graphe4.plot(traj[:, 0],traj[:, 2], 'r-', label="$Y(X)$")
graphe4.set_xlabel('$X$')
graphe4.set_ylabel('$Y$')

graphe2.plot(t,traj[:, 1], 'b-', label="$R*wy$")
graphe1.legend()
graphe2.legend()
graphe3.legend()

fig.tight_layout()
plt.show()
#print(traj)

# remarque ici les rotations selon Z n'affectent pas le mouvement puisqu'il n'y a pas de couple de frottement
