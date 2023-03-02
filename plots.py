from matplotlib import pyplot as plt
import numpy as np 


def plotting(theta0, a, loss):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    X, Y = np.meshgrid(theta0, a)
    Z = np.array(loss).reshape(10, 20)
    ax.plot_wireframe(X, Y, Z, color='black')
    ax.set_xlabel('theta0')
    ax.set_ylabel('a')
    plt.savefig('loss.png')
    return