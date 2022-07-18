import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import Dnum
from modules.functions import *
import modules.PYDrawing3D
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

def sigma(z):
    u, v = z
    return Dnum.split((cos(u)*cos(v), cos(u)*sin(v), sin(u)))



u = np.array([math.pi/4, math.pi/4])
du = np.array([1, 0])
z = Dnum(u,du)
print('simga(u + du) = sigma(u) + Jacobian(sigma) * du i_0')
print('for example if sigma parametrizes the sphere...')
print(f'sigma({z}) = {sigma(z)}')

u = np.array([math.pi/4, math.pi/4])
du = np.array([[1,0], [0,1]])
z = Dnum(u,du)
print()
print('simga(u + I) = sigma(u) + Jacobian(sigma) * I i_0')
print('for example if sigma parametrizes the sphere...')
print(f'Jacobian(sigma) = \n{sigma(z).im}')