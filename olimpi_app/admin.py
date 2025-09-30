from django.contrib import admin

# Register your models here.
from .models import Equipos, Participantes, Arbitros, Disciplinas, Pistas, Encuentros, EncuentrosEquipos

admin.site.register(Equipos)
admin.site.register(Arbitros)
admin.site.register(Disciplinas)
admin.site.register(Participantes)
admin.site.register(Pistas)


# Inline para EncuentrosEquipos dentro de Encuentros
class EncuentrosEquiposInline(admin.TabularInline):
    model = EncuentrosEquipos

    def get_extra(self, request, obj=None, **kwargs):
        # Si estamos editando un encuentro, usamos la regla de la disciplina
        if obj and obj.idDis:
            return obj.idDis.regla
        # Si no hay objeto (nuevo), por defecto 2
        return 2

# Admin personalizado para Encuentros
class EncuentrosAdmin(admin.ModelAdmin):
    inlines = [EncuentrosEquiposInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        encuentro = form.instance
        disciplina = encuentro.idDis
        equipos_count = encuentro.encuentrosequipos_set.count()
        min_equipos = disciplina.min_equipos
        max_equipos = disciplina.max_equipos
        if equipos_count < min_equipos or equipos_count > max_equipos:
            from django.core.exceptions import ValidationError
            raise ValidationError(f"El número de equipos debe estar entre {min_equipos} y {max_equipos} para la disciplina {disciplina.nomDis}.")

admin.site.register(Encuentros, EncuentrosAdmin)
admin.site.register(EncuentrosEquipos)

