import numpy as np

import attr

@attr.s(slots=True)
class Jacobian:
    f=attr.ib() # function

    # cache some variables to save processing time
    n=attr.ib(init=False, default=None)
    jac=attr.ib(init=False, default=None)


@attr.s(slots=True)
class JacobianForward(Jacobian):
    def __call__(self, x, dx=1e-8):
        if self.n is None:
            self.n = len(x)
            self.jac = np.zeros((self.n, self.n))
        func = self.f(x)

        for j in range(self.n):
            Dxj = (abs(x[j])*dx if x[j] != 0 else dx)
            d = np.zeros(self.n)
            d[j] = Dxj
            self.jac[:, j] = (self.f(x+d) - func)/Dxj
        return self.jac


@attr.s(slots=True)
class JacobianCenter(Jacobian):
    def __call__(self, x, dx=1e-8):
        if self.n is None:
            self.n = len(x)
            self.jac = np.zeros((self.n, self.n))
        for j in range(self.n):
            Dxj = (abs(x[j])*dx if x[j] != 0 else dx)
            d = np.zeros(self.n)
            d[j] = Dxj
            self.jac[:, j] = (self.f(x+d) - self.f(x-d))/(2*Dxj)
        return self.jac


class EKF:
    def __init__(self, dt):
        """
        v=[
            p[0:2]
            v[3:5]
            q[6:9]
        ] - 10
        """
        self.J = JacobianCenter(self.func)
        self.dt = dt

    def func(self, x, u=None):
        """
        x = [p,v,q]
        """
        if u is None:
            u = np.zeros(6)

        p = x[:3] + x[3:6]*self.dt

        rot = np.array(Quaternion(*x[6:]).to_rot())
        g = np.array([0,0,-9.8])
        a = np.array([0.1,0,9.8])
        aa = rot.dot(a)
        v = x[3:6]+g*self.dt+aa*self.dt

        q = Quaternion(*x[6:])
        w = Quaternion(0,u[3],u[4],u[5])
        q = q + 0.5*w*q*self.dt

        xx = np.array([0,0,0, 0,0,0, q.w,q.x,q.y,q.z])
        xx[:3] = p
        xx[3:6] = v

        return xx

    def reset(self):
        n = 10
        self.R = np.eye(n)
        self.Q = np.eye(n)
        self.P = np.eye(n)

        p = np.array([0,0,0])
        v = np.array([0,0,0])
        q = np.array([1,0,0,0])

        self.x = np.hstack((p,v,q))

    def predict(self, u):
        self.x = self.func(self.x,u)
        self.F = self.J(self.x)

        dP = self.F.dot(self.P)+self.P.dot(self.F.T)+self.Q
        I = np.eye(dP.shape[0])
        self.P = I+dP*self.dt
        # self.P = self.F.dot(self.P.dot(self.F.T))+self.Q

    def update(self, z):
        """

        """
        # H = np.eye(len(self.x))
        H = np.diag([0,0,0, 1,1,1, 1,1,1,1])
        I = np.eye(len(self.x))

        # kalman gain
        S = H.dot(self.P.dot(H.T)) + self.R
        K = self.P.dot(H.T.dot(np.linalg.inv(S)))

        # update
        zk = z - H.dot(self.x)
        x = self.x + K.dot(zk)
        P = (I - K.dot(H)).dot(self.P)

        q = Quaternion(*x[6:])
        if abs(1 - q.magnitude) > 1e-6:
            q.normalize
            x[6] = q.w
            x[7] = q.x
            x[8] = q.y
            x[9] = q.z

        self.x = x
        self.P = P

        return x
