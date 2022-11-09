from math import sqrt, pi, asin
from scipy.special import hyp2f1, ellipkinc
import pandas as pd


k_V = 2.7458122499512 # coefficient of pumpkin shape volume
k_Sp = 0.739668778  # coefficient of pumpkin shape area
k_S = k_Sp * sqrt(pi) 
R_b = 6.122831782671 # radius of fully the inflated balloon pumpkin (m)
So_b = k_S * R_b


def volume_cone_pumpkin(eps):
    """
    calculate volume of the cone-pumpkin shape balloon depends on epsilon
    using scipy.special package's funtctions: 
    - ellipkinc: calculate incomplete elliptic integral of the first kind
    - hyp2f1: 2F1 hypergeometric function
    
    :param eps: epsilon = x / Rx, where Rx is radius of balloon 
    :return: volume and radius of the cone-pumpkin shape balloon
    """
    f_V = pi / 3 * eps / sqrt(1 - eps ** 4) - ellipkinc(asin(eps), -1) + k_V
    f_S = eps / sqrt(1 - eps ** 4) + 2 * k_S - hyp2f1(1/2, 1/4, 5/4, eps ** 4) * eps
    Rx = 2 * So_b / f_S
    V = f_V * Rx ** 3
    
    return V, Rx


def radius_cone_pumpkin(V_b):
    """
    calculate radius of pumpkin part, calculate x and height of cone part of the cone-pumpkin shape balloon,
    getting accurate epsilon using simple bisection method (with eps_error)  
    using volume_cone_pumpkin function: calculate volume of the cone-pumpkin shape balloon depends on epsilon

    :param V_b: balloon volume
    :return: epsilon, radius of the cone-pumpkin shape balloon, x and height of cone part
    """
    eps_error = 1e-6
    eps0 = 0
    eps1 = 1
 
    while (abs((eps1 - eps0) / eps1)) >= eps_error:
        eps = (eps0 + eps1) / 2
        V_b_eq = volume_cone_pumpkin(eps)[0] - V_b 

        if (V_b_eq < 0):
            eps1 = eps
        else:
            eps0 = eps

    Rx = volume_cone_pumpkin(eps)[1]
    x_cone = eps * Rx
    h_cone = x_cone / sqrt(1 / (eps**4) - 1)
    print("Difference of volumes: ", V_b_eq)

    return eps, Rx, x_cone, h_cone


# output results to csv file

df = pd.DataFrame(columns=['epsilon', 'radius of the balloon', 'x of cone', 'height of cone'], dtype=object)
df.to_csv('./results/cone_pumpkin_conjugate.csv', index=False)

volume_arr = [192.219]
for i in volume_arr:
    eps, Rx, x_cone, h_cone = radius_cone_pumpkin(i)
    new_row = pd.DataFrame([[eps, Rx, x_cone, h_cone]]) 
    new_row.to_csv('./results/cone_pumpkin_conjugate.csv', mode='a', index=False, header=False) 
