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

        Renvoie une liste de valeurs en
        fonction du noeud et du temps
        """
        r, c, p, q = X
        # r, c, p, q, b = X

        # Calcul de l'effectif des raisonnés
        dr = self.gamma(t) * q * (1-r) - \
            (self.B1+self.B2)*r + self.F(r, c)*r*c + \
            self.G(r, p)*r*p
        # Effectif dse contrôlés
        dc = self.B1*r + self.C1*p - \
            self.C2*c - self.F(r, c)*r*c + \
            self.H(c, p)*c*p - self.phi(t)*c*(r+c+p+q)
        # Effectif des paniqués
        dp = self.B2*r - self.C1*p + self.C2*c - \
            self.G(r, p)*r*p - self.H(c, p)*c*p
        # Comportements du quotidien
        dq = -self.gamma(t)*q*(1-r)
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

        nTypes = nx.get_node_attributes(self.Graph, 'type')
        for i in nodes:
            i4 = i * 4

            # Si le noeud est un noeud de départ on
            # fixe C1 à 0.
            # Nécessité de changer se fonctionnement (appel
            # aux params des noeuds
            if nTypes[i] == "good":
                self.C1 = 0
            else:
                self.C1 = 0.3

            # Couplage linéaire
            # Variables pour le noeud i
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
        # Création du graph (orienté)
        Graph = nx.DiGraph()
        # Ajout liste de liens et noeuds
        Graph.add_nodes_from(nodes)
        Graph.add_edges_from(edges)

        print(nx.info(Graph))

        return Graph

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

    def runSimulation(self, n1, n2, nedges, endT=60, stepT=0.1):
        # nb noeuds
        n1 = 3
        n2 = 2

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

            self.Graph = self.graphCreation(
                [
                    (0, {'type': 'good'}),
                    (1, {'type': 'good'}),
                    (2, {'type': 'good'}),
                    (3, {'type': 'bad'}),
                    (4, {'type': 'bad'})
                ],
                [(0, 3), (1, 3), (2, 4)])

            self.cMat = self.conectivityMatrix(N, self.Graph.edges())

            # PCRn simulation
            # see network()

            # Model solving
            # Conditions initiales
            # Voir si factorisable
            # TODO: à modifier
            X0 = [0 for k in range(4*N)]
            for k in range(N):
                X0[3+4*k] = 1

            # Paramètres temporels
            self.time = np.arange(0, endT, stepT)

            # NB self.network est la fonction de calcul
            orbit = odeint(self.network, X0, self.time, args=(self.Graph,))

            # Toutes les lignes, une colone toutes les 4
            # à partir de la troisième
            # P = orbit[:, 2::4]
            # R = orbit[:, ::4]
            # C = orbit[:, 1::4]

            # sP = np.sum(P, axis=1)
            # sR = np.sum(R, axis=1)
            # sC = np.sum(C, axis=1)

            return orbit

        else:
            print('conditions non valides')
