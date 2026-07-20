import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.integrate import odeint
from scipy.optimize import fsolve
from math import *
import matplotlib.patches as patches
# pour lancée d'amateur: oméga_y=-0.034482758620689724, xo_point=0.017241379310344862
# pour lancée de pro, oméga_y=-1, xo_point=0.26
# On définit les ci:
M = 7
R = 0.20
J = 0.4 * M * (R**2)
coef_frottement_dynamique = 1.5
coef_frottement_statique = 0.5
g = 9.81
Oméga_x=.5
Oméga_y=-1
Oméga_z=0
k = (1 + M * (R**2) / J)

# On définit les fonctions:
phi = 0
thêta = pi/2
psi = 0
xo = 0
yo = 0
zo = 0
xo_point = 0.26
yo_point = 1

# Constantes d'adimensionnement
vo= (xo_point ** 2 + yo_point ** 2 ) ** (1 / 2)
if vo==0:
    vo=((thêta_point * sin(psi) - phi_point * sin(thêta) * cos(psi))**2+(thêta_point * cos(psi) + phi_point * sin(thêta) * sin(psi))**2+(psi_point + phi_point * cos(thêta))**2 )**.5
x1=15*R
y1=300*R
def coef_frottement_d(x,y):
    mu_d=coef_frottement_dynamique*(1-np.exp(-((x/x1)**2+(y/y1)**2)))
    return mu_d

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
def résol(n):
    liste_CI_Oméga_y=np.linspace(Oméga_y, Oméga_y, n)
    liste_CI_xo_point=np.linspace(xo_point,xo_point,n)
    coef_frottement_dynamique2=np.linspace(coef_frottement_dynamique, coef_frottement_dynamique,n)
    TMAX = 15  # durée max de l'intégration exprimée en unité naturelle
    N = 3000  #nombre de points à calculer
    t = np.linspace(0, TMAX, N)  # intervalle de temps d'intégration
    x = np.linspace(-5, 5, 400)
    y = np.linspace(0, 100, 4000)
    X, Y = np.meshgrid(x, y)
    Z = coef_frottement_d(X, Y)
    fig, ax = plt.subplots(figsize=(2, 10))
    ax.imshow(Z, extent=[-1, 1, 0, 10], origin='lower', cmap='viridis')
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 10)
    triangle_vertices = [(-0.65, 9.65), (0, 8.65), (0.65, 9.65)]
    triangle = patches.Polygon(triangle_vertices, closed=True, edgecolor='black', facecolor='black')
    ax.add_patch(triangle)
    # Ajouter des labels et un titre
    ax.set_xlabel('x',fontsize=20)
    ax.set_ylabel('y',fontsize=20)
    ax.set_title('piste de bowling',fontsize=20)
    for i in range(n):
        def coef_frottement_d(x,y):
            mu_d=coef_frottement_dynamique2[i]*(1-np.exp(-((x/x1)**2+(y/y1)**2)))
            return mu_d
        def inversion(Oméga_x,Oméga_y,Oméga_z):
            thêta_point = cos(psi) * Oméga_x + sin(psi) * Oméga_y
            phi_point= (1 / sin(thêta)) * (sin(psi) * Oméga_x - cos(psi) * Oméga_y)
            psi_point=Oméga_z - phi_point * cos(thêta)
            return(thêta_point, phi_point, psi_point)

        thêta_point, phi_point, psi_point = inversion(Oméga_x, liste_CI_Oméga_y[i], Oméga_z)
        A =  (thêta_point * sin(psi) - phi_point * sin(thêta) * cos(psi)) + liste_CI_xo_point[i] * (k-1)
        B =  (thêta_point * cos(psi) + phi_point * sin(thêta) * sin(psi)) - yo_point * (k-1)
        C = (psi_point + phi_point * cos(thêta))
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
        CI = [xo, liste_CI_xo_point[i], yo, yo_point]
        traj = odeint(rhs, CI, t, full_output=0)
        ax.plot(traj[:, 0],traj[:, 2], color=colors[i % len(colors)])
    plt.show()   
      # Définir les limites des axes
  
print(résol(5))    
    

