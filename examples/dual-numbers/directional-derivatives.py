import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import dnum as dn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import modules.PYDrawing3D
from mpl_toolkits.mplot3d import Axes3D

def sigma(u, v):
    return (dn.cos(u)*dn.cos(v), dn.cos(u)*dn.sin(v), dn.sin(u))

U, V = np.linspace(-np.pi/2, np.pi/2, num=100), np.linspace(-np.pi, np.pi, num=100)
U, V = np.meshgrid(U, V)
U, V = np.array([dn(x) for x in U]), np.array([dn(x) for x in V])
U, V = dn.split(U), dn.split(V)

X, Y, Z = sigma(U,V)

dX, dY, dZ = X.im, Y.im, Z.im
X, Y, Z = X.re, Y.re, Z.re

def plot(u, v, du, dv):
    u, v = dn(u, du), dn(v, dv)
    x, y, z = sigma(u,v)

    dx, dy, dz = x.im, y.im, z.im
    x, y, z = x.re, y.re, z.re

    fig = plt.figure()
    ax = Axes3D(fig, computed_zorder=False, auto_add_to_figure=False)
    fig.add_axes(ax)

    ax.plot_surface(X, Y, Z, cmap=cm.plasma, linewidth=1, zorder=0)
    ax.scatter(x, y, z, color="black", zorder=10)
    ax.arrow3D(x , y, z, dx, dy, dz, mutation_scale=10, color="blue", arrowstyle="-|>", zorder=10)
    ax.set_xlim3d(-1,1)
    ax.set_ylim3d(-1,1)
    ax.set_zlim3d(-1,1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

point = np.array([np.pi/4, np.pi/4])
J_point = np.array([[1,0], [0,1]])
u, v = point
du, dv = J_point

print('simga(u + I) = sigma(u) + Jacobian(sigma) * I i_0')
print('for example if sigma parametrizes the sphere...')
print(f'Jacobian(sigma) = \n{dn.split(sigma(dn(u,du), dn(v, dv))).im}')

point = np.array([np.pi/4, np.pi/4])
J_point = np.array([1,0])
u, v = point
du, dv = J_point

print('simga(u + v) = sigma(u) + Jacobian(sigma) * v i_0')
print('for example if sigma parametrizes the sphere...')
print(f'sigma_u = \n{dn.split(sigma(dn(u,du), dn(v, dv))).im}')

dn.backward(True)

point = np.array([np.pi/4, np.pi/4])
J_point = np.array([[1,0], [0,1]])
u, v = point
du, dv = J_point

print('simga(u + v) = sigma(u) + Jacobian(sigma) * v i_0')
print('for example if sigma parametrizes the sphere...')
print(f'Jacobian(simga)=')
s = sigma(dn(u,du), dn(v, dv))
for i, _ in enumerate(s):
    print(f'{s[i].d(1)}')
print(f'Jacobian(simga) first row =')
print(dn.split(s).d([[1,0,0]]))

