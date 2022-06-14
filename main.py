import time
from natural_shape_balloon import Natural_Shape_Balloon
import matplotlib.pyplot as plt
start_time = time.time()

if __name__ == "__main__": 
  
  balloon = Natural_Shape_Balloon()
  z_sol, r_sol  = balloon.solve_z_r()

  print("--- %s seconds ---" % (time.time() - start_time))

  plt.plot(z_sol, r_sol)
  plt.gca().set_aspect('equal', adjustable = 'box')
  plt.show()

