from  scipy.optimize import fmin_cg
from math import degrees
from optimization import *


class Natural_Shape_Balloon:
  def __init__(self, h=15000, initial_theta= 0.08, initial_a = 7.5):
        self.h = h
        self.initial_guess = [initial_theta, initial_a]
        self.result = fmin_cg(F, self.initial_guess, args = [self.h], full_output=True)

  def solve_z_r(self):   
    params = self.result[0]
    self.z_sol, self.r_sol = Solve(params[0], params[1], self.h)[2], Solve(params[0], params[1], self.h)[3]
    return self.z_sol, self.r_sol
  
  def Volume(self):
    v = 0
    for i in range(len(self.z_sol)-1):
      r1 = self.r_sol[i]
      r2 = self.r_sol[i+1]
      dz = self.z_sol[i+1] - self.z_sol[i]
      v = v + np.pi*dz*(r1*r1 + r2*r2 + r1*r2)/3
    return v
