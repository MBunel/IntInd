import numpy as np
from django.db import transaction
from itertools import chain
from PCRn.models import Simulation, Node, Edge, Results, Network


class dbConnector:

    def __init__(self, data):
        print(__name__)
        # self.dbWrite("a", "b")

    # Transaction principale
    @transaction.atomic
    def dbWrite(self, nodeList, res):

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
        nodes = self.nodesWrite(nodeList, network, "pcr")

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

    def PcrWrite(self):
        print(__name__)

    def nodesWrite(self, nodeList, network, pcr):
        """Ajoute une liste de noeuds dans la table nodes

        :param nodeList: Noeuds à ajouter list
        :param network: Un objet network
        :param pcr: Un objet pcr
        :returns:
        :rtype: list

        """
        nodes = []
        for i in nodeList:
            node = Node(network=network, m_id=i, comment="NA")
            node.save()
            nodes.append(node)
        return nodes

    def linComWrite(self):
        print(__name__)

    def QuadComWrite(self):
        print(__name__)

    def edgesWrite(self, sim, nodeList, edgeList):
        edges = [Edge(idA=0, idB=1) for i in edgeList]
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
