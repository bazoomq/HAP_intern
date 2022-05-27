from asyncio import constants
from scipy.special import hyp2f1
import numpy as np
from scipy.interpolate import interp1d

#sol = solve_ivp(f, t_span=[0, s1], y0=[theta0, T0, z0, r0], t_eval=np.arange(0, s1, ds))
rp_max = 6.122831
l = 16.0544
ds = 0.0001
g = 9.8
payload_weight = 24*g
r_tollerance = -0.1
wp = 0.229158

R_id = 8314.462;        # gas constant                                   (J/K/mol*1000)
mu_air  = 28.966;             # air molar mass                                 (gram)
xmu_air = R_id / mu_air ;     # mu/R ratio for air    (  P = (rho/mu)RT  )
mu_gas = 4
dT_gas = 0
Hatm = [0, 500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000, 7000,
  8000, 9000, 10000, 11000, 12000, 14000, 16000, 18000, 20000, 24000, 28000, 32000, 36000 ]

Patm = [101330, 95464, 89877, 84559, 79499, 74690, 70123, 61661, 54052, 47217, 41106,
  35653, 30801, 26500, 22700, 19399, 14170, 10353, 7565, 5529, 2971, 1616, 889, 499]

Tatm =[ 288.2, 284.9, 281.7, 278.4, 275.2, 271.9, 268.7, 262.2, 255.7, 249.2, 242.7,
  236.2, 292.7, 223.3, 216.8, 216.7, 216.7, 216.7, 216.7, 216.7, 220.6, 224.5, 228.5, 239.3]

Beta = [0.000119267, 0.000120614, 0.000121985, 0.00012341, 0.000124796, 0.000126191,
  0.000128599, 0.000131705, 0.000135193, 0.0001386, 0.000142321, 0.000146286, 0.000150402,
  0.00015478, 0.000157143, 0.000157047, 0.000156925, 0.000156872, 0.000156763, 0.000155277,
  0.000152236, 0.000149403, 0.000144373, 0]
  
def f_interp1d():

    def get_sr(rp_max):
        r_list = np.linspace(0, rp_max, int(rp_max/0.001))
        s_list = []

        for r in r_list:
            # equation for calculating S0
            s = r * hyp2f1(1 / 4, 1 / 2, 5 / 4, (r / rp_max) ** 4)
            s_list.append(s)
        return r_list, s_list
    
    rs, s_half = get_sr(rp_max)
    f = interp1d(s_half, rs, kind='cubic')
    return f


def s1():
    s1 = 2 * hyp2f1(1/4, 1/2, 5/4, 1) * rp_max
    return s1
