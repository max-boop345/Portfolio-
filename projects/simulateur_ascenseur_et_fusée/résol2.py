from scipy.integrate import odeint, solve_ivp
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt 

G = 6.67e-11
Mt = 6e24 #les masses en kg
Ml =  0#7.4e22
M = 1
rTL = 384400000 #distance terre lune en m

#CI
x0 = .5 # en m
y0 = 0.1 #en rad ?
z0 = 0
x0_point = 0 # en m/s
y0_point = 0 # en rad/s
z0_point = 0


#Adimentionement
w0 = sqrt(G*(Mt+Ml)/(rTL**3))
t0 = 2*np.pi/w0
v0 = rTL/t0

a0 = v0*t0
mt = Mt/(Mt+Ml)
ml = Ml/(Mt+Ml)
m = M/(Mt+Ml)

def rhs(x,t):
    x, x_point, y, y_point, z, z_point = x[0], x[1], x[2], x[3], x[4], x[5]
    normeTM= sqrt((x+ml*rTL)**2 + (y)**2 + z**2)
    normeLM= sqrt((x-mt*rTL)**2 + (y)**2 + z**2)
    
    Ftm=-G*Mt/(a0*normeTM**3)
    Flm=-G*Ml/(a0*normeLM**3)
    
    
    x_2point = Ftm * (x+ml*rTL) + Flm * (x-mt*rTL) + (w0**2) *x/a0 +2*w0*y_point/a0
    y_2point =  Ftm*y + Flm*y - 2*w0*x_point/a0
    z_2point = Ftm*z+Flm*z
    
    return [x_point, x_2point, y_point, y_2point, z_point, z_2point]

TMAX =1  # durée max de l'intégration exprimée en unité naturelle
N = 1000#nombre de points à calculer
t = np.linspace(0, TMAX, N)  # intervalle de temps d'intégration

CI = [x0,x0_point/v0, y0,y0_point, z0,z0_point]  # condition initiale : hauteur=1

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

graphe1.plot(t, traj[:, 0], 'r-', label="$x(T)$")
#graphe1.plot(t, traj[:, 2], 'b-', label="$theta(T)$")
graphe1.set_xlabel('$T$')
graphe1.set_ylabel('$X$')
#graphe1.set_xlim([0,2]);graphe1.set_ylim([0,.6])
graphe1.axhline(0, ls='--')
graphe1.axvline(0, ls='--')

graphe2.plot(t, ((traj[:, 0]+ml*rTL)**2+traj[:,2]**2)/(6371000/rTL), 'r-', label='$\dot{x}(T)$')
graphe2.set_xlabel('$T$')
graphe2.set_ylabel('$\dot{Z}$')
graphe2.set_xlim([0,2]);graphe2.set_ylim([0,10**6])
graphe2.axhline(0, ls='--')
graphe2.axvline(0, ls='--')

graphe3.plot(t, -(traj[:,1]**2+traj[:,3]**2)/2 - mt/np.sqrt((traj[:,0]+ml)**2+traj[:,2]**2) - ml/np.sqrt((traj[:,0]-1+ml)**2+traj[:,2]**2), 'r-', label="$EP$")
graphe3.plot(t, 0.5*(traj[:,1]**2+traj[:,3]**2),'b', label="$EC$")
graphe3.plot(t,-(traj[:,1]**2+traj[:,3]**2)/2 - mt/np.sqrt((traj[:,0]+ml)**2+traj[:,2]**2) - ml/np.sqrt((traj[:,0]-1+ml)**2+traj[:,2]**2) + 0.5*(traj[:,1]**2+traj[:,3]**2),'g', label="$EM$" )
graphe3.set_xlabel('$T$')
graphe1.set_ylabel('$x$')
#graphe1.set_xlim([0,2]);
#graphe3.set_ylim([-.5, .5])
graphe3.axhline(0, ls='--')
graphe1.axvline(0, ls='--')
graphe4.plot(traj[:,0],traj[:,2], 'r-', label="$Y(X)$")
graphe4.set_xlabel('$x$')
graphe4.set_ylabel('$y$')

#graphe2.plot(t, traj[:, 1], 'b-', label="$R*wy$")
graphe1.legend()
graphe2.legend()
graphe3.legend()

fig.tight_layout()
plt.show()
#print(traj)

    