import numpy as np
from scipy.integrate import odeint
import networkx as nx

from functools import partialmethod


class Model:
    """
    Documentation for ClassName

    """
    def __init__(self, *args):
        """
        Fonction d'initialisation
        """
        super(Model, self).__init__()
        self.args = args

        self.alpha1 = 0.1
        self.alpha2 = 0.1
        self.delta1 = 0.1
        self.delta2 = 0.1
        self.mu1 = 0.1
        self.mu2 = 0.1

        self.eps = 0.2

    # TODO: Factoriser ?
    def h(self, s, smin, smax, hmin, hmax):
        if s < smin:
            rvalue = hmin
        elif s > smax:
            rvalue = hmax
        else:
            rvalue = ((hmin - hmax) / 2) * \
                np.cos(((s - smin) * np.pi) / (smax - smin)) + \
                (hmin + hmax) / 2
        return rvalue

    phi = partialmethod(h, smin=1, smax=50, hmin=0, hmax=1)

    gamma = partialmethod(h, smin=1, smax=3, hmin=0, hmax=1)

    f = partialmethod(h, smin=0, smax=1, hmin=1, hmax=0)

    def _f(self, cons1, cons2, var1, var2):
        h1 = var1 / (var2 + 0.01)
        h2 = var2 / (var1 + 0.01)

        rvalue = cons1 * self.f(h1) + \
            cons2 * self.f(h2)
        return rvalue

    def F(self, r, p):
        rvalue = self._f(-self.alpha1, self.alpha2, r, p)
        return rvalue

    def G(self, r, p):
        rvalue = self._f(-self.delta1, self.delta2, r, p)
        return rvalue

    def H(self, r, p):
        rvalue = self._f(self.mu1, -self.mu2, r, p)
        return rvalue

    def GenFunction(self, p1, p2, smin, smax, hmin, hmax):

        def h(self, s, smin, smax, hmin, hmax):
            if s < smin:
                rvalue = hmin
            elif s > smax:
                rvalue = hmax
            else:
                rvalue = ((hmin - hmax) / 2) * \
                    np.cos(((s - smin) * np.pi) / (smax - smin)) + \
                    (hmin + hmax) / 2
            return rvalue

        f = partialmethod(h, smin=0, smax=1, hmin=1, hmax=0)

        def _f(self, cons1, cons2, var1, var2):
            h1 = var1 / (var2 + 0.01)
            h2 = var2 / (var1 + 0.01)

            rvalue = cons1 * self.f(h1) + \
                cons2 * self.f(h2)
            return rvalue

        def fun(self, r, p):
            rvalue = self._f(p1, p2, r, p)
            return rvalue

        # return fun

        print('a')

    def PCR(self, X: list, t: int) -> list:
        """
        Formulation du modèle PCR

        Renvoie une liste de valeurs en
        fonction du noeud et du temps
        """
        r, c, p, q = X
        # r, c, p, q, b = X

        # Calcul de l'effectif des raisonnés
        dr = self.gamma(t) * q * (1-r) - \
            (self.B1 + self.B2) * r + \
            self.F(r, c) * r * c + \
            self.G(r, p) * r * p

        # Effectif des contrôlés
        dc = self.B1 * r + \
            self.C1 * p - \
            self.C2 * c - \
            self.F(r, c) * r * c + \
            self.H(c, p) * c * p - \
            self.phi(t) * c * (r + c + p + q)

        # Effectif des paniqués
        dp = self.B2 * r - \
            self.C1 * p + \
            self.C2 * c - \
            self.G(r, p) * r * p - \
            self.H(c, p) * c * p

        # Comportements du quotidien
        dq = -self.gamma(t) * q * (1 - r)

        # Et db ?
        # db = self.phi(t)*c(1-b)

        return [dr, dc, dp, dq]

    def runSimulation(self, endT=60, stepT=0.1):

        __Tests = True
        if all(__Tests):

            # Model solving
            # Conditions initiales
            # Voir si factorisable
            # TODO: à modifier
            X0 = [0, 0, 0, 0]

            # Paramètres temporels
            self.time = np.arange(0, endT, stepT)
            # NB self.network est la fonction de calcul
            orbit = odeint(self.network, X0, self.time)
            return orbit
        else:
            print('conditions non valides')
