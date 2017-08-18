import numpy as np
from django.db import transaction
from itertools import chain, groupby
from PCRn.models import Simulation, Node, Edge, Results, Network, Pcr


class dbConnector:

    def __init__(self, data):
        print(__name__)
        # self.dbWrite("a", "b")

        # TODO: remplacer par import
        self.time = np.arange(0, 60, 0.1)

        self.pcrCol = ('B1', 'B2', 'C1', 'C2')

    # Transaction principale
    # Le décorateur rend la transaction atomique
    @transaction.atomic
    def dbWrite(self, nodeList, edgeList, res):

        # 1 Création du network
        # Si on crée un nv réseau
        if True:
            network = self.networkWrite("netname")
        # Sinon on renvoie l'id du précédent
        else:
            network = Network.object.filter(id__exact=id)

        # 2 Création de la simulation
        # On crée une nouvelle simulation liée au réseau
        sim = self.simWrite("cat", 60, 0.1, network)

        # 3 Ajout des noeuds
        # Ajout des nœuds
        nodes = self.nodesWrite(nodeList, network)

        # 4 Ajout des Liens
        # Todo ajouter couplage
        self.edgesWrite(nodes, edgeList)

        # 4 Ajout des res
        # Ajout des résultats
        self.resWirte(sim, nodes, self.time, res)

        # Ajout des liens
        # Vérification de l'existance des fonctions de couplage
        # orgs = Organisation.objects.filter(name__iexact = 'Fjuk inc')
        # if True:
        # else:
        #
        # Si non on la crée
        # Création du lien

    def networkWrite(self, title):
        net = Network(title=title)
        net.save()
        return net

    def _hWrite(self):
        print(__name__)

    def HWrite(self):
        print(__name__)

    def FWrite(self):
        print(__name__)

    def GWrite(self):
        print(__name__)

    def PcrWrite(self, pcrList):

        # Nettoyage de pcrList
        # On supprime du dictionnaire les valeurs non utilisées
        pcrList = [(x[0],
                    {k: v for (k, v) in x[1].items() if k in self.pcrCol})
                   for x in pcrList]
        # On trie la liste des noeuds par leurs paramètres (obligatoire pour
        # groupby)
        pcrList.sort(key=lambda x: tuple([x[1][i] for i in self.pcrCol]))
        # On regroupe les paramètres des noeuds (i.e. enléve les doublons)
        pcrGroup = groupby(pcrList, key=lambda x: x[1])
        # pcrGroup est de la forme [{dic}, grouper]
        # grouper est de la même forme qu'un ind de pcrList (après filtrage)
        # On extrait une liste de la forme [((id_noeuds), {dic fusioné})]
        # la lambda regroupe les id (tj en première position,
        # cf. structure pcrList) dans un tout petit et mignon tuple (🐰)
        pcrGrouped = [(tuple(map(lambda y: y[0], b)), a) for a, b in pcrGroup]

        pcrs = []
        for i in pcrGrouped:
            # On vérifie qu'il n'existe pas déjà une ligne correspondant
            dbline = Pcr.objects.filter(b1__exact=i[1]['B1'],
                                        b2__exact=i[1]['B2'],
                                        c1__exact=i[1]['C1'],
                                        c2__exact=i[1]['C2'])
            # Si ce n'est pas le cas on en crée une nouvelle
            if not dbline:
                # On ajoute une ligne
                pcr = Pcr(b1=i[1]['B1'],
                          b2=i[1]['B2'],
                          c1=i[1]['C1'],
                          c2=i[1]['C2'])
                pcr.save()
            else:
                # Si la ligne existe déjà
                # on sélectione la première occurence
                # on en supprime la structure en liste
                pcr = dbline[:1][0]
            # On exporte sous la forme [(id_noeuds, object_pcr_orm)]
            pcrs.append((i[0], pcr))

        return pcrs

    def nodesWrite(self, nodeList, network):
        """Ajoute une liste de noeuds dans la table nodes

        :param nodeList: Noeuds à ajouter list
        :param network: Un objet network
        :param pcr: Un objet pcr
        :returns:
        :rtype: list

        """

        # Ajout options pcr avant ajour noeuds
        pcr = self.PcrWrite(nodeList)

        nodes = []
        for i in nodeList:
            # on récupère l'objet pcr correspondant à l'id
            # du noeud.
            # pcr est de la forme [((id1, id2), pcr)]
            # si i est dans la liste des ids [0] on renvoie
            # le pcr correspondant
            pcr_id = [p[1] for p in pcr if i[0] in p[0]]
            # On crée un nouveau noeud
            node = Node(network=network, m_id=i[0],
                        pcr=pcr_id[0],
                        comment="NA")
            node.save()
            nodes.append(node)
        return nodes

    def linComWrite(self):
        print(__name__)

    def QuadComWrite(self):
        print(__name__)

    def edgesWrite(self, nodeList, edgeList):
        edges = [Edge(idOrg=nodeList[i[0]],
                      idDest=nodeList[i[1]]) for i in edgeList]
        Edge.objects.bulk_create(edges)

    def simWrite(self, type, duration, timestep, network):
        """Écrit un nouveau tuple dans la table Simulation

        :param type: Type de la simulation str
        :param duration: Durée de la simulation float
        :param timestep:Pas de la simulation
        :param network: Object network (clé étrangère)
        :returns: Object Simulation
        :rtype:

        """
        sim = Simulation(catastrophe_type=type,
                         duration=duration,
                         timestep=timestep,
                         network=network)
        sim.save()
        return sim

    def resWirte(self, sim, nodes, time, res):
        output = chain()
        # Pour chaque ligne
        for r in range(len(res)):
            # On récupère le temps associé
            tvalue = time[r]
            # TODO: Remplacer 4 par N valeurs
            # On groupe les colones par noeuds
            # toutes les 4 valeurs on a un nouveau noeud
            resG = zip(*(iter(res[r]),)*4)
            # On crée une liste de Results pour chaque noeuds
            resOb = [Results(simulation=sim,
                             node=nodes[i],
                             time=tvalue,
                             dr=v[0], dc=v[1], dp=v[2],
                             dq=v[3]) for i, v in enumerate(resG)]
            # On chaine les itérables pour créer une longue chaine de
            # générateurs. Le calcul n'est pas effectué
            output = chain(output, resOb)
        # On entre les données massivement dans la base.
        Results.objects.bulk_create(output)

    def DBRead(self):
        print(__name__)

    def SimulationList(self):
        sl = Simulation.objects.all()
        return sl
