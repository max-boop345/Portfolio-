import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.integrate import odeint
from scipy.optimize import fsolve
from math import *
import matplotlib.patches as patches

# On définit les ci:
M = 7
R = 0.20
J = 0.4 * M * (R**2)
coef_frottement_dynamique = 1.5
coef_frottement_dynamique2 =np.linspace(coef_frottement_dynamique*0.5, 2*coef_frottement_dynamique,4)
coef_frottement_statique = 0.5
print(coef_frottement_dynamique2)
g = 9.81
Oméga_x=0.5
Oméga_y=-1
Oméga_z=0


# On définit les fonctions:
phi = 0
thêta = pi/2
psi = 0
def inversion(Oméga_x,Oméga_y,Oméga_z):
    thêta_point = cos(psi) * Oméga_x + sin(psi) * Oméga_y
    phi_point= (1 / sin(thêta)) * (sin(psi) * Oméga_x - cos(psi) * Oméga_y)
    psi_point=Oméga_z - phi_point * cos(thêta)
    return(thêta_point, phi_point, psi_point)

thêta_point, phi_point, psi_point = inversion(Oméga_x, Oméga_y, Oméga_z)    
#thêta_point = 0
#psi_point = 0
#phi_point = -5
xo = 0
yo = 0
zo = 0
xo_point = 0.26
yo_point = 1

# Constantes d'adimensionnement
vo= (xo_point ** 2 + yo_point ** 2 ) ** (1 / 2)
if vo==0:
    vo=((thêta_point * sin(psi) - phi_point * sin(thêta) * cos(psi))**2+(thêta_point * cos(psi) + phi_point * sin(thêta) * sin(psi))**2+(psi_point + phi_point * cos(thêta))**2 )**.5


k = (1 + M * (R**2) / J)
#on définit les costante d'intégration:
A =  (thêta_point * sin(psi) - phi_point * sin(thêta) * cos(psi)) + xo_point * (k-1)
B =  (thêta_point * cos(psi) + phi_point * sin(thêta) * sin(psi)) - yo_point * (k-1)
C = (psi_point + phi_point * cos(thêta))
#on introduit des constante de calcul:
print(A,B)
Fo = -M * g * coef_frottement_dynamique
#print(A, B, C,k)
#on définit les vitesses de glissements a t=0
Vgxo=xo_point * k / vo - A * R
Vgyo=yo_point * k / vo + B * R

x1=15*R
y1=300*R
def coef_frottement_d(x,y):
    mu_d=coef_frottement_dynamique2[1]*(1-np.exp(-((x/x1)**2+(y/y1)**2)))
    return mu_d


def rhs(x, t):
  Vgx = (x[1] * k - A)
  Vgy = (x[3] * k + B)
  alpha=g*R*coef_frottement_d(x[0],x[2])/(vo**2)
  norme_Vg=(Vgx**2 +Vgy**2)**0.5
  if abs(Vgx)<= 10**(-5) and abs(Vgy)<=10**(-5):
      return [ A / k ,0 ,- B / k, 0]
  x_pointpoint = -alpha * Vgx /norme_Vg
  y_pointpoint = -alpha * Vgy /norme_Vg     
  return [x[1], x_pointpoint, x[3], y_pointpoint]

TMAX = 15  # durée max de l'intégration exprimée en unité naturelle
N = 3000  #nombre de points à calculer
t = np.linspace(0, TMAX, N)  # intervalle de temps d'intégration

CI = [xo, xo_point, yo, yo_point]  # condition initiale : hauteur=1

traj = odeint(rhs, CI, t, full_output=0)  #on stocke dans la matrice traj[i,j]=y_j(t_i) le resultat de l'integration
def affiche_sol():
    taille_graphe = 1.57 * 2
    espace_entre_graphes = .28
    hauteur = taille_graphe * (2 + 1 * espace_entre_graphes)
    largeur = taille_graphe * (2 + 1 * espace_entre_graphes)
    fig = figure(figsize=(largeur, hauteur))
    graphe1 = fig.add_subplot(221)
    graphe2 = fig.add_subplot(222)
    graphe3 = fig.add_subplot(223)
    graphe4 = fig.add_subplot(224)
    
    graphe3.plot(t, traj[:, 0], 'r-', label="$X(T)$")
    graphe3.plot(t, traj[:, 2], 'b-', label="$Y(T)$")
    graphe3.set_xlabel('$T$',fontsize=20)
    graphe3.set_ylabel('$X$',fontsize=20)
    #graphe1.set_xlim([0,2]);graphe1.set_ylim([0,.6])
    graphe3.axhline(0, ls='--')
    graphe3.axvline(0, ls='--')
    
    graphe2.plot(t, traj[:, 3], 'r-', label='$\dot{Y}(T)$')
    graphe2.set_xlabel('$T$',fontsize=20)
    #graphe2.set_ylabel('$\dot{Z}$')
    #graphe2.set_xlim([0,2]);graphe2.set_ylim([-1,1.1])
    graphe2.axhline(0, ls='--')
    graphe2.axvline(0, ls='--')
    
    graphe1.plot(t, traj[:, 3]*k+B, 'b-', label="$Vgy$")
    graphe1.plot(t, traj[:, 1]*k-A, 'r-', label="$Vgx$")
    graphe1.set_xlabel('$T$',fontsize=20)
    #graphe3.set_ylabel('$Y$')
    #graphe1.set_xlim([0,2]);
    #graphe3.set_ylim([-.5, .5])
    graphe1.axhline(0, ls='--')
    graphe1.axvline(0, ls='--')
    graphe4.plot(traj[:, 0],traj[:, 2], 'r-', label="$Y(X)$")
    graphe4.set_xlabel('$X$',fontsize=20)
    graphe4.set_ylabel('$Y$',fontsize=20)
    graphe4.set_xlim([-1,1]);
    graphe2.plot(t, (traj[:, 3]*(1-k)-B), 'b-', label="$R*wx$")
    graphe1.legend(fontsize=20)
    graphe2.legend(fontsize=20)
    graphe3.legend(fontsize=20)

    fig.tight_layout()
    plt.show()
    #print(traj)

def affiche_graphe():
   x = np.linspace(-5, 5, 400)
   y = np.linspace(0, 100, 4000)
   X, Y = np.meshgrid(x, y)

   # Calculer les valeurs de la fonction sur la grille
   Z = coef_frottement_d(X, Y)

   # Afficher les valeurs avec imshow
   plt.imshow(Z, extent=[-1, 1, 0, 10], origin='lower', cmap='viridis')
   plt.colorbar()  # Ajouter une barre de couleur
   plt.title('mu_d(x, y)',fontsize=14)
   plt.xlabel('x')
   plt.ylabel('y')
   plt.show()
   
def affiche_xy():
    triangle_vertices = [(-0.65, 9.65), (0, 8.65), (0.65, 9.65)]
    triangle = patches.Polygon(triangle_vertices, closed=True, edgecolor='black', facecolor='black')
    x = np.linspace(-5, 5, 400)
    y = np.linspace(0, 100, 4000)
    X, Y = np.meshgrid(x, y)
    
    # Calculer les valeurs de la fonction sur la grille
    Z = coef_frottement_d(X, Y)
    fig, ax = plt.subplots(figsize=(2, 10))
    c = ax.imshow(Z, extent=[-1, 1, 0, 10], vmax=3, origin='lower', cmap='viridis')
    # Tracer la courbe (par exemple, une ligne droite de x à y)
    ax.plot(traj[:, 0],traj[:, 2], 'r-', label="$Y(X)$")

    # Définir les limites des axes
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 10)
    
    # Ajouter des labels et un titre
    ax.set_xlabel('x',fontsize=20)
    ax.set_ylabel('y',fontsize=20)
    ax.set_title('piste de bowling',fontsize=20)
    ax.add_patch(triangle)
    fig.colorbar(c, ax=ax)

 
    # Afficher le graphique
    plt.show()

print(affiche_sol())
print(affiche_xy())
#print(affiche_graphe())

# remarque ici les rotations selon Z n'affectent pas le mouvement puisqu'il n'y a pas de couple de frottement
