from django.test import TestCase

import numpy as np
from scipy.integrate import odeint

# Create your tests here.


class NetworkTest(TestCase):

    def setUp(self):
        self.eps = 0.2
        self.cMat = []
        self.N = 5
        self.Nbad = 2
        self.B1 = 0.5
        self.B2 = 0.5
        self.C2 = 0.2
        self.alpha1 = 0.1
        self.alpha2 = 0.1
        self.delta1 = 0.1
        self.delta2 = 0.1
        self.mu1 = 0.1
        self.mu2 = 0.1

        self.edges = [(1, 2), (2, 3)]

        self.cMat = np.array([[0 for i in range(self.N)] for j in range(self.N)])

        for edge in self.edges:
            j = edge[1]
            i = edge[0]
            self.cMat[j][i] = 1
        for i in range(self.N):
            self.cMat[i][i] = - sum(self.cMat[j][i] for j in range(self.N) if j!= i)

        self.X0 = [0 for k in range(4*self.N)]
        for k in range(self.N):
            self.X0[3+4*k] = 1

        self.time = np.arange(0, 60, 0.1)

    def h(self, s, smin, smax, hmin, hmax):
        if s < smin:
            return hmin
        elif s > smax:
            return hmax
        else:
            return ((hmin-hmax)/2)*np.cos(((s-smin)*np.pi)/(smax-smin))\
                + (hmin+hmax)/2

    def phi(self, t):
        return self.h(t, 1, 50, 0, 1)

    def gamma(self, t):
        return self.h(t, 1, 3, 0, 1)

    def f(self, s):
        if s < 0:
            return 1
        elif s > 1:
            return 0
        else:
            return 0.5*np.cos(s*np.pi)+0.5

    def F(self, r, c):
        return -self.alpha1*self.f(r/(c+0.01))+self.alpha2*self.f(c/(r+0.01))

    def G(self, r, p):
        return -self.delta1*self.f(r/(p+0.01))+self.delta2*self.f(p/(r+0.01))

    def H(self, c, p):
        return self.mu1*self.f(c/(p+0.01))-self.mu2*self.f(p/(c+0.01))

    def PCR(self, X, t, C1):
        r, c, p, q = X
        dr = self.gamma(t)*q*(1-r) - \
            (self.B1+self.B2)*r + \
            self.F(r, c)*r*c + self.G(r, p)*r*p
        dc = self.B1*r + C1*p - self.C2*c - \
            self.F(r, c)*r*c + self.H(c, p)*c*p - \
            self.phi(t)*c*(r+c+p+q)
        dp = self.B2*r - C1*p + self.C2*c - \
            self.G(r, p)*r*p - self.H(c, p)*c*p
        dq = -self.gamma(t)*q*(1-r)
        return [dr, dc, dp, dq]

    def networkG(self, X, t):
        dX = [0 for k in range(4*self.N)]
        for i in range(self.Nbad):
            [dX[0+4*i], dX[1+4*i], dX[2+4*i], dX[3+4*i]] = \
                self.PCR([X[0+4*i], X[1+4*i], X[2+4*i], X[3+4*i]], t, 0) \
                + np.array([self.eps*sum(self.cMat[i][j]*X[0+4*j] for j in range(self.N)), \
                            self.eps*sum(self.cMat[i][j]*X[1+4*j] for j in range(self.N)), \
                            self.eps*sum(self.cMat[i][j]*X[2+4*j] for j in range(self.N)), 0])
        for i in range(self.Nbad, self.N):
            [dX[0+4*i], dX[1+4*i], dX[2+4*i], dX[3+4*i]] = \
                self.PCR([X[0+4*i], X[1+4*i], X[2+4*i], X[3+4*i]], t, 0.3) \
                + np.array([self.eps*sum(self.cMat[i][j]*X[0+4*j] for j in range(self.N)), \
                            self.eps*sum(self.cMat[i][j]*X[1+4*j] for j in range(self.N)), \
                            self.eps*sum(self.cMat[i][j]*X[2+4*j] for j in range(self.N)), 0])
        return dX

    def networkR(self, y: list, t: float) -> list:
        dX = []
        for i in range(self.N):
            i4 = i * 4
            if i < self.Nbad:
                C1 = 0
            else:
                C1 = 0.3
            Xpcr = [y[i4], y[1+i4], y[2+i4], y[3+i4]]
            a, b, c = 0, 0, 0
            for j in range(self.N):
                a += self.cMat[i][j]*y[4*j]
                b += self.cMat[i][j]*y[1+4*j]
                c += self.cMat[i][j]*y[2+4*j]
            l = list(map(lambda x: x*self.eps, [a, b, c, 0]))
            temp = [x + y for x, y in zip(self.PCR(Xpcr, t, C1), l)]
            dX = dX + temp
        return dX

    def test_networkfunction(self):
        """
        On vérifie que les deux version du modèle renvoient la
        même sortie
        """
        r1 = odeint(self.networkG, self.X0, self.time)
        r2 = odeint(self.networkR, self.X0, self.time)

        self.assertEqual(np.array_equal(r1, r2), True)
