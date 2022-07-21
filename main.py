import time
from natural_shape_balloon import Natural_Shape_Balloon
import matplotlib.pyplot as plt
import pandas as pd
from math import degrees

start_time = time.time()

fparams_list = []
result = [0,0,0,0,1]
for h in reversed(range(15000, 22500, 500)):
  fitted_params=[]
  ds = 0.001
  for k in range(4):
    if len(fitted_params) == 0:
      if h == 22000:
        initial_guess = [0.84, 1.2]
      else:
        initial_guess = [fparams_list[-1][0]-0.02, fparams_list[-1][1]+0.2]
    else:
      initial_guess = [fitted_params[0], fitted_params[1]]
      ds = ds / 2
    if result[4] == 2:
      ds = 0.01
      initial_guess = [fparams_list[-1][0]-0.02, fparams_list[-1][1]+0.2]
    balloon = Natural_Shape_Balloon(h, initial_guess[0], initial_guess[1])
    results = balloon.result
    fitted_params = [results[0][0], results[0][1]]
    fitted_params.append(degrees(fitted_params[0]))
    fitted_params.append(h)
    z_sol, r_sol = balloon.solve_z_r()
    fitted_params.append(r_sol[-1])
    fitted_params.append(balloon.Volume())
    #fitted_params.append(degrees(theta_f))
  fparams_list.append(fitted_params)
df = pd.DataFrame(fparams_list)
df.to_csv('th_a1.csv')
print("--- %s seconds ---" % (time.time() - start_time))
