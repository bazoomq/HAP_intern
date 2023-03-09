import numpy as np
from params import *
from density import density


def barometric(height, p0):
    """
    calculate differential pressure using barometric approach ????
    :param height: current altitude of the balloon
    :param p0: differential pressure at the nadir of the balloon
    :return: differential pressure, difference between ????
    """
    
    P_atm, T_gas = density(height)[2], density(height)[3]
    p_air = P_atm
    p_gas = P_atm + p0
    dT_gas = 0

    p_gas_arr, p_air_arr, dp_arr = [], [], []
    for i in np.arange(0, l + ds, ds):
        p_gas -= p_gas * mu_gas * g * ds / R / T_gas
        p_air -= p_air * mu_air * g * ds / R / (T_gas + dT_gas)
        dp = p_gas - p_air

        p_gas_arr.append(p_gas)
        p_air_arr.append(p_air)
        dp_arr.append(dp)
    return p_gas, dp