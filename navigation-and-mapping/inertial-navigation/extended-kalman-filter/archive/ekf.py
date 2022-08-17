import numpy as np
from pyrk import RK4

class Jacobian:
    def __init__(self, f):
        self.f = f
        self.jac = None
        self.n = 0
        
    def check(self, x):
        if self.n == 0:
            self.n = len(x)
            self.jac = np.zeros((self.n, self.n))

# class JacobianForward(Jacobian):
#     def __call__(self, x, dx=1e-8):
#         # if self.n == 0:
#         self.check(x)
#             # self.n = len(x)
#             # self.jac = np.zeros((self.n, self.n))
#         func = self.f(x)
        
#         for j in range(self.n):
#             Dxj = (abs(x[j])*dx if x[j] != 0 else dx)
#             d = np.zeros(self.n)
#             d[j] = Dxj
#             self.jac[:, j] = (self.f(x+d) - func)/Dxj
#         return self.jac
    
class JacobianCenter(Jacobian):
    def __call__(self, t, x, u=None, dx=1e-8):
        self.check(x)
        
        for j in range(self.n):
            Dxj = (abs(x[j])*dx if x[j] != 0 else dx)
            d = np.zeros(self.n)
            d[j] = Dxj
            if u is None:
                self.jac[:, j] = (self.f(t, x+d) - self.f(t, x-d))/(2*Dxj)
            else:
                self.jac[:, j] = (self.f(t, x+d, u) - self.f(t, x-d, u))/(2*Dxj)
        return self.jac

class EKF:
    """
    This is a continuous-discrete extended kalman filter
    """
    def __init__(self, func, dt):
        """
        func(t, x, u)
        x: state (n,1)
        z: measurement (m,1)
        R: measurement noise covariance (m,m)
        Q: process noise covariance (n,n)
        """
        self.func = func
        self.rk = RK4(func, dt)
        self.J = JacobianCenter(self.func)
        self.dt = dt
        
    def reset(self, n, m):
        self.R = np.eye(m)
        self.Q = np.eye(n)
        self.P = np.eye(n)
        
        self.x = np.zeros(n)
        self.H = np.eye(m)
        self.I = np.eye(n)
        
    def predict(self, u):
        self.x = self.rk(self.dt, self.x, u)
        F = self.J(self.dt, self.x, u)
        self.P = F @ self.P @ F.T + self.Q
        
    def update(self, z):
        H = self.H
        I = self.I
        
        y = z - H.dot(self.x)
        # S = H.dot(self.P.dot(H.T)) + self.R
        S = H @ self.P @ H.T + self.R
        # K = self.P.dot(H.T.dot(np.linalg.inv(S)))
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K.dot(y)
        self.P = (I - K.dot(H)).dot(self.P)
        
        # q = Quaternion(*self.x[6:])
        # if abs(1 - q.magnitude) > 1e-6:
        #     q.normalize
        #     self.x[6] = q.w
        #     self.x[7] = q.x
        #     self.x[8] = q.y
        #     self.x[9] = q.z
        
        # self.x = x
        # self.P = P
        
        return self.x