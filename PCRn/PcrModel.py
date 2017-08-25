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

        # TODO: Attribuer une valeur par noeuds
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

    def PCR(self, X: list, t: int, node) -> list:
        """
        Formulation du modèle PCR

        Renvoie une liste de valeurs en
        fonction du noeud et du temps
        """
        r, c, p, q = X
        # r, c, p, q, b = X

        # Calcul de l'effectif des raisonnés
        dr = self.gamma(t) * q * (1-r) - \
            (node['B1'] + node['B2']) * r + \
            self.F(r, c) * r * c + \
            self.G(r, p) * r * p

        # Effectif des contrôlés
        dc = node['B1'] * r + \
            node['C1'] * p - \
            node['C2'] * c - \
            self.F(r, c) * r * c + \
            self.H(c, p) * c * p - \
            self.phi(t) * c * (r + c + p + q)

        # Effectif des paniqués
        dp = node['B2'] * r - \
            node['C1'] * p + \
            node['C2'] * c - \
            self.G(r, p) * r * p - \
            self.H(c, p) * c * p

        # Comportements du quotidien
        dq = -self.gamma(t) * q * (1 - r)

        # Et db ?
        # db = self.phi(t)*c(1-b)

        return [dr, dc, dp, dq]

    def network(self, y: list, t: float, graph) -> list:
        """FIXME! briefly describe function

        :param y: liste variables (valeur précédente pour tous les noeuds)
        :param t: pas de temps
        :param graph: objet graph
        :returns:
        :rtype:

        """

        dX = []
        nodes = graph.nodes()
        N = len(nodes)

        # On calcule les paramètres pour chaque noeud
        for i in nodes:
            i4 = i * 4

            node = graph.node[i]

            # Couplage linéaire
            # Variables pour le noeud i
            Xpcr = y[i4:i4+3]

            # À migrer dans une fonction
            a, b, c = 0, 0, 0

            for j in range(N):
                a += self.cMat[i][j]*y[4*j]
                b += self.cMat[i][j]*y[1+4*j]
                c += self.cMat[i][j]*y[2+4*j]

            l = list(map(lambda x: x*self.eps, [a, b, c, 0]))

            # zipped = []
            # if True:
            #     l = linearCoupling()
            #     zipped.append(l)
            # if True:
            #     q = quadraticCoupling()
            #     zipped.append(q)
            # pcr = self.PCR(Xpcr, t, node)
            # zipped.append(pcr)
            # temp = [sum(i) for i in zip(*zipped)]

            temp = [x + y for x, y in zip(self.PCR(Xpcr, t, node), l)]
            dX = dX + temp

        return dX

    def linearCoupling(self, N, i, y):
        a, b, c = 0, 0, 0

        # Multiplier par edges params
        for j in range(N):
            a += self.cMat[i][j]*y[4*j]
            b += self.cMat[i][j]*y[1+4*j]
            c += self.cMat[i][j]*y[2+4*j]

        return [a, b, c, 0]

    def quadraticCoupling(self, N, i, y, Xpcr):
        print('aa')

        # quadratic coupling
        # needs a 3x3 matrix 'Quad' of coefficients for each pair [i,k]
        a, b, c = 0, 0, 0
        for k in range(N):
            quadc = self.qMat[i][k]
            a += self.cMatQ[i][k] * y[4*k] * \
                (quadc[0][1] * Xpcr[1] + quadc[0][2] * Xpcr[2]) -\
                self.cMatQ[i][k] * Xpcr[0] * \
                (quadc[1][0] * y[1+4*k] + quadc[2][0] * y[2+4*k])
            b += self.cMatQ[i][k] * y[1+4*k] * \
                (quadc[1][0] * Xpcr[0] + quadc[1][2] * Xpcr[2]) -\
                self.cMatQ[i][k] * Xpcr[1] * \
                (quadc[0][1] * y[4*k]+quadc[2][1] * y[2+4*k])
            c += self.cMatQ[i][k] * y[2+4*k] * \
                (quadc[2][0] * Xpcr[0] + quadc[2][1] * Xpcr[1]) -\
                self.cMatQ[i][k] * Xpcr[2] * \
                (quadc[1][2] * y[1+4*k] + quadc[0][2] * y[4*k])

        return[a, b, c, 0]

    def graphCreation(self, nodes, edges):
        # Création du graph (orienté)
        Graph = nx.DiGraph()
        # Ajout liste de liens et noeuds
        Graph.add_nodes_from(nodes)
        Graph.add_edges_from(edges)

        print(nx.info(Graph))

        return Graph

    def exportNodes(self, G):
        nodes = [(i, G.node[i]) for i in G.nodes()]
        return nodes

    def conectivityMatrix(self, N: int, edges: list) -> np.array:
        # connectivity matrix (couplage linéaire)

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

    def adjacencyMatrix(selfelf, N: int, edges: list) -> np.array:
        # Adjacencyy matrix where diagonal terms are zeros
        A = np.zeros(shape=(N, N), dtype=int)

        for edge in edges:
            j, i = edge
            A[j][i] = 1

        for i in range(N):
            A[i][i] = 0

        return A

    def quadraticMatrix(self, N: int, edges: list) -> np.array:
        # A matrix that contains the (3,3) matrix of quadratic
        # coupling coefficients
        A = np.zeros(shape=(N, N), dtype=np.array)

        for edge in edges:
            j, i = edge
            # each element is a 3x3 matrix quad; to be linked
            # with the edge in the future...
            A[j][i] = self.quad
            # A[j][i] = edge.quad
        for i in range(N):
            A[i][i] = np.zeros(3, 3)

        return A

    def runSimulation(self, endT=60, stepT=0.1):

        # Création du graphe
        self.Graph = self.graphCreation(
            [
                (0, {'B1': 0.5, 'B2': 0.5, 'C1': 0,
                     'C2': 0.2, 'S1': 0, 'S2': 0}),
                (1, {'B1': 0.5, 'B2': 0.5, 'C1': 0,
                     'C2': 0.2, 'S1': 0, 'S2': 0}),
                (2, {'B1': 0.2, 'B2': 0.5, 'C1': 0,
                     'C2': 0.2, 'S1': 0, 'S2': 0}),
                (3, {'B1': 0.5, 'B2': 0.4, 'C1': 0.3,
                     'C2': 0.2, 'S1': 0, 'S2': 0}),
                (4, {'B1': 0.5, 'B2': 0.4, 'C1': 0.3,
                     'C2': 0.2, 'S1': 0, 'S2': 0})
            ],
            [(0, 3), (1, 3), (2, 4)])

        # nb noeuds et nb liens
        NbNodes = len(self.Graph.nodes())
        NbEdges = len(self.Graph.edges())

        # Tests
        __Tests = [
            2 <= NbNodes, NbNodes <= 10,
            2 <= NbEdges, NbEdges <= 50
        ]

        if all(__Tests):
            self.cMat = self.conectivityMatrix(NbNodes, self.Graph.edges())
            # Model solving
            # Conditions initiales
            # Voir si factorisable
            # TODO: à modifier
            X0 = [0 for k in range(4*NbNodes)]
            for k in range(NbNodes):
                X0[3+4*k] = 1
            # Paramètres temporels
            self.time = np.arange(0, endT, stepT)
            # NB self.network est la fonction de calcul
            orbit = odeint(self.network, X0, self.time, args=(self.Graph,))

            return orbit
        else:
            print('conditions non valides')
