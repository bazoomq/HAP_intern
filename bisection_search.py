import numpy as np
from matplotlib import pyplot as plt
from solve import Solve
from params import *
#import random
import logging

param_logger = logging.getLogger("param_logger")
program_handler = logging.FileHandler('param.log')
program_handler.setLevel(level=logging.WARNING)
param_logger.warning('START OF THE LOGGING')


def theta0_p0(params, rmax_in, velocity):
    """

    :param params: list of parameters: searching boundaries (for theta0 and p0) 
    :param rmax: current maximum radius of the balloon
    :param velocity: current velocity (input)
    :return: result array: theta0, a, theta (theta_last) and radius (r_last) on the top of the balloon,
    """      
    rmax_out = 0
    rmax_tol = 1e-6

    r_last = 0.1
    theta_last = 0
    p0 = -14.16 #random.uniform(params[3], params[2])
    theta0_max, theta0_min, p0_max, p0_min = params
    #theta_last_arr, r_last_arr, p0_arr, theta0_arr, rmax_arr = [], [], [], [], []
   # df = open('log2.txt', 'w')
    #print("theta_last               theta0                  r_last                  p0                        rmax", file=df)
    while (abs(theta_last + 90) > 1e-3) or (abs(r_last) > 1e-3):
        param_logger.warning("Big cycle")

        p0_max, p0_min = params[2], params[3]
    
        theta0_max += np.radians(0.05)
        theta0_min -= np.radians(0.05)
        p0_max += 0.05
        p0_min -= 0.05
        while (abs(theta_last + 90 ) > 1e-3):
            param_logger.warning("theta cycle")

            theta0 = (theta0_min + theta0_max) / 2

            result = Solve([theta0, p0], rmax_in, velocity)
            result = np.array(result)    
            theta, _, z, r, p_gas, _ = result 

            # for i in range(2, len(theta)):
            #     count = 0
            #     if np.sign(theta[i] - theta[i - 1]) + np.sign(theta[i - 1] - theta[i - 2]) == 0:
            #         count += 1

            # if count > 1:
            #     continue
            
            theta_last = np.degrees(theta[-1])
            r_last = r[-1]
            #print(np.degrees(theta_last))
            
            if theta_last + 90 < 0:
                theta0_max = theta0 
            else: 
                theta0_min = theta0
            
            plt.plot(z, r)
            plt.savefig("theta0.png")   
            plt.clf()
        # without loops   
        print(theta_last, theta0)
        while (abs(r_last) > 1e-3):
            param_logger.warning("r_last cycle")

            p0 = (p0_min + p0_max) / 2
            result = Solve([theta0, p0], rmax_in, velocity)
            result = np.array(result)    
            theta, _, z, r, p_gas, _ = result 
                
            theta_last = np.degrees(theta[-1])
            r_last = r[-1] 
            print(r_last, p0, p0_min, p0_max)
            if r_last < 0:
                p0_max = p0 
            else:
                p0_min = p0
            plt.plot(z, r)
            plt.savefig("p0.png")   
            plt.clf()
            
        rmax_out = max(r)
        while abs(rmax_out - rmax_in) > rmax_tol: 
            param_logger.warning("r_max cycle")
 
            if rmax_out != 0:
                rmax_in = rmax_out
            theta, _, z, r, p_gas, _ = Solve([theta0, p0], rmax_in, velocity)
            rmax_out = max(r)
        plt.plot(z, r)
        plt.savefig("total.png")   
        plt.clf()
        # theta_last_arr.append(theta_last)
        # theta0_arr.append(theta0)
        # p0_arr.append(p0)
        # r_last_arr.append(r_last)
        # rmax_arr.append(rmax_out)
        #print(theta_last, "        ", np.degrees(theta0), "        ", r_last, "        ", p0, "        ", rmax_out, file=df)
        param_logger.warning(theta_last, np.degrees(theta0), r_last, p0, rmax_out, np.degrees(theta0_min), np.degrees(theta0_max), p0_min, p0_max)


    res = np.array([theta0, p0, theta_last, r_last, rmax_out, z, r, theta, p_gas])
    return res
