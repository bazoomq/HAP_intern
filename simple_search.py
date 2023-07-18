import numpy as np
from matplotlib import pyplot as plt
from solve import Solve
from params import *


def theta0_p0(params, rmax_in, velocity, height):
    """
    searching optimal parameters theta0 and p0, and rmax for current rmax_in and velocity
    
    :param params: list of parameters: searching boundaries (for theta0 and p0) 
    :param rmax_in: input maximal radius of the balloon on current altitude
    :param velocity: current velocity (input)
    :return: result array: theta0, p0, theta (theta_last) and radius (r_last) on the top of the balloon
    """      
    rmax_tol = 1e-3

    r_last = 0.1
    theta_last = 0
    theta0 = 85.5 # start p0
    theta0_max, theta0_min, p0_max, p0_min = params
    
    while (abs(theta_last + 90) > 1e-2) or (abs(r[-1]) > 1e-2):
        p0_prev = p0_min
        p0_step = (p0_max - p0_min) / 10
        # p0 computing loop
        while (abs(r_last) > 1e-2):
            p0 = p0_prev + p0_step
            result = Solve([theta0, p0], rmax_in, velocity, height)
            result = np.array(result)    
            theta, _, z, r, p_gas, p_air = result 
            
            r_last = r[-1]
            
            if r_last > 0:
                p0_prev = p0
            
            elif r_last < 0:
                p0_step /= 10
        
        theta0_prev = theta0_min
        theta0_step = (theta0_max - theta0_min) / 10
        
        # theta0 computing loop
        while (abs(theta_last + 90) > 1e-2):
            theta0 = theta0_prev + theta0_step
            result = Solve([theta0, p0], rmax_in, velocity, height)
            result = np.array(result)    
            theta, _, z, r, p_gas, p_air = result 
            
            theta_last = np.degrees(theta[-1])
            plt.clf()
            plt.plot(z, r)
            plt.savefig('plot.png')
            if theta_last > -90:
                theta0_prev = theta0
            
            elif theta_last < -90:
                theta0_step /= 10
                
        # rmax synchronization
        rmax_out = max(r)
        while abs(rmax_out - rmax_in) > rmax_tol: 
            if rmax_out != 0:
                rmax_in = rmax_out
            theta, _, z, r, p_gas, p_air = Solve([theta0, p0], rmax_out, velocity, height)
            rmax_out = max(r)
            
            
        theta_last = np.degrees(theta[-1])
        r_last = r[-1]

    res = np.array([theta0, p0, theta_last, r_last, rmax_out, z, r, theta, p_gas, p_air])
    return res
