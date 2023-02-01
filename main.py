import time
import numpy as np
from matplotlib import pyplot as plt
from solve import buoyancy
from density import density
from params import *
from theta0_a import theta0_a
import pandas as pd


def initialize(height):
    """ 
    defining initial parameters for a and theta0
    :param height: current altitude
    :return: min and max values  
    """
    if height < 21500:
        theta0_max = 2
        theta0_min = 0
        a_max = 10
        a_min = 7
    else:
        theta0_max = 90
        theta0_min = 20
        a_max = 5
        a_min = -400

    return a_min, a_max, theta0_min, theta0_max


def main(number_of_cores, height):
    """
    finding optimal solution optimizing maximal radius (r_max) and mass of gas (m_gas)
    :param: number_of_cores - number of cores which we use for calculations
    :param: height - current altitude (m)
    :return: results in txt file, data in csv files and plots
    """
    rho_atm, _, P_atm, T_gas = density(height)

    a_min, a_max, theta0_min, theta0_max = initialize(height)
    rmax_tol = 1e-2
    mgas_tol = 1e-1
    
    velocity = 4  
    
    m_gas_output = 0
    m_gas = 3.491565771 # mass of the lighter-than-air (LTA) gas (kg)

    delta_mgas = m_gas - m_gas_output    
    while abs(delta_mgas) > mgas_tol:
        rmax = rp_max
        rmax_new = 0
        
        while rmax - rmax_new > rmax_tol:
            if rmax_new != 0:
                rmax = rmax_new

            theta0, a, theta_last, r_last, max_radius, z, r, theta = theta0_a([theta0_max, theta0_min, a_max, a_min], rmax, velocity, number_of_cores)

            rmax_new = max_radius 
            

        volume = np.pi / 3 * ds * np.cos(np.radians(theta0)) * (r[0] ** 2 + r[0] * r[1] + r[1] ** 2)
        m_gas_output = 0
        for i in range(2, len(r)):
            dV_i = np.pi / 3 * ds * np.cos(theta[i - 1]) * (r[i - 1] ** 2 + r[i - 1] * r[i] + r[i] ** 2)
            volume += dV_i
            dm_i = (P_atm + buoyancy(height)*(z[i] - a)) * dV_i * mu_gas / (R * T_gas) 
            m_gas_output += dm_i
            
        
        Fg = (m_payload + m_b + m_gas) * g
        Fa = rho_atm * volume * g
        
        velocity_output = np.sign(Fa - Fg) * math.sqrt((2 * abs(Fa - Fg) / (Cx * rho_atm * math.pi * rmax ** 2)))
        F_drag = -Cx * (rho_atm * velocity_output * abs(velocity_output) * math.pi * rmax ** 2) / 2 
        dF = (Fa - Fg) + F_drag    

        delta_mgas =  m_gas - m_gas_output
        delta_velocity = velocity - velocity_output

        print("velocity_output = ", velocity_output, ", velocity = ", velocity, ", difference = ", abs(delta_velocity))
        print("m gas output = ", m_gas_output, ", m gas = ", m_gas, ", difference = ", abs(delta_mgas))

        velocity = velocity - (delta_velocity / 2 )
        

    Fg = (m_payload + m_b + m_gas) * g
    Fa = rho_atm * volume * g
    
    velocity_output = np.sign(Fa - Fg) * math.sqrt((2 * abs(Fa - Fg) / (Cx * rho_atm * math.pi * rmax ** 2)))
    F_drag = -Cx * (rho_atm * velocity_output * abs(velocity_output) * math.pi * rmax ** 2) / 2 
    dF = (Fa - Fg) + F_drag

    f = open('%s' % output_filename, 'w')

    print("_______________________height = ", height, "_______________________", file=f)
    print("theta0: ", theta0, ", a: ", a, file=f)
    print("Maximum radius: ", max_radius, file=f)
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
    main(number_of_cores, height)
    end = time.time()
    
    f = open('%s' % output_filename, 'a')
    print("Running time: ", end - start, "s", file=f)
