import numpy as np
from matplotlib import pyplot as plt
import concurrent.futures
from solve import Solve
from params import *


def get_grid(params, rmax_in, velocity):
    """
    getting a grid to search theta0 and p0
    :param theta_max, theta_min, p0_max, p0_min: searching boundaries
    :param step_theta, step_p0: grid step  
    :return: grid of theta and p0 
    """
    
    theta0_max, theta0_min, p0_max, p0_min, theta0_step, p0_step = params
    optimal_z, optimal_r, loss_min = [], [], 1000
    rmax_out = 0
    rmax_tol = 1e-3
    #for i in np.arange(np.radians(theta0_max), np.radians(theta0_min), -np.radians(theta0_step)):
    for j in np.arange(p0_max, p0_min, -p0_step):
        rmax_in = 3
        while abs(rmax_out - rmax_in) > rmax_tol:  
            if rmax_out != 0:
                rmax_in = rmax_out
            theta, _, z, r, p_gas, _ = Solve([np.radians(1.22314215), j], rmax_in, velocity)
            rmax_out = max(r)
            r_diff = rmax_out - rmax_in
            print(r_diff)
        print("*********************************")
        #grid.append([[i, j], rmax_out])
        loss = np.sqrt((90 + np.degrees(theta[-1])) ** 2 + (r[-1]) ** 2) # rp_max - maximum possible radius of the balloon
        if loss < loss_min:           
            loss_min = loss
            theta0, p0 = np.radians(1.22314215), j
            theta_last = theta[-1]
            r_last = r[-1]
            optimal_z = z
            optimal_r = r
            optimal_pgas = p_gas
            optimal_theta = theta

    res = np.array([np.degrees(theta0), p0, theta_last, r_last, max(optimal_r), loss_min, optimal_z, optimal_r, optimal_theta, optimal_pgas])

    return res            

def theta0_p0(grid_params, rmax_in, velocity, number_of_cores):
    """

    :param grid_params: list of grid parameters: searching boundaries and grid step (for theta0 and p0) 
    :param rmax: current maximum radius of the balloon
    :param velocity: current velocity (input)
    :number_of_cores: the number of cores that are involved in parallel computing
    :return: result array: theta0, a, theta (theta_last) and radius (r_last) on the top of the balloon, 
    """      

    theta0_max, theta0_min, p0_max, p0_min, theta_step, p0_step = grid_params
    grid = get_grid(theta0_max, theta0_min, p0_max, p0_min, theta_step, p0_step, rmax_in, velocity)
    optimal_z, optimal_r, loss_min = [], [], 1000 

    with concurrent.futures.ProcessPoolExecutor(max_workers=number_of_cores) as executor:
        results = [[executor.submit(Solve, g[0], g[1], velocity), g[0]] for g in grid]
        results = np.array(results)    

        for i, f in enumerate(concurrent.futures.as_completed(results[:, 0])):
            theta, _, z, r, p_gas, _ = f.result()
     
            loss = np.sqrt(((90 + np.degrees(theta[-1])) / 90) ** 2 + (r[-1] / rp_max) ** 2) # rp_max - maximum possible radius of the balloon
            if loss < loss_min:           
                loss_min = loss
                theta0, p0 = results[i, 1]
                theta_last = theta[-1]
                r_last = r[-1]
                optimal_z = z
                optimal_r = r
                optimal_pgas = p_gas
                optimal_theta = theta
                if (abs(np.degrees(theta_last) + 90) < 1e-2) and (abs(r_last) < 1e-3):
                    print("break")
                    break

    res = np.array([np.degrees(theta0), p0, theta_last, r_last, max(optimal_r), loss_min, optimal_z, optimal_r, optimal_theta, optimal_pgas])

    return res
