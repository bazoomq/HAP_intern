from scipy.special import hyp2f1, ellipkinc
import numpy as np
from pynverse import inversefunc 
from math import asin
import matplotlib.pyplot as plt

r_0 = 5
dr = 0.01
w_d = 0.2254
ds = 0.1

def z(point_r):
  return (point_r**3/(3*(r_0**2)))*hyp2f1(1/2, 3/4, 7/4, point_r**4/r_0**4)

def r_z(point_z):
  return inversefunc(z, y_values = point_z)

def S(point_r):
  return (r_0**2)*ellipkinc(asin(point_r/r_0), -1)/r_0

def r_d(s):
  r_arr = np.array([i*dr for i in range(0, int(r_0/dr)+1)])
  s_arr = np.array([S(i*dr) for i in range(0, int(r_0/dr)+1)])
  if s<=S(r_0):
    for i in range(len(s_arr)):
      if s>= s_arr[i] and s<=s_arr[i+1]:
        return r_arr[i] + (s - s_arr[i])*(r_arr[i+1] - r_arr[i])/(s_arr[i+1]-s_arr[i])
  else:
    return r_d(2*S(r_0)-s)

def z_d(s):
  if s<=S(r_0):
    return z(r_d(s))
  else:
    return 2*z(r_0) - z(r_d(2*S(r_0) - s))

k2 = np.array([z_d(i*ds) for i in range(0, int(2*S(r_0)/ds)+1)])
k3 = np.array([r_d(i*ds) for i in range(0, int(2*S(r_0)/ds)+1)])
plt.plot(k2, k3)
plt.gca().set_aspect('equal', adjustable = 'box')
plt.show()
print(z_d(S(r_0)))