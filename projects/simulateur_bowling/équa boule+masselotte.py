import sympy as sp
from scipy.integrate import odeint, solve_ivp
import numpy as np
import matplotlib.pyplot as plt
#from numba import jit

# On introduit des constantes
M = 7
m = .1 * M
R = 0.20
J = 0.4 * M * (R**2)
l = 0.1 * R
coef_frottement_dynamique = 1.5
coef_frottement_statique = 0.5
g = 9.81


# Définir les variables et fonctions symboliques
t = sp.symbols('t')

# On définit les angles d'euler
theta = sp.Function('theta')(t)
psi = sp.Function('psi')(t)
phi = sp.Function('phi')(t)
angle = sp.Matrix([theta, psi, phi])

# On définit les coordonées de B
x = sp.Function('x')(t)
y = sp.Function('y')(t)
x_point = sp.diff(x, t)
y_point = sp.diff(y, t)
x_pointpoint = sp.diff(x_point ,t)
y_pointpoint = sp.diff(y_point ,t)
pos_B = sp.Matrix([x, y, R])
vB = sp.diff(pos_B)
aB = sp.diff(vB)

# On définit le vecteur BA


# Définir les dérivées par rapport à t
theta_point = sp.diff(theta, t)
psi_point = sp.diff(psi, t)
phi_point = sp.diff(phi, t)
theta_pointpoint = sp.diff(theta_point, t)
psi_pointpoint = sp.diff(psi_point, t)
phi_pointpoint = sp.diff(phi_point, t)

# Construire Oméga
wx = theta_point * sp.cos(t).subs(t, psi) + phi_point * \
    sp.sin(t).subs(t, theta) * sp.sin(t).subs(t, psi)
wy = theta_point * sp.sin(t).subs(t, psi) - phi_point * \
    sp.sin(t).subs(t, theta) * sp.cos(t).subs(t, psi)
wz = psi_point + phi_point * sp.cos(t).subs(t, theta)
Omega = sp.Matrix([wx, wy, wz])
Omega_point = sp.diff(Omega)

# calcul de l'accélération de A                  BA=l*z(theta)
xa = x + l * sp.sin(t).subs(t, theta) * sp.sin(t).subs(t, psi)
ya = y - l * sp.sin(t).subs(t, theta) * sp.cos(t).subs(t, psi)
za = R + l * sp.cos(t).subs(t, theta)
pos_A = sp.Matrix([xa, ya, za])
pos_BA = sp.Matrix([xa - x, ya - y, za - R])
# v(A/R) = v(B/R) + v(A/R') + Oméga^BA
vAx_Rb = l * theta_point * (sp.cos(t).subs(t, theta) * sp.sin(t).subs(t, phi))
vAy_Rb = -l * theta_point * (sp.cos(t).subs(t, theta) * sp.cos(t).subs(t, phi))
vAz_Rb = -l * theta_point * sp.sin(t).subs(t, theta)
vA_Rb = sp.Matrix([vAx_Rb, vAy_Rb, vAz_Rb])
vA = vB + vA_Rb + Omega.cross(pos_BA)
# a(A/R)= a(B/R)+a(A/R')+ 2 Omega ^ v(A/R') + Omega_point ^ BA + Omega^(Omega^BA)
aAx_Rb = l * theta_pointpoint * sp.cos(t).subs(t, theta) * sp.sin(t).subs(
    t, psi) - l * theta_point ** 2 * sp.sin(t).subs(t, theta) * sp.sin(t).subs(t, psi)
aAy_Rb = - l * theta_pointpoint * (sp.cos(t).subs(t, theta) * sp.cos(t).subs(
    t, phi)) + l * theta_point ** 2 * sp.sin(t).subs(t, theta) * sp.cos(t).subs(t, psi)
aAz_Rb = - l * theta_pointpoint * \
    sp.sin(t).subs(t, theta) - l * theta_point ** 2 * sp.cos(t).subs(t, theta)
aA_Rb = sp.Matrix([aAx_Rb, aAy_Rb, aAz_Rb])
aA = aB + aA_Rb + 2 * \
    Omega.cross(vA_Rb) + Omega_point.cross(pos_BA) + \
    Omega.cross(Omega.cross(pos_BA))

# calcul de l'accélération de G
xG = x + (m / (m + M)) * l * sp.sin(t).subs(t, theta) * sp.sin(t).subs(t, psi)
yG = y - (m / (m + M)) * l * sp.sin(t).subs(t, theta) * sp.cos(t).subs(t, psi)
zG = R + (m / (m + M)) * l * sp.cos(t).subs(t, theta)
pos_G = sp.Matrix([xG, yG, zG])
pos_BG = sp.Matrix([xG - x, yG - y, zG - R])
# v(G/R) = v(B/R) + v(G/R') + Oméga^BG
vGx_Rb = (m / (m + M)) * l * theta_point * \
    (sp.cos(t).subs(t, theta) * sp.sin(t).subs(t, phi))
vGy_Rb = -(m / (m + M)) * l * theta_point * \
    (sp.cos(t).subs(t, theta) * sp.cos(t).subs(t, phi))
vGz_Rb = -(m / (m + M)) * l * theta_point * sp.sin(t).subs(t, theta)
vG_Rb = sp.Matrix([vGx_Rb, vGy_Rb, vGz_Rb])
vG = vB + vG_Rb + Omega.cross(pos_BG)
# a(A/R)= a(B/R)+a(A/R')+ 2 Omega ^ v(A/R') + Omega_point ^ BA + Omega^(Omega^BA)
aGx_Rb = (m / (m + M)) * l * theta_pointpoint * sp.cos(t).subs(t, theta) * sp.sin(t).subs(t, psi) - \
    (m / (m + M)) * l * theta_point ** 2 * \
    sp.sin(t).subs(t, theta) * sp.sin(t).subs(t, psi)
aGy_Rb = - (m / (m + M)) * l * theta_pointpoint * (sp.cos(t).subs(t, theta) * sp.cos(t).subs(t, phi)
                                                   ) + (m / (m + M)) * l * theta_point ** 2 * sp.sin(t).subs(t, theta) * sp.cos(t).subs(t, psi)
aGz_Rb = - (m / (m + M)) * l * theta_pointpoint * sp.sin(t).subs(t, theta) - \
    (m / (m + M)) * l * theta_point ** 2 * sp.cos(t).subs(t, theta)
aG_Rb = sp.Matrix([aGx_Rb, aGy_Rb, aGz_Rb])
aG = aB + aG_Rb + 2 * \
    Omega.cross(vG_Rb) + Omega_point.cross(pos_BG) + \
    Omega.cross(Omega.cross(pos_BG))


# Écriture de Vg
Vg = vB + Omega.cross(sp.Matrix([0, 0, -R]))
norme_Vg = Vg.norm()
# Écriture des
# Bilan des forces:
P_B = sp.Matrix([0, 0, -M * g])
P_A = sp.Matrix([0, 0, -m * g])
N = sp.Matrix([0, 0, aA[2]]) - P_A - P_B
# On définit T
Tx = sp.Piecewise(((-coef_frottement_dynamique * N.norm() / norme_Vg)
                  * Vg[0], norme_Vg != 0), (M * aB[0] + m * aA[0], norme_Vg == 0))
Ty = sp.Piecewise(((-coef_frottement_dynamique * N.norm() / norme_Vg)
                  * Vg[1], norme_Vg != 0), (M * aB[1] + m * aA[1], norme_Vg == 0))
T = sp.Matrix([Tx, Ty, 0])

# TRC
TRC = sp.Eq(M * aB + m * aA, P_B + P_A + N + T)
TRC1 = sp.Eq(M * aB[0] + m * aA[0], P_B[0] + P_A[0] + N[0] + T[0])
TRC2 = sp.Eq(M * aB[1] + m * aA[1], P_B[1] + P_A[1] + N[1] + T[1])
TRC3 = sp.Eq(M * aB[2] + m * aA[2], P_B[2] + P_A[2] + N[2] + T[2])

# Bilan des Moments en B

MP_A = pos_BA.cross(P_A)
MT = sp.Matrix([0, 0, -R]).cross(T)

# TMC
# Calcul de L_B
L_B = J * Omega + pos_BG.cross((m+M)*vG)
L_B_point = sp.diff(L_B, t)

TMC = sp.Eq(L_B_point, MP_A + MT)
TMC1 = sp.Eq(L_B_point[0], MP_A[0] + MT[0])
TMC2 = sp.Eq(L_B_point[1], MP_A[1] + MT[1])
TMC3 = sp.Eq(L_B_point[2], MP_A[2] + MT[2])

# On crée une matrice pour inverser le système
equations=[TRC1, TRC2, TMC1, TMC2, TMC3]
equations_Vg=[TMC1, TMC2, TMC3]          #On à d'autres systèmes d'eq si Vg=0
variables=[x_pointpoint, y_pointpoint, theta_pointpoint, psi_pointpoint, phi_pointpoint]
variables_Vg=[theta_pointpoint, psi_pointpoint, phi_pointpoint]
def generate_matrix(equations, variables):
    # Initialiser les matrices des coefficients et des termes constants
    A = sp.zeros(len(equations), len(variables))
    B = sp.zeros(len(equations), 1)
    
    # Parcourir chaque équation
    for i, eq in enumerate(equations):
        # Mettre l'équation sous forme de a1*x1 + a2*x2 + ... = b
        eq = eq.expand().rewrite(sp.Add)
        
        # Parcourir chaque variable
        for j, var in enumerate(variables):
            # Extraire le coefficient de la variable
            coeff = eq.coeff(var)
            A[i, j] = coeff
            
        # Extraire le terme constant (termes sans variables)
        B[i] = -eq.subs({var: 0 for var in variables})
    
    return A, B

A, B = generate_matrix(equations, variables)
A_Vg = generate_matrix(equations_Vg, variables_Vg)[0] #Matrice des eq si Vg=0
det_A=A.det()
det_A_Vg=A_Vg.det()
#singular_condition = sp.Eq(det_A, 0)
#singular_condition_Vg = sp.Eq(det_A_Vg, 0)
A_inv= A.inv() 
A_Vg_inv = A_Vg.inv() #if not singular_condition else eye(5)



eq1= sp.Eq((A_inv*B)[0],0)   
eq2= sp.Eq((A_inv*B)[1],0)    
eq3= sp.Eq((A_inv*B)[2],0)  
eq4= sp.Eq((A_inv*B)[3],0)  
eq5= sp.Eq((A_inv*B)[4],0)

eq1_Vg = sp.Eq((A_Vg_inv*B)[0],0)           #eq si Vg=0
eq2_Vg = sp.Eq((A_Vg_inv*B)[1],0)    
eq3_Vg = sp.Eq((A_Vg_inv*B)[2],0)  


# Convertir les équations symboliques en fonctions lambda

f_eq1 = sp.lambdify((x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point), eq1.lhs - eq1.rhs)
f_eq2 = sp.lambdify((x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point), eq2.lhs - eq2.rhs)
f_eq3 = sp.lambdify((x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point), eq3.lhs - eq3.rhs)
f_eq4 = sp.lambdify((x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point), eq4.lhs - eq4.rhs)
f_eq5 = sp.lambdify((x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point), eq5.lhs - eq5.rhs)

f_eq1_Vg = sp.lambdify((x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point), eq1_Vg.lhs - eq1_Vg.rhs)
f_eq2_Vg = sp.lambdify((x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point), eq2_Vg.lhs - eq2_Vg.rhs)
f_eq3_Vg = sp.lambdify((x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point), eq3_Vg.lhs - eq3_Vg.rhs)


# On jit les eq pour les rendres plus rapide
#f_eq1_jit = jit(nopython=True)(f_eq1)
#f_eq2_jit = jit(nopython=True)(f_eq2)
#f_eq3_jit = jit(nopython=True)(f_eq3)
#f_eq4_jit = jit(nopython=True)(f_eq4)
#f_eq5_jit = jit(nopython=True)(f_eq5)

#f_eq1_Vg_jit = jit(nopython=True)(f_eq1_Vg)
#f_eq2_Vg_jit = jit(nopython=True)(f_eq2_Vg)
#f_eq3_Vg_jit = jit(nopython=True)(f_eq3_Vg)
#f_eq4_Vg_jit = jit(nopython=True)(f_eq4_Vg)
#f_eq5_Vg_jit = jit(nopython=True)(f_eq5_Vg)

# On définit le système d'équation diff pour Odeint
def system(variables, t):
    x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point = variables
    dthetadt = theta_point
    dpsidt = psi_point
    dphidt = phi_point
    if norme_Vg > 10**(-2):
        if abs(det_A)<10**(-2):
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        dxdt = x_point
        dydt = y_point
        dx_dotdt = f_eq1(x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point)
        dy_dotdt = f_eq2(x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point)
        dtheta_dotdt = f_eq3(x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point)
        dpsi_dotdt = f_eq4(x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point)
        dphi_dotdt = f_eq5(x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point)
        return [dxdt, dydt, dthetadt, dpsidt, dphidt, dx_dotdt, dy_dotdt, dtheta_dotdt, dpsi_dotdt, dphi_dotdt]
    else :
        if abs(det_A_Vg)<10**(-2):
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        dxdt = Omega.cross(sp.Matrix([0, 0, -R]))[0]
        dydt = Omega.cross(sp.Matrix([0, 0, -R]))[1]
        dx_dotdt = 0
        dy_dotdt = 0
        dtheta_dotdt = f_eq1_Vg(x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point)
        dpsi_dotdt = f_eq2_Vg(x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point)
        dphi_dotdt = f_eq3_Vg(x, y, theta, psi, phi, x_point, y_point, theta_point, psi_point, phi_point)
        return [dxdt, dydt, dthetadt, dpsidt, dphidt, dx_dotdt, dy_dotdt, dtheta_dotdt, dpsi_dotdt, dphi_dotdt]

# Conditions initiales
CI = [0, 0, sp.pi/2, 0, 0, 0, 0, 0, 0, 0]

# Intervalle de temps
t = np.linspace(0, .15, 1000)

# Résoudre les équations différentielles
#solution = odeint(system, CI, t)

# Temps de simulation
t_span = (0, 10)
t_eval = np.linspace(t_span[0], t_span[1], 100)

# Résolution du système d'équations différentielles
solution = solve_ivp(system, t_span, CI, t_eval=t_eval, method='RK45', rtol=1e-5, atol=1e-8)

# Extraire les résultats
x_sol = solution[:, 0]
y_sol = solution[:, 1]
theta_sol = solution[:, 2]
psi_sol = solution[:, 3]
phi_sol = solution[:, 4]

# Tracer les résultats
plt.figure(figsize=(10, 8))
plt.subplot(3, 1, 1)
plt.plot(t, x_sol, label='x(t)')
plt.plot(t, y_sol, label='y(t)')
plt.legend()
plt.title('Solutions x(t) et y(t)')

plt.subplot(3, 1, 2)
plt.plot(t, theta_sol, label='theta(t)')
plt.plot(t, psi_sol, label='psi(t)')
plt.plot(t, phi_sol, label='phi(t)')
plt.legend()
plt.title('Solutions theta(t), psi(t), et phi(t)')

plt.subplot(3, 1, 3)
plt.plot(t, solution[:, 5], label='x_dot(t)')
plt.plot(t, solution[:, 6], label='y_dot(t)')
plt.plot(t, solution[:, 7], label='theta_dot(t)')
plt.plot(t, solution[:, 8], label='psi_dot(t)')
plt.plot(t, solution[:, 9], label='phi_dot(t)')
plt.legend()
plt.title('Solutions des dérivées')

plt.tight_layout()
plt.show()










# Résolution
#Méthode des moindres carrés

#solution = sp.dsolve([TRC1, TRC2, TMC1, TMC2, TMC3], ics=CI)

# Définir l'équation
# equation = sp.Eq(Omega, [0,0,0])

# Afficher l'équation
# print("Équation wx = 0:")
# (equation)
