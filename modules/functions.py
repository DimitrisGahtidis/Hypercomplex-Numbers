
from modules.numbers import Dnum
import math
import numpy as np

def sin(z):
    return Dnum(np.sin(z.re), np.cos(z.re) * z.im)
def cos(z):
    return Dnum(np.cos(z.re), -np.sin(z.re) * z.im)
def tan(z):
    return Dnum(np.tan(z.re), 1/(np.cos(z.re)**2) * z.im)
def exp(z):
    return Dnum(np.exp(z.re), np.exp(z.re) * z.im)
def log(z):
    return Dnum(np.log(z.re), 1/(z.re) * z.im)
def pow(z, n):
    return Dnum(np.pow(z.re,n), n * np.pow(z.re, n-1) * z.im)
def sqrt(z):
    return Dnum(np.sqrt(z.re), (0.5) * np.sqrt(z.re) * z.im)
def acos(z):
    return Dnum(np.acos(z.re), (-1)/np.sqrt(1-z.re**2) * z.im)
def asin(z):
    return Dnum(np.asin(z.re), 1/np.sqrt(1-z.re**2) * z.im)
def atan(z):
    return Dnum(np.atan(z.re), 1/(1+z.re**2) * z.im)
def sinh(z):
    return Dnum(np.sinh(z.re), np.cosh(z.re) * z.im)
def cosh(z):
    return Dnum(np.cosh(z.re), np.sinh(z.re) * z.im)
def tanh(z):
    return Dnum(np.tanh(z.re), (1 - np.tanh(z.re)**2) * z.im)
def asinh(z):
    return Dnum(np.asinh(z.re), 1/(1-z.re**2) * z.im)
def acosh(z):
    return Dnum(np.acosh(z.re), 1/np.sqrt(z.re**2-1) * z.im)
def erf(z):
    return Dnum(np.erf(z.re), (2/np.sqrt(np.pi))*np.exp(-(z.re**2)) * z.im)