from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

l = 16
payload_weight = 24
ds = 0.01
g = 9.8
b = 1
w = 0.22

def Solve(theta0, A):
    T0 = payload_weight/np.cos(theta0)
    z0 = 0
    r0 = 0
    def func(t, y):
        theta, T, z, r = y
        twopir = 2*np.pi*r
        cos = np.cos(theta)
        sin = np.sin(theta)
        p = b*(z-A)
        return [
            -twopir * (w * sin + p) / T,
            twopir * w * cos,
            cos,
            sin
        ]
    sol = solve_ivp(func, t_span = [0, l], y0=[theta0, T0, z0, r0], t_eval=np.arange(0, l, ds))
    return [sol.y[2], sol.y[3]]

[z, r] = Solve(np.pi/2, 0)
plt.plot(z, r)
plt.gca().set_aspect('equal', adjustable = 'box')
plt.show()
