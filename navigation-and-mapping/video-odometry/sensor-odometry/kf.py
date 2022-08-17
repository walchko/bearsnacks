
import numpy as np
from dataclasses import dataclass, field
# from dataclasses import asdict, astuple
# from dataclasses import InitVar
from typing import Any
from squaternion import Quaternion

# @attr.s(slots=True)
# @dataclass
class Jacobian:
    def __init__(self, f):
        self.f = f
        self.jac = None
        self.n = 0
        
    def check(self, x):
        if self.n == 0:
            self.n = len(x)
            self.jac = np.zeros((self.n, self.n))
#     f: Any = None # function
    
#     # cache some variables to save processing time
#     n: int = field(init=False, default=0) #=attr.ib(init=False, default=None)
#     jac: Any = field(init=False, default=None) #=attr.ib(init=False, default=None)
    
    
# @attr.s(slots=True)
# @dataclass
class JacobianForward(Jacobian):
    def __call__(self, x, dx=1e-8):
        # if self.n == 0:
        self.check(x)
            # self.n = len(x)
            # self.jac = np.zeros((self.n, self.n))
        func = self.f(x)
        
        for j in range(self.n):
            Dxj = (abs(x[j])*dx if x[j] != 0 else dx)
            d = np.zeros(self.n)
            d[j] = Dxj
            self.jac[:, j] = (self.f(x+d) - func)/Dxj
        return self.jac
    
    
# @attr.s(slots=True)
# @dataclass #(slots=True)
class JacobianCenter(Jacobian):
    def __call__(self, x, dt, dx=1e-8):
        # if self.n == 0:
        self.check(x)
            # self.n = len(x)
            # self.jac = np.zeros((self.n, self.n))
        for j in range(self.n):
            Dxj = (abs(x[j])*dx if x[j] != 0 else dx)
            d = np.zeros(self.n)
            d[j] = Dxj
            self.jac[:, j] = (self.f(x+d,dt) - self.f(x-d,dt))/(2*Dxj)
        # print(self.jac)
        return self.jac

    
    
class EKF:
    def __init__(self, func, dt):
        """
        v=[
            p[0:2]
            v[3:5]
            q[6:9]
        ] - 10
        """
        self.func = func
        self.J = JacobianCenter(self.func)
        self.dt = dt
        
#     def func(self, x, u=None):
#         if u is None:
#             u = np.zeros(6)
            
#         p = x[:3] + x[3:6]*self.dt
        
#         rot = np.array(Quaternion(*x[6:]).to_rot())
#         g = np.array([0,0,-9.8])
#         a = np.array([0.1,0,9.8])
#         aa = rot.dot(a)
#         v = x[3:6]+g*self.dt+aa*self.dt
        
#         q = Quaternion(*x[6:])
#         w = Quaternion(0,u[3],u[4],u[5])
#         q = q + 0.5*w*q*self.dt
        
#         xx = np.array([0,0,0, 0,0,0, q.w,q.x,q.y,q.z])
#         xx[:3] = p
#         xx[3:6] = v
        
#         # print("xx", xx)
        
#         return xx
        
    def reset(self):
        n = 10
        self.R = np.eye(n)
        self.Q = np.eye(n)
        self.P = np.eye(n)
        
        p = np.array([0,0,0])
        v = np.array([0,0,0])
        q = np.array([1,0,0,0])
        
#         aa = 0.001
#         gg = 0.0001
#         ba = np.array([aa,aa,aa])
#         bg = np.array([gg,gg,gg])
        self.x = np.hstack((p,v,q))
        
    def predict(self, u):
        self.x = self.func(self.x,self.dt,u)
        self.F = self.J(self.x, self.dt)
        self.P = self.F.dot(self.P.dot(self.F.T))+self.Q
        
    def update(self, z):
        H = np.eye(len(self.x))
        H = np.diag([0,0,0, 1,1,1, 1,1,1,1])
        I = np.eye(len(self.x))
        
        y = z - H.dot(self.x)
        S = H.dot(self.P.dot(H.T)) + self.R
        K = self.P.dot(H.T.dot(np.linalg.inv(S)))
        x = self.x + K.dot(y)
        P = (I - K.dot(H)).dot(self.P)
        
        q = Quaternion(*self.x[6:])
        if abs(1 - q.magnitude) > 1e-6:
            q.normalize
            self.x[6] = q.w
            self.x[7] = q.x
            self.x[8] = q.y
            self.x[9] = q.z
        
        self.x = x
        self.P = P
        
        return x