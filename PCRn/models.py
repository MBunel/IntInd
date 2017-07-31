from django.db import models

# Create your models here.


class Network(models.Model):
    title = models.CharField(blank=False, max_length=20)


class Simulation(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    catastrophe_type = models.CharField(max_length=5)
    duration = models.FloatField(blank=False)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)


class Global_Result(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    time = models.FloatField(blank=False)
    dr = models.FloatField(blank=False)
    dc = models.FloatField(blank=False)
    dp = models.FloatField(blank=False)
    dq = models.FloatField(blank=False)

    class Meta:
        db_table = 'Global_Result'
        managed = False


class Function_h(models.Model):
    smin = models.FloatField(blank=False)
    smax = models.FloatField(blank=False)
    hmin = models.FloatField(blank=False)
    hmax = models.FloatField(blank=False)


class FunctionH(models.Model):
    h1 = models.ForeignKey(Function_h,
                           related_name="h1",
                           on_delete=models.CASCADE)
    h2 = models.ForeignKey(Function_h,
                           related_name="h2",
                           on_delete=models.CASCADE)
    mu1 = models.FloatField(blank=False)
    mu2 = models.FloatField(blank=False)


class FunctionG(models.Model):
    g1 = models.ForeignKey(Function_h,
                           related_name="g1",
                           on_delete=models.CASCADE)
    g2 = models.ForeignKey(Function_h,
                           related_name="g2",
                           on_delete=models.CASCADE)
    delta1 = models.FloatField(blank=False)
    delta2 = models.FloatField(blank=False)


class FunctionF(models.Model):
    f1 = models.ForeignKey(Function_h,
                           related_name="f1",
                           on_delete=models.CASCADE)
    f2 = models.ForeignKey(Function_h,
                           related_name="f2",
                           on_delete=models.CASCADE)
    alpha1 = models.FloatField(blank=False)
    alpha2 = models.FloatField(blank=False)


class Pcr(models.Model):
    b1 = models.FloatField(blank=False)
    b2 = models.FloatField(blank=False)
    s1 = models.FloatField(blank=False)
    s2 = models.FloatField(blank=False)
    c1 = models.FloatField(blank=False)
    c2 = models.FloatField(blank=False)
    Phi = models.ForeignKey(Function_h,
                            related_name="phi",
                            on_delete=models.CASCADE)
    Gamma = models.ForeignKey(Function_h,
                              related_name="gamma",
                              on_delete=models.CASCADE)
    F = models.ForeignKey(FunctionF,
                          on_delete=models.CASCADE)
    H = models.ForeignKey(FunctionG,
                          on_delete=models.CASCADE)
    H = models.ForeignKey(FunctionH,
                          on_delete=models.CASCADE)


class Node(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    pcr = models.ForeignKey(Pcr, on_delete=models.CASCADE)
    m_id = models.IntegerField()
    # geom = models.PointField()
    comment = models.CharField(max_length=150, blank=True)


class Linear_Coupling(models.Model):
    r = models.FloatField(blank=False)
    c = models.FloatField(blank=False)
    p = models.FloatField(blank=False)
    q = models.FloatField(blank=False)
    b = models.FloatField(blank=False)


class Quadratic_Coupling(models.Model):
    rc = models.FloatField(blank=False)
    rp = models.FloatField(blank=False)
    cp = models.FloatField(blank=False)
    cr = models.FloatField(blank=False)
    pr = models.FloatField(blank=False)
    pc = models.FloatField(blank=False)


class Edge(models.Model):
    edgeInd = models.IntegerField(default=-1)
    comment = models.CharField(max_length=150, blank=True)
    idOrg = models.ForeignKey(Node,
                              related_name="idOrg",
                              on_delete=models.CASCADE)
    idDest = models.ForeignKey(Node,
                               related_name="idDest",
                               on_delete=models.CASCADE)
    idLinearCp = models.ForeignKey(Linear_Coupling,
                                   related_name="idLinearCp",
                                   on_delete=models.CASCADE)
    idQuadraCp = models.ForeignKey(Quadratic_Coupling,
                                   related_name="idQuadraCp",
                                   on_delete=models.CASCADE)


class Results(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    time = models.FloatField(blank=False)
    dr = models.FloatField(blank=False)
    dc = models.FloatField(blank=False)
    dp = models.FloatField(blank=False)
    dq = models.FloatField(blank=False)
