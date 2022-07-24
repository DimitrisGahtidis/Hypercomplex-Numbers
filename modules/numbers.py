from turtle import backward
import numpy as np
from functools import cache
import types

class dnum:
    backward_mode = False
    def __init__(self, re, d=lambda v: (v*0), cacheless=None):
        if cacheless is True:
            if type(d) != types.FunctionType:
                self.re, self.d = re, lambda v: (v*d)
            else:
                self.re, self.d = re, d
        else:
            if type(d) != types.FunctionType:
                self.re, self.d = re, cache(lambda v: (v*d))
            else:
                self.re, self.d = re, cache(d)

    # Properties
    @property
    def im(self):
        return self.d(1)

    @property
    def T(self):
        if dnum.backward_mode is True:
            if hasattr(self.re, "T"): # and hasattr(self.im, "T"):
                return dnum(self.re.T, lambda v: self.d(v).T)
        else:
            if hasattr(self.re, "T") and hasattr(self.im, "T"):
                return dnum(self.re.T, self.im.T)
    
    # Class methods
    @classmethod
    def backward(cls, boolean):
        cls.backward_mode = boolean

    # Decorator to convert "w" to a dnum if it is a scalar                
    def dnum_check(func): 
        def wrapper(*args, **kwargs):
            self, w = args
            if type(w) != dnum:
                w = dnum(w)
            args = self, w
            return func(*args, **kwargs)
        return wrapper

    # Arithmetic operations
    @dnum_check
    def __add__(self, w):
        if dnum.backward_mode is True:
            return dnum(self.re + w.re,  lambda v: self.d(v) + w.d(v))
        else:
            return dnum(self.re + w.re,  self.im + w.im)
    @dnum_check
    def __sub__(self, w):
        if dnum.backward_mode is True:
            return dnum(self.re - w.re,  lambda v: self.d(v) - w.d(v))
        else:
            return dnum(self.re - w.re,  self.im - w.im)
    @dnum_check
    def __mul__(self, w):
        if dnum.backward_mode is True:
            return dnum(self.re * w.re,  lambda v: w.d((v* self.re)) + self.d((v* w.re)))
        else:
            return dnum(self.re * w.re,  self.re * w.im + self.im * w.re)
    @dnum_check
    def __matmul__(self, w):
        if dnum.backward_mode is True:
            return dnum(self.re @ w.re,  lambda v: w.d(self.d(v) + (v*w.re)))#lambda v: self.d(v) @ w.re + self.re @ w.d(v))
        else:
            return dnum(self.re @ w.re,  self.im @ w.re + self.re @ w.im)
    @dnum_check
    def __rmatmul__(self, w):
        if dnum.backward_mode is True:
            return dnum(w.re @ self.re,  lambda v: w.d(v) @ self.re + w.re @ self.d(v))
        else:
            return dnum(w.re @ self.re,  w.re @ self.im + w.im @ self.re)
    @dnum_check
    def __truediv__(self, w):
        if dnum.backward_mode is True:
            return dnum(self.re / w.re, lambda v:  (self.d(np.dot( v, w.re) / (w.re * w.re)) - w.d((v* self.re) / (w.re * w.re))))
        else:
            return dnum(self.re / w.re,  (self.im * w.re - self.re * w.im) / (w.re * w.re))
    def __pow__(self, s):
        if dnum.backward_mode is True:
            return dnum(self.re**s,  lambda v:  self.d((v* s * self.re**(s-1))))
        else:
            return dnum(self.re**s,  s * self.re**(s-1) * self.im)
    @dnum_check
    def __radd__(self, w):
        return w.__add__(self)
    @dnum_check
    def __rsub__(self, w):
        return w.__sub__(self)
    @dnum_check
    def __rmul__(self, w):
        return w.__mul__(self)
    @dnum_check
    def __rtruediv__(self, w):
        return w.__truediv__(self)
    def __pos__(self):
        return self
    def __neg__(self):
        if dnum.backward_mode is True:
            return dnum(-self.re, lambda v: self.d(-v))
        else:
            return dnum(-self.re,  -self.im)
    def __abs__(self):
        return abs(self.re)
    def __repr__(self):
        if self.backward_mode is True:
            return f"{self.re} + {self.d} i_0"
        else:
            return f"{self.re} + {self.im} i_0"
    def __str__(self):
        if self.backward_mode is True:
            return f"{self.re} + {self.d} i_0"
        else:
            return f"{self.re} + {self.im} i_0"

    # Logical operators
    @dnum_check
    def __gt__(self, w):
        return self.re > w.re
    @dnum_check
    def __lt__(self, w):
        return self.re < w.re
    @dnum_check
    def __ge__(self, w):
        return self.re >= w.re
    @dnum_check
    def __le__(self, w):
        return self.re <= w.re
    @dnum_check
    def __ne__(self, w):
        return self.re != w.re

    # Container emulation
    def __getitem__(self, key):
        if dnum.backward_mode is True:
            return dnum(self.re[key],  lambda v: self.d(v)[key])
        else:
            return dnum(self.re[key],  self.im[key])
    @dnum_check
    def __setitem__(self, key, w): # There is some redundancy in this method that must be patched
        if type(w) == dnum:
            if dnum.backward_mode is True:
                self.re[key] = w.re
                self.im[key] = lambda v: w.d(v)
            else:
                self.re[key] = w.re
                self.im[key] = w.im

    def reshape(self, *args, **kwargs):
        if dnum.backward_mode is True:
            if hasattr(self.re, "reshape"): # and hasattr(lambda v: self.d(v), "reshape"):
                return dnum(self.re.reshape(*args, **kwargs), lambda v: self.d(v).reshape(*args, **kwargs))
        else:
            if hasattr(self.re, "reshape") and hasattr(self.im, "reshape"):
                return dnum(self.re.reshape(*args, **kwargs), self.im.reshape(*args, **kwargs))

    def split(array):
        if dnum.backward_mode is True:
            if hasattr(array, '__iter__'):
                # d_array = np.array([dnum.split(row).d for row in array])
                re_array = np.array([dnum.split(row).re for row in array])
                def vecmul(v):
                        return np.array([dnum.split(row).d(value) for value, row in zip(v, array)]).sum(axis=0)
                def matmul(A):
                    return np.array([vecmul(row) for row in A])
                return dnum(re_array,  matmul, cacheless=True)
            else:
                return array
        else:
            if hasattr(array, '__iter__'):
                d_array = np.array([dnum.split(row).im for row in array])
                re_array = np.array([dnum.split(row).re for row in array])
                return dnum(re_array,  d_array)
            else:
                return array
    
    def sin(z):
        if dnum.backward_mode is True:
            return dnum(np.sin(z.re), lambda v: z.d((v* np.cos(z.re))))
        else:
            return dnum(np.sin(z.re), np.cos(z.re) * z.im)
    def cos(z):
        if dnum.backward_mode is True:
            return dnum(np.cos(z.re),  lambda v: z.d((v* -np.sin(z.re))))
        else:
            return dnum(np.cos(z.re), -np.sin(z.re) * z.im)
    def tan(z):
        if dnum.backward_mode is True:
            return dnum(np.tan(z.re), lambda v: z.d(v/(np.cos(z.re)**2)))
        else:
            return dnum(np.tan(z.re), 1/(np.cos(z.re)**2) * z.im)
    def exp(z):
        if dnum.backward_mode is True:
            return dnum(np.exp(z.re), lambda v: z.d((v* np.exp(z.re))))
        else: 
            return dnum(np.exp(z.re), np.exp(z.re) * z.im)
    def log(z):
        if dnum.backward_mode is True:
            return dnum(np.log(z.re), lambda v: z.d(v/(z.re)))
        else: 
            return dnum(np.log(z.re), 1/(z.re) * z.im)
    def pow(z, n):
        if dnum.backward_mode is True:
            return dnum(np.pow(z.re,n), lambda v:  z.d((v* n * np.pow(z.re, n-1))))
        else:
            return dnum(np.pow(z.re,n), n * np.pow(z.re, n-1) * z.im)
    def sqrt(z):
        if dnum.backward_mode is True:
            return dnum(np.sqrt(z.re), lambda v: z.d((v* (0.5) * np.sqrt(z.re))))
        else:
            return dnum(np.sqrt(z.re), (0.5) * np.sqrt(z.re) * z.im)
    def acos(z):
        if dnum.backward_mode is True:
            return dnum(np.acos(z.re), lambda v: z.d((-v)/np.sqrt(1-z.re**2)))
        else:
            return dnum(np.acos(z.re), (-1)/np.sqrt(1-z.re**2) * z.im)
    def asin(z):
        if dnum.backward_mode is True:
            return dnum(np.asin(z.re), lambda v: z.d(v/np.sqrt(1-z.re**2)))
        else:
            return dnum(np.asin(z.re), 1/np.sqrt(1-z.re**2) * z.im)
    def atan(z):
        if dnum.backward_mode is True:
            return dnum(np.atan(z.re), lambda v: z.d(v/1/(1+z.re**2)))
        else:
            return dnum(np.atan(z.re), 1/(1+z.re**2) * z.im)
    def sinh(z):
        if dnum.backward_mode is True:
            return dnum(np.sinh(z.re), lambda v: z.d((v* np.cosh(z.re))))
        else:
            return dnum(np.sinh(z.re), np.cosh(z.re) * z.im)
    def cosh(z):
        if dnum.backward_mode is True:
            return dnum(np.cosh(z.re), lambda v : z.d((v* np.sinh(z.re))))
        else:
            return dnum(np.cosh(z.re), np.sinh(z.re) * z.im)
    def tanh(z):
        if dnum.backward_mode is True:
            return dnum(np.tanh(z.re), lambda v: z.d((v* (1 - np.tanh(z.re)**2))))
        else:
            return dnum(np.tanh(z.re), (1 - np.tanh(z.re)**2) * z.im)
    def asinh(z):
        if dnum.backward_mode is True:
            return dnum(np.asinh(z.re), lambda v: z.d(v/(1-z.re**2)))
        else:
            return dnum(np.asinh(z.re), 1/(1-z.re**2) * z.im)
    def acosh(z):
        if dnum.backward_mode is True:
            return dnum(np.acosh(z.re), lambda v: z.d(v/np.sqrt(z.re**2-1)))
        else:
            return dnum(np.acosh(z.re), 1/np.sqrt(z.re**2-1) * z.im)
    def erf(z):
        if dnum.backward_mode is True:
            return dnum(np.erf(z.re), lambda v: z.d((v* (2/np.sqrt(np.pi))*np.exp(-(z.re**2)))))
        else:
            return dnum(np.erf(z.re), (2/np.sqrt(np.pi))*np.exp(-(z.re**2)) * z.im)
            
