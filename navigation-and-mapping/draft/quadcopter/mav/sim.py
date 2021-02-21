#!/usr/bin/env python

import numpy as np
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

from the_collector import BagIt
from the_collector import Pickle

from squaternion import Quaternion
from pyrk import RK4

bag = BagIt(Pickle)

# def vanderpol(t, xi, u):
#     dx, x = xi
#     mu = 4.0 # damping
#
#     ddx = mu*(1-x**2)*dx-x
#     dx = dx
#
#     return np.array([ddx, dx])
#
# rk = RK4(vanderpol)

def func(t, x, u):
    p = x[3:6]
    v = u[:3]
    q = Quaternion(*x[6:])
    q = 0.5*Quaternion(0,u[3],u[4],u[5])*q

    xx = np.array([0,0,0, 0,0,0, q.w,q.x,q.y,q.z])
    xx[:3] = p
    xx[3:6] = v

    return xx

rk = RK4(func)


num = 100
x = np.array([0,0,0, 0,0,0, 1,0,0,0])
t = 0
step = 0.1
# true = [] # true states
# save = [] # noisey states
noise = np.random.uniform(-1,1,(num,10))
# scale = np.diag([0.1,0.1,0.1, 0.1,0.1,0.1, 0.01,0.01,0.01,0.01])
scale = np.diag([1.,1.,1., 0.5,0.5,0.5, 0.1,0.1,0.1,0.1])

for i in range(num):
    u = np.array([0.1,0,0, 0,0,0.1]) # linear x, rotational z
    x = rk.step(x,u,t,step)
    t += step
    # true.append(x)
    # save.append( scale.dot( scale.dot(noise[i,:]) ) )

    bag.push("truth", x)
    bag.push("meas", x + scale.dot(noise[i,:]))

    print(f">> [{i}]: {x}")
    print(f"+ {Quaternion(*x[6:]).magnitude}")

bag.write('sim', timestamp=False)
