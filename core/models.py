from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------
# MODELO DE ROL DE USUARIO
# -----------------------------
class RolUsuario(models.Model):
    id_rol = models.AutoField(primary_key=True, db_column='ID_ROL')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')

    class Meta:
        verbose_name = "Rol de Usuario"
        verbose_name_plural = "Roles de Usuario"
        db_table = 'ROL_USUARIO'

    def __str__(self):
        return self.nombre

# -----------------------------
# MODELO DE USUARIO PERSONALIZADO
# -----------------------------
class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True, db_column='ID_USUARIO')
    email = models.EmailField(db_column='EMAIL')
    password = models.CharField(max_length=128, db_column='PASSWORD')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    apellido_paterno = models.CharField(max_length=50, db_column='APELLIDO_PATERNO')
    apellido_materno = models.CharField(max_length=50, db_column='APELLIDO_MATERNO')
    rol = models.ForeignKey(RolUsuario, on_delete=models.CASCADE, db_column='ID_ROL', null=True, blank=True)

    favoritos = models.ManyToManyField(
        'Tema',
        blank=True,
        related_name='usuarios_favoritos',
        db_table='CORE_USUARIO_FAVORITOS'
    )

    first_name = models.CharField(max_length=150, db_column='FIRST_NAME', blank=True)
    last_name = models.CharField(max_length=150, db_column='LAST_NAME', blank=True)
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    is_staff = models.BooleanField(default=False, db_column='IS_STAFF')
    is_superuser = models.BooleanField(default=False, db_column='IS_SUPERUSER')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido_paterno', 'apellido_materno']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='user'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='user'
    )

    class Meta:
        db_table = 'USUARIO'

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

# -----------------------------
# MODELO DE SECCIÓN DEL FORO
# -----------------------------
class SeccionForo(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID_SECCION')
    nombre = models.CharField(max_length=100, db_column='NOMBRE')
    descripcion = models.CharField(max_length=255, db_column='DESCRIPCION', blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'SECCION_FORO'

# -----------------------------
# MODELO DE TEMA DEL FORO
# -----------------------------
class Tema(models.Model):
    id_tema = models.AutoField(primary_key=True, db_column='ID_TEMA')
    titulo = models.CharField(max_length=100, db_column='TITULO')
    contenido = models.TextField(db_column='CONTENIDO')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='FECHA_CREACION')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='ID_USUARIO')
    seccion = models.ForeignKey(SeccionForo, on_delete=models.CASCADE, db_column='ID_SECCION')
    activo = models.BooleanField(default=True, db_column='ACTIVO')

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'TEMA'

# -----------------------------
# MODELO DE COMENTARIO
# -----------------------------
class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True, db_column='ID_COMENTARIO')
    contenido = models.TextField(db_column='CONTENIDO')
    fecha_comentario = models.DateTimeField(auto_now_add=True, db_column='FECHA_COMENTARIO')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='ID_USUARIO')
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, db_column='ID_TEMA')
    activo = models.BooleanField(default=True, db_column='ACTIVO')

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.tema.titulo}"

    class Meta:
        db_table = 'COMENTARIO'

# -----------------------------
# MODELO DE VALORACIÓN
# -----------------------------
class Valoracion(models.Model):
    id_valoracion = models.AutoField(primary_key=True, db_column='ID_VALORACION')
    valor = models.IntegerField(choices=[(i, i) for i in range(1, 6)], db_column='VALOR')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='ID_USUARIO')
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, db_column='ID_TEMA')

    class Meta:
        unique_together = ('usuario', 'tema')
        db_table = 'VALORACION'

    def __str__(self):
        return f"{self.usuario.username} valoró {self.tema.titulo} con {self.valor}"