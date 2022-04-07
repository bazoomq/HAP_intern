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

den_gas = 2
buoyancy = 2
ds = 0.01
w_p = 0.2254
count = 0


sol = {
    "s":[[0]],
    "r":[[r_0]],
    "theta" : [[theta_0]],
    "T":[[T_0]],
    "z":[[z_0]]
    }

wden_list=[]

#TODO /////////////////////////////////////////////
def den_atmosphere(z):
    pass

#TODO ////////////////////////////////////////////
def buoyancy(z):
    global den_gas
    return 9.8*(den_atmosphere(z)-den_gas)
#TODO ///////////////////////////////////////////
def pump_rad(s):
    return 2

def weight_density(s):
    global wden_list
    global w_p
    global ds, count
    if len(wden_list) == 0:
        return w_p
    else:
        if (s/ds).is_integer()==True:
            return (pump_rad(s)*w_p)/sol["r"][count-1][int(s/ds)]
        else:
            return (2*pump_rad(s)*w_p)/(sol["r"][count-1][int(s/ds)]+sol["r"][count-1][int(s/ds)+1])

def theta_deriv(s,radius, angle_theta, film_T, height_z):
    global buoyancy, p_0
    return -2*pi*radius*(weight_density(s)*sin(radians(angle_theta))+buoyancy*height_z+p_0)/film_T

def T_deriv(s,radius, angle_theta, film_T, height_z):
    return 2*pi*radius*weight_density(s)*cos(radians(angle_theta))

def z_deriv(s,radius, angle_theta, film_T, height_z):
    return cos(radians(angle_theta))

def r_deriv(s,radius, angle_theta, film_T, height_z):
    return sin(radians(angle_theta))

def GetSolution():
    global sol, ds, length, wden_list, w_p, count
    coefs = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    if count > 0:
        wden_list.append([])
        for s in range(int(length/ds)):
            wden_list[-1].append(weight_density(s))
    for i in range(int(length/ds)):
        coefs[0][0]=theta_deriv(sol["s"][count][-1], sol["r"][count][-1], sol["theta"][count][-1], sol["T"][count][-1], sol["z"][count][-1])
        coefs[1][0]=T_deriv(sol["s"][count][-1], sol["r"][count][-1], sol["theta"][count][-1], sol["T"][count][-1], sol["z"][count][-1])
        coefs[2][0]=r_deriv(sol["s"][count][-1], sol["r"][count][-1], sol["theta"][count][-1], sol["T"][count][-1], sol["z"][count][-1])
        coefs[3][0]=z_deriv(sol["s"][count][-1], sol["r"][count][-1], sol["theta"][count][-1], sol["T"][count][-1], sol["z"][count][-1])
        coefs[0][1]=theta_deriv(sol["s"][count][-1]+ds*(1/2), sol["r"][count][-1]+(coefs[0][0]/2), sol["theta"][count][-1]+(coefs[1][0]/2), sol["T"][count][-1]+(coefs[2][0]/2), sol["z"][count][-1]+(coefs[3][0]/2))
        coefs[1][1]=T_deriv(sol["s"][count][-1]+ds*(1/2), sol["r"][count][-1]+(coefs[0][0]/2), sol["theta"][count][-1]+(coefs[1][0]/2), sol["T"][count][-1]+(coefs[2][0]/2), sol["z"][count][-1]+(coefs[3][0]/2))
        coefs[2][1]=r_deriv(sol["s"][count][-1]+ds*(1/2), sol["r"][count][-1]+(coefs[0][0]/2), sol["theta"][count][-1]+(coefs[1][0]/2), sol["T"][count][-1]+(coefs[2][0]/2), sol["z"][count][-1]+(coefs[3][0]/2))
        coefs[3][1]=z_deriv(sol["s"][count][-1]+ds*(1/2), sol["r"][count][-1]+(coefs[0][0]/2), sol["theta"][count][-1]+(coefs[1][0]/2), sol["T"][count][-1]+(coefs[2][0]/2), sol["z"][count][-1]+(coefs[3][0]/2))
        coefs[0][2]=theta_deriv(sol["s"][count][-1]+ds*(1/2), sol["r"][count][-1]+(coefs[0][1]/2), sol["theta"][count][-1]+(coefs[1][1]/2), sol["T"][count][-1]+(coefs[2][1]/2), sol["z"][count][-1]+(coefs[3][1]/2))
        coefs[1][2]=T_deriv(sol["s"][count][-1]+ds*(1/2), sol["r"][count][-1]+(coefs[0][1]/2), sol["theta"][count][-1]+(coefs[1][1]/2), sol["T"][count][-1]+(coefs[2][1]/2), sol["z"][count][-1]+(coefs[3][1]/2))
        coefs[2][2]=r_deriv(sol["s"][count][-1]+ds*(1/2), sol["r"][count][-1]+(coefs[0][1]/2), sol["theta"][count][-1]+(coefs[1][1]/2), sol["T"][count][-1]+(coefs[2][1]/2), sol["z"][count][-1]+(coefs[3][1]/2))
        coefs[3][2]=z_deriv(sol["s"][count][-1]+ds*(1/2), sol["r"][count][-1]+(coefs[0][1]/2), sol["theta"][count][-1]+(coefs[1][1]/2), sol["T"][count][-1]+(coefs[2][1]/2), sol["z"][count][-1]+(coefs[3][1]/2))
        coefs[0][3]=theta_deriv(sol["s"][count][-1], sol["r"][count][-1], sol["theta"][count][-1], sol["T"][count][-1], sol["z"][count][-1])
        coefs[1][3]=T_deriv(sol["s"][count][-1], sol["r"][count][-1], sol["theta"][count][-1], sol["T"][count][-1], sol["z"][count][-1])
        coefs[2][3]=r_deriv(sol["s"][count][-1], sol["r"][count][-1], sol["theta"][count][-1], sol["T"][count][-1], sol["z"][count][-1])
        coefs[3][3]=z_deriv(sol["s"][count][-1], sol["r"][count][-1], sol["theta"][count][-1], sol["T"][count][-1], sol["z"][count][-1])
        sol["s"][count].append(sol["s"][count][-1]+ds)
        sol["theta"][count].append(sol["theta"][count][-1]+(ds/6)*(coefs[0][0]+2*coefs[0][1]+2*coefs[0][2]+coefs[0][3]))
        sol["T"][count].append(sol["T"][count][-1]+(ds/6)*(coefs[1][0]+2*coefs[1][1]+2*coefs[1][2]+coefs[1][3]))
        sol["r"][count].append(sol["r"][count][-1]+(ds/6)*(coefs[2][0]+2*coefs[2][1]+2*coefs[2][2]+coefs[2][3]))
        sol["z"][count].append(sol["z"][count][-1]+(ds/6)*(coefs[3][0]+2*coefs[3][1]+2*coefs[3][2]+coefs[3][3]))
    if count == 0:
        wden_list.append([])
    count += 1
    sol["s"].append([])
    sol["s"][count].append(sol["s"][count-1][0])
    sol["theta"].append([])
    sol["theta"][count].append(sol["theta"][count-1][0])
    sol["T"].append([])
    sol["T"][count].append(sol["T"][count-1][0])
    sol["r"].append([])
    sol["r"][count].append(sol["r"][count-1][0])
    sol["z"].append([])
    sol["z"][count].append(sol["z"][count-1][0])

for i in range(1):
    GetSolution()
print(len(sol["s"]))
print(len(sol["s"][-2]))
ndic = {"s":sol["s"][-2],
        "r":sol["r"][-2],
        "theta":sol["theta"][-2],
        "T":sol["T"][-2],
        "z":sol["z"][-2]}
df = pd.DataFrame(ndic)
print(df)
print(wden_list)
df.plot(x='z', y='r', kind = 'scatter')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
