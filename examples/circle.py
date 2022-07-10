import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import Dnum
from modules.functions import *
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

def gamma(t):
    return (cos(t),sin(t))

steps = 100

time = [i/(steps-1) for i in range(steps)]
time = [2 * math.pi * t for t in time]
time = [Dnum(t, 1) for t in time]

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
    plt.clf()
    plt.plot(X,Y, color="black")
    plt.scatter(X[i], Y[i], color="black")
    plt.arrow(X[i] , Y[i], dX[i], dY[i], color="black", width=0.02)
    plt.ylim(-2, 2)
    plt.xlim(-2, 2)
    plt.title(f"Time = {np.round(time[i].re, decimals=2)} sec")
    plt.xlabel("X")
    plt.ylabel("Y")


fig = plt.figure()
curve_ani = animation.FuncAnimation(fig, animate_function, interval=10, frames=steps)
plt.show()
