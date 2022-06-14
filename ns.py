from  scipy.optimize import fmin_cg
import matplotlib.pyplot as plt
from math import degrees
from optimization import *
import time
start_time = time.time()


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


if __name__ == "__main__": 
  
  balloon = Natural_Shape_Balloon()
  z_sol, r_sol  = balloon.solve_z_r()

  print("--- %s seconds ---" % (time.time() - start_time))

  plt.plot(z_sol, r_sol)
  plt.gca().set_aspect('equal', adjustable = 'box')
  plt.show()

