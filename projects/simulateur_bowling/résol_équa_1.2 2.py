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
Oméga_x=0
Oméga_y=0
Oméga_z=0


# On définit les fonctions:
phi = 0
thêta = 0
psi = pi/2
thêta_point = 1
psi_point = 0
phi_point = 0
xo = 0
yo = 0
zo = 0
xo_point = 0
yo_point = 0

# Constantes d'adimensionnement
vo= (xo_point ** 2 + yo_point ** 2 ) ** (1 / 2)
if vo==0:
    vo=1
Oméga_o=vo / R
tau= R / vo 


#on définit les costante d'intégration:
A = (tau ** 1 ) * (thêta_point * sin(psi) - phi_point * sin(thêta) * cos(psi)) + xo_point * M * tau / J
B = (tau ** 1 ) * (thêta_point * cos(psi) + phi_point * sin(thêta) * sin(psi)) - yo_point * M * tau / J
C = (tau ** 1 ) * (psi_point + phi_point * cos(thêta))
#on introduit des constante de calcul:
k = (1 + M * (R**2) / J)
Fo = -M * g * coef_frottement_dynamique
print(A, B, C,k)
#on définit les vitesses de glissements a t=0
Vgxo=xo_point * k / vo - A * R
Vgyo=yo_point * k / vo + B * R


def rhs(x, t):
  Vgx = (x[1] * k - A)
  Vgy = (x[3] * k + B)
  x_pointpoint = -R*(1/vo**2)*g * coef_frottement_dynamique * (k * x[1] - A) * (1/((Vgx**2 + Vgy**2)**(0.5)))
  y_pointpoint = -R*(1/vo**2)*g * coef_frottement_dynamique * (k * x[3] + B) * (1/((Vgx**2 + Vgy**2)**(0.5)))
  if abs(Vgx)<= 10**(-5) and abs(Vgy)<=10**(-5):
      return [R * A / k ,0 ,- R * B / k, 0]
  #if abs(x[0])>5 or x[2]>100 or x[2]<0:
  #    return 
  return [x[1], x_pointpoint, x[3], y_pointpoint]

TMAX = 1  # durée max de l'intégration exprimée en unité naturelle
N = 1000  #nombre de points à calculer
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
graphe1.plot(t, traj[:, 2], 'b-', label="$Y(T)$")
graphe1.set_xlabel('$T$')
graphe1.set_ylabel('$X$')
#graphe1.set_xlim([0,2]);graphe1.set_ylim([0,.6])
graphe1.axhline(0, ls='--')
graphe1.axvline(0, ls='--')

graphe2.plot(t, traj[:, 1], 'r-', label='$\dot{X}(T)$')
graphe2.set_xlabel('$T$')
graphe2.set_ylabel('$\dot{Z}$')
#graphe2.set_xlim([0,2]);graphe2.set_ylim([-1,1.1])
graphe2.axhline(0, ls='--')
graphe2.axvline(0, ls='--')

graphe3.plot(t, traj[:, 1]*k-A*R, 'r-', label="$Vgx$")
graphe3.set_xlabel('$T$')
graphe1.set_ylabel('$Y$')
#graphe1.set_xlim([0,2]);
#graphe3.set_ylim([-.5, .5])
graphe3.axhline(0, ls='--')
graphe1.axvline(0, ls='--')
graphe4.plot(traj[:, 0],traj[:, 2], 'r-', label="$Y(X)$")
graphe4.set_xlabel('$X$')
graphe4.set_ylabel('$Y$')

graphe2.plot(t, (traj[:, 1]*(1-k)+A*R), 'b-', label="$R*wy$")
graphe1.legend()
graphe2.legend()
graphe3.legend()

fig.tight_layout()
plt.show()
#print(traj)

# remarque ici les rotations selon Z n'affectent pas le mouvement puisqu'il n'y a pas de couple de frottement
