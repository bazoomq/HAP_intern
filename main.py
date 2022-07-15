import time
import numpy as np
import pandas as pd
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


def main(grid_params):
    theta_max, theta_min, a_max, a_min, theta_step, a_step = grid_params
    grid = get_grid(theta_max, theta_min, a_max, a_min, theta_step, a_step)
    optimal_z, optimal_r, loss_min = [], [], 100
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        results = [[executor.submit(Solve, g), g] for g in grid]
        results = np.array(results)
        for i, f in enumerate(concurrent.futures.as_completed(results[:, 0])):
            theta, T, z, r = f.result()
            if -92 < np.degrees(theta[-1]) < -88 and -0.1 < r[-1] < 0.1:
                loss = np.sqrt(((np.pi / 2 + theta[-1]) / (np.pi / 2)) ** 2 + r[-1] ** 2)
                print("Theta0, a: ", results[i, 1], "Loss: ", loss)
                if loss < loss_min:
                    loss_min = loss
                    optimal_z = z
                    optimal_r = r
                    optimal_theta = theta
                    theta_last = theta[-1]
                    r_last = r[-1]
                    theta0, a = results[i, 1]
    print("Total lost (for theta0 and a): ", loss_min)
    print("Max R: ", max(optimal_r))
    print("Last theta: ", np.degrees(theta_last), "Last R: ", r_last)
    print("theta0: ", np.degrees(theta0), "a: ", a)
    plt.plot(optimal_z, optimal_r)
    plt.show()

    res = np.array([np.degrees(theta0), a, theta_last, r_last, max(optimal_r), loss_min,
                    optimal_z, optimal_r, optimal_theta])
    return res


if __name__=="__main__":
    start = time.time()
    theta_max = 63
    theta_min = 55
    if h < 21850:
        a_max = 16
        a_min = 0
    else:
        a_max = 0
        a_min = -50
    number_of_steps_theta = 100
    number_of_steps_a = 64

    number_of_recurse = 2
    for i in range(number_of_recurse):
        print('DEPTH ', i)
        print(theta_max, theta_min)
        print(a_max, a_min)
        theta_step = (theta_max - theta_min) / number_of_steps_theta
        a_step = (a_max - a_min) / number_of_steps_a
        res = main([theta_max, theta_min, a_max, a_min, theta_step, a_step])
        theta0, a = res[0], res[1]
        print(theta0, a)
        theta_max, theta_min = theta0 + 2, theta0 - 2
        a_max, a_min = a + 2, a - 2

    V = np.pi / 3 * ds * np.cos(np.radians(theta0)) * (res[7][0] ** 2 + res[7][0] * res[7][1] + res[7][1] ** 2)
    for i in range(2, len(res[7])):
        V += np.pi / 3 * ds * np.cos(res[8][i - 1]) * (res[7][i - 1] ** 2 + res[7][i - 1] * res[7][i] + res[7][i] ** 2)
    print("Volume of the balloon: ", V)
    end = time.time()
    print("Running time: ", end - start, "s")
