import numpy as np
from density import density
from params import *
from simple_search import theta0_p0
from main import initialize


def float_search(velocity, height_min, height_max):
    rmax_in = 6.1
    mgas_tol = 1e-2
    m_gas = 3.49156577061832 # mass of the lighter-than-air (LTA) gas (kg)
    m_gas_output = 0
    delta_mgas = m_gas - m_gas_output
    height_prev = height_min
    height_step = (height_max - height_min) / 10
    
    while delta_mgas > mgas_tol:
        delta_mgas_prev = delta_mgas
        
        height = height_prev + height_step
        rho_atm, _, P_atm, T_gas, T_atm = density(height)

        p0_min, p0_max, theta0_min, theta0_max = initialize(height)
        
        theta0, p0, theta_last, r_last, rmax_out, z, r, theta, p_gas, p_air = theta0_p0([theta0_max, theta0_min, p0_max, p0_min], rmax_in, velocity, height)
        volume = np.pi / 3 * ds * np.cos(theta0) * (r[0] ** 2 + r[0] * r[1] + r[1] ** 2)
        m_gas_output = 0
        
        # compute volume, forces and m_gas
        for i in range(2, len(r)):
            dV_i = np.pi / 3 * ds * np.cos(theta[i - 1]) * (r[i - 1] ** 2 + r[i - 1] * r[i] + r[i] ** 2)
            volume += dV_i
            ro_gas_prev = p_gas[i - 1] * mu_gas / (R * T_gas)
            ro_gas_curr = p_gas[i] * mu_gas / (R * T_gas) 

            dm_i = (ro_gas_prev + ro_gas_curr) * dV_i / 2
            m_gas_output += dm_i
            
        delta_mgas = abs(m_gas - m_gas_output)
        
        if delta_mgas - delta_mgas_prev < 0:
            height_prev = height
        else:
            height_step /= 10
            
    return height


float_search(0, 25000, 25350)


        