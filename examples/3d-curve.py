import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import Dnum
from modules.functions import *
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def gamma(t):
    return (sin(math.pi/5 * t),sin(math.pi/3 * t), t)

steps = 100

time = [i/(steps-1) for i in range(steps)]
time = [20 * t for t in time]
time = [Dnum(t, 1) for t in time]

curve = [gamma(t) for t in time]

X = []
Y = []
Z = []
dX = []
dY = []
dZ = []

for point in curve:
    x, y, z = point
    x, dx = x.re, x.im
    y, dy = y.re, y.im
    z, dz = z.re, z.im
    X.append(x)
    Y.append(y)
    Z.append(z)
    dX.append(dx)
    dY.append(dy)
    dZ.append(dz)


def animate_function(i):
    ax.clear()
    ax.plot3D(X, Y, Z, color="black")
    ax.scatter(X[i], Y[i], Z[i], color="blue")
    ax.quiver(X[i] , Y[i], Z[i], dX[i], dY[i], dZ[i], color="blue", normalize=True)
    ax.set_ylim(-2, 2)
    ax.set_xlim(-2, 2)
    ax.set_title(f"Time = {np.round(time[i].re, decimals=2)} sec")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")


fig = plt.figure()
ax = plt.axes(projection='3d')
curve_ani = animation.FuncAnimation(fig, animate_function, interval=10, frames=steps)
plt.show()