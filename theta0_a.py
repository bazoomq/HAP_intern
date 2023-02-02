import numpy as np
from matplotlib import pyplot as plt
from solve import Solve
from params import *


def theta0_a(params, velocity):
    """

    :param params: list of parameters: searching boundaries and steps (for theta0 and a) 
    :param rmax: current maximum radius of the balloon
    :param velocity: current velocity (input)
    :return: result array: theta0, a, theta (theta_last) and radius (r_last) on the top of the balloon,
    """      
    rmax = rp_max
    rmax_new = 0
    rmax_tol = 1e-2

    r_last = 1
    theta_last = 0

    theta0 = params[0]
    while (abs(theta_last + 90) > 1e-2) or (abs(r_last) > 1e-2) : 
        theta0_max, theta0_min, a_max, a_min = params
        while (abs(r_last) > 1e-2):
            a = (a_min + a_max) / 2
            result = Solve([theta0, a], rmax, velocity)
            result = np.array(result)    
            theta, _, z, r = result 
                
            theta_last = np.degrees(theta[-1])
            r_last = r[-1] 
            
            if r_last < 0:
                a_min = a
            else:
                a_max = a
        #     print("a min = ", a_min, "a max = ", a_max)
        #     # print('r_last: ', r_last)
        #     # print('theta_last: ', theta_last)
        # print('a = ', a)
        # print('theta_last ', theta_last)

        while (abs(theta_last + 90) > 1e-2):
            theta0 = (theta0_min + theta0_max) / 2

            result = Solve([theta0, a], rmax, velocity)
            result = np.array(result)    
            theta, _, z, r = result 
            
            theta_last = np.degrees(theta[-1])
            r_last = r[-1]
            print(np.degrees(theta_last))
            if theta_last < -90:
                theta0_max = theta0
            else: 
                theta0_min = theta0
            # print('theta0 max ', theta0_max, 'theta0 min', theta0_min)
            # #print('r_last: ', r_last)
            # #print('theta_last: ', theta_last)

        max_radius = max(r)

        while rmax - rmax_new > rmax_tol:
            if rmax_new != 0:
                rmax = rmax_new
            
            rmax_new = max_radius 


        
    res = np.array([theta0, a, theta_last, r_last, max(r), z, r, theta])
    return res
