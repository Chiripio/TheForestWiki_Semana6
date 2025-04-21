from pathlib import Path
import os
import sys
import oracledb

# 📁 Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Inicializa Oracle Client (wallet y client opcional dentro de oracle_wallet)
if any(cmd in sys.argv for cmd in ['runserver', 'shell', 'migrate', 'makemigrations', 'dbshell']):
    client_dir = os.path.join(BASE_DIR, 'oracle_wallet', 'lib')  # opcional
    wallet_dir = os.path.join(BASE_DIR, 'oracle_wallet', 'network', 'admin')

    # Establecer TNS_ADMIN para uso del wallet
    os.environ['TNS_ADMIN'] = wallet_dir

    # Inicializa cliente Oracle si está disponible (versión completa)
    if os.path.exists(client_dir):
        oracledb.init_oracle_client(lib_dir=client_dir)
    else:
        print("⚠️ No se encontró lib_dir, usando configuración externa del sistema")

    print("⏳ Inicializando cliente Oracle desde settings.py...")
    print("📁 TNS_ADMIN usado:", os.environ.get("TNS_ADMIN"))

    # Mostrar contenido de tnsnames.ora (depuración)
    try:
        with open(os.path.join(os.environ['TNS_ADMIN'], "tnsnames.ora"), "r") as f:
            print("\n📄 Contenido de tnsnames.ora desde settings.py:")
            print(f.read())
    except Exception as e:
        print("⚠️ No se pudo leer tnsnames.ora:", e)

    # Integración con sqlplus (solo si existe)
    if 'dbshell' in sys.argv:
        from django.db.backends.oracle.base import DatabaseWrapper
        sqlplus_path = os.path.join(client_dir, 'sqlplus')
        if os.path.isfile(sqlplus_path):
            DatabaseWrapper.client_executable_name = sqlplus_path

# 🔐 Django core settings
SECRET_KEY = 'django-insecure-^ge!t53#o611d!l-$@k1w-6%1b!645w)d%cs22+dnn45#8eh%m'
DEBUG = True
ALLOWED_HOSTS = []

# 📦 Apps instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TheForestWiki_Semana5.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TheForestWiki_Semana5.wsgi.application'

# ✅ Conexión limpia a Oracle usando oracledb + wallet
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'edu_high',  # ← Alias definido en tnsnames.ora
        'USER': 'forestwiki',
        'PASSWORD': 'NuevaPassword123',
        'OPTIONS': {
            'encoding': 'UTF-8',
            'threaded': True
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = True
LOGIN_URL = 'iniciar_sesion'
AUTH_USER_MODEL = 'core.Usuario'