import numpy as np
from scipy.integrate import odeint
import networkx as nx

class Model(object):
    """
    Documentation for ClassName

    """
    def __init__(self, args):
        super(Model, self).__init__()
        self.args = args

        # TODO: Factoriser
        self.alpha1 = 0
        self.alpha2 = 0.1
        self.delta1 = 0.1
        self.delta2 = 0.1
        self.mu1 = 0.1
        self.mu2 = 0.1

        self.B1 = 0.5
        self.B2 = 0.5

        self.C1 = 0
        self.C2 = 0.2

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

    def phi(self, t):
        rvalue = self.h(t, 1, 50, 0, 1)
        return rvalue

    def gamma(self, t):
        rvalue = self.h(t, 1, 3, 0, 1)
        return rvalue

    def f(self, s):
        if s < 0:
            rvalue = 1
        elif s > 1:
            rvalue = 0
        else:
            rvalue = 0.5 * np.cos(s * np.pi) + 0.5
        return rvalue

    def F(self, r, c):
        rvalue = -self.alpha1 * self.f(r / (c + 0.01)) + \
            self.alpha2 * self.f(c / (r + 0.01))
        return rvalue

    def G(self, r, p):
        rvalue = -self.delta1 * self.f(r / (p + 0.01)) + \
            self.delta2 * self.f(p / (r + 0.01))
        return rvalue

    def H(self, c, p):
        rvalue = self.mu1 * self.f(c / (p + 0.01)) - \
            self.mu2 * self.f(p / (c + 0.01))
        return rvalue

    def PCR(self, X, t, C1):
        r, c, p, q = X
        dr = self.gamma(t) * q * (1-r) - \
            (self.B1+self.B2)*r + self.F(r, c)*r*c + \
            self.G(r, p)*r*p

        dc = self.B1*r + self.C1*p - \
            self.C2*c - self.F(r, c)*r*c + \
            self.H(c, p)*c*p - self.phi(t)*c*(r+c+p+q)

        dp = self.B2*r - self.C1*p + self.C2*c - \
            self.G(r, p)*r*p - self.H(c, p)*c*p

        dq = -self.gamma(t)*q*(1-r)

        return [dr, dc, dp, dq]

    def network(self, y, t, N, Nbad, eps, A):
        dX = []

        for i in range(N):
            i4 = i * 4
            if i < Nbad:
                C1value = 0
            else:
                C1value = 0.3

            t = self.PCR([y[i4], y[1+i4], y[2+i4], y[3+i4]], t, C1value) \
                + np.array([eps*sum(A[i][j]*y[4*j] for j in range(N)), \
                        eps*sum(A[i][j]*y[1+4*j] for j in range(N)), \
                        eps*sum(A[i][j]*y[2+4*j] for j in range(N)), \
                        0])

            dX = dX + t

        return dX

    def runSimulation(self):

        n1 = 3
        n2 = 6
        nedges = 30

        eps = 0.2

        test = [
            2 <= n1, n1 <= 10,
            2 <= n2, n2 <= 10,
            2 <= nedges, nedges <= 50
        ]

        if all(test):

            N = n1 + n2
            Nbad = n1
            badnodes = range(Nbad)
            Ngood = n2
            goodnodes = range(Nbad, Nbad+Ngood)

            edges = []

            # Extraction noeuds
            # TODO

            # connectivity matrix
            A = np.array([[0]*N]*N)
            for edge in edges:
                j = edge[1]
                i = edge[0]
                A[j][i] = 1
            for i in range(N):
                A[i][i] = -sum(A[j][i] for j in range(N) if j != i)

            # Création du graph

            Graph = nx.DiGraph()
            # Ajout liste de liens et noeuds
            Graph.add_nodes_from()
            Graph.add_edges_from()

            # Pathfinding
            # Write

            # PCRn simulation
            # see network()

            # Model solving
            X0 = [0 for k in range(4*N)]
            for k in range(N):
                X0[3+4*k] = 1

            time = np.arange(0, 60, 0.1)

            orbit = odeint(self.network, X0, time, args=(N, Nbad, eps, A))

            solution = orbit.T
            P = sum(solution[2+4*i] for i in range(N))
            R = sum(solution[4*i] for i in range(N))
            C = sum(solution[1+4*i] for i in range(N))




        else:
            print('conditions non valides')
