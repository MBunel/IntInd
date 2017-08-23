from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^runSim$', views.runSimulation),
    url(r'^getSims$', views.getSimulations),
    url(r'^getSimParams$', views.getSimulationParameters),
    url(r'^getSimData$', views.getSimulationData)
]
