from django.contrib import admin

# Register your models here.


from .models import EquiposEncuentros, Equipo, Participante, Pista, Disciplina, Arbitro, Encuentro  


admin.site.register(EquiposEncuentros)
admin.site.register(Equipo)
admin.site.register(Participante)
admin.site.register(Pista)
admin.site.register(Disciplina)
admin.site.register(Arbitro)
admin.site.register(Encuentro)


