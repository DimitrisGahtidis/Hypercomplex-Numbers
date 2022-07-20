import numpy as np
from functools import cache
from typing import Any, Callable

class Dnum:
    def __init__(self, re, im=0):
        jacobian = cache(lambda x=None: im)
        self.re, self.im = re, jacobian
        self.jacobian = jacobian
            
    def dnum_check(func): #this decorator is deisned to convert "w" to a Dnum if it is a scalar
        def wrapper(*args, **kwargs):
            self, w = args
            if type(w) != Dnum:
                w = Dnum(w)
            args = self, w
            return func(*args, **kwargs)
        return wrapper
    # Arithmetic operations
    @dnum_check
    def __add__(self, w):
        return Dnum(self.re + w.re,  self.im() + w.im())
    @dnum_check
    def __sub__(self, w):
        return Dnum(self.re - w.re,  self.im() - w.im())
    @dnum_check
    def __mul__(self, w):
        return Dnum(self.re * w.re,  self.re * w.im() + self.im() * w.re)
    @dnum_check
    def __matmul__(self, w):
        return Dnum(self.re @ w.re,  self.im() @ w.re + self.re @ w.im())
    @dnum_check
    def __rmatmul__(self, w):
        return Dnum(w.re @ self.re,  w.re @ self.im() + w.re @ self.im())
    @dnum_check
    def __truediv__(self, w):
        return Dnum(self.re / w.re,  (self.im() * w.re - self.re * w.im()) / (w.re * w.re))
    def __pow__(self, s):
        return Dnum(self.re**s,  s * self.re**(s-1) * self.im())
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
        return Dnum(-self.re,  -self.im())
    def __abs__(self):
        return abs(self.re)
    def __repr__(self):
        return f"{self.re} + {self.im()} i_0"
    def __str__(self):
        return f"{self.re} + {self.im()} i_0"

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
        return Dnum(self.re[key],  self.im()[key])
    @dnum_check
    def __setitem__(self, key, w):
        if type(w) == Dnum:
            self.re[key] = w.re
            self.im()[key] =  w.im()

    def split(self):
        if hasattr(self, '__iter__'):
            im = np.array([Dnum.split(row).im() for row in self])
            re = np.array([Dnum.split(row).re for row in self])
            return Dnum(re,  im)
        else:
            return self
