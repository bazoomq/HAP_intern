from math import exp
from params import *


def density(height):
  """
  calculate air and gas densities at the current altitude
  :param height: altitude for which density is calculated
  :return: [rho_atm, rho_gas] - air and gas densities, P_atm - air pressure, T_gas - temperature of the LTA gas
  """
  for n in range(0, 24):
    if height > Hatm[n]:
      i = n

    T_atm = Tatm[i] + (height - Hatm[i]) * (Tatm[i + 1] - Tatm[i]) / (Hatm[i + 1] - Hatm[i]) # air temperature at the current altitude (K)
    P_atm = Patm[i] * exp(-Beta[i] * (height - Hatm[i])) # air pressure at the current altitude (Pa)
    rho_atm = P_atm / xmu_air / T_atm # air density at the current altitude (kg/m^3)
    xmu_gas = R / mu_gas # R / mu ratio for the LTA gas

    T_gas = T_atm + dT_gas # temperature of the LTA gas (K)
    rho_gas = P_atm / xmu_gas / T_gas # gas density at the current altitude (kh/m^3)

  return rho_atm, rho_gas, P_atm, T_gas, T_atm
