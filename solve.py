import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
from density import density
from calculate_rp import get_sr
from params import *


def buoyancy(height):
    """
    calculate buoyancy on the current altitude
    using density(height) function
    
    :param height: altitude
    :return: buoyancy value
    """
    ro_atm = density(height)[0]
    ro_gas = density(height)[1]
    buoyancy = (ro_atm - ro_gas) * g
    return buoyancy


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
    theta0, a = params

    rs, s_half = get_sr(rp_max) # just gets lists of s and r for half of the balloon's core length
    f = interp1d(s_half, rs, kind='cubic') # interpolate r's in all points on that interval [0, l/2]
    

    def func(t, y):
        if t <= l / 2:
            rp = f(t)
        else:
            rp = f(l - t)
        theta, T, z, r = y
        
        p = buoyancy(height) * (z - a) # differential pressure of the balloon, a is determined by the algorithm
        sin = np.sin(theta)
        cos = np.cos(theta)
        return [
            - 2 * np.pi * (rp * wp * sin + p * r) / T, # derivative of theta
            2 * np.pi * rp * wp * cos, # derivative of T
            cos, # derivative of z 
            sin # derivative of r
        ]
    
    # boundary conditions (theta0, T0, z0, r0), theta0 is determined by the algorithm
    T0 = (L0 + Cx * density(height)[0][0] * velocity * abs(velocity) * math.pi * rmax**2 / 2) / np.cos(theta0)
    z0, r0 = 0, 0 

    sol = solve_ivp(func, t_span=[0, l], y0=[theta0, T0, z0, r0], t_eval=np.arange(0, l, ds)) 

    return sol.y
