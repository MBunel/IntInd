import numpy as np
from scipy.integrate import odeint
import networkx as nx

from functools import partialmethod


class Model(object):
    """
    Documentation for ClassName

    """
    def __init__(self, *args):
        super(Model, self).__init__()
        self.args = args

        # TODO: Factoriser
        self.alpha1 = 0.1
        self.alpha2 = 0.1
        self.delta1 = 0.1
        self.delta2 = 0.1
        self.mu1 = 0.1
        self.mu2 = 0.1

        self.B1 = 0.5
        self.B2 = 0.5

        self.C1 = 0
        self.C2 = 0.2

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

    def f(self, s):
        if s < 0:
            rvalue = 1
        elif s > 1:
            rvalue = 0
        else:
            rvalue = 0.5 * np.cos(s * np.pi) + 0.5
        return rvalue

    def _f(self, cons1, cons2, var1, var2):
        rvalue = cons1 * self.f(var1/(var2+0.01)) \
            + cons2 * self.f(var2/(var1+0.01))
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

    def PCR(self, X: list, t: int) -> list:
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

    def network(self, y: list, t: float) -> list:
        # import params
        N, Nbad, A = [0]*3
        dX = []
        for i in range(N):
            i4 = i * 4
            if i < Nbad:
                self.C1 = 0
            else:
                self.C1 = 0.3
            Xpcr = [y[i4], y[1+i4], y[2+i4], y[3+i4]]
            a, b, c = 0, 0, 0
            for j in range(N):
                a += A[i][j]*y[4*j]
                b += A[i][j]*y[1+4*j]
                c += A[i][j]*y[2+4*j]
            l = list(map(lambda x: x*self.eps, [a, b, c, 0]))
            temp = [x + y for x, y in zip(self.PCR(Xpcr, t), l)]
            dX = dX + temp
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

            # Extraction liens
            edges = []

            for k in range(nedges):
                a, b = 0, 0
                while a==b:
                    a, b = randint(0, N-1), randint(0, N-1)
                c = randint(1, 2)
                if c==1:
                    edges = edges + [(a,b)]
                else:
                    edges = edges + [(b,a)]

            # connectivity matrix

            # ⚠ np.empty ne définit pas de valeur d'initialisation
            # pour le contenu de l'array. Les valeurs initiales dépendent
            # du contenut de la mémoire, toutes les valeurs doivent êtres
            # réécrites. J'utilise donc np.zero
            A = np.zero(shape=(N, N), dtype=int)

            # Remplit la matrice de contiguité en fonction de l'existance ou
            # non d'un lien. Si un lien existe un 1 est ajouté, sinon la valeur
            # reste à zéro
            for edge in edges:
                j, i = edge
                A[j][i] = 1

            # Comptabilise le nombre de connections pour chaque
            # colone (et donc noeud)
            for i in range(N):
                A[i][i] = -sum(A[j][i] for j in range(N) if j != i)

            # Création du graph
            Graph = nx.DiGraph()
            # Ajout liste de liens et noeuds
            Graph.add_nodes_from()
            Graph.add_edges_from(edges)

            # Pathfinding
            isolated_nodes = []
            isolated_nodes_number = 0
            evacuated_nodes = []
            evacuated_nodes_number = 0
            for k in range(Nbad):
                connection = 0
                for j in range(Nbad, N):
                    if nx.has_path(Graph, k, j):
                        connection = connection + 1
                        evacuated_nodes_number = evacuated_nodes_number + 1
                        evacuated_nodes = evacuated_nodes + [[k, nx.shortest_path(Graph, k, j)]]
                if connection == 0:
                    isolated_nodes_number = isolated_nodes_number + 1
                    isolated_nodes = isolated_nodes + [k]

            # PCRn simulation
            # see network()

            # Model solving
            # Conditions initiales
            # Voir si factorisable
            X0 = [0 for k in range(4*N)]
            for k in range(N):
                X0[3+4*k] = 1

            time = np.arange(0, 60, 0.1)

            orbit = odeint(self.network, X0, time, args=(N, Nbad, self.eps, A))

            solution = orbit.T
            P = sum(solution[2+4*i] for i in range(N))
            R = sum(solution[4*i] for i in range(N))
            C = sum(solution[1+4*i] for i in range(N))

            print(P, R, C)

        else:
            print('conditions non valides')
