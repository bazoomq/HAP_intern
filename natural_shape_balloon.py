from  scipy.optimize import fmin_cg
from math import degrees
from optimization import *



class Natural_Shape_Balloon:
  def __init__(self, h=15000, initial_theta= 0.08, initial_a = 7.5):
        self.h = h
        self.initial_guess = [initial_theta, initial_a]
        

  def solve_z_r(self):
    result = fmin_cg(F, self.initial_guess, args = [self.h])  
    fitted_params = result
    print(degrees(fitted_params[0]))
    print(fitted_params[1])
    z_sol, r_sol = Solve(fitted_params[0], fitted_params[1], self.h)[2], Solve(fitted_params[0], fitted_params[1], self.h)[3]
    return z_sol, r_sol


