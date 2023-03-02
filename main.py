import time
import numpy as np
from matplotlib import pyplot as plt
from solve import buoyancy, Solve
from density import density
from params import *
from grid_search import theta0_a
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

def initialize(height):
    """ 
    defining initial parameters for a and theta0 grid
    :param height: current altitude
    :return: min and max values and step of grid  
    """
    if height < 21500:
        theta0_max = 10
        theta0_min = 0
        a_max = 10
        a_min = 0
        number_of_steps_a = 80
        number_of_steps_theta0 = 100
    else:
        theta0_max = 90
        theta0_min = 20
        a_max = 5.1
        a_min = -400
        number_of_steps_a = 100
        number_of_steps_theta0 = 70

    return a_min, a_max, number_of_steps_a, theta0_min, theta0_max, number_of_steps_theta0


def main(number_of_cores, height):
    """
    finding optimal solution optimizing maximal radius (r_max) and mass of gas (m_gas)
    :param: number_of_cores - number of cores which we use for calculations
    :param: height - current altitude (m)
    :return: results in txt file, data in csv files and plots
    """
    rho_atm, _, P_atm, T_gas = density(height)

    a_min, a_max, number_of_steps_a, theta0_min, theta0_max, number_of_steps_theta0 = initialize(height)
    rmax_tol = 1e-4
    mgas_tol = 1e-2
    
    velocity = 2.918
    
    m_gas_output = 0
    m_gas = 3.491565771 # mass of the lighter-than-air (LTA) gas (kg)

    delta_mgas = m_gas - m_gas_output

    while abs(delta_mgas) > mgas_tol:
        rmax_in = rp_max
        rmax_out = 0
        count_rmax = 0
        epsilon = np.finfo(float).eps # very small number

        #theta0, a = 1.2, 8.5

        i = 0
        while True:
            
            a_min, a_max, number_of_steps_a, theta0_min, theta0_max, number_of_steps_theta0 = initialize(height)
            # print("R_max before = ", rmax)
            # print("R max new = ", rmax_new)
            # print("R_max after = ", rmax)

            number_of_recurse = 2
            for i in range(number_of_recurse):
                theta0_step = (theta0_max - theta0_min) / number_of_steps_theta0
                a_step = (a_max - a_min) / number_of_steps_a
                
                theta0, a, theta_last, r_last, max_radius, loss, z, r, theta = theta0_a([theta0_max, theta0_min, a_max, a_min, theta0_step, a_step], rmax_in, velocity, number_of_cores)
                
                theta0_max, theta0_min = theta0 + theta0_step + epsilon, theta0 - theta0_step - epsilon
                a_max, a_min = a + a_step + epsilon, a - a_step - epsilon 
            print("theta0: ", theta0, ", a: ", a)
            # plt.plot(z, r)
            # plt.savefig("after_grid%s.png" % i)

            rmax_out = max_radius

            while abs(rmax_out - rmax_in) > rmax_tol:
                rmax_in = rmax_out

                theta, _, z, r = Solve([theta0, a], rmax_in, velocity)
                rmax_out = max(r)
                
            theta_last = theta[-1]
            r_last = r[-1]
            # plt. plot(z, r)
            # plt.savefig("after_rmax%s.png" % i)

            if (abs(np.degrees(theta_last) + 90) < 1e-3) and (abs(r_last) < 1e-3):
                break
            
            print("last theta: ", np.degrees(theta_last), ", last r: ", r_last)
            i+=1

        #print("Iterations for finding optimal rmax: ", count_rmax)

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

        print("output velocity: ", velocity_output, ", input velocity: ", velocity, ", difference = ", abs(delta_velocity))
        print("output m_gas = ", m_gas_output, ", input m_gas = ", m_gas, ", difference = ", abs(delta_mgas))

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
    print("Last theta: ", np.degrees(theta_last), ", Last R: ", r_last, file=f)
    print("Total lost (for theta0 and a): ", loss, file=f)
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
