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

        model = Model()

        return JsonResponse({'nodes': data['nodes'], 'links': data['links']})
