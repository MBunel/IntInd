from django.shortcuts import render
from django.http import JsonResponse
import json

from PCRn.PcrModel import Model


# Create your views here.
def index(request):
    return render(request,
                  'PCRn/index.xhtml',
                  {'projectName': 'Nom projet'})


def runSimulation(request):
    """ Fonction d'appel modèle"""

    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))

        nodes = [n['_l_id'] for n in data['nodes']]
        edges = [tuple(e['idP']) for e in data['edges']]

        model = Model()
        model.graphCreation(nodes, edges)
        model.runSimulation(1,2,3)

        return JsonResponse({'nodes': data['nodes'], 'links': data['edges']})
