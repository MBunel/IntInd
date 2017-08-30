from django.shortcuts import render


# Create your views here.
def index(request):
    print('a')


def runSimulation(request):
    if request.method == 'POST':
        print('aa')
