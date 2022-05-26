from scipy.integrate import solve_ivp
import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
from math import exp, radians
#import float_alt

l = 16.0544
ds = 0.0001
g = 9.8
payload_weight = 24*g


R_id = 8314.462;        # gas constant                                   (J/K/mol*1000)
mu_air  = 28.966;             # air molar mass                                 (gram)
xmu_air = R_id / mu_air ;     # mu/R ratio for air    (  P = (rho/mu)RT  )
mu_gas = 4
dT_gas = 0
Hatm = [0, 500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000, 7000,
  8000, 9000, 10000, 11000, 12000, 14000, 16000, 18000, 20000, 24000, 28000, 32000, 36000 ]

Patm = [101330, 95464, 89877, 84559, 79499, 74690, 70123, 61661, 54052, 47217, 41106,
  35653, 30801, 26500, 22700, 19399, 14170, 10353, 7565, 5529, 2971, 1616, 889, 499]

Tatm =[ 288.2, 284.9, 281.7, 278.4, 275.2, 271.9, 268.7, 262.2, 255.7, 249.2, 242.7,
  236.2, 292.7, 223.3, 216.8, 216.7, 216.7, 216.7, 216.7, 216.7, 220.6, 224.5, 228.5, 239.3]

Beta = [0.000119267, 0.000120614, 0.000121985, 0.00012341, 0.000124796, 0.000126191,
  0.000128599, 0.000131705, 0.000135193, 0.0001386, 0.000142321, 0.000146286, 0.000150402,
  0.00015478, 0.000157143, 0.000157047, 0.000156925, 0.000156872, 0.000156763, 0.000155277,
  0.000152236, 0.000149403, 0.000144373, 0]

def densities(h):
    for n  in range(0,24):
      if h > Hatm[n]:
          i = n
      T_atm = Tatm[i] + (h - Hatm[i]) * (Tatm[i + 1] - Tatm[i]) / (Hatm[i + 1] - Hatm[i])
      P_atm = Patm[i] * exp(-Beta[i] * (h - Hatm[i]))
      rho_atm = P_atm / xmu_air / T_atm

      xmu_gas = R_id / mu_gas
      T_gas = T_atm + dT_gas

      ro_gas = P_atm/xmu_gas/T_gas

    return [rho_atm, ro_gas]

def b(h):
    ro_atm, ro_gas = densities(h)[0], densities(h)[1]
    return g*(ro_atm - ro_gas)

def Solve(theta0, a, h):
    def func(t, y):
        theta, T, z, r = y
        twopir = 2*np.pi*r
        w = 0.22
        cos = np.cos(theta)
        sin = np.sin(theta)
        p = b(h)*(z-a)
        return [
            -twopir * (w * sin + p) / T,
            twopir * w * cos,
            cos,
            sin
        ]
    T0 = payload_weight/np.cos(theta0)
    z0, r0 = 0, 0
    sol = solve_ivp(func, t_span = [0, l], y0=[theta0, T0, z0, r0], t_eval=np.arange(0, l, ds))
    return sol.y

def F(params):
  theta_0, a = params
  w = 0.22
  theta_d = radians(54)
  h_d = 21850 
  b_d = b(h_d)
  lam = (payload_weight/b_d)**(1/3)
  theta_s, z_s, r_s = Solve(theta_0, a, h)[0], Solve(theta_0, a, h)[2], Solve(theta_0, a, h)[3]
  r_ds = Solve(theta_d, 0, h_d)[3]              #r_d (float altitude)
  intg_theta, intg_rztheta, intg_rd = 0, 0, 0   #integral of sin(theta), r(z-a)sin(theta) and r_d
  for i in range(len(theta_s)):
    intg_theta += ds*np.sin(theta_s[i])
    intg_rztheta += ds*np.sin(theta_s[i])*r_s[i]*(z_s[i]-a)
    intg_rd += ds*r_ds[i]
  return (intg_theta/lam)**2 + (1+(2*np.pi*b(h)*intg_rztheta+2*np.pi*w*intg_rd)/(b_d*(lam**3)))**2

h = 11500
initial_guess = [0.010, 9]
result = optimize.fmin_cg(F, initial_guess)
fitted_params = result
print(fitted_params)
z_sol, r_sol = Solve(fitted_params[0], fitted_params[1], h)[2], Solve(fitted_params[0], fitted_params[1], h)[3]
plt.plot(z_sol, r_sol)
plt.gca().set_aspect('equal', adjustable = 'box')
plt.show()
