import numpy as np
from matplotlib import pyplot as plt
from solve import Solve
from params import *
import random


def theta0_p0(params, rmax_in, velocity):
    """

    :param params: list of parameters: searching boundaries (for theta0 and p0) 
    :param rmax: current maximum radius of the balloon
    :param velocity: current velocity (input)
    :return: result array: theta0, a, theta (theta_last) and radius (r_last) on the top of the balloon,
    """      
    rmax_out = 0
    rmax_tol = 1e-9

    r_last = 0.1
    theta_last = 0
    p0 = -14.16 #random.uniform(params[3], params[2])
    
    while (abs(theta_last + 90) > 1e-3) or (abs(r_last) > 1e-3):
        theta0_max, theta0_min, p0_max, p0_min = params
        
        while (abs(theta_last + 90) > 1e-4):
            theta0 = (theta0_min + theta0_max) / 2

            result = Solve([theta0, p0], rmax_in, velocity)
            result = np.array(result)    
            theta, _, z, r, p_gas, _ = result 
            
            theta_last = np.degrees(theta[-1])
            r_last = r[-1]
            #print(np.degrees(theta_last))
            
            if theta_last < -90:
                theta0_max = theta0
            else: 
                theta0_min = theta0
                
                
        while (abs(r_last) > 1e-3):
            p0 = (p0_min + p0_max) / 2
            result = Solve([theta0, p0], rmax_in, velocity)
            result = np.array(result)    
            theta, _, z, r, p_gas, _ = result 
                
            theta_last = np.degrees(theta[-1])
            r_last = r[-1] 
            
            if r_last < 0:
                p0_max = p0
            else:
                p0_min = p0
                

        while abs(rmax_out - rmax_in) > rmax_tol:  
            if rmax_out != 0:
                rmax_in = rmax_out
            theta, _, z, r, p_gas, _ = Solve([theta0, p0], rmax_in, velocity)
            rmax_out = max(r)


    res = np.array([theta0, p0, theta_last, r_last, rmax_out, z, r, theta, p_gas])
    return res
