from django.db import models

# Create your models here.


class Simulation(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)


class Parameters(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    parameter = models.CharField(blank=False, max_length=20)
    value = models.FloatField(blank=False)


class Node(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    m_id = models.IntegerField()


class Edge(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    idA = models.ForeignKey(Node, related_name="idA",
                            on_delete=models.CASCADE)
    idB = models.ForeignKey(Node, related_name="idB",
                            on_delete=models.CASCADE)


class Results(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    time = models.FloatField(blank=False)
    dr = models.FloatField(blank=False)
    dc = models.FloatField(blank=False)
    dp = models.FloatField(blank=False)
    dq = models.FloatField(blank=False)
