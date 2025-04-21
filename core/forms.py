from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from core.models import Usuario, RolUsuario
import re

# -------------------------
# FORMULARIO DE REGISTRO
# -------------------------

class FormularioRegistro(UserCreationForm):
    nombre_completo = forms.CharField(
        label='Nombre completo',
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Ej: Juan Pérez Soto'
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white', 'placeholder': 'Correo electrónico'})
    )

    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white', 'placeholder': 'Nombre de usuario'})
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white', 'placeholder': 'Contraseña'})
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white', 'placeholder': 'Confirmar contraseña'})
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")

        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Debe incluir al menos una letra mayúscula.")

        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("Debe incluir al menos una letra minúscula.")

        if not re.search(r"[0-9]", password):
            raise forms.ValidationError("Debe incluir al menos un número.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("Debe incluir al menos un carácter especial.")

        return password

    def save(self, commit=True):
        user = super().save(commit=False)

        nombre_completo = self.cleaned_data.get('nombre_completo', '')
        partes = nombre_completo.strip().split()

        if len(partes) >= 3:
            user.nombre = partes[0]
            user.apellido_paterno = partes[1]
            user.apellido_materno = ' '.join(partes[2:])
        elif len(partes) == 2:
            user.nombre = partes[0]
            user.apellido_paterno = partes[1]
            user.apellido_materno = ''
        elif len(partes) == 1:
            user.nombre = partes[0]
            user.apellido_paterno = ''
            user.apellido_materno = ''
        else:
            user.nombre = user.apellido_paterno = user.apellido_materno = ''

        user.email = self.cleaned_data['email']

        # Asignar rol por defecto "Jugador"
        try:
            user.rol = RolUsuario.objects.get(nombre__iexact='Jugador')
        except RolUsuario.DoesNotExist:
            user.rol = None

        if commit:
            user.save()
        return user

# -------------------------
# FORMULARIO DE LOGIN
# -------------------------

class FormularioLogin(forms.Form):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Contraseña'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("❌ Usuario o contraseña incorrectos.")
        return cleaned_data

# -------------------------
# FORMULARIO DE PERFIL
# -------------------------

class FormularioPerfil(forms.ModelForm):
    nueva_password = forms.CharField(
        label="Nueva contraseña (opcional)",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Nueva contraseña'
        }),
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white'}),
        }

    def clean_nueva_password(self):
        password = self.cleaned_data.get('nueva_password')
        if password:
            if len(password) < 8:
                raise forms.ValidationError("❌ La contraseña debe tener al menos 8 caracteres.")
            if not any(c.isupper() for c in password):
                raise forms.ValidationError("❌ La contraseña debe incluir una letra mayúscula.")
            if not any(c.islower() for c in password):
                raise forms.ValidationError("❌ La contraseña debe incluir una letra minúscula.")
            if not any(c.isdigit() for c in password):
                raise forms.ValidationError("❌ La contraseña debe incluir un número.")
            if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
                raise forms.ValidationError("❌ La contraseña debe incluir un carácter especial.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        nueva_password = self.cleaned_data.get('nueva_password')
        if nueva_password:
            user.set_password(nueva_password)
        if commit:
            user.save()
        return user

# -------------------------
# FORMULARIOS DEL FORO
# -------------------------

from .models import Tema, Comentario, Valoracion, SeccionForo

class FormularioTema(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['titulo', 'contenido', 'seccion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control bg-dark text-white'}),
            'seccion': forms.Select(attrs={'class': 'form-control bg-dark text-white'}),
        }

class FormularioComentario(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control bg-dark text-white'}),
        }

class FormularioValoracion(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['valor']
        widgets = {
            'valor': forms.Select(attrs={'class': 'form-control bg-dark text-white'}),
        }

class FormularioSeccion(forms.ModelForm):
    class Meta:
        model = SeccionForo
        fields = ['nombre', 'descripcion']
        labels = {
            'nombre': 'Nombre de la sección',
            'descripcion': 'Descripción (opcional)',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
        }

class FormularioEditarComentario(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control bg-dark text-white', 'rows': 2}),
        }
        labels = {
            'contenido': 'Editar comentario'
        }

# -------------------------
# FORMULARIO DE RECUPERACIÓN DE CONTRASEÑA
# -------------------------

class FormularioRecuperar(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Ingresa tu correo electrónico'
        })
    )

