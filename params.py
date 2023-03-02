from scipy.special import hyp2f1
import math
import argparse
import os 


# parser = argparse.ArgumentParser()
# parser.add_argument("--number_of_cores", help="how many cores to use for multiproccessing", type=int)
# parser.add_argument("--height", help="height of the balloon", type=int)
# parser.add_argument('--input_cone_pumpkin', type=argparse.FileType('r'), help='input file path for cone-pumpkin conjugation algorithm')
# parser.add_argument('--output_cone_pumpkin', type=argparse.FileType('w'), help='output file path for cone-pumpkin conjugation algorithm')
# parser.add_argument('--input', type=argparse.FileType('r'), help='input file path for main algorithm')
# parser.add_argument('--output', type=argparse.FileType('w'), help='output file path for main algorithm')
# args = parser.parse_args()

number_of_cores = 15 #args.number_of_cores
height = 17000 #args.height
# input_cone_pumpkin = args.input_cone_pumpkin
# output_cone_pumpkin = args.output_cone_pumpkin
# input = args.input
# output = args.output

output_filename = os.path.join('results', 'result_output_for_altitude_%s.txt' % height)
z2r_csv_filename = os.path.join('results', 'z2r_%s.csv' % height)
plot_filename = os.path.join('plots', 'height_%s.svg' % height)

ds = 0.002 # system integration step
Cx = 0.47 # balloon drag coefficient (determined by the special algorithm)

wp = 0.229158 # pumpkin shape balloon film weight density 
rp_max = 6.122831782671 # radius of fully the inflated balloon pumpkin (m)
l = 2 * hyp2f1(1/4, 1/2, 5/4, 1) * rp_max # maximum core length (m)

g = 9.8065 # free fall acceleration at release location (m/s^2)
m_payload = 11.922531663 # payload mass (kg)
L0 = m_payload * g # payload weight (N)
m_b = 8.646213297 # balloon mass (kg)
m_gas = 3.491565771 # mass of the lighter-than-air (LTA) gas (kg)

R = 8314.462 # gas constant (J/K/mol*1000)
mu_air = 28.966 # air molar mass (g)
xmu_air = R / mu_air # R/mu_air ratio for air (P = (rho/mu)RT)
mu_gas = 4 # LTA gas molar mass (g)
dT_gas = 0 # additional temperature of the LTA gas due to greenhouse effect (K)

k_Sp = 0.739668778 # coefficient for meridian length calculation
k_S = k_Sp * math.sqrt(math.pi) 
k_Vp = 1.21852421611857 # coefficient for design pumpkin shape volume calculation
k_V = 2.74581225 
s0_b = k_S * rp_max # meridian length of the balloon from pole to equator (m)
V_max = k_Vp * s0_b ** 3 # design volume of the balloon fully inflated to its pumpkin shape (m^3)


# Standard Atmosphere
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
Tatm = [
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
