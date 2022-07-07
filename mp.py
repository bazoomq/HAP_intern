import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.special import hyp2f1
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
from density import density
from calculate_rp import get_sr
import concurrent.futures


g = 9.8065
L0 = 24.06031 * g
wp = 0.229158
rp_max = 6.122831
l = 2 * hyp2f1(1/4, 1/2, 5/4, 1) * rp_max
ds = 0.002
h = 19000


def b(h):
    ro_atm = density(h)[0]
    ro_gas = density(h)[1]
    b = (ro_atm - ro_gas) * g
    return b


rs, s_half = get_sr(rp_max)
f = interp1d(s_half, rs, kind='cubic')


def Solve(params):
    def func(t, y):
        if t <= l / 2:
            rp = f(t)
        else:
            rp = f(l - t)
        theta, T, z, r = y
        p = b(h) * (z - params[1])
        sin = np.sin(theta)
        cos = np.cos(theta)
        return [
            - 2 * np.pi * (rp * wp * sin + p * r) / T,
            2 * np.pi * rp * wp * cos,
            cos,
            sin
        ]

    T0 = L0 / np.cos(params[0])
    z0, r0 = 0, 0

    sol = solve_ivp(func, t_span=[0, l], y0=[params[0], T0, z0, r0], t_eval=np.arange(0, l, ds))

    return sol.y


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
                    theta_last = theta[-1]
                    r_last = r[-1]
                    theta0, a = results[i, 1]
    print("Total lost (for theta0 and a): ", loss_min)
    print("Max R: ", max(optimal_r))
    print("Last theta: ", np.degrees(theta_last), "Last R: ", r_last)
    print("theta0: ", np.degrees(theta0), "a: ", a)
    plt.plot(optimal_z, optimal_r)
    plt.show()

    res = np.array([np.degrees(theta0), a, theta_last, r_last, max(optimal_r), loss_min])
    return res


if __name__=="__main__":
    start = time.time()
    theta_max = 90
    theta_min = 0
    if h < 21850:
        a_max = 16
        a_min = 0
    else:
        a_max = 0
        a_min = -400
    count_of_step_theta = 900
    count_of_step_a = 64

    number_of_recurse = 2
    for i in range(number_of_recurse):
        print('DEPTH ', i)
        print(theta_max, theta_min)
        print(a_max, a_min)
        theta_step = (theta_max - theta_min) / count_of_step_theta
        a_step = (a_max - a_min) / count_of_step_a
        res = main([theta_max, theta_min, a_max, a_min, theta_step, a_step])
        theta0, a = res[0], res[1]
        print(theta0, a)
        theta_max, theta_min = theta0 + 2, theta0 - 2
        a_max, a_min = a + 2, a - 2

    print(res)

    #data.to_excel("output.xlsx")
    end = time.time()
    print("Running time: ", end - start, "s")