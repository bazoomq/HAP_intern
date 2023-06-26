import numpy as np
from matplotlib import pyplot as plt
from solve import Solve
from params import *
#import random
import logging

# param_logger = logging.getLogger("param_logger")
# program_handler = logging.FileHandler('param.log')
# program_handler.setLevel(level=logging.WARNING)
# param_logger.warning('START OF THE LOGGING')


def theta0_p0(params, rmax_in, velocity):
    """

    :param params: list of parameters: searching boundaries (for theta0 and p0) 
    :param rmax: current maximum radius of the balloon
    :param velocity: current velocity (input)
    :return: result array: theta0, a, theta (theta_last) and radius (r_last) on the top of the balloon,
    """      
    rmax_tol = 1e-3

    r_last = 0.1
    theta_last = 0
    p0 = -14.16 #random.uniform(params[3], params[2])
    theta0_max, theta0_min, p0_max, p0_min = params
    count = 0
    while (abs(theta_last + 90) > 1e-3) or (abs(r[-1]) > 1e-3):
        # param_logger.warning("Big cycle")
        count += 1
        theta0_prev = theta0_min
        theta0_step = (theta0_max - theta0_min) / 10
        while (abs(theta_last + 90) > 1e-3):
            theta0 = theta0_prev + theta0_step
            result = Solve([theta0, p0], rmax_in, velocity)
            result = np.array(result)    
            theta, _, z, r, p_gas, p_air = result 
            
            theta_last = np.degrees(theta[-1])
            
            if theta_last > -90:
                theta0_prev = theta0
            
            elif theta_last < - 90:
                theta0_step /= 10
            
        p0_prev = p0_min
        p0_step = (p0_max - p0_min) / 10
        while (abs(r_last) > 1e-3):
            p0 = p0_prev + p0_step
            result = Solve([theta0, p0], rmax_in, velocity)
            result = np.array(result)    
            theta, _, z, r, p_gas, p_air = result 
            
            r_last = r[-1]
            
            if r_last > 0:
                p0_prev = p0
            
            elif r_last < 0:
                p0_step /= 10
        
        
        
        rmax_out = max(r)
        while abs(rmax_out - rmax_in) > rmax_tol: 
            if rmax_out != 0:
                rmax_in = rmax_out
            theta, _, z, r, p_gas, p_air = Solve([theta0, p0], rmax_out, velocity)
            rmax_out = max(r)
            
            
        theta_last = np.degrees(theta[-1])
        r_last = r[-1]
        # plt.plot(z, r)
        # plt.savefig("total.png")   
        # plt.clf()
        # param_logger.warning(theta_last, np.degrees(theta0), r_last, p0, rmax_out, np.degrees(theta0_min), np.degrees(theta0_max), p0_min, p0_max)

    print(count)
    res = np.array([theta0, p0, theta_last, r_last, rmax_out, z, r, theta, p_gas, p_air])
    return res
