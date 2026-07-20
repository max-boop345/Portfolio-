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
thêta = 0
psi = pi * 1 / 2
thêta_point = 20
psi_point = 0
phi_point = 0
xo = 0
yo = 0
zo = 0
xo_point = 0
yo_point = 0


#on définit les costante d'intégration:
A = thêta_point * sin(psi) - phi_point * sin(thêta) * cos(
    psi) - xo_point * M * R / J
B = thêta_point * cos(psi) + phi_point * sin(thêta) * sin(
    psi) - yo_point * M * R / J
C = psi_point + phi_point * cos(thêta)
#on introduit des constante de calcul:
k = (1 + M * (R**2) / J)

#on définit une fonction pour calculer un coef de frottement qui dépend de la position
x1=100000*R
y1=100000*R
def coef_frottement_d(x,y):
    mu_d=coef_frottement_dynamique*exp(-((x/x1)**2+(y/y1)**2))
    return mu_d
    

#print(A, B, C,k)
#on définit les vitesses de glissements a t=0
Vgxo=xo_point*k-A*R
Vgyo=yo_point*k+B*R


def rhs(x, t):
  Fo = -M * g * coef_frottement_d(x[0],x[2])
  Vgx = x[1] * k - A * R
  Vgy = x[3] * k + B * R
  x_pointpoint = (1 / M) * Fo * (k * x[1] - A * R) * (1/((Vgx**2 + Vgy**2)**(0.5)))
  y_pointpoint = (1 / M) * Fo * (k * x[3] + B * R) * (1/((Vgx**2 + Vgy**2)**(0.5)))
  if abs(Vgx)<= 10**(-5) and abs(Vgy)<=10**(-5):
      return [R * A / k ,0 ,- R * B / k, 0]
  return [x[1], x_pointpoint, x[3], y_pointpoint]

TMAX = .2  # durée max de l'intégration exprimée en unité naturelle
N = 5000  #nombre de points à calculer
t = np.linspace(0, TMAX, N)  # intervalle de temps d'intégration

CI = [xo, xo_point, yo, yo_point]  # condition initiale : hauteur=1

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

graphe1.plot(t, traj[:, 0], 'r-', label="$X(T)$")
#graphe1.set_xlabel('$T$')
#graphe1.set_ylabel('$Z$')
#graphe1.set_xlim([0,2]);graphe1.set_ylim([0,.6])
graphe1.axhline(0, ls='--')
graphe1.axvline(0, ls='--')

graphe2.plot(t, traj[:, 1], 'r-', label='$\dot{X}(T)$')
#graphe2.set_xlabel('$T$')
#graphe2.set_ylabel('$\dot{Z}$')
#graphe2.set_xlim([0,2]);graphe2.set_ylim([-1,1.1])
graphe2.axhline(0, ls='--')
graphe2.axvline(0, ls='--')

graphe3.plot(t, traj[:, 1]*k-A*R, 'r-', label="$Vgx$")
graphe1.set_xlabel('$T$',fontsize=20)
graphe2.set_xlabel('$T$',fontsize=20)
graphe3.set_xlabel('$T$',fontsize=20)
#graphe1.set_ylabel('$Y$')
#graphe1.set_xlim([0,2]);
#graphe3.set_ylim([-.5, .5])
graphe3.axhline(0, ls='--')
graphe1.axvline(0, ls='--')

graphe2.plot(t, (traj[:, 1]*(1-k)+A*R), 'b-', label="$R*wy$")
graphe1.legend(fontsize=20)
graphe2.legend(fontsize=20)
graphe3.legend(fontsize=20)


fig.tight_layout()
plt.show()
#print(traj)
