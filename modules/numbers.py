import numpy as np

class Dnum:
    def __init__(self, re, im = 0):
        self.re, self.im = re, im
    def scalar_check(func): #this decorator is deisned to convert "w" to a Dnum if it is a scalar
        def wrapper(*args, **kwargs):
            self, w = args
            if type(w) != Dnum:
                w = Dnum(w)
            args = self, w
            return func(*args, **kwargs)
        return wrapper
    @scalar_check
    def __add__(self, w):
        return Dnum(self.re + w.re, self.im + w.im)
    @scalar_check
    def __sub__(self, w):
        return Dnum(self.re - w.re, self.im - w.im)
    @scalar_check
    def __mul__(self, w):
        return Dnum(self.re * w.re, self.re * w.im + self.im * w.re)
    @scalar_check
    def __matmul__(self, w):
        return Dnum(self.re @ w.re, self.re @ w.im + self.im @ w.re)
    @scalar_check
    def __truediv__(self, w):
        return Dnum(self.re / w.re, (self.im * w.re - self.re * w.im) / (w.re * w.re))
    def __pow__(self, s):
        return Dnum(self.re**s, s * self.re**(s-1) * self.im)
    @scalar_check
    def __radd__(self, w):
        return w.__add__(self)
    @scalar_check
    def __rsub__(self, w):
        return w.__sub__(self)
    @scalar_check
    def __rmul__(self, w):
        return w.__mul__(self)
    @scalar_check
    def __rtruediv__(self, w):
        return w.__truediv__(self)
    def __pos__(self):
        return self
    def __neg__(self):
        return Dnum(-self.re, -self.im)
    def __abs__(self):
        return abs(self.re)
    def __repr__(self):
        return f"{self.re} + {self.im} i_0"
    def __str__(self):
        return f"{self.re} + {self.im} i_0"
    def __getitem__(self, key):
        return Dnum(self.re[key], self.im[key])

    def split(self):
        if hasattr(self, '__iter__'):
            im = np.array([x.im for x in self])
            re = np.array([x.re for x in self])
            return Dnum(re, im)
        else:
            self.im = self.im
            self.re = self.re