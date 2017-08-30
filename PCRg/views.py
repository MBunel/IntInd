from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request,
                  'PCRg/index.xhtml',
                  {'projectname': 'Nom projet'},
                  content_type='application/xhtml+xml')


def runSimulation(request):
    if request.method == 'POST':
        print('aa')
