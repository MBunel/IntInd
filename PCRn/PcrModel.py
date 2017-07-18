
import numpy as np
from django.db import transaction
from scipy.integrate import odeint
import networkx as nx

from functools import partialmethod

from PCRn.models import Simulation, Node, Edge, Results


class Model(object):
    """
    Documentation for ClassName

    """
    def __init__(self, *args):
        """
        Fonction d'initialisation
        """
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
        """
        Formulation du modèle PCR
        """
        r, c, p, q = X
        # r, c, p, q, b = X
        dr = self.gamma(t) * q * (1-r) - \
            (self.B1+self.B2)*r + self.F(r, c)*r*c + \
            self.G(r, p)*r*p
        dc = self.B1*r + self.C1*p - \
            self.C2*c - self.F(r, c)*r*c + \
            self.H(c, p)*c*p - self.phi(t)*c*(r+c+p+q)
        dp = self.B2*r - self.C1*p + self.C2*c - \
            self.G(r, p)*r*p - self.H(c, p)*c*p
        dq = -self.gamma(t)*q*(1-r)
        # db = self.phi(t)*c(1-b)
        # Et db ?
        return [dr, dc, dp, dq]

    def network(self, y: list, t: float, N, Nbad) -> list:
        # import params
        # N, Nbad = 6, 3
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
                a += self.cMat[i][j]*y[4*j]
                b += self.cMat[i][j]*y[1+4*j]
                c += self.cMat[i][j]*y[2+4*j]
            l = list(map(lambda x: x*self.eps, [a, b, c, 0]))
            temp = [x + y for x, y in zip(self.PCR(Xpcr, t), l)]
            dX = dX + temp
        return dX

    def graphCreation(self, nodes, edges):
        # Création du graph
        self.Graph = nx.DiGraph()
        # Ajout liste de liens et noeuds
        self.Graph.add_nodes_from(nodes)
        self.Graph.add_edges_from(edges)

        print(nx.info(self.Graph))

        return self.Graph

    def conectivityMatrix(self, N: int, edges: list) -> np.array:
        # connectivity matrix

        # ⚠ np.empty ne définit pas de valeur d'initialisation
        # pour le contenu de l'array. Les valeurs initiales dépendent
        # du contenut de la mémoire, toutes les valeurs doivent êtres
        # réécrites. J'utilise donc np.zeros
        A = np.zeros(shape=(N, N), dtype=int)

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

        return A

    def runSimulation(self, n1, n2, nedges, endT=60, stepT=0.1):
        # nb noeuds
        n1 = 3
        n2 = 6

        # ne sert qu'au test
        nedges = 30

        __Tests = [
            2 <= n1, n1 <= 10,
            2 <= n2, n2 <= 10,
            2 <= nedges, nedges <= 50
        ]

        if all(__Tests):

            N = n1 + n2
            Nbad = n1
            badnodes = range(Nbad)
            Ngood = n2
            goodnodes = range(Nbad, Nbad+Ngood)

            self.cMat = self.conectivityMatrix(N, [(1, 2), (2, 3)])

            # PCRn simulation
            # see network()

            # Model solving
            # Conditions initiales
            # Voir si factorisable
            X0 = [0 for k in range(4*N)]
            for k in range(N):
                X0[3+4*k] = 1
                # X0[3+4*k] = 1

            # Paramètres temporels
            self.time = np.arange(0, endT, stepT)

            orbit = odeint(self.network, X0, self.time, args=(N, Nbad))

            solution = orbit.T
            # 4 = nb eq diff
            # valeur de p, r et c pour tous les noeuds à toutes les dates
            # len = N + t
            P = solution[2::4]
            R = solution[::4]
            C = solution[1::]


            sP = sum(P)
            sR = sum(R)
            sC = sum(C)

            # Test Db
            self.dbWrite([i for i in range(9)], solution)

        else:
            print('conditions non valides')

    @transaction.atomic
    def dbWrite(self, nodeList, res):
        sim = self.simWrite()

        # self.parmsWrite(simId)

        nodes = self.nodesWrite(sim, nodeList)

        self.resWirte(sim, nodes, self.time, res)

    def simWrite(self):
        sim = Simulation(timestamp=1)
        sim.save()

        return sim

    def parmsWrite(self, sim):
        print('a')

    def nodesWrite(self, sim, nodeList):
        nodes = []

        for i in nodeList:
            node = Node(simulation=sim, m_id=i)
            node.save()
            nodes.append(node)

        return nodes

    def edgesWrite(self, sim, nodeList, edgeList):

        edges = [Edge(idA=0, idB=1) for i in edgeList]

        Edge.objects.bulk_create(edges)

    def resWirte(self, sim, nodes, time, res):

        a = []
        for i in range(0, len(res), 4):
            nodeI = i // 4
            timeI = i // (4*9)
            import pdb; pdb.set_trace()
            b = Results(Simulation=sim,
                        node=nodes[nodeI],
                        time=time[timeI],
                        dr=res[i],
                        dc=res[i+1],
                        dp=res[i+2],
                        dq=res[i+3])

            a.append(b)

        Results.objects.bulk_create(a)
