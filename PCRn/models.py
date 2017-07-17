from django.db import models

# Create your models here.


class Simulation(models.Model):
    timestamp = models.TimeField()


class Parameters(models.Model):
    simulation = models.ForeignKey(Simulation)
    parameter = models.CharField(blank=False, max_length=20)
    value = models.FloatField(blank=False)


class Node(models.Model):
    simulation = models.ForeignKey(Simulation)


class Link(models.Model):
    simulation = models.ForeignKey(Simulation)
    idA = models.ForeignKey(Node, related_name="idA")
    idB = models.ForeignKey(Node, related_name="idB")


class Results(models.Model):
    simulation = models.ForeignKey(Simulation)
    time = models.FloatField(blank=False)
    variable = models.CharField(blank=False, max_length=20)
    value = models.FloatField(blank=False)
