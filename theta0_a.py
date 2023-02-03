import numpy as np
from matplotlib import pyplot as plt
import concurrent.futures
from solve import Solve
from params import *


def get_grid(theta_max, theta_min, a_max, a_min, step_theta, step_a):
    """
    getting a grid to search theta0 and a
    :param theta_max, theta_min, a_max, a_min: searching boundaries
    :param step_theta, step_a: grid step  
    :return: grid of theta and a 
    """
    grid = []

    #print("a_max: ", a_max,"a_min: ", a_min,"step_a: ", step_a, "theta_max: ",  
    #theta_max, "theta_min: ", theta_min, "step_theta: ", step_theta)

    for i in np.arange(np.radians(theta_max), np.radians(theta_min), -np.radians(step_theta)):
        for j in np.arange(a_max, a_min, -step_a):
            grid.append([i, j])
    return grid


def theta0_a(grid_params, rmax, velocity, number_of_cores):
    """

    :param grid_params: list of grid parameters: searching boundaries and grid step (for theta0 and a) 
    :param rmax: current maximum radius of the balloon
    :param velocity: current velocity (input)
    :number_of_cores: the number of cores that are involved in parallel computing
    :return: result array: theta0, a, theta (theta_last) and radius (r_last) on the top of the balloon, 
    """      

    theta0_max, theta0_min, a_max, a_min, theta_step, a_step = grid_params
    grid = get_grid(theta0_max, theta0_min, a_max, a_min, theta_step, a_step)
    optimal_z, optimal_r, loss_min = [], [], 1000
    with concurrent.futures.ProcessPoolExecutor(max_workers=number_of_cores) as executor:
        results = [[executor.submit(Solve, g, rmax, velocity), g] for g in grid]
        results = np.array(results)    
        count = 0

        for i, f in enumerate(concurrent.futures.as_completed(results[:, 0])):
            count += 1
            theta, _, z, r = f.result()

            # sgn_arr = []
            # for i in range(2, len(theta)):
            #     count = 0
            #     if np.sign(theta[i] - theta[i - 1]) + np.sign(theta[i-1] - theta[i - 2]) == 0:
            #         count += 1

            # if count > 1:
            #     continue
     
            loss = np.sqrt(((90 + np.degrees(theta[-1])) / 90) ** 2 + (r[-1] / rp_max) ** 2) # rp_max - maximum possible radius of the balloon
            if loss < loss_min:           
                loss_min = loss
                theta0, a = results[i, 1]
                theta_last = theta[-1]
                r_last = r[-1]
                optimal_z = z
                optimal_r = r
                optimal_theta = theta
                if (abs(np.degrees(theta_last) + 90) < 1e-2) and (abs(r_last) < 1e-3):
                    print("break")
                    break

    res = np.array([np.degrees(theta0), a, theta_last, r_last, max(optimal_r), loss_min, optimal_z, optimal_r, optimal_theta])
    #print("Iterations for finding optimal theta0 and a for this rmax and velocity: ", count)
    #del theta, z, r, grid, results, theta0, optimal_r, optimal_z, optimal_theta

    return res
