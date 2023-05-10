import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
from density import density
from calculate_rp import get_sr
from params import *


def Solve(params, rmax, velocity):
    """
    integration of a system of the differential equations that determine the shape of the balloon 
    at the current altitude with current velocity and maximum radius
    
    using scipy.interpolation package's function:
    - interp1d: interpolate a 1-D function
    scipy.integrate package's function:
    - solve_ivp: this function numerically integrates a system of ordinary differential equations given an initial value, use 4th order Runge-Kutta method
    and get_sr(rp_max) function

    :param params: [theta0, a] - current theta0 and a values - params of a system 
    :param rmax: maximal radius of the natural shape balloon
    :param velocity: velocity of the natural shape balloon
    :return: solution of a system of the differential equations: lists of theta, T, z, r respectively
    """
    theta0, p0 = params
    rho_atm, _, P_atm, T_gas = density(height)
    rs, s_half = get_sr(rp_max) # just gets lists of s and r for half of the balloon's core length
    f = interp1d(s_half, rs, kind='cubic') # interpolate r's in all points on that interval [0, l/2]

    p_gas = P_atm + p0
    p_air = P_atm
    
    
    def func(t, y):
        if t <= l / 2:
            rp = f(t)
        else:
            rp = f(l - t)
        theta, T, z, r, p_gas, p_air = y
                
        k_h = mu_gas * g / (R * T_gas)
        k_h_air = mu_air * g / (R * T_gas)
        
        sin = np.sin(theta)
        cos = np.cos(theta)
        
        return [
            - 2 * np.pi * (rp * wp * sin + (p_gas - p_air) * r) / T, # derivative of theta
            2 * np.pi * rp * wp * cos, # derivative of T
            cos, # derivative of z 
            sin, # derivative of r
            - p_gas * k_h * cos, # derivative of p_gas 
            - p_air * k_h_air * cos # derivative of p_air
        ]
    
    # boundary conditions (theta0, T0, z0, r0), theta0 is determined by the algorithm
    T0 = (L0 + Cx * rho_atm * velocity * abs(velocity) * math.pi * rmax ** 2 / 2) / np.cos(theta0)
    z0, r0 = 0, 0 

    sol = solve_ivp(func, t_span=[0, l], y0=[theta0, T0, z0, r0, p_gas, p_air], t_eval=np.arange(0, l, ds)) 

    return sol.y
