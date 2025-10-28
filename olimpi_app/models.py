from django.db import models

class EncuentrosEquipos(models.Model):
    idEnc = models.ForeignKey('Encuentros', on_delete=models.CASCADE)
    equipo = models.ForeignKey('Equipos', on_delete=models.CASCADE)
    puntos = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'ENCUENTROS_EQUIPOS'
        unique_together = (('idEnc', 'equipo'),)

    def __str__(self):
        return f"Encuentro {self.idEnc.idEnc} - Equipo {self.equipo.nomEqu} ({self.puntos} puntos)"


class Equipos(models.Model):
    idEqu = models.AutoField(primary_key=True)
    oliEqu = models.CharField(max_length=1, choices=[('S', 'S'), ('N', 'N')])
    nomEqu = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'EQUIPOS'
    
    def __str__(self):
        return f"Equipo {self.nomEqu}"


class Participantes(models.Model):
    idPar = models.AutoField(primary_key=True)
    curPar = models.CharField(max_length=2)
    nomPar = models.CharField(max_length=75)
    neaePar = models.CharField(max_length=1)
    
    class Meta:
        db_table = 'PARTICIPANTES'
    
    def __str__(self):
        return self.nomPar


class Disciplinas(models.Model):
    idDis = models.AutoField(primary_key=True)
    nomDis = models.CharField(max_length=50)
    min_equipos = models.PositiveIntegerField(default=2, help_text="Número mínimo de equipos por disciplina")
    max_equipos = models.PositiveIntegerField(default=4, help_text="Número máximo de equipos por disciplina")

    class Meta:
        db_table = 'DISCIPLINAS'

    def __str__(self):
        return self.nomDis


class Pistas(models.Model):
    idPis = models.AutoField(primary_key=True)
    idPisPadre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    nomPis = models.CharField(max_length=25)
    cubPis = models.CharField(max_length=1, choices=[('S', 'S'), ('N', 'N')])
    
    class Meta:
        db_table = 'PISTAS'
    
    def __str__(self):
        return self.nomPis


class Arbitros(models.Model):
    idArb = models.AutoField(primary_key=True)
    nomArb = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'ARBITROS'
    
    def __str__(self):
        return self.nomArb


from django.db import models
from django.core.exceptions import ValidationError

# ... tus otros modelos igual ...

class Encuentros(models.Model):
    ESTADOS = [
        ('P', 'Pendiente'),
        ('E', 'En curso'),
        ('F', 'Finalizado'),
        ('C', 'Cancelado'),
    ]
    
    idEnc = models.AutoField(primary_key=True)
    estEnc = models.CharField(max_length=1, choices=ESTADOS)
    finiEnc = models.DateTimeField()
    ffinEnc = models.DateTimeField()
    idPis = models.ForeignKey(Pistas, on_delete=models.CASCADE)
    idDis = models.ForeignKey(Disciplinas, on_delete=models.CASCADE)
    idEqu = models.ManyToManyField(Equipos, through='EncuentrosEquipos')
    idArb = models.ForeignKey(Arbitros, on_delete=models.CASCADE)

    def clean(self):
        """Validación a nivel de modelo"""
        # Validación de fechas
        if self.finiEnc and self.ffinEnc and self.finiEnc >= self.ffinEnc:
            raise ValidationError({
                'ffinEnc': 'La fecha de fin debe ser posterior a la fecha de inicio.'
            })
        
        # Validación de equipos (solo si el objeto ya existe)
        if self.pk and self.idDis:
            equipos_count = self.encuentrosequipos_set.count()
            self._validar_cantidad_equipos(equipos_count)

    def _validar_cantidad_equipos(self, equipos_count):
        """Método auxiliar para validar cantidad de equipos"""
        if self.idDis:
            min_equipos = self.idDis.min_equipos
            max_equipos = self.idDis.max_equipos
            
            if equipos_count < min_equipos:
                raise ValidationError(
                    f'Se requieren al menos {min_equipos} equipos para la disciplina {self.idDis.nomDis}. '
                    f'Actualmente tiene {equipos_count}.'
                )
            if equipos_count > max_equipos:
                raise ValidationError(
                    f'Se permiten máximo {max_equipos} equipos para la disciplina {self.idDis.nomDis}. '
                    f'Actualmente tiene {equipos_count}.'
                )

    def save(self, *args, **kwargs):
        # Forzar la validación al guardar
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'ENCUENTROS'
        constraints = [
            models.CheckConstraint(
                check=models.Q(finiEnc__lt=models.F('ffinEnc')),
                name='check_fecha_fin_posterior'
            )
        ]
    
    def __str__(self):
        return f"Encuentro {self.finiEnc} - {self.idDis.nomDis}"