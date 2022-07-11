import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import Dnum
from modules.functions import *
import modules.PYDrawing3D
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def gamma(t):
    return (sin(math.pi/5 * t),sin(math.pi/3 * t), 5*t)

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

X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)
dX = np.array(dX)
dY = np.array(dY)
dZ = np.array(dZ)



def animate_function(i):
    x, y, z = X[i], Y[i], Z[i]
    dx, dy, dz = dX[i], dY[i], dZ[i]
    t = time[i].re

    ax.clear()
    ax.plot3D(X[:i+1], Y[:i+1], Z[:i+1], color="black")
    ax.plot3D(X, Y, Z, color="black", linestyle="--")
    ax.scatter(x, y, z, color="black")
    ax.arrow3D(x , y, z, dx, dy, dz, mutation_scale=10, color="blue", arrowstyle="-|>")
    ax.set_xlim3d([-1, 1])
    ax.set_ylim3d([-1, 1])
    ax.set_zlim3d([0, 100])
    ax.set_title(f"Time = {np.round(t, decimals=2)} sec")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

fig = plt.figure()
ax = plt.axes(projection='3d')

curve_ani = animation.FuncAnimation(fig, animate_function, interval=100, frames=steps)

plt.show()

# Saving the Animation
folder_path = os.path.abspath(os.path.join('.','animations'))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

file_path = os.path.join(folder_path, '3d-curve.gif')
writergif = animation.PillowWriter(fps=steps/6)
curve_ani.save(file_path, writer=writergif)

