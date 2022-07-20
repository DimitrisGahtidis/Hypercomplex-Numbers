
from modules.numbers import Dnum as dn
import math
import numpy as np

def sin(z):
    return dn(np.sin(z.re), np.cos(z.re) * z.im())
def cos(z):
    return dn(np.cos(z.re), -np.sin(z.re) * z.im())
def tan(z):
    return dn(np.tan(z.re), 1/(np.cos(z.re)**2) * z.im())
def exp(z):
    return dn(np.exp(z.re), np.exp(z.re) * z.im())
def log(z):
    return dn(np.log(z.re), 1/(z.re) * z.im())
def pow(z, n):
    return dn(np.pow(z.re,n), n * np.pow(z.re, n-1) * z.im())
def sqrt(z):
    return dn(np.sqrt(z.re), (0.5) * np.sqrt(z.re) * z.im())
def acos(z):
    return dn(np.acos(z.re), (-1)/np.sqrt(1-z.re**2) * z.im())
def asin(z):
    return dn(np.asin(z.re), 1/np.sqrt(1-z.re**2) * z.im())
def atan(z):
    return dn(np.atan(z.re), 1/(1+z.re**2) * z.im())
def sinh(z):
    return dn(np.sinh(z.re), np.cosh(z.re) * z.im())
def cosh(z):
    return dn(np.cosh(z.re), np.sinh(z.re) * z.im())
def tanh(z):
    return dn(np.tanh(z.re), (1 - np.tanh(z.re)**2) * z.im())
def asinh(z):
    return dn(np.asinh(z.re), 1/(1-z.re**2) * z.im())
def acosh(z):
    return dn(np.acosh(z.re), 1/np.sqrt(z.re**2-1) * z.im())
def erf(z):
    return dn(np.erf(z.re), (2/np.sqrt(np.pi))*np.exp(-(z.re**2)) * z.im())