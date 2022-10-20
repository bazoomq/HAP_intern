import numpy as np
from matplotlib import pyplot as plt
import concurrent.futures
from solve import Solve
from params import *


def get_grid(theta_max, theta_min, a_max, a_min, step_theta, step_a):
    grid = []
    for i in np.arange(np.radians(theta_max), np.radians(theta_min), -np.radians(step_theta)):
        for j in np.arange(a_max, a_min, -step_a):
            grid.append([i, j])
    return grid


def theta0_a(grid_params, rmax, velocity, number_of_cores):
    def Solve1(p):
        return Solve(p, rmax, velocity)
        
    theta_max, theta_min, a_max, a_min, theta_step, a_step = grid_params
    grid = get_grid(theta_max, theta_min, a_max, a_min, theta_step, a_step)
    optimal_z, optimal_r, loss_min = [], [], 100
    with concurrent.futures.ProcessPoolExecutor(max_workers=number_of_cores) as executor:
        results = [[executor.submit(Solve1, g), g] for g in grid]
        results = np.array(results)
        for i, f in enumerate(concurrent.futures.as_completed(results[:, 0])):
            theta, T, z, r = f.result()
            if -92 < np.degrees(theta[-1]) < -88 and -0.1 < r[-1] < 0.1:
                loss = np.sqrt(((np.pi / 2 + theta[-1]) / (np.pi / 2)) ** 2 + r[-1] ** 2)
                if loss < loss_min:
                    loss_min = loss
                    theta0, a = results[i, 1]
                    theta_last = theta[-1]
                    r_last = r[-1]
                    optimal_z = z
                    optimal_r = r
                    optimal_theta = theta

    res = np.array([np.degrees(theta0), a, theta_last, r_last, max(optimal_r), loss_min, optimal_z, optimal_r, optimal_theta])
    return res
