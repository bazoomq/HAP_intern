import time
import numpy as np
from matplotlib import pyplot as plt
from solve import Solve, b
from density import density
from params import *
from theta0_a import theta0_a


def main(number_of_cores, h):
    if h < 21500:
        theta0_max = 25
        theta0_min = 0
        a_max = 16
        a_min = 5
        number_of_steps_a = 50
    else:
        theta0_max = 90
        theta0_min = 20
        a_max = 5.1
        a_min = -400
        number_of_steps_a = 100
        
    number_of_steps_theta0 = 90

    tol_rmax = 1e-1
    tol_mgas = 1e-1

    init_velocity = 1  
    velocity = init_velocity  
    velocity_output = 3
    velocity_tollerance = 1e-1
    m_gas_out = 0
    m_gas = 3.491565771
    while abs(velocity - velocity_output) > velocity_tollerance or abs(m_gas_out - m_gas) > tol_mgas:
        velocity = velocity_output
        m_gas = m_gas_out

        print("velocity = ", velocity)
        rmax = rp_max
        rmax_new = 0
        count_rmax = 0
        
        while rmax - rmax_new > tol_rmax:
            if rmax_new != 0:
                rmax = rmax_new

            number_of_recurse = 5
            for i in range(number_of_recurse):
                print('r_max = ', rmax, ', DEPTH ', i)
                # print(theta_max, theta_min)
                # print(a_max, a_min)
                theta_tol = 3 / (1.2)**i
                if i <= 5:
                    r_tol = 2 / 2 ** i 
                else:
                    r_tol = 2 / 2**5

                theta_step = (theta0_max - theta0_min) / number_of_steps_theta0
                a_step = (a_max - a_min) / number_of_steps_a
                res = theta0_a([theta0_max, theta0_min, a_max, a_min, theta_step, a_step], [theta_tol, r_tol], rmax, velocity, number_of_cores)
                theta0_max, theta0_min = res[0] - 10 / 2 ** i, res[0] + 10 / 2 ** i

                if h < 21500:
                    a_max, a_min = res[1] - 2 / 2 ** i, res[1] + 2 / 2 * i    
                else:
                    a_max, a_min = res[1] - 50 / 2 ** i, res[1] + 50 / 2 * i

            rmax_new = res[4] 
            count_rmax += 1

        print("Iterations for finding optimal rmax: ", count_rmax)

        V = np.pi / 3 * ds * np.cos(np.radians(res[0])) * (res[7][0] ** 2 + res[7][0] * res[7][1] + res[7][1] ** 2)
        m_gas_out = 0
        for i in range(2, len(res[7])):
            dV_i = np.pi / 3 * ds * np.cos(res[8][i - 1]) * (res[7][i - 1] ** 2 + res[7][i - 1] * res[7][i] + res[7][i] ** 2)
            V += dV_i
            dm_i = (density(h)[1] + b(h)*(res[6][i] - res[1])) * dV_i * mu_gas / (R * density(h)[2]) 
            m_gas_out += dm_i
            
        
        theta0, a = res[0], res[1]
        Fg = (m_payload + m_b + m_gas) * g
        Fa = density(h)[0][0] * V * g
        
        velocity_output = np.sign(Fa - Fg) * math.sqrt((2 * abs(Fa - Fg) / (Cx * density(h)[0][0] * math.pi * rmax ** 2)))
        F_drag = -Cx * (density(h)[0][0] * velocity_output * abs(velocity_output) * math.pi * rmax ** 2) / 2 
        dF = (Fa - Fg) + F_drag

        
        
    theta0, a = res[0], res[1]
    Fg = (m_payload + m_b + m_gas) * g
    Fa = density(h)[0][0] * V * g
    
    velocity_output = np.sign(Fa - Fg) * math.sqrt((2 * abs(Fa - Fg) / (Cx * density(h)[0][0] * math.pi * rmax ** 2)))
    F_drag = -Cx * (density(h)[0][0] * velocity_output * abs(velocity_output) * math.pi * rmax ** 2) / 2 
    dF = (Fa - Fg) + F_drag

    print("__________________________________")
    print("____________RESULTS_______________")
    print("____________h = ", h, "____________")

    print("theta0: ", theta0, ", a: ", a)
    print("Total lost (for theta0 and a): ", res[5])
    print("r max: ", res[4])
    print("Last theta: ", np.degrees(res[2]), ", Last R: ", res[3])
    print("Volume of the balloon: ", V)
    print("Difference between m_gas and calculated m_gas: ", m_gas_out - m_gas)
    print("Difference between forces", dF)
    print("Velocity of the balloon: ", velocity)
    print("Velocity of the balloon output: ", velocity_output)
    print("Difference between input and output velocities: ", velocity - velocity_output)
    print("Difference betweend Fa and Fg: ", Fa - Fg)

    plt.plot(res[6], res[7])
    # plt.text(0.5, 0.5, 'height: {}, velocity: {}'.format(h, round(velocity, 3)))
    # plt.text(0.5, 0.2, 'theta0: {}, a: {}, volume: {}'.format(round(theta0, 4), round(a, 3), round(V, 3)))
    plt.savefig('height_%s.svg' % h)


if __name__=="__main__":
    start = time.time()
    
    main(number_of_cores, h)

    end = time.time()
    print("Running time: ", end - start, "s")
