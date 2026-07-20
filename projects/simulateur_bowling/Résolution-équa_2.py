import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.integrate import odeint
from scipy.optimize import fsolve
from math import *
from scipy.integrate import solve_ivp

# On définit les ci:
M = 7
R = 0.20
J = 0.4 * M * (R**2)
coef_frottement_dynamique = 1
coef_frottement_statique = 0.5
g = 9.81
Oméga_x=0
Oméga_y=0
Oméga_z=0

def inversion(Oméga_x,Oméga_y, Oméga_z):
    theta_point=( - sin(thêta) * cos(psi) * Oméga_x - sin(thêta) * sin(psi) * Oméga_y ) / sin(thêta)
    phi_point=( - sin(psi) * Oméga_x + cos(psi) * Oméga_y) / sin(thêta)
    psi_point= Oméga_z - phi_point * cos(thêta)
    return theta_point, psi_point, phi_point

# On définit les fonctions:
phi = 0
thêta = np.pi/2
psi = 0
thêta_point, psi_point, phi_point = inversion(Oméga_x,Oméga_y,Oméga_z)[0], inversion(Oméga_x,Oméga_y,Oméga_z)[1], inversion(Oméga_x,Oméga_y,Oméga_z)[2]
print (thêta_point, psi_point, phi_point)
phi_point=-1

xo = 0
yo = 0
zo = 0
xo_point = -1
yo_point = 0

# Constantes d'adimensionnement
vo= (xo_point ** 2 + yo_point ** 2 ) ** (1 / 2)
Oméga_o=vo / R
tau= R / vo



#on définit les costante d'intégration:
A = tau * (thêta_point * sin(psi) - phi_point * sin(thêta) * cos(psi) + xo_point * M / J)
B = tau * (thêta_point * cos(psi) + phi_point * sin(thêta) * sin(psi) - yo_point * M / J)
C = tau * (psi_point + phi_point * cos(thêta))
#on introduit des constante de calcul:
k = (1 + M * (R**2) / J)
Fo = -M * g * coef_frottement_dynamique
#print(A, B, C,k)
#on définit les vitesses de glissements a t=0
Vgxo=(1 / vo) * xo_point * k - A * R
Vgyo=(1 / vo) * yo_point * k + B * R


TMAX = 5  # durée max de l'intégration exprimée en unité naturelle, ie 1 tau
N = 5000 #nombre de points à calculer
t = np.linspace(0, TMAX, N)  # intervalle de temps d'intégration

CI = [xo / R, xo_point / vo, yo / R, yo_point / vo]  # condition initiale : hauteur=1, vitesse nulle

taille_graphe = 1.57 * 2
espace_entre_graphes = .28
hauteur = taille_graphe * (2 + 1 * espace_entre_graphes)
largeur = taille_graphe * (2 + 1 * espace_entre_graphes)
fig = figure(figsize=(largeur, hauteur))


def rhs(t,x):
    Vgx = x[1] * k - A * R
    Vgy = x[3] * k + B * R
    x_pointpoint = (R / (M * (vo ** 2 ) )) * (Fo * k * x[1] - Fo * A * R) / ((Vgx**2 + Vgy**2)**(0.5))
    y_pointpoint = (R / (M * (vo ** 2 ) )) * (Fo * k * x[3] + Fo * B * R) / ((Vgx**2 + Vgy**2)**(0.5))
  #if abs(Vgx) <=Vgxo*(10**(-2)) or abs(Vgy) <=Vgyo*(10**(-2)):
    #return [0, 0, 0, 0]
  #else:
    #return [x[1], x_pointpoint, x[3], y_pointpoint]
    return [x[1], x_pointpoint, x[3], y_pointpoint]



def vitesse_nulle(t, x): 
    """pour éviter des divergences"""
    Vgx = x[1] * k / vo - A * R
    Vgy = x[3] * k / vo + B * R
    Vg=(Vgx**2 + Vgy**2)**(0.5)
    return Vg-1e-2

vitesse_nulle.terminal = True

evenements=[vitesse_nulle]


sol=solve_ivp(rhs,t_span=(0,TMAX),y0=CI,t_eval=t,events=evenements)#,method='DOP853')

fig=figure(figsize=(largeur,hauteur))
graphe1=fig.add_subplot(131)
graphe2=fig.add_subplot(132)
graphe3=fig.add_subplot(133)
    
graphe1.plot(sol.t,sol.y[0],'r-',label="$X(T)$")
graphe3.plot(sol.t,sol.y[1]*k-A*R, 'r-', label="$Vgx$")
graphe3.plot(sol.t, sol.y[3]*k+B*R, 'b-', label="$Vgy$")

    
fig.tight_layout()
