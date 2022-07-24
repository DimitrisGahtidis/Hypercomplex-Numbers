import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import dnum as dn
import modules.PYDrawing3D
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def gamma(t):
    return (dn.sin(np.pi/5 * t),dn.sin(np.pi/3 * t), 5*t/100)

def d_gamma(t):
    return (np.pi/5 * dn.cos(np.pi/5 * t),np.pi/3 * dn.cos(np.pi/3 * t), dn(5)/100)

def norm(point):
    x,y,z = point
    return np.sqrt(x**2 + y**2 + z**2)

steps = 100

time = [i/(steps-1) for i in range(steps)]
time = [20 * t for t in time]
time = [dn(t, 1) for t in time]

curve = [gamma(t) for t in time]
tangent_space = [d_gamma(t) for t in time]


position = np.array([(x.re, y.re, z.re) for x, y, z in curve])
velocity = np.array([(x.im, y.im, z.im) for x, y, z in curve])
acceleration = np.array([(dx.im, dy.im, dz.im) for dx, dy, dz in tangent_space])

coordinates = ([point[0] for point in position], [point[1] for point in position], [point[2] for point in position])

tangent = []
binormal = []
normal = []

for v in velocity:
    if norm(v) != 0:
        tangent.append(np.array(v)/norm(v))
    else:
        tangent.append(np.array(v))

for t, a in zip(tangent, acceleration):
    b = np.cross(t,a)
    if norm(b) != 0:
        binormal.append(b/norm(b))
    else:
        binormal.append(b)

for b, t in zip(binormal, tangent):
    n = np.cross(b,t)
    if norm(n) != 0:
        normal.append(n/norm(n))
    else:
        normal.append(n)

def animate_function(i):
    X, Y, Z = coordinates
    point = position[i]
    tangent_vector = tangent[i]
    normal_vector = normal[i]
    binormal_vector = binormal[i]
    t = time[i].re

    ax.clear()
    ax.plot3D(X[:i+1], Y[:i+1], Z[:i+1], color="black")
    ax.plot3D(*coordinates, color="black", linestyle="--", label="Trajectory")
    ax.scatter(*point, color="black", label = "Particle")
    ax.arrow3D(*point, *tangent_vector, mutation_scale=10, color="blue", arrowstyle="-|>", label="Tangent vector")
    ax.arrow3D(*point, *normal_vector, mutation_scale=10, color="red", arrowstyle="-|>", label="Normal vector")
    ax.arrow3D(*point, *binormal_vector, mutation_scale=10, color="green", arrowstyle="-|>", label="Binormal vector")
    ax.set_xlim3d([-1, 1])
    ax.set_ylim3d([-1, 1])
    ax.set_zlim3d([-0.75, 1.25])
    ax.set_title(f"Time = {np.round(t, decimals=2)} sec")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend(loc="upper left", bbox_to_anchor=(1.05,1))
    plt.tight_layout()

fig = plt.figure()
ax = plt.axes(projection='3d')

curve_ani = animation.FuncAnimation(fig, animate_function, interval=100, frames=steps)

plt.show()

# Saving the Animation
folder_path = os.path.abspath(os.path.join('.','animations'))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

file_path = os.path.join(folder_path, 'frenet-frame-3d-curve.gif')
writergif = animation.PillowWriter(fps=steps/6)
curve_ani.save(file_path, writer=writergif)


