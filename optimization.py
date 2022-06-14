from bouyancy import b
from interp_s0 import f_interp1d
import numpy as np
from math import radians
from constants import *
from scipy.integrate import solve_ivp


def Solve(theta0, a, h):
    def func(t, y):
        w_d = 0.22
        theta, T, z, r = y
        cos = np.cos(theta)
        sin = np.sin(theta)
        p = b(h)*(z-a)
        if t <= l / 2:
            r_d = f_interp1d(t)
        else:
            r_d = f_interp1d(l - t)
        return [
            -2*np.pi*(r_d*w_d * sin+r*p)/T,
            2*np.pi* r_d*w_d * cos,
            cos,
            sin
        ]
    T0 = payload_weight/np.cos(theta0)
    z0, r0 = 0, 0
    sol = solve_ivp(func, t_span = [0, l], y0=[theta0, T0, z0, r0], t_eval=np.arange(0, l, ds))
    return sol.y

def F(params,h):
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
