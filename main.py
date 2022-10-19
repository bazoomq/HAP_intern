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
        theta_max = 90
        theta_min = 20
        a_max = 5.1
        a_min = -400
        number_of_steps_a = 400
        
    number_of_steps_theta = 1000

    for i in range(number_of_recurse = 2):
        print('DEPTH ', i)
        print(theta_max, theta_min)
        print(a_max, a_min)
        
        theta_step = (theta_max - theta_min) / number_of_steps_theta
        a_step = (a_max - a_min) / number_of_steps_a
        
        tol_rmax = 1e-3
        tol_mgas = 5 * 1e-3
        rmax = rp_max
        rmax_new = 0
        m_gas = 3.491565771

        for velocity in np.arange(-5.0, 5.0, 0.01):
            while rmax - rmax_new > tol_rmax:
                if rmax_new != 0:
                    rmax = rmax_new
                res = theta0_a([theta_max, theta_min, a_max, a_min, theta_step, a_step], rmax, velocity, number_of_cores)
                rmax_new = res[4] 
            V = np.pi / 3 * ds * np.cos(np.radians(theta0)) * (res[7][0] ** 2 + res[7][0] * res[7][1] + res[7][1] ** 2)
            m_gas_ = 0
            for i in range(2, len(res[7])):
                dV_i = np.pi / 3 * ds * np.cos(res[8][i - 1]) * (res[7][i - 1] ** 2 + res[7][i - 1] * res[7][i] + res[7][i] ** 2)
                V += dV_i
                dm_i = (density[1] + b(h)*(res[6][i] - res[1])) * dV_i * mu_gas / (R * density[2]) 
                m_gas_ += dm_i

            if m_gas_ - m_gas < tol_mgas:
                break

        theta0, a = res[0], res[1]
        print(theta0, a)
        theta_max, theta_min = theta0 + 2, theta0 - 2
        a_max, a_min = a + 2, a - 2

    
    print("______________________________")
    print("Total lost (for theta0 and a): ", res[5])
    print("Max R: ", res[4])
    print("Last theta: ", np.degrees(res[2]), "Last R: ", res[3])
    print("theta0: ", theta0, "a: ", a)
    print("Volume of the balloon: ", V)

    plt.plot(res[6], res[7])
    plt.text(0.5, 0.5, 'height: {}, theta0: {}, a: {}, volume: {}'.format(h, theta0, a, V))
    plt.savefig('height_%s.png' % h)


if __name__=="__main__":
    start = time.time()
    #parser = argparse.ArgumentParser()
    #parser.add_argument("number_of_cores", help="how many cores to use for multiproccessing", type=int)
    #parser.add_argument("height", help="height of balloon", type=int)
    #args = parser.parse_args()
    #number_of_cores = args.number_of_cores
    #h = args.height

    number_of_cores = 4
    h = 24700
    main(number_of_cores, h)

    end = time.time()
    print("Running time: ", end - start, "s")
