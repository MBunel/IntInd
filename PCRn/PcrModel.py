import numpy as np
from scipy.integrate import odeint
import networkx as nx

from functools import partialmethod, partial


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
            node['phi'](t) * c * (r + c + p + q)

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

            Xpcr = y[i4:i4+4]

            zipped = []
            # if True:
            # Calcul du couplage linéaire
            l = self.linearCoupling(N, i, y)
            zipped.append(l)
            # if True:
            # Calcul couplage quadratique
            #     q = quadraticCoupling()
            #     zipped.append(q)
            # calcul modèle pcr
            pcrRes = self.PCR(Xpcr, t, node)
            zipped.append(pcrRes)

            # On ajoute les valeurs calculées avec les fonctions de
            # couplage avec les valeurs calculées par le modèle pcr
            temp = [sum(x) for x in zip(*zipped)]
            # Concaténation des résultats pour ce noeud, avec les
            # résultats précédents
            dX = dX + temp

        return dX

    def linearCoupling(self, N, i, y):
        a, b, c = 0, 0, 0

        # Multiplier par edges params
        for j in range(N):
            a += self.cMat[i][j]*y[4*j] * self.eps
            b += self.cMat[i][j]*y[1+4*j] * self.eps
            c += self.cMat[i][j]*y[2+4*j] * self.eps

        return [a, b, c, 0]

    def quadraticCoupling(self, N, i, y, Xpcr):

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

    def adjacencyMatrix(self, N: int, edges: list) -> np.array:
        # Adjacencyy matrix where diagonal terms are zeros

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
            if i != j:
                A[j][i] = 1
            else:
                raise ValueError("Lien %s non conforme, i = j" % edge)
        return A

    def conectivityMatrix(self, N: int, edges: list) -> np.array:
        # connectivity matrix (couplage linéaire)

        A = self.adjacencyMatrix(N, edges)

        # Comptabilise le nombre de connections pour chaque
        # colone (et donc noeud)
        for i in range(N):
            A[i][i] = -sum(A[j][i] for j in range(N) if j != i)

        return A

    def quadraticMatrix(self, N: int, edges: list) -> np.array:
        """Génére une matrice quadratique

        """
        # On définit une matrice de dimension 4, dont les deux
        # premières dimensions correspondent au noeuds. Les
        # dimensions suivantes correspondent à la matrice de
        # couplage (3x3) définie à 0 de base
        A = np.full(shape=(N, N, 3, 3),
                    fill_value=np.zeros((3, 3), dtype=int))
        # Pour chaque lien
        for edge in edges:
            j, i = edge
            # On vérifie qu'il ne s'agit pas d'un lien
            # d'un noeud à lui même
            if i != j:
                # On ajoute la matrice renvoyée par l'ajax
                A[j][i] = self.quad
                # A[j][i] = edge.quad
            else:
                raise ValueError("Lien %s non conforme, i = j" % edge)

        return A

    def runSimulation(self, endT=60, stepT=0.1):

        # centralisation params function, à enlever
        paramsH = {'Mu1': 0.1, 'Mu2': 0.1},
        paramsF = {'Al1': 0.1, 'Al2': 0.1}
        paramsG = {'Del1': 0.1, 'Del2': 0.1}

        nF = NodeFunction()

        # Création du graphe
        # Valeurs fixées, a remplacer par un passage
        # des params par l'ajax
        self.Graph = self.graphCreation(
            [
                (0, {'B1': 0.5, 'B2': 0.5, 'C1': 0,
                     'C2': 0.2, 'S1': 0, 'S2': 0,
                     'H': paramsH, 'F': paramsF, 'G': paramsG,
                     'phi': nF.phi}),
                (1, {'B1': 0.5, 'B2': 0.5, 'C1': 0,
                     'C2': 0.2, 'S1': 0, 'S2': 0,
                     'H': paramsH, 'F': paramsF, 'G': paramsG,
                     'phi': nF.phi}),
                (2, {'B1': 0.2, 'B2': 0.5, 'C1': 0,
                     'C2': 0.2, 'S1': 0, 'S2': 0,
                     'H': paramsH, 'F': paramsF, 'G': paramsG,
                     'phi': nF.phi}),
                (3, {'B1': 0.5, 'B2': 0.4, 'C1': 0.3,
                     'C2': 0.2, 'S1': 0, 'S2': 0,
                     'H': paramsH, 'F': paramsF, 'G': paramsG,
                     'phi': nF.phi}),
                (4, {'B1': 0.5, 'B2': 0.4, 'C1': 0.3,
                     'C2': 0.2, 'S1': 0, 'S2': 0,
                     'H': paramsH, 'F': paramsF, 'G': paramsG,
                     'phi': nF.phi})
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


class NodeFunction:
    """Génére les fonctions du système pour chaque noeud
    """
    def __init__(self, *args):
        """
        Fonction d'initialisation
        """
        super(NodeFunction, self).__init__()
        self.args = args

        # Params par def des fonctions h
        self.pp = {'smin': 1, 'smax': 50, 'hmin': 0, 'hmax': 1}
        self.pg = {'smin': 1, 'smax': 3, 'hmin': 0, 'hmax': 1}
        self.hp = {'smin': 0, 'smax': 1, 'hmin': 1, 'hmax': 0}

        # Définition phi et gamma
        self.phi = partial(self.h, **self.pp)
        self.gamma = partial(self.h, **self.pg)

        self.F = self.genFun('F', (0.1, 0.1), self.hp)
        self.G = self.genFun('G', (0.1, 0.1), self.hp)
        self.H = self.genFun('H', (0.1, 0.1), self.hp)

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

    def _f(self, fun, cons1, cons2, var1, var2):
        h1 = var1 / (var2 + 0.01)
        h2 = var2 / (var1 + 0.01)

        rvalue = cons1 * fun(h1) + \
            cons2 * fun(h2)
        return rvalue

    def genFun(self, fType, fParams, hParams):
        # Création d'un swich
        # test de la valeur de type + opposé
        # des constantes en fonction de la fonction
        _swich = {
            'F': lambda x, y: (-x, y),
            'G': lambda x, y: (-x, y),
            'H': lambda x, y: (x, -y)
        }

        try:
            cons1, cons2 = _swich[fType](*fParams)
        except KeyError:
            # Si la clé n'est pas dans le swich
            print("%s non défint" % fType)

        # Définition de la fonction h personalisée
        hVal = partial(self.h, **hParams)
        # Définition de la fonction f personalisée
        _fVal = partial(self._f, hVal, cons1, cons2)

        def fun(r, p):
            rvalue = _fVal(r, p)
            return rvalue

        return fun

    def getParams(self):
        print('hey')
