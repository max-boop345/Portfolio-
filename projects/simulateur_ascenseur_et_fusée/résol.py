import sympy as sp
from scipy.integrate import odeint, solve_ivp
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt 

G = 6.67*(10**-11)
Mt = 6*(10**24) #les masses en kg
Ml = 7.4*(10**22)
M = 1000
rTL = 384400000 #distance terre lune en m

#CI
GM0 = 0.5 # en m
theta0 = np.pi/2 #en rad ?
z0 = 0
GM0_point = 0.5 # en m/s
theta0_point = 0 # en rad/s
z0_point = 0


#Adimentionement
w0 = sqrt(G*(Mt+Ml)/(rTL**3))
v0 = sqrt(GM0_point**2+z0_point**2+(GM0*theta0_point)**2)
t0 = rTL/v0
a0 = v0*t0
mt = Mt/(Mt+Ml)
ml = Ml/(Mt+Ml)
m = M/(Mt+Ml)

t = sp.symbols('t')

#création vecteur position r (TL) dans (R') référentielle lié à r en rotation à vitesse w0 dans (R) galliléen
theta_r= w0 * t
r = sp.Matrix([rTL,0,0])


#creation vecteur position, vitesse et accélération du point M 
GM = sp.Function('GM')(t)
GM_point = sp.diff(GM,t)
#GM_2point = sp.diff(GM,t,2)
theta = sp.Function('theta')(t)
theta_point = sp.diff(theta,t)
#theta_2point = sp.diff(theta,t,2)
z = sp.Function('z')(t)
z_point = sp.diff(z,t)
#z_2point = sp.diff(z,t,2)
position = sp.Matrix([GM, 0, z])
vitesse = sp.Matrix([GM_point, GM * theta_point, z_point])
#acceleration = sp.Matrix([GM_2point - GM * theta_point**2, 2*GM_point*theta_point + GM*theta_2point, z_2point ])

#création vecteur des forces /M
GT = ml * sp.Matrix([-sp.cos(theta)*rTL, sp.sin(theta)*rTL, 0])
GL = mt * sp.Matrix([sp.cos(theta)*rTL, -sp.sin(theta)*rTL, 0])
TM= position - GT
LM = position - GL

FT_M = - 1/a0 * G*Mt/((TM.norm())**3) * TM
FL_M = - 1/a0 * G*Ml/((LM.norm())**3) * LM
Fie = 1/a0 * w0**2 * sp.Matrix([position[0],0,0])
Fic = - 1/a0 * 2*sp.Matrix([0,0,w0]).cross(vitesse)


# Conversion en fonction Python
FT_M_func = sp.lambdify([GM, theta, z], FT_M, "numpy")
FL_M_func = sp.lambdify([GM, theta, z], FL_M, "numpy")
Fie_func = sp.lambdify([GM, theta], Fie, "numpy")
Fic_func = sp.lambdify([GM, GM_point, theta, theta_point, z, z_point], Fic, "numpy")


def rhs(x, t):
    GM = x[0]
    GM_point = x[1]
    theta = x[2]
    theta_point = x[3]
    z = x[4]
    z_point = x[5]

    # Calcul des forces avec les valeurs actuelles de GM, theta, et z
    FT_M_val = FT_M_func(GM, theta, z).flatten()
    FL_M_val = FL_M_func(GM, theta, z).flatten()
    Fie_val = Fie_func(GM, theta).flatten()
    Fic_val = Fic_func(GM, GM_point, theta, theta_point, z, z_point).flatten()
    
    
    GM_2point = GM*theta_point**2 + FT_M_val[0] + FL_M_val[0] + Fie_val[0] + Fic_val[0]
    theta_2point = -2*GM_point*theta_point + FT_M_val[1] + FL_M_val[1] + Fie_val[1] + Fic_val[1]
    z_2point = FT_M_val[2] + FL_M_val[2] + Fie_val[2] + Fic_val[2]
    
    return [GM_point,GM_2point, theta_point,theta_2point, z_point,z_2point]


TMAX = 10  # durée max de l'intégration exprimée en unité naturelle
N = 1000  #nombre de points à calculer
t = np.linspace(0, TMAX, N)  # intervalle de temps d'intégration

CI = [GM0,GM0_point/v0, theta0,theta0_point, z0,z0_point]  # condition initiale : hauteur=1

traj = odeint(rhs, CI, t)  #on stocke dans la matrice traj[i,j]=y_j(t_i) le resultat de l'integration

taille_graphe = 1.57 * 2
espace_entre_graphes = .28
hauteur = taille_graphe * (2 + 1 * espace_entre_graphes)
largeur = taille_graphe * (2 + 1 * espace_entre_graphes)
fig = plt.figure(figsize=(largeur, hauteur))
graphe1 = fig.add_subplot(221)
graphe2 = fig.add_subplot(222)
graphe3 = fig.add_subplot(223)
graphe4 = fig.add_subplot(224)

graphe1.plot(t, traj[:, 0], 'r-', label="$GM(T)$")
graphe1.plot(t, traj[:, 2], 'b-', label="$theta(T)$")
graphe1.set_xlabel('$T$')
graphe1.set_ylabel('$X$')
#graphe1.set_xlim([0,2]);graphe1.set_ylim([0,.6])
graphe1.axhline(0, ls='--')
graphe1.axvline(0, ls='--')

graphe2.plot(t, traj[:, 1], 'r-', label='$\dot{GM}(T)$')
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
graphe4.set_xlabel('$GM$')
graphe4.set_ylabel('$theta$')

#graphe2.plot(t, traj[:, 1], 'b-', label="$R*wy$")
graphe1.legend()
graphe2.legend()
graphe3.legend()

fig.tight_layout()
plt.show()
#print(traj)


