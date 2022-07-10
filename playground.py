from modules.numbers import Dnum
from modules.functions import *
import matplotlib.pyplot as plt


def sigma(u, v):
    return (cos(u)*sin(v), cos(u)*cos(v), sin(u))

u = Dnum(math.pi/4, 1)
v = Dnum(math.pi/4, 1) 

point = sigma(u,v) # point = sigma(u,v) + J_sigma @ V 
x, y, z = point
x, dx = x.re, x.im
y, dy = y.re, y.im
z, dz = z.re, z.im

print(x, y, x)
print(dx, dy, dz)


def gamma(t):
    if t.re < 1:
        return (Dnum(1),t)
    elif 1 <= t.re:
        s = t - 1
        return (1 - s,Dnum(1))

def phi(s):
        return (s-1)**3 + 1

steps = 200

time = [i for i in range(steps)]
time = [s*2 / (steps-1) for s in time]
time = [s for s in time]
time = [Dnum(s, 1) for s in time]
time = [phi(s) for s in time]

curve = [gamma(t) for t in time]

X = []
Y = []

for point in curve:
    x, y = point
    x, dx = x.re, x.im
    y, dy = y.re, y.im
    X.append(x)
    Y.append(y)
    plt.gcf()
    plt.clf()
    plt.plot(X,Y, color="black")
    plt.scatter(x, y, color="black")
    plt.arrow(x , y, dx/2, dy/2, color="black", head_width=0.05)
    plt.ylim(-2, 2)
    plt.xlim(-2, 2)
    plt.show(block=False)
    plt.pause(1/60)
plt.show()
