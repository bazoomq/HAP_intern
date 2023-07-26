from math import sqrt, pi, asin
from scipy.special import hyp2f1, ellipkinc
import pandas as pd
from params import *
import matplotlib.pyplot as plt
import numpy as np


def volume_cone_pumpkin(eps):
    """
    calculate volume of the cone-pumpkin conjugated balloon depends on epsilon
    using scipy.special package's funtctions: 
    - ellipkinc: calculate incomplete elliptic integral of the first kind
    - hyp2f1: 2F1 hypergeometric function
    
    :param eps: epsilon = x / Rx, where Rx is radius of balloon 
    :return: volume and radius of the cone-pumpkin shape balloon
    """
    f_V = pi / 3 * (eps / sqrt(1 - eps ** 4) - hyp2f1(1/2, 1/4, 5/4, eps ** 4) * eps) + k_V
    f_S = eps / sqrt(1 - eps ** 4) + 2 * k_S - hyp2f1(1/2, 1/4, 5/4, eps ** 4) * eps
    Rx = 2 * s0_b / f_S
    V = f_V * Rx ** 3
    
    return V, Rx


def radius_cone_pumpkin(V_b):
    """
    calculate radius of the pumpkin part, calculate radius and height of the cone part of the cone-pumpkin conjugated balloon,
    getting accurate epsilon using simple bisection method (with eps_error)  
    using volume_cone_pumpkin function: calculate volume of the cone-pumpkin conjugated balloon depends on epsilon

    :param V_b: balloon volume
    :return: epsilon, radius of the pumpkin part, radius (on the top) and height of the cone part
    """
    eps_error = 1e-9
    eps0 = 0
    eps1 = 1
 
    while (abs((eps1 - eps0) / eps1)) >= eps_error:
        eps = (eps0 + eps1) / 2
        volume_diff = volume_cone_pumpkin(eps)[0] - V_b 

        if (volume_diff < 0):
            eps1 = eps
        else:
            eps0 = eps

    pumpkin_radius = volume_cone_pumpkin(eps)[1]
    cone_radius = eps * pumpkin_radius
    cone_height = cone_radius / sqrt(1 / (eps**4) - 1)
    print("Difference of volumes: ", volume_diff)

    return eps, pumpkin_radius, cone_radius, cone_height


def calculation_from_file(input, output):
    """
    get data from a CSV file, perform calculations and write the results to another CSV file    
    :param input: path to csv file to read the list of input volumes
    :param output: path to csv file to save results 
    :return: 
    """
    df = pd.DataFrame(columns=['epsilon', 'radius of the balloon', 'x of cone', 'height of cone'], dtype=object)
    df.to_csv(output_cone_pumpkin, index=False)

    volume_arr = pd.read_csv(input_cone_pumpkin).values
    for i in volume_arr:
        eps, Rx, x_cone, h_cone = radius_cone_pumpkin(i)
        new_row = pd.DataFrame([[eps, Rx, x_cone, h_cone]]) 
        new_row.to_csv(output_cone_pumpkin, mode='a', index=False, header=False) 
    
    return


def make_plot(pumpkin_radius, cone_radius, cone_height, name):
    z_arr, r_arr = [], []
    z_lag = hyp2f1(1/2, 3/4, 7/4, cone_radius ** 4 / pumpkin_radius ** 4) * (cone_radius ** 3) / (3 * pumpkin_radius ** 2)
    
    A = [0, 0]
    B = [cone_radius, cone_height]
    C = [0, cone_height]
    
    for r in np.arange(cone_radius, pumpkin_radius, (pumpkin_radius - cone_radius) / 100):
        z = hyp2f1(1/2, 3/4, 7/4, r ** 4 / pumpkin_radius ** 4) * (r ** 3) / (3 * pumpkin_radius ** 2)   
        z_arr.append(z + cone_height - z_lag)
        r_arr.append(r)
        
    for r in np.arange(pumpkin_radius, 0, -pumpkin_radius / 100):
        z = hyp2f1(1/2, 3/4, 7/4, r ** 4 / pumpkin_radius ** 4) * (r ** 3) / (3 * pumpkin_radius ** 2)
        z_arr.append(-z + cone_height - z_lag + pumpkin_radius * k_Vp)
        r_arr.append(r)

    plt.clf()
    plt.gca().set_aspect('equal')
    plt.plot(z_arr, r_arr)
    
    plt.plot([A[1], B[1]], [A[0], B[0]], 'b-')  
    plt.plot([A[1], C[1]], [A[0], C[0]], 'b-')  
    plt.plot([B[1], C[1]], [B[0], C[0]], 'b-')  
    plt.savefig(name)
    
    return
    
    
if __name__=="__main__":
    """
    how to use: 
    python cone_pumpkin_conjugation.py --input_cone_pumpkin INPUT_FILE_PATH --output_cone_punpkin OUTPUT_FILE_PATH
    """
    #calculation_from_file(input_cone_pumpkin, output_cone_pumpkin)
    
    make_plot(2.779112032701169, 2.7426552741646253, 11.77641299398457, "plot_129.png")
    make_plot(3.381259022081012, 3.3038462243182645, 10.604168056633558, "plot_192.png")
    make_plot(4.11331314513517, 3.936275990706959, 8.973747194794122, "plot_284.png")
    make_plot(5.022450308907609, 4.539925815154523, 6.434290066509123, "plot_424.png")
    make_plot(6.122831760301824, 0.18315056023670923, 0.00016387785680984195, "plot_630.png")