from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import Equipos, Participantes, Arbitros, Disciplinas, Pistas, Encuentros, EncuentrosEquipos

admin.site.register(Equipos)
admin.site.register(Arbitros)
admin.site.register(Disciplinas)
admin.site.register(Participantes)
admin.site.register(Pistas)

class EncuentrosEquiposInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if hasattr(self, 'instance') and self.instance.idDis:
            # Contar equipos no eliminados
            equipos_count = 0
            for form in self.forms:
                if (form.cleaned_data and 
                    not form.cleaned_data.get('DELETE', False) and 
                    form.cleaned_data.get('equipo')):
                    equipos_count += 1
            
            # Validar
            min_equipos = self.instance.idDis.min_equipos
            max_equipos = self.instance.idDis.max_equipos
            
            if equipos_count < min_equipos:
                raise ValidationError(
                    f'Se requieren al menos {min_equipos} equipos para la disciplina {self.instance.idDis.nomDis}. '
                    f'Actualmente tiene {equipos_count}. Agregue más equipos.'
                )
            if equipos_count > max_equipos:
                raise ValidationError(
                    f'Se permiten máximo {max_equipos} equipos para la disciplina {self.instance.idDis.nomDis}. '
                    f'Actualmente tiene {equipos_count}. Elimine algunos equipos.'
                )

class EncuentrosEquiposInline(admin.TabularInline):
    model = EncuentrosEquipos
    formset = EncuentrosEquiposInlineFormSet
    extra = 1  # Muestra 1 formulario vacío por defecto

class EncuentrosAdmin(admin.ModelAdmin):
    inlines = [EncuentrosEquiposInline]
    
    def save_related(self, request, form, formsets, change):
        """Validación adicional después de guardar los equipos"""
        super().save_related(request, form, formsets, change)
        # Re-validar después de guardar los equipos relacionados
        instance = form.instance
        if instance.idDis:
            equipos_count = instance.encuentrosequipos_set.count()
            if equipos_count < instance.idDis.min_equipos:
                raise ValidationError(
                    f'ERROR: Después de guardar, el encuentro tiene {equipos_count} equipos, '
                    f'pero se requieren al menos {instance.idDis.min_equipos} para {instance.idDis.nomDis}.'
                )

admin.site.register(Encuentros, EncuentrosAdmin)
admin.site.register(EncuentrosEquipos)