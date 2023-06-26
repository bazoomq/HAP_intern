import time
import numpy as np
from matplotlib import pyplot as plt
from density import density
from params import *
from simple_search import theta0_p0
import pandas as pd


def initialize(height):
    """ 
    defining initial parameters for p0 and theta0
    :param height: current altitude
    :return: min and max values  
    """
    if height < 21500:
        theta0_max = 1.4
        theta0_min = 1.0
        p0_max = -13.5
        p0_min = -14.5
    else:
        theta0_max = 90
        theta0_min = 20
        p0_max = 200
        p0_min = 0
    return p0_min, p0_max, np.radians(theta0_min), np.radians(theta0_max)


def main(height):
    """
    finding optimal solution optimizing maximal radius (r_max) and mass of gas (m_gas)
    :param: height - current altitude (m)
    :return: results in txt file, data in csv files and plots
    """
    rho_atm, _, P_atm, T_gas, T_atm = density(height)

    p0_min, p0_max, theta0_min, theta0_max = initialize(height)
    
    mgas_tol = 1e-7
    
    v_min = 2.8
    v_max = 3.2
    #velocity = v_min + (v_max - v_min) / 2 
    m_gas_output = 0
    m_gas = 3.491565771 # mass of the lighter-than-air (LTA) gas (kg)

    delta_mgas = m_gas - m_gas_output
    rmax_in = 3 
     
    while abs(delta_mgas) > mgas_tol:
        velocity = v_min + (v_max - v_min) / 2

        theta0, p0, theta_last, r_last, rmax_out, z, r, theta, p_gas, p_air = theta0_p0([theta0_max, theta0_min, p0_max, p0_min], rmax_in, velocity)

        volume = np.pi / 3 * ds * np.cos(theta0) * (r[0] ** 2 + r[0] * r[1] + r[1] ** 2)
        m_gas_output = 0
        Fa = 0
        for i in range(2, len(r)):
            dV_i = np.pi / 3 * ds * np.cos(theta[i - 1]) * (r[i - 1] ** 2 + r[i - 1] * r[i] + r[i] ** 2)
            volume += dV_i
            ro_gas_prev = p_gas[i - 1] * mu_gas / (R * T_gas)
            ro_gas_curr = p_gas[i] * mu_gas / (R * T_gas) 
            ro_air_prev = p_air[i - 1] * mu_air / (R * T_atm) 
            ro_air_curr = p_air[i] * mu_air / (R * T_atm) 

            Fa += (ro_air_curr + ro_air_prev) * dV_i / 2 * g
            dm_i = (ro_gas_prev + ro_gas_curr) * dV_i / 2
            m_gas_output += dm_i
            
        
        Fg = (m_payload + m_b + m_gas) * g
        Fa_integral = rho_atm * volume * g
        print("cycle: ", Fa, "integral: ", Fa_integral)
        velocity_output = np.sign(Fa - Fg) * math.sqrt((2 * abs(Fa - Fg) / (Cx * rho_atm * math.pi * rmax_out ** 2)))
        F_drag = -Cx * (rho_atm * velocity_output * abs(velocity_output) * math.pi * rmax_out ** 2) / 2 
        dF = (Fa - Fg) + F_drag    

        delta_mgas =  m_gas - m_gas_output

            
        if delta_mgas < 0:
            v_max = velocity
        else:
            v_min = velocity
        
        #velocity = v_min + (v_max - v_min) / 2

            
        #print("velocity_output = ", velocity_output, ", velocity = ", velocity, ", difference = ", abs(delta_velocity))
        print("m gas output = ", m_gas_output, ", m gas = ", m_gas, ", difference = ", abs(delta_mgas))
    # rmax = max_radius

    # Fg = (m_payload + m_b + m_gas) * g
    # Fa = rho_atm * volume * g
    
    # velocity_output = np.sign(Fa - Fg) * math.sqrt((2 * abs(Fa - Fg) / (Cx * rho_atm * math.pi * rmax ** 2)))
    # F_drag = -Cx * (rho_atm * velocity_output * abs(velocity_output) * math.pi * rmax ** 2) / 2 
    # dF = (Fa - Fg) + F_drag

    f = open('%s' % output_filename, 'w')

    print("_______________________height = ", height, "_______________________", file=f)
    print("theta0: ", np.degrees(theta0), ", p0: ", p0, file=f)
    print("Maximum radius: ", rmax_out, file=f)
    print("Last theta: ", theta_last, ", Last R: ", r_last, file=f)
    print("___________________________________________________________________", file=f)
    print("Volume of the balloon: ", volume, file=f)
    print("Difference between m_gas and calculated m_gas: ", m_gas_output - m_gas, file=f)
    print("Difference betweend Fa and Fg: ", Fa - Fg, file=f)
    print("Difference between all forces {(Fa - Fg) + F_drag}: ", dF, file=f)
    print("Input velocity of the balloon: ", velocity, file=f)
    print("Output velocity of the balloon: ", velocity_output, file=f)
    print("Difference between input and output velocities: ", velocity - velocity_output, file=f)
    
    plt.plot(z, r)
    plt.savefig('%s' % plot_filename)
 
    df = pd.DataFrame(data = {'z': z, 'r': r})
    df.to_csv('%s' % z2r_csv_filename)


if __name__=="__main__":
    """
    how to use:
    python main.py --number_of_cores NUMBER_OF_CORES --height HEIGHT
    """
    start = time.time()
    main(height)
    end = time.time()
    
    f = open('%s' % output_filename, 'a')
    print("Running time: ", end - start, "s", file=f)
