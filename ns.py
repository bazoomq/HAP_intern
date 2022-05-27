from more_itertools import count_cycle
from scipy.integrate import solve_ivp
import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
from math import exp, radians
from utils import f_interp1d, s1
import utils
#import float_alt


def get_rp(s, gt):
    return float(gt.loc[s])


def densities(h):
    for n  in range(0,24):
      if h > utils.Hatm[n]:
          i = n
      T_atm = utils.Tatm[i] + (h - utils.Hatm[i]) * (utils.Tatm[i + 1] - utils.Tatm[i]) / (utils.Hatm[i + 1] - utils.Hatm[i])
      P_atm = utils.Patm[i] * exp(-utils.Beta[i] * (h - utils.Hatm[i]))
      rho_atm = P_atm / utils. xmu_air / T_atm

      xmu_gas = utils.R_id / utils.mu_gas
      T_gas = T_atm + utils.dT_gas

      ro_gas = P_atm/xmu_gas/T_gas

    return [rho_atm, ro_gas]

def b(h):
    ro_atm, ro_gas = densities(h)[0], densities(h)[1]
    return utils.g*(ro_atm - ro_gas)

# def Solve(theta0, a, h):
#   def func(t, y):
#       theta, T, z, r = y
#       twopir = 2*np.pi*r
#       w = 0.22
#       cos = np.cos(theta)
#       sin = np.sin(theta)
#       p = b(h)*(z-a)
#       return [
#           -twopir * (w * sin + p) / T,
#           twopir * w * cos,
#           cos,
#           sin
#       ]
#   T0 = payload_weight/np.cos(theta0)
#   z0, r0 = 0, 0
#   sol = solve_ivp(func, t_span = [0, l], y0=[theta0, T0, z0, r0], t_eval=np.arange(0, l, ds))
#   return sol.y


def Solve(theta0, a, h):  
    def func(t, y):
      if t <= s1() / 2:
          import pdb
          
          rp = f_interp1d()(t)
      else:
          rp = f_interp1d()(s1 - t)
      if r<utils.r_tollerance:
        return 
      theta, T, z, r = y
   
      p = b(h) * (z - a)
      sin = np.sin(theta)
      cos = np.cos(theta)
  
      return [
      - 2 * np.pi * (rp *utils.wp * sin + p*r) / T,
      2 * np.pi * rp *utils.wp * cos,
      cos,
      sin
      ]

    T0 = utils.payload_weight / np.cos(theta0)
    z0, r0 = 0, 0

    sol = solve_ivp(func, t_span=[0, s1], y0=[theta0, T0, z0, r0], t_eval=np.arange(0, s1, utils.ds))
    
    return sol.y, sol.t



def F(params):
  theta_0, a = params
  w = 0.22
  theta_d = radians(54)
  h_d = 21850 
  b_d = b(h_d)
  lam = (utils.payload_weight/b_d)**(1/3)
  theta_s, z_s, r_s = Solve(theta_0, a, h)[0], Solve(theta_0, a, h)[2], Solve(theta_0, a, h)[3]
  r_ds = Solve(theta_d, 0, h_d)[3]              #r_d (float altitude)
  intg_theta, intg_rztheta, intg_rd = 0, 0, 0   #integral of sin(theta), r(z-a)sin(theta) and r_d
  for i in range(len(theta_s)):
    intg_theta += utils.ds*np.sin(theta_s[i])
    intg_rztheta += utils.ds*np.sin(theta_s[i])*r_s[i]*(z_s[i]-a)
    intg_rd += utils.ds*r_ds[i]
  return (intg_theta/lam)**2 + (1+(2*np.pi*b(h)*intg_rztheta+2*np.pi*w*intg_rd)/(b_d*(lam**3)))**2

h = 10300
success = False
counter_limit = 10 
counter = 0
while counter<counter_limit:
  the0 = np.pi/np.random.randint(1,100)
  A = np.random.random() * 10
  print("the0: ", the0, "A:", A)
  initial_guess = [the0, A ]
  import pdb
  pdb.set_trace()
  result = optimize.minimize(F, initial_guess,method ="BFGS", options = {"xatol": 1e-8, 'disp': True})
  success = result.success
  print("success ", success)
  
  if success:
    fitted_params = result.x
    print(fitted_params)  
    z_sol, r_sol = Solve(fitted_params[0], fitted_params[1], h)[2], Solve(fitted_params[0], fitted_params[1], h)[3]
    plt.plot(z_sol, r_sol)
    plt.gca().set_aspect('equal', adjustable = 'box')
    plt.show()


  counter += 1
  print(counter)
  if counter > counter_limit:
    raise ValueError(result.message)

