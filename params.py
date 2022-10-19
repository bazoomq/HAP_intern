from scipy.special import hyp2f1
import argparse
import math


parser = argparse.ArgumentParser()
parser.add_argument("number_of_cores", help="how many cores to use for multiproccessing", type=int)
parser.add_argument("height", help="height of balloon", type=int)
args = parser.parse_args()
number_of_cores = args.number_of_cores
h = args.height

g = 9.8065
L0 = 24.06031 * g
wp = 0.229158
rp_max = 6.122831
l = 2 * hyp2f1(1/4, 1/2, 5/4, 1) * rp_max
ds = 0.002
R = 8314.462
mu_air = 28.966
xmu_air = R / mu_air
mu_gas = 4
dT_gas = 0
Cx = 0.47
S0 = 0.739668778 * math.sqrt(math.pi) * rp_max
V_max = 1.21852421611856 * S0 ** 3 

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