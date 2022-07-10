
from modules.numbers import Dnum
import math

def sin(z):
    return Dnum(math.sin(z.re), math.cos(z.re) * z.im)
def cos(z):
    return Dnum(math.cos(z.re), -math.sin(z.re) * z.im)
def tan(z):
    return Dnum(math.tan(z.re), 1/(math.cos(z.re)**2) * z.im)
def exp(z):
    return Dnum(math.exp(z.re), math.exp(z.re) * z.im)
def log(z):
    return Dnum(math.log(z.re), 1/(z.re) * z.im)
def pow(z, n):
    return Dnum(math.pow(z.re,n), n * math.pow(z.re, n-1) * z.im)
def sqrt(z):
    return Dnum(math.sqrt(z.re), (0.5) * math.sqrt(z.re) * z.im)
def acos(z):
    return Dnum(math.acos(z.re), (-1)/math.sqrt(1-z.re**2) * z.im)
def asin(z):
    return Dnum(math.asin(z.re), 1/math.sqrt(1-z.re**2) * z.im)
def atan(z):
    return Dnum(math.atan(z.re), 1/(1+z.re**2) * z.im)
def sinh(z):
    return Dnum(math.sinh(z.re), math.cosh(z.re) * z.im)
def cosh(z):
    return Dnum(math.cosh(z.re), math.sinh(z.re) * z.im)
def tanh(z):
    return Dnum(math.tanh(z.re), (1 - math.tanh(z.re)**2) * z.im)
def asinh(z):
    return Dnum(math.asinh(z.re), 1/(1-z.re**2) * z.im)
def acosh(z):
    return Dnum(math.acosh(z.re), 1/math.sqrt(z.re**2-1) * z.im)
def erf(z):
    return Dnum(math.erf(z.re), (2/math.sqrt(math.pi))*math.exp(-(z.re**2)) * z.im)