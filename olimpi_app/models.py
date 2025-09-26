# olimpi_app/models.py
from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator


#---------------------------
# EquiposEncuentros
#---------------------------

class EquiposEncuentros(models.Model):
    idEquEnc = models.BigAutoField(primary_key=True)
    idEqu = models.ForeignKey('Equipo', on_delete=models.CASCADE)
    idEnc = models.ForeignKey('Encuentro', on_delete=models.CASCADE)
    puntosEquEnc = models.IntegerField()

    def __str__(self):
        return f"EquipoEncuentro {self.idEquEnc}"

# ---------------------------
# Equipos
# ---------------------------
class Equipo(models.Model):
    OLI_CHOICES = [
        ('S', 'Sí'),
        ('N', 'No'),
    ]

    idEqu = models.BigAutoField(primary_key=True)  # number → BigAutoField
    oliEqu = models.CharField(max_length=1, choices=OLI_CHOICES)
    nomEqu = models.CharField(max_length=50)
    def __str__(self):
        return f"Equipo {self.idEqu}"

# ---------------------------
# Participantes
# ---------------------------
class Participante(models.Model):
    NEAE_CHOICES = [
        ('S', 'Sí'),
        ('N', 'No'),
    ]

    idPar = models.BigAutoField(primary_key=True)
    curPar = models.CharField(max_length=2)
    cenPar = models.CharField(max_length=50)
    nomPar = models.CharField(max_length=75)
    neaePar = models.CharField(max_length=1, choices=NEAE_CHOICES)
    corPar = models.CharField(max_length=100)

    def __str__(self):
        return self.nomPar

# ---------------------------
# Pistas
# ---------------------------

class Pista(models.Model):
    CUB_CHOICES = [
        ('S', 'Sí'),
        ('N', 'No'),
    ]

    idPis = models.BigAutoField(primary_key=True)
    idPisPadre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_pistas'
    )
    nomPis = models.CharField(max_length=25)
    cubPis = models.CharField(max_length=1, choices=CUB_CHOICES)

    def __str__(self):
        return self.nomPis

# ---------------------------
# Disciplinas
# ---------------------------
class Disciplina(models.Model):
    idDis = models.BigAutoField(primary_key=True)
    nomDis = models.CharField(max_length=50)

    def __str__(self):
        return self.nomDis

# ---------------------------
# Árbitros
# ---------------------------
class Arbitro(models.Model):
    idArb = models.BigAutoField(primary_key=True)
    nomArb = models.CharField(max_length=50)

    def __str__(self):
        return self.nomArb

# ---------------------------
# Encuentros
# ---------------------------
class Encuentro(models.Model):
    ESTADO_CHOICES = [
        ('F', 'Finalizado'),
        ('E', 'En curso'),
        ('O', 'Otro'),
    ]

    idEnc = models.BigAutoField(primary_key=True)
    estEnc = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    finiEnc = models.DateField()
    ffinEnc = models.DateField()
    idPis = models.ForeignKey(Pista, on_delete=models.CASCADE)
    idDis = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    idArb = models.ForeignKey(Arbitro, on_delete=models.CASCADE)


    def __str__(self):
        return f"Encuentro {self.idEnc}"


