from math import exp
from params import *

def density(z):
  for n in range(0, 24):
    if z > Hatm[n]:
      i = n

    T_atm = Tatm[i] + (z - Hatm[i]) * (Tatm[i + 1] - Tatm[i]) / (Hatm[i + 1] - Hatm[i])
    P_atm = Patm[i] * exp(-Beta[i] * (z - Hatm[i]))
    ro_atm = P_atm / xmu_air / T_atm
    xmu_gas = R / mu_gas

    T_gas = T_atm + dT_gas
    ro_gas = P_atm / xmu_gas / T_gas

  return [ro_atm, ro_gas]
