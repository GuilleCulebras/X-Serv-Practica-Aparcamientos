from django.contrib import admin
from aparcamientos.models import Aparcamiento, Comentario, Seleccionado, CSS
# Register your models here.

admin.site.register(Aparcamiento)
admin.site.register(Comentario)
admin.site.register(Seleccionado)
admin.site.register(CSS)
