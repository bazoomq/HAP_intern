from math import cos, sin, radians, pi
import pandas as pd
import matplotlib.pyplot as plt

theta_0=80
L_0 = float(input("Enter the payload:"))
p_0 = float(input("Enter the pressure at the base of balloon:"))
length = float(input("Enter the length of film:"))
r_0 = 0
T_0 = (L_0 + pi*(r_0**2)*p_0)/cos(radians(theta_0))
z_0 = 0

weight_density = 1
buoyancy = 2
ds = 0.01


sol = {
    "r":[r_0],
    "theta" : [theta_0],
    "T":[T_0],
    "z":[z_0]
    }

def theta_deriv(radius, angle_theta, film_T, height_z):
    global weight_density, buoyancy, p_0
    return -2*pi*radius*(weight_density*sin(radians(angle_theta))+buoyancy*height_z+p_0)/film_T

def T_deriv(radius, angle_theta, film_T, height_z):
    global weight_density
    return 2*pi*radius*weight_density*cos(radians(angle_theta))

def z_deriv(radius, angle_theta, film_T, height_z):
    return cos(radians(angle_theta))

def r_deriv(radius, angle_theta, film_T, height_z):
    return sin(radians(angle_theta))

def GetSolution():
    global sol, ds, length
    coefs = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(int(length/ds)):
        coefs[0][0]=theta_deriv(sol["r"][-1], sol["theta"][-1], sol["T"][-1], sol["z"][-1])
        coefs[1][0]=T_deriv(sol["r"][-1], sol["theta"][-1], sol["T"][-1], sol["z"][-1])
        coefs[2][0]=r_deriv(sol["r"][-1], sol["theta"][-1], sol["T"][-1], sol["z"][-1])
        coefs[3][0]=z_deriv(sol["r"][-1], sol["theta"][-1], sol["T"][-1], sol["z"][-1])
        coefs[0][1]=theta_deriv(sol["r"][-1]+(coefs[0][0]/2), sol["theta"][-1]+(coefs[1][0]/2), sol["T"][-1]+(coefs[2][0]/2), sol["z"][-1]+(coefs[3][0]/2))
        coefs[1][1]=T_deriv(sol["r"][-1]+(coefs[0][0]/2), sol["theta"][-1]+(coefs[1][0]/2), sol["T"][-1]+(coefs[2][0]/2), sol["z"][-1]+(coefs[3][0]/2))
        coefs[2][1]=r_deriv(sol["r"][-1]+(coefs[0][0]/2), sol["theta"][-1]+(coefs[1][0]/2), sol["T"][-1]+(coefs[2][0]/2), sol["z"][-1]+(coefs[3][0]/2))
        coefs[3][1]=z_deriv(sol["r"][-1]+(coefs[0][0]/2), sol["theta"][-1]+(coefs[1][0]/2), sol["T"][-1]+(coefs[2][0]/2), sol["z"][-1]+(coefs[3][0]/2))
        coefs[0][2]=theta_deriv(sol["r"][-1]+(coefs[0][1]/2), sol["theta"][-1]+(coefs[1][1]/2), sol["T"][-1]+(coefs[2][1]/2), sol["z"][-1]+(coefs[3][1]/2))
        coefs[1][2]=T_deriv(sol["r"][-1]+(coefs[0][1]/2), sol["theta"][-1]+(coefs[1][1]/2), sol["T"][-1]+(coefs[2][1]/2), sol["z"][-1]+(coefs[3][1]/2))
        coefs[2][2]=r_deriv(sol["r"][-1]+(coefs[0][1]/2), sol["theta"][-1]+(coefs[1][1]/2), sol["T"][-1]+(coefs[2][1]/2), sol["z"][-1]+(coefs[3][1]/2))
        coefs[3][2]=z_deriv(sol["r"][-1]+(coefs[0][1]/2), sol["theta"][-1]+(coefs[1][1]/2), sol["T"][-1]+(coefs[2][1]/2), sol["z"][-1]+(coefs[3][1]/2))
        coefs[0][3]=theta_deriv(sol["r"][-1], sol["theta"][-1], sol["T"][-1], sol["z"][-1])
        coefs[1][3]=T_deriv(sol["r"][-1], sol["theta"][-1], sol["T"][-1], sol["z"][-1])
        coefs[2][3]=r_deriv(sol["r"][-1], sol["theta"][-1], sol["T"][-1], sol["z"][-1])
        coefs[3][3]=z_deriv(sol["r"][-1], sol["theta"][-1], sol["T"][-1], sol["z"][-1])
        sol["theta"].append(sol["theta"][-1]+(ds/6)*(coefs[0][0]+2*coefs[0][1]+2*coefs[0][2]+coefs[0][3]))
        sol["T"].append(sol["T"][-1]+(ds/6)*(coefs[1][0]+2*coefs[1][1]+2*coefs[1][2]+coefs[1][3]))
        sol["r"].append(sol["r"][-1]+(ds/6)*(coefs[2][0]+2*coefs[2][1]+2*coefs[2][2]+coefs[2][3]))
        sol["z"].append(sol["z"][-1]+(ds/6)*(coefs[3][0]+2*coefs[3][1]+2*coefs[3][2]+coefs[3][3]))
GetSolution()
df = pd.DataFrame(sol)
print(df)
df.plot(x='z', y='r', kind = 'scatter')
plt.show()