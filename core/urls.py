from django.urls import path
from . import views
from core import views

urlpatterns = [
    # Página principal
    path('', views.menuprincipal, name='menuprincipal'),

    # Navegación temática
    path('foro/', views.foro, name='foro'),
    path('lugares/', views.lugares, name='lugares'),
    path('animales/', views.animales, name='animales'),
    path('armas/', views.armas, name='armas'),
    path('construcciones/', views.construcciones, name='construcciones'),
    path('consumibles/', views.consumibles, name='consumibles'),
    path('enemigos/', views.enemigos, name='enemigos'),
    path('flora/', views.flora, name='flora'),
    path('historia/', views.historia, name='historia'),
    path('direccion/', views.direccion, name='direccion'),
    path('logros/', views.logros, name='logros'),

    # Usuario
    path('micuenta/', views.micuenta, name='micuenta'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('recuperar/', views.recuperar_contraseña, name='recuperar'),
    path('iniciar/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar/', views.cerrar_sesion, name='cerrar_sesion'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('eliminar_usuario/', views.eliminar_usuario, name='eliminar_usuario'),

    # Vista de administrador
    path('admin_visual/', views.admin_visual, name='admin_visual'),

    # 🧵 Foro: secciones, temas, comentarios, valoraciones
    path('secciones/', views.lista_secciones, name='lista_secciones'),
    path('seccion/<int:seccion_id>/', views.temas_por_seccion, name='temas_por_seccion'),
    path('tema/nuevo/', views.crear_tema, name='crear_tema'),
    path('tema/<int:tema_id>/comentar/', views.comentar_tema, name='comentar_tema'),
    path('tema/<int:tema_id>/valorar/', views.valorar_tema, name='valorar_tema'),
    path('comentario/<int:comentario_id>/editar/', views.editar_comentario, name='editar_comentario'),
    

    # API
    path('api/temas/', views.api_temas, name='api_temas'),

    # Mis temas 
    path('mis-temas/', views.mis_temas, name='mis_temas'),

    # Favoritos
    path('tema/<int:tema_id>/favorito/', views.agregar_quitar_favorito, name='agregar_quitar_favorito'),

    # Baneo
    path('tema/<int:tema_id>/banear/', views.banear_tema, name='banear_tema'),
    path('comentario/<int:comentario_id>/banear/', views.banear_comentario, name='banear_comentario'),

    # Ver favoritos
    path('mis-favoritos/', views.mis_favoritos, name='mis_favoritos'),

    # Eliminar (solo vía POST)
    path('comentario/<int:comentario_id>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),
    path('seccion/<int:seccion_id>/eliminar/', views.eliminar_seccion, name='eliminar_seccion'),
    path('tema/<int:tema_id>/eliminar/', views.eliminar_tema, name='eliminar_tema'),

    path('temas_api/', views.temas_api_html, name='temas_api_html'),
]
