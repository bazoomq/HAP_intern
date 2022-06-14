from constants import *
from math import exp
def densities(h):
    for n  in range(0,24):
      if h > Hatm[n]:
          i = n
      T_atm = Tatm[i] + (h - Hatm[i]) * (Tatm[i + 1] - Tatm[i]) / (Hatm[i + 1] - Hatm[i])
      P_atm = Patm[i] * exp(-Beta[i] * (h - Hatm[i]))
      rho_atm = P_atm / xmu_air / T_atm

      xmu_gas = R_id / mu_gas
      T_gas = T_atm + dT_gas

      ro_gas = P_atm/xmu_gas/T_gas

    return [rho_atm, ro_gas]

def b(h):
    ro_atm, ro_gas = densities(h)[0], densities(h)[1]
    return g*(ro_atm - ro_gas)
