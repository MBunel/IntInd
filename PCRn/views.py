from django.shortcuts import render
from django.http import JsonResponse
from dbAcess import dbConnector
import json

from PCRn.PcrModel import Model


# Create your views here.
def index(request):
    return render(request,
                  'PCRn/index.xhtml',
                  {'projectName': 'Nom projet'},
                  content_type='application/xhtml+xml')


def runSimulation(request):
    """ Fonction d'appel modèle"""

    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))

        # Extraction des noeuds du corps de la requête sous la
        # forme d'un tuple (id, d), avec un d un dictionnaire
        # contenant l'ensemble des paramètres envoyés par la
        # requête POST
        nodes = [(i, v) for i, v in enumerate(data['nodes'])]
        # TODO: à modifier pour rendre en compte les paramètres
        edges = [tuple(e['idP']) for e in data['edges']]

        model = Model()
        model.graphCreation(nodes, edges)
        # model.runSimulation(1,2,3)
        return JsonResponse({'nodes': data['nodes'], 'links': data['edges']})


def getSimulations(request):
    """"Renvoie une liste de simulations"""
    if request.method == 'GET':
        conn = dbConnector()
        sim = conn.SimulationList()

        return JsonResponse(sim)


def getSimulationData(request):
    """Récupère et renvoie les données d'une simulation"""
    if request.method == 'GET':
        print(__name__)
        # on renvoie les résultats
