from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from collections import defaultdict

from core.forms import FormularioTema
from core.models import Usuario, RolUsuario, Tema, Comentario, Valoracion, SeccionForo
from core.forms import (
    FormularioRegistro, FormularioLogin, FormularioPerfil,
    FormularioTema, FormularioComentario, FormularioValoracion
)

# -------------------------
# VISTAS DE NAVEGACIÓN
# -------------------------
def menuprincipal(request):
    return render(request, 'core/menuprincipal_wiki.html')

def foro(request):
    temas = Tema.objects.filter(activo=True).select_related('usuario', 'seccion').order_by('-fecha_creacion')[:5]
    comentarios = Comentario.objects.filter(
        activo=True,
        id_comentario__isnull=False,
        tema__isnull=False,
        tema__id_tema__isnull=False
    ).select_related('usuario', 'tema', 'tema__seccion').order_by('-fecha_comentario')[:5]
    
    form = FormularioTema() if request.user.is_authenticated else None
    valoraciones_usuario = defaultdict(int)
    if request.user.is_authenticated:
        valoraciones = Valoracion.objects.filter(usuario=request.user).select_related('tema')
        for v in valoraciones:
            valoraciones_usuario[v.tema.id_tema] = v.valor

    return render(request, 'core/forowiki.html', {
        'form': form,
        'temas': temas,
        'comentarios': comentarios,
        'valoraciones_usuario': valoraciones_usuario
    })

def lugares(request):
    return render(request, 'core/Lugarestf.html')

def animales(request):
    return render(request, 'core/animales.html')

def armas(request):
    return render(request, 'core/Armas.html')

def construcciones(request):
    return render(request, 'core/construcciones.html')

def consumibles(request):
    return render(request, 'core/consumibles.html')

def enemigos(request):
    return render(request, 'core/Enemigos.html')

def flora(request):
    return render(request, 'core/flora.html')

def historia(request):
    return render(request, 'core/historia.html')

def logros(request):
    return render(request, 'core/Logros.html')

def direccion(request):
    return render(request, 'core/direccion.html')

def temas_api_html(request):
    return render(request, 'core/temas_api.html')

# -------------------------
# USUARIO - Registro e inicio de sesión
# -------------------------
def registrarse(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ ¡Registro exitoso! Ahora puedes iniciar sesión.")
            return redirect('iniciar_sesion')
        else:
            messages.error(request, "❌ Por favor corrige los errores del formulario.")
    else:
        form = FormularioRegistro()
    return render(request, 'core/registrase_wiki.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = FormularioLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = authenticate(request, username=username, password=password)
            if usuario:
                # Recarga desde base de datos para asegurar que el rol se actualiza
                usuario_refrescado = Usuario.objects.select_related('rol').get(pk=usuario.pk)
                login(request, usuario_refrescado)
                request.session['usuario_id'] = usuario_refrescado.id_usuario
                request.session['usuario_nombre'] = usuario_refrescado.nombre
                messages.success(request, f"✅ ¡Bienvenido, {usuario_refrescado.username}!")
                if usuario_refrescado.rol and usuario_refrescado.rol.nombre.lower() == 'administrador':
                    return redirect('admin_visual')
                return redirect('menuprincipal')
            else:
                messages.error(request, '❌ Usuario o contraseña incorrectos.')
        else:
            messages.error(request, "❌ Formulario inválido.")
    else:
        form = FormularioLogin()
    return render(request, 'core/inicio_sesion_wiki.html', {'form': form})

@login_required
def micuenta(request):
    Usuario = get_user_model()
    usuario_actualizado = Usuario.objects.select_related('rol').get(pk=request.user.pk)
    print(f"Rol directo en micuenta: {usuario_actualizado.rol.nombre}")
    temas_favoritos = usuario_actualizado.favoritos.all()
    return render(request, 'core/micuentatf.html', {'temas_favoritos': temas_favoritos, 'usuario': usuario_actualizado})

@login_required
def cerrar_sesion(request):
    logout(request)
    messages.success(request, "✅ Has cerrado sesión.")
    return redirect('iniciar_sesion')

# -------------------------
# EDITAR PERFIL
# -------------------------
@login_required
def editar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        form = FormularioPerfil(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, usuario)
            messages.success(request, "✅ Perfil actualizado correctamente.")
            return redirect('micuenta')
        else:
            messages.error(request, "❌ Por favor corrige los errores del formulario.")
    else:
        form = FormularioPerfil(instance=usuario)
    return render(request, 'core/editar_perfil.html', {'form': form})

# -------------------------
# ELIMINAR USUARIO
# -------------------------
@login_required
def eliminar_usuario(request):
    if request.method == 'POST':
        try:
            usuario = request.user
            usuario.delete()
            logout(request)
            messages.success(request, '✅ Tu cuenta ha sido eliminada correctamente.')
            return redirect('menuprincipal')
        except Exception as e:
            messages.error(request, f'❌ Error al eliminar la cuenta: {str(e)}')
            return redirect('editar_perfil')
    return redirect('editar_perfil')

# -------------------------
# VISTA DE ADMINISTRADOR
# -------------------------
@login_required
def admin_visual(request):
    Usuario = get_user_model()
    usuario_actualizado = Usuario.objects.get(pk=request.user.pk)
    if usuario_actualizado.rol and usuario_actualizado.rol.nombre != 'Administrador':
        messages.warning(request, '⚠️ Solo los administradores pueden acceder aquí.')
        return redirect('menuprincipal')
    
    # ✅ Manejo del formulario POST para crear una nueva sección
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')
        if nombre:
            nueva = SeccionForo(nombre=nombre, descripcion=descripcion)
            nueva.save()
            messages.success(request, f"✅ Sección '{nombre}' creada exitosamente.")
            return redirect('admin_visual')
    temas = Tema.objects.all()
    comentarios = Comentario.objects.select_related('usuario', 'tema', 'tema__seccion')
    secciones = SeccionForo.objects.all()
    return render(request, 'core/admin_visual.html', {'temas': temas, 'comentarios': comentarios, 'secciones': secciones})

# -------------------------
# RECUPERAR CONTRASEÑA (simulada)
# -------------------------
from core.forms import FormularioRecuperar  # asegúrate de tener esta línea arriba

def recuperar_contraseña(request):
    if request.method == 'POST':
        form = FormularioRecuperar(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Usuario.objects.filter(email=email).exists():
                messages.success(request, "✅ Se han enviado las instrucciones a tu correo.")
            else:
                messages.warning(request, "⚠️ No existe una cuenta con ese correo.")
            return redirect('recuperar')
    else:
        form = FormularioRecuperar()

    return render(request, 'core/recuperarcontra.html', {'form': form})  # 🔴 esta línea es clave

# -------------------------
# FORO - Secciones, Temas, Comentarios, Valoraciones
# -------------------------
def lista_secciones(request):
    secciones = SeccionForo.objects.all()
    return render(request, 'core/secciones.html', {'secciones': secciones})

def temas_por_seccion(request, seccion_id):
    seccion = SeccionForo.objects.get(pk=seccion_id)
    temas = seccion.tema_set.filter(activo=True)
    return render(request, 'core/temas.html', {'seccion': seccion, 'temas': temas})

@login_required
def crear_tema(request):
    if request.method == 'POST':
        form = FormularioTema(request.POST)
        if form.is_valid():
            tema = form.save(commit=False)
            tema.usuario = request.user
            tema.save()
            messages.success(request, "✅ Tema creado exitosamente.")
            return redirect('temas_por_seccion', seccion_id=tema.seccion.id)
        else:
            messages.error(request, "❌ Error al crear el tema.")
    else:
        form = FormularioTema()
    return render(request, 'core/crear_tema.html', {'form': form})

@login_required
def comentar_tema(request, tema_id):
    tema = get_object_or_404(Tema, pk=tema_id, activo=True)

    if request.method == 'POST':
        comentario_id = request.POST.get('comentario_id')
        contenido = request.POST.get('contenido', '').strip()

        if not contenido:
            messages.warning(request, "⚠️ El contenido del comentario no puede estar vacío.")
            return redirect('foro')

        if comentario_id:
            # Editar comentario existente
            comentario = get_object_or_404(Comentario, pk=comentario_id)
            if request.user != comentario.usuario and (not request.user.rol or request.user.rol.nombre != 'Administrador'):
                messages.error(request, "❌ No tienes permiso para editar este comentario.")
                return redirect('foro')

            comentario.contenido = contenido
            comentario.save()
            messages.success(request, "✏️ Comentario actualizado correctamente.")
        else:
            # Crear nuevo comentario
            comentario = Comentario.objects.create(
                contenido=contenido,
                usuario=request.user,
                tema=tema
            )
            messages.success(request, "✅ Comentario publicado correctamente.")
    return redirect('foro')

@login_required
def valorar_tema(request, tema_id):
    tema = get_object_or_404(Tema, pk=tema_id, activo=True)
    if request.method == 'POST':
        valor = request.POST.get('valor')
        if valor:
            valoracion, created = Valoracion.objects.update_or_create(
                usuario=request.user,
                tema=tema,
                defaults={'valor': int(valor)}
            )
            messages.success(request, "⭐ Has valorado este tema.")
        else:
            messages.warning(request, "⚠️ No se recibió un valor válido.")
        return redirect('foro')
    return redirect('foro')

# -------------------------
# FAVORITOS - Agregar/Quitar y Mostrar
# -------------------------
@login_required
def agregar_quitar_favorito(request, tema_id):
    tema = get_object_or_404(Tema, id_tema=tema_id)
    if tema in request.user.favoritos.all():
        request.user.favoritos.remove(tema)
        messages.info(request, f"❌ Tema '{tema.titulo}' eliminado de tus favoritos.")
    else:
        request.user.favoritos.add(tema)
        messages.success(request, f"⭐ Tema '{tema.titulo}' añadido a tus favoritos.")
    return redirect('temas_por_seccion', seccion_id=tema.seccion.id)

# -------------------------
# BANEO - Temas y Comentarios
# -------------------------
@login_required
def banear_tema(request, tema_id):
    if request.user.rol.nombre != 'Administrador':
        messages.error(request, "❌ No tienes permisos para realizar esta acción.")
        return redirect('menuprincipal')
    tema = get_object_or_404(Tema, id_tema=tema_id)
    tema.activo = not tema.activo
    tema.save()
    estado = "activado" if tema.activo else "baneado"
    messages.success(request, f"🛠️ Tema '{tema.titulo}' ha sido {estado}.")
    return redirect('admin_visual')

@login_required
def banear_comentario(request, comentario_id):
    if request.user.rol.nombre != 'Administrador':
        messages.error(request, "❌ No tienes permisos para realizar esta acción.")
        return redirect('menuprincipal')
    comentario = get_object_or_404(Comentario, id=comentario_id)
    comentario.activo = not comentario.activo
    comentario.save()
    estado = "activado" if comentario.activo else "baneado"
    messages.success(request, f"🛠️ Comentario ID {comentario.id} ha sido {estado}.")
    return redirect('admin_visual')

# -------------------------
# API REST PROPIA
# -------------------------
def api_temas(request):
    temas = Tema.objects.all().values(
        'id_tema', 'titulo', 'contenido', 'fecha_creacion',
        'usuario__username', 'seccion__nombre'
    )
    return JsonResponse(list(temas), safe=False)

# -------------------------
# ELIMINAR SECCIÓN
# -------------------------
@login_required
def eliminar_seccion(request, seccion_id):
    seccion = get_object_or_404(SeccionForo, pk=seccion_id)

    if request.method == 'POST':
        try:
            seccion.delete()
            messages.success(request, f"🗑️ Sección '{seccion.nombre}' eliminada correctamente.")
        except Exception as e:
            messages.error(request, f"❌ Error al eliminar la sección: {str(e)}")

    return redirect('admin_visual')

# -------------------------
# VISTA: MIS TEMAS
# -------------------------
@login_required
def mis_temas(request):
    temas = Tema.objects.filter(usuario=request.user)
    return render(request, 'core/mis_temas.html', {'temas': temas})

@login_required
def mis_favoritos(request):
    favoritos = request.user.favoritos.all()
    return render(request, 'core/mis_favoritos.html', {'favoritos': favoritos})

@login_required
def eliminar_tema(request, tema_id):
    if request.method == 'POST':
        tema = get_object_or_404(Tema, pk=tema_id)
        if request.user != tema.usuario and (not request.user.rol or request.user.rol.nombre != 'Administrador'):
            messages.error(request, "❌ No tienes permiso para eliminar este tema.")
            return redirect('admin_visual')
        
        seccion_id = tema.seccion.id  # guardar antes de eliminar
        tema.delete()
        messages.success(request, "🗑️ Tema eliminado correctamente.")
        if 'admin_visual' in request.META.get('HTTP_REFERER', ''):
            return redirect('admin_visual')
        return redirect('temas_por_seccion', seccion_id=seccion_id)
    return redirect('admin_visual')

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)

    # Validar que el comentario esté asociado a un tema válido
    if not comentario.tema or not comentario.tema.id_tema:
        messages.error(request, "❌ Este comentario no está vinculado a un tema válido.")
        return redirect('foro')

    # Verificar permisos del usuario
    if request.user != comentario.usuario and (not request.user.rol or request.user.rol.nombre != 'Administrador'):
        messages.error(request, "❌ No tienes permiso para eliminar este comentario.")
        return redirect('foro')

    comentario.delete()
    messages.success(request, "🗑️ Comentario eliminado correctamente.")

    # Redirigir de forma contextual
    if 'admin_visual' in request.META.get('HTTP_REFERER', ''):
        return redirect('admin_visual')
    else:
        return redirect('foro')

@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)

    if request.user != comentario.usuario and (not request.user.rol or request.user.rol.nombre != 'Administrador'):
        messages.error(request, "❌ No tienes permiso para editar este comentario.")
        return redirect('foro')

    if request.method == 'POST':
        nuevo_contenido = request.POST.get('contenido_editado', '').strip()
        if nuevo_contenido:
            comentario.contenido = nuevo_contenido
            comentario.save()
            messages.success(request, "✏️ Comentario editado correctamente.")
        else:
            messages.warning(request, "⚠️ El contenido no puede estar vacío.")
        return redirect('foro')
    
    # No permite método GET directo para editar
    return redirect('foro')