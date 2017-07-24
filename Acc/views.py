from django.shortcuts import render, HttpResponseRedirect


# Create your views here.
def index(request):
    return render(request,
                  'Acc/index.xhtml',
                  {'projectName': 'projet'})


def aprp(request):
    return render(request,
                  'Acc/apropos.xhtml',
                  {'projectName': 'projet'})


def rickroll(request):
    return HttpResponseRedirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
