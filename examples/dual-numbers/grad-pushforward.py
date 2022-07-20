import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import Dnum as dn
from modules.functions import *
import numpy as np

def sigma(z):
    u, v = z
    return (cos(u)*cos(v), cos(u)*sin(v), sin(u))



u = np.array([math.pi/4, math.pi/4])
du = np.array([1, 0])
z = dn(u,du)
print('simga(u + du) = sigma(u) + Jacobian(sigma) * du i_0')
print('for example if sigma parametrizes the sphere...')
print(f'sigma({z}) = {dn.split(sigma(z))}')

u = np.array([math.pi/4, math.pi/4])
du = np.array([[1,0], [0,1]])
z = dn(u,du)
print()
print('simga(u + I) = sigma(u) + Jacobian(sigma) * I i_0')
print('for example if sigma parametrizes the sphere...')
print(f'Jacobian(sigma) = \n{dn.split(sigma(z))}')