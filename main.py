import time
import numpy as np
from matplotlib import pyplot as plt
from solve import Solve, b
from density import density
from params import *
from theta0_a import theta0_a
import argparse


def main(number_of_cores, h):
    if h < 21500:
        theta_max = 25
        theta_min = 0
        a_max = 16
        a_min = 5
        number_of_steps_a = 100
    else:
        theta_max = 70
        theta_min = 65
        a_max = -3
        a_min = -4
        number_of_steps_a = 20
        
    number_of_steps_theta = 100


    tol_rmax = 1e-3
    tol_mgas = 5 * 1e-3


    for velocity in np.arange(3.0, 3.1, 0.01):
        print("velocity = ", velocity)
        rmax = rp_max
        rmax_new = 0
        count_rmax = 0
        
        while rmax - rmax_new > tol_rmax:
            if rmax_new != 0:
                rmax = rmax_new

            number_of_recurse = 2
            for i in range(number_of_recurse):
                print('r_max = ', rmax, ', DEPTH ', i)
                # print(theta_max, theta_min)
                # print(a_max, a_min)
                theta_step = (theta_max - theta_min) / number_of_steps_theta
                a_step = (a_max - a_min) / number_of_steps_a
                res = theta0_a([theta_max, theta_min, a_max, a_min, theta_step, a_step], rmax, velocity, number_of_cores)
                theta_max, theta_min = res[0] + 2, res[0] - 2
                a_max, a_min = res[1] + 2, res[1] - 2

            rmax_new = res[4] 
            count_rmax += 1

        print("Iterations for finding optimal rmax: ", count_rmax)

        V = np.pi / 3 * ds * np.cos(np.radians(res[0])) * (res[7][0] ** 2 + res[7][0] * res[7][1] + res[7][1] ** 2)
        m_gas_ = 0
        for i in range(2, len(res[7])):
            dV_i = np.pi / 3 * ds * np.cos(res[8][i - 1]) * (res[7][i - 1] ** 2 + res[7][i - 1] * res[7][i] + res[7][i] ** 2)
            V += dV_i
            dm_i = (density(h)[1] + b(h)*(res[6][i] - res[1])) * dV_i * mu_gas / (R * density(h)[2]) 
            m_gas_ += dm_i

        if abs(m_gas_ - m_gas) < tol_mgas:
            break
    
    Fg = (m_payload + m_b + m_bl + m_gas) * g
    Fa = density(h)[0][0] * V * g

    theta0, a = res[0], res[1]

    print("_______________________________")
    print("____________RESULTS____________")
    print("____________h = ", h, "____________")

    print("theta0: ", res[0], ", a: ", res[1])
    print("Total lost (for theta0 and a): ", res[5])
    print("r max: ", res[4])
    print("Last theta: ", np.degrees(res[2]), ", Last R: ", res[3])
    print("Volume of the balloon: ", V)
    print("Difference between m_gas and calculated m_gas: ", abs(m_gas_ - m_gas))
    print("Difference between Fg and Fa", Fg - Fa)
    print("Velocity of the ballon: ", velocity)

    plt.plot(res[6], res[7])
    plt.text(0.5, 0.5, 'height: {}, theta0: {}, a: {}, volume: {}, velocity: {}'.format(h, theta0, a, V, velocity))
    plt.savefig('height_%s.png' % h)


if __name__=="__main__":
    start = time.time()
    
    main(number_of_cores, h)

    end = time.time()
    print("Running time: ", end - start, "s")
