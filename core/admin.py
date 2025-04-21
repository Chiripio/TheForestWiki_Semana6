from django.contrib import admin
from .models import Usuario, RolUsuario, SeccionForo, Tema, Comentario, Valoracion

# 🧑‍💻 Personalización del panel de administración para el modelo Usuario
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nombre_completo', 'rol')
    search_fields = ('username', 'email', 'nombre', 'apellido_paterno', 'apellido_materno')
    list_filter = ('rol',)

    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}"
    nombre_completo.short_description = 'Nombre completo'

# 🧱 Personalización del panel para RolUsuario
class RolUsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# 🧵 Registro del resto de los modelos del foro
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(RolUsuario, RolUsuarioAdmin)
admin.site.register(SeccionForo)
admin.site.register(Tema)
admin.site.register(Comentario)
admin.site.register(Valoracion)