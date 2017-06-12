from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, 'PCRn/index.xhtml')


def runSimulation(request):
    """ Fonction d'appel modèle"""

    if request.method == 'GET':
        a = request.GET.get("x", "")
        b = request.GET.get("y", "")
        c = request.GET.get("z", "")

        return JsonResponse({'test': a, 'test1': b, 'test2': c})
