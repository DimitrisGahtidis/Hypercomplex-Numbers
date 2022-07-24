import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import dnum as dn
import modules.PYDrawing3D
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D


n_side_points = 50

lattice = []
for x in range(n_side_points):
    for y in range(n_side_points):
        lattice.append(dn(x/n_side_points*8-4,y/n_side_points*8-4))

steps = 200
d_theta = 1/steps

transformation = []
X = []
Y = []

for i in range(steps):
    transformation.append([point * dn.exp(dn(0,d_theta*i)) for point in lattice])

for lattice in transformation:
    X.append([point.re for point in lattice])
    Y.append([point.im for point in lattice])


def animate_function(i):
    x = X[i]
    y = Y[i]

    ax.clear()
    ax.vlines(0, -2, 2, color="blue", label=f'$|x + y \\varepsilon| = 0$', zorder=-1)
    ax.vlines([-1,1], -2, 2, color="red", label=f'$|x + y \\varepsilon| = 1$', zorder=-1)
    ax.scatter(x, y, color="black", zorder=1)
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_title(f'$e^{{{round(d_theta*i,2)}\\varepsilon}} (x + y \\varepsilon)$')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend(loc="upper left", bbox_to_anchor=(1.05,1))
    plt.tight_layout()

fig = plt.figure()
ax = plt.axes()

curve_ani = animation.FuncAnimation(fig, animate_function, interval=100, frames=steps)

plt.show()

# Saving the Animation
folder_path = os.path.abspath(os.path.join('.','animations'))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

file_path = os.path.join(folder_path, 'dual-number-rotor.gif')
writergif = animation.PillowWriter(fps=steps/10)
curve_ani.save(file_path, writer=writergif)