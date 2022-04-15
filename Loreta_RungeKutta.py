from math import cos, sin, radians, pi
import pandas as pd
import matplotlib.pyplot as plt
from math import exp

g = 9.8
L_0 = 1 * g
p_0 = 0
length = 15
r_0 = 0
z_0 = 0
weight_density = 0.2254
# buoyancy = 2
ds = 0.0001
R_id = 8314.462;        # gas constant                                   (J/K/mol*1000)
mu_air  = 28.966;             # air molar mass                                 (gram)
xmu_air = R_id / mu_air ;     # mu/R ratio for air    (  P = (rho/mu)RT  )
mu_gas = 4
dT_gas = 0
h = 6000
Hatm = [0,
  500,
  1000,
  1500,
  2000,
  2500,
  3000,
  4000,
  5000,
  6000,
  7000,
  8000,
  9000,
  10000,
  11000,
  12000,
  14000,
  16000,
  18000,
  20000,
  24000,
  28000,
  32000,
  36000 ]

Patm = [101330,
  95464,
  89877,
  84559,
  79499,
  74690,
  70123,
  61661,
  54052,
  47217,
  41106,
  35653,
  30801,
  26500,
  22700,
  19399,
  14170,
  10353,
  7565,
  5529,
  2971,
  1616,
  889,
  499]
Tatm =[
  288.2,
  284.9,
  281.7,
  278.4,
  275.2,
  271.9,
  268.7,
  262.2,
  255.7,
  249.2,
  242.7,
  236.2,
  292.7,
  223.3,
  216.8,
  216.7,
  216.7,
  216.7,
  216.7,
  216.7,
  220.6,
  224.5,
  228.5,
  239.3]
Beta = [0.000119267,
  0.000120614,
  0.000121985,
  0.00012341,
  0.000124796,
  0.000126191,
  0.000128599,
  0.000131705,
  0.000135193,
  0.0001386,
  0.000142321,
  0.000146286,
  0.000150402,
  0.00015478,
  0.000157143,
  0.000157047,
  0.000156925,
  0.000156872,
  0.000156763,
  0.000155277,
  0.000152236,
  0.000149403,
  0.000144373,
  0]


def densities(h_atm):
    for n  in range(0,24):
      if h_atm > Hatm[n]:
          i = n
      T_atm = Tatm[i] + (h_atm - Hatm[i]) * (Tatm[i + 1] - Tatm[i]) / (Hatm[i + 1] - Hatm[i])
      P_atm = Patm[i] * exp(-Beta[i] * (h_atm - Hatm[i]))
      rho_atm = P_atm / xmu_air / T_atm

      xmu_gas = R_id / mu_gas
      T_gas = T_atm + dT_gas

      ro_gas = P_atm/xmu_gas/T_gas

    return [rho_atm, ro_gas]

def buoyancy(h_atm):
    ro_atm, ro_gas = densities(h_atm)[0], densities(h_atm)[1]
    return g*(ro_atm - ro_gas)

def theta_deriv(radius, angle_theta, film_T, height_z):
    # global weight_density, h, p_0
    w = weight_density*sin(radians(angle_theta))
    x = w+buoyancy(h)*height_z+p_0
    return -2*pi*radius*x/film_T

def T_deriv(radius, angle_theta, film_T, height_z):
    global weight_density
    return 2*pi*radius*weight_density * cos(radians(angle_theta))

def z_deriv(radius, angle_theta, film_T, height_z):
    return cos(radians(angle_theta))

def r_deriv(radius, angle_theta, film_T, height_z):
    return sin(radians(angle_theta))

def GetSolution():
    global r,theta,T,z, ds, length
    k_theta = [0,0,0,0]
    k_T = [0,0,0,0]
    k_r = [0,0,0,0]
    k_z= [0,0,0,0]
    for i in range(int(length/ds)):
        k_theta[0]=theta_deriv(r[-1], theta[-1], T[-1], z[-1])
        k_T[0]=T_deriv(r[-1], theta[-1], T[-1], z[-1])
        k_r[0]=r_deriv(r[-1], theta[-1], T[-1], z[-1])
        k_z[0]=z_deriv(r[-1], theta[-1], T[-1], z[-1])

        k_theta[1]=theta_deriv(r[-1]+ds*(k_theta[0]/2), theta[-1]+ds*(k_T[0]/2), T[-1]+ds*(k_r[0]/2), z[-1]+ds*(k_z[0]/2))
        k_T[1]=T_deriv(r[-1]+ds*(k_theta[0]/2), theta[-1]+ds*(k_T[0]/2), T[-1]+ds*(k_r[0]/2), z[-1]+ds*(k_z[0]/2))
        k_r[1]=r_deriv(r[-1]+ds*(k_theta[0]/2), theta[-1]+ds*(k_T[0]/2), T[-1]+ds*(k_r[0]/2), z[-1]+ds*(k_z[0]/2))
        k_z[1]=z_deriv(r[-1]+ds*(k_theta[0]/2), theta[-1]+ds*(k_T[0]/2), T[-1]+ds*(k_r[0]/2), z[-1]+ds*(k_z[0]/2))

        k_theta[2]=theta_deriv(r[-1]+ds*(k_theta[1]/2), theta[-1]+ds*(k_T[1]/2), T[-1]+ds*(k_r[1]/2), z[-1]+ds*(k_z[1]/2))
        k_T[2]=T_deriv(r[-1]+ds*(k_theta[1]/2), theta[-1]+ds*(k_T[1]/2), T[-1]+ds*(k_r[1]/2), z[-1]+ds*(k_z[1]/2))
        k_r[2]=r_deriv(r[-1]+ds*(k_theta[1]/2), theta[-1]+ds*(k_T[1]/2), T[-1]+ds*(k_r[1]/2), z[-1]+ds*(k_z[1]/2))
        k_z[2]=z_deriv(r[-1]+ds*(k_theta[1]/2), theta[-1]+ds*(k_T[1]/2), T[-1]+ds*(k_r[1]/2), z[-1]+ds*(k_z[1]/2))

        k_theta[3]=theta_deriv(r[-1]+ds*k_theta[2], theta[-1]+ds*k_T[2], T[-1]+ds*k_r[2], z[-1]+ds*k_z[2])
        k_T[3]=T_deriv(r[-1]+ds*k_theta[2], theta[-1]+ds*k_T[2], T[-1]+ds*k_r[2], z[-1]+ds*k_z[2])
        k_r[3]=r_deriv(r[-1]+ds*k_theta[2], theta[-1]+ds*k_T[2], T[-1]+ds*k_r[2], z[-1]+ds*k_z[2])
        k_z[3]=z_deriv(r[-1]+ds*k_theta[2], theta[-1]+ds*k_T[2], T[-1]+ds*k_r[2], z[-1]+ds*k_z[2])


        theta.append(theta[-1]+(ds/6)*(k_theta[0]+2*k_theta[1]+2*k_theta[2]+k_theta[3]))
        T.append(T[-1]+(ds/6)*(k_T[0]+2*k_T[1]+2*k_T[2]+k_T[3]))
        r.append(r[-1]+(ds/6)*(k_r[0]+2*k_r[1]+2*k_r[2]+k_r[3]))
        z.append(z[-1]+(ds/6)*(k_z[0]+2*k_z[1]+2*k_z[2]+k_z[3]))

if __name__=="__main__":

    for theta_0 in range(650, 670, 1):
        theta_0 = theta_0/10
        T_0 = (L_0 + pi*(r_0**2)*p_0)/cos(radians(theta_0))
        r = [r_0]
        theta = [theta_0]
        T = [T_0]
        z = [z_0]

        GetSolution()
        print("theta_0: ", theta_0, "  theta: ", theta[-1], "  r: ", r[-1])
            #df = pd.DataFrame(sol)
            #df.plot(x='z', y='r', kind = 'scatter')
            #plt.gca().set_aspect('equal', adjustable='box')
            #plt.show()
 
