from django.test import TestCase

import numpy as np
from random import randint, random
from scipy.integrate import odeint
from functools import partialmethod

import matplotlib.pyplot as plt

# Create your tests here.


class NetworkTest(TestCase):

    def setUp(self):
        """
        Définition des paramètres partagés
        """
        self.eps = 0.2
        self.cMat = []
        self.N = 5
        self.Nbad = 3
        self.B1 = 0.1
        self.B2 = 0.5
        self.C2 = 0.2
        self.alpha1 = 0.1
        self.alpha2 = 0.5
        self.delta1 = 0.1
        self.delta2 = 0.
        self.mu1 = 0.5
        self.mu2 = 0.2

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

    # version de Guillaume
    def h(self, s, smin, smax, hmin, hmax):
        if s < smin:
            return hmin
        elif s > smax:
            return hmax
        else:
            return ((hmin-hmax)/2)*np.cos(((s-smin)*np.pi)/(smax-smin))\
                + (hmin+hmax)/2

    # version réécrite
    def hR(self, s, smin, smax, hmin, hmax):
        if s < smin:
            rvalue = hmin
        elif s > smax:
            rvalue = hmax
        else:
            rvalue = ((hmin - hmax) / 2) * \
                np.cos(((s - smin) * np.pi) / (smax - smin)) + \
                (hmin + hmax) / 2
        return rvalue

    # version de Guillaume
    def phi(self, t):
        return self.h(t, 1, 50, 0, 1)

    # version curryfiée (réécrite)
    phiR = partialmethod(hR, smin=1, smax=50, hmin=0, hmax=1)

    # version de Guillaume
    def gamma(self, t):
        return self.h(t, 1, 3, 0, 1)

    # version curryfiée
    gammaR = partialmethod(hR, smin=1, smax=3, hmin=0, hmax=1)

    # version de Guillaume (non modifiée)
    def f(self, s):
        if s < 0:
            return 1
        elif s > 1:
            return 0
        else:
            return 0.5*np.cos(s*np.pi)+0.5

    # fonction ajoutée, non présente dans le code de Guillaume
    def _f(self, cons1, cons2, var1, var2):
        rvalue = cons1 * self.f(var1/(var2+0.01)) \
            + cons2 * self.f(var2/(var1+0.01))
        return rvalue

    # Originale
    def F(self, r, c):
        return -self.alpha1*self.f(r/(c+0.01))+self.alpha2*self.f(c/(r+0.01))

    # Remake (avec appel à _f)
    def FR(self, r, p):
        rvalue = self._f(-self.alpha1, self.alpha2, r, p)
        return rvalue

    # Originale
    def G(self, r, p):
        return -self.delta1*self.f(r/(p+0.01))+self.delta2*self.f(p/(r+0.01))

    # Remake (idem)
    def GR(self, r, p):
        rvalue = self._f(-self.delta1, self.delta2, r, p)
        return rvalue

    # Originale (idem)
    def H(self, c, p):
        return self.mu1*self.f(c/(p+0.01))-self.mu2*self.f(p/(c+0.01))

    # Remake
    def HR(self, r, p):
        rvalue = self._f(self.mu1, -self.mu2, r, p)
        return rvalue

    # Originale
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
        # il manque db ?
        return [dr, dc, dp, dq]

    # Remake
    def PCRR(self, X, t):
        r, c, p, q = X
        dr = self.gammaR(t) * q * (1-r) - \
            (self.B1+self.B2)*r + self.FR(r, c)*r*c + \
            self.GR(r, p)*r*p
        dc = self.B1*r + self.C1*p - \
            self.C2*c - self.FR(r, c)*r*c + \
            self.HR(c, p)*c*p - self.phiR(t)*c*(r+c+p+q)
        dp = self.B2*r - self.C1*p + self.C2*c - \
            self.GR(r, p)*r*p - self.HR(c, p)*c*p
        dq = -self.gammaR(t)*q*(1-r)
        return [dr, dc, dp, dq]

    # Originale
    def network(self, X, t):
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

    # Remakexs
    def networkR(self, y: list, t: float) -> list:
        dX = []
        for i in range(self.N):
            i4 = i * 4
            if i < self.Nbad:
                self.C1 = 0
            else:
                self.C1 = 0.3
            Xpcr = [y[i4], y[1+i4], y[2+i4], y[3+i4]]
            a, b, c = 0, 0, 0
            for j in range(self.N):
                a += self.cMat[i][j]*y[4*j]
                b += self.cMat[i][j]*y[1+4*j]
                c += self.cMat[i][j]*y[2+4*j]
            l = list(map(lambda x: x*self.eps, [a, b, c, 0]))
            temp = [x + y for x, y in zip(self.PCRR(Xpcr, t), l)]
            dX = dX + temp
        return dX

    # Ensemble des fonctions de test on commence par tester que chaque
    # version d'une fonction renvoie le même résultats avec paramètes
    # identiques (tirés aléatoirement). Pui on vérifie que les
    # fonction "composées" renvoient également le même résultat. Enfin
    # on vérifie que la fonction "network" ainsi que sa réecriture
    # renvoie le même résultat.

    def test_phifunction(self):
        v = randint(1, 100)
        ph1 = self.phi(v)
        ph2 = self.phiR(v)

        self.assertEqual(ph1, ph2)

    def test_gammafuction(self):
        v = randint(1, 100)
        ga1 = self.gamma(v)
        ga2 = self.gammaR(v)

        self.assertEqual(ga1, ga2)

    def test_Ffuction(self):
        v = randint(1, 100)
        w = randint(1, 100)
        F1 = self.F(v, w)
        F2 = self.FR(v, w)

        self.assertEqual(F1, F2)

    def test_Gfuction(self):
        v = randint(1, 100)
        w = randint(1, 100)
        G1 = self.G(v, w)
        G2 = self.GR(v, w)

        self.assertEqual(G1, G2)

    def test_Hfuction(self):
        v = randint(1, 100)
        w = randint(1, 100)
        H1 = self.H(v, w)
        H2 = self.HR(v, w)

        self.assertEqual(H1, H2)

    def test_PCRfuction(self):
        l = [randint(1, 100) for i in range(4)]

        # Valeur du pas de temps
        t = random()

        # Dans un cas d'utilisatiuon standard la valeur de C1 est
        # choisie en fonction de l'index d'itération de la boucle
        # contenue dans la fonction network. Ici on génére la valeur
        # aléatoirement et on l'enregistre en temps qu'attribut de
        # l'objet (puisque PCRR récupère cet attribut)
        self.C1 = random()

        PCR1 = self.PCR(l, t, self.C1)
        PCR2 = self.PCRR(l, t)

        self.assertEqual(PCR1, PCR2)

    def test_networkfunction(self):
        """
        On vérifie que les deux version du modèle renvoient la
        même sortie
        """
        r1 = odeint(self.network, self.X0, self.time)
        r2 = odeint(self.networkR, self.X0, self.time)

        self.graphgen(r1.T, r2.T)

        self.assertEqual(np.array_equal(r1, r2), True)

    def graphgen(self, r1, r2):

        P1 = sum(r1[2+4*i] for i in range(self.N)) / self.N
        R1 = sum(r1[4*i] for i in range(self.N)) / self.N
        C1 = sum(r1[1+4*i] for i in range(self.N)) / self.N
        X1 = sum(r1[3+4*i] for i in range(self.N)) / self.N

        P2 = sum(r2[2::4]) / self.N
        R2 = sum(r2[::4]) / self.N
        C2 = sum(r2[1::4]) / self.N
        X2 = sum(r2[3::4]) / self.N

        fig, (ax, ay, z) = plt.subplots(3, sharey=True)
        ax.grid()
        ax.plot(self.time, R1, 'o')
        ax.plot(self.time, C1, 'b')
        ax.plot(self.time, P1, 'r')
        ax.plot(self.time, X1)
        ax.set_title("Base")

        ay.grid()
        ay.plot(self.time, R2, 'o')
        ay.plot(self.time, C2, 'b')
        ay.plot(self.time, P2, 'r')
        ay.plot(self.time, X2)
        ay.set_title("Modifié")

        z.text(.02, .02, """eps = {}, N = {},  Nbad = {},
        B1 = {}, B2 = {}, C2 = {},
        alpha1 = {}, alpha2 = {},
        delta1 = {}, delta2 = {},
        mu1 = {},mu2 = {}""".format(self.eps, self.N, self.Nbad, self.B1,
                                  self.B2, self.C2, self.alpha1,
                                  self.alpha2, self.delta1,
                                  self.delta2, self.mu1, self.mu2))
        plt.show()
