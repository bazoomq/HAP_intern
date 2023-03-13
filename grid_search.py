import numpy as np
from matplotlib import pyplot as plt
import concurrent.futures
from solve import Solve
from params import *
from plots import plotting
import pandas as pd


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
    # X = np.linspace(theta0_min, theta0_max, 100)
    # Y = np.linspace(a_min, a_max, 80)
    with concurrent.futures.ProcessPoolExecutor(max_workers=number_of_cores) as executor:
        results = [[executor.submit(Solve, g, rmax, velocity), g] for g in grid]
        results = np.array(results)
        count = 0
        loss_arr, theta0_arr, a_arr = [], [], []
        for i, f in enumerate(concurrent.futures.as_completed(results[:, 0])):
            count += 1
            theta, _, z, r = f.result()
            theta0_, a_ = results[i, 1]
            theta0_arr.append(np.degrees(theta0_))
            a_arr.append(a_)
            count = 0
            for j in range(2, len(theta)):
                if np.sign(theta[j] - theta[j - 1]) + np.sign(theta[j - 1] - theta[j - 2]) == 0:
                    count += 1

            if count > 1:
                loss = -1
                loss_arr.append(loss)
                continue
            
            loss = np.sqrt(((90 + np.degrees(theta[-1])) / 90) ** 2 + (r[-1]) ** 2) # rp_max - maximum possible radius of the balloon
            loss_arr.append(loss)
            if loss < loss_min:           
                loss_min = loss
                theta0, a = theta0_, a_
                theta_last = theta[-1]
                r_last = r[-1]
                optimal_z = z
                optimal_r = r
                optimal_theta = theta
    
    df = pd.DataFrame(data={"theta0": theta0_arr, "a": a_arr, "loss": loss_arr})
    df.to_csv("file.csv", sep=',', index=False)
    res = np.array([np.degrees(theta0), a, theta_last, r_last, max(optimal_r), loss_min, optimal_z, optimal_r, optimal_theta])
    #print("Iterations for finding optimal theta0 and a for this rmax and velocity: ", count)
    #del theta, z, r, grid, results, theta0, optimal_r, optimal_z, optimal_theta
    
    return res #, theta0_arr, a_arr, loss_arr
    