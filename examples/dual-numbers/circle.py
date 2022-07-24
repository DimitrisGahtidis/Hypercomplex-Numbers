import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import dnum as dn
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

def gamma(t):
    return (dn.cos(t),dn.sin(t))

steps = 100

time = [i/(steps-1) for i in range(steps)]
time = [2 * np.pi * t for t in time]
time = [dn(t, 1) for t in time]

curve = [gamma(t) for t in time]

X = []
Y = []
dX = []
dY = []

for point in curve:
    x, y = point
    x, dx = x.re, x.im
    y, dy = y.re, y.im
    X.append(x)
    Y.append(y)
    dX.append(dx)
    dY.append(dy)

X = np.array(X)
Y = np.array(Y)
dX = np.array(dX)
dY = np.array(dY)

def animate_function(i):
    ax.clear()
    ax.plot(X[:i+1],Y[:i+1], color="black")
    ax.plot(X,Y, color="black", linestyle="--")
    ax.scatter(X[i], Y[i], color="black")
    ax.arrow(X[i] , Y[i], dX[i], dY[i], color="blue", width=0.02)
    ax.set_ylim(-2, 2)
    ax.set_xlim(-2, 2)
    ax.set_title(f"Time = {np.round(time[i].re, decimals=2)} sec")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")


fig = plt.figure()
ax = plt.axes()
curve_ani = animation.FuncAnimation(fig, animate_function, interval=100, frames=steps)
plt.show()

# Saving the Animation
folder_path = os.path.abspath(os.path.join('.','animations'))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

file_path = os.path.join(folder_path, 'circle.gif')
writergif = animation.PillowWriter(fps=steps/6)
curve_ani.save(file_path, writer=writergif)
