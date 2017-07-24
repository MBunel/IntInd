from django.shortcuts import render, HttpResponseRedirect
from datetime import date


# Create your views here.
def index(request):
    year = date.today().year
    if year != 2017:
        year = '2017–{}'.format(year)

    return render(request,
                  'Acc/index.xhtml',
                  {'projectName': 'projet', 'year': year})


def aprp(request):
    return render(request,
                  'Acc/apropos.xhtml',
                  {'projectName': 'projet'})


def rickroll(request):
    return HttpResponseRedirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
