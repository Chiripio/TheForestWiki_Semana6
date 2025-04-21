import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TheForestWiki_Semana5.settings')
django.setup()

from django.db import connection

engine = connection.settings_dict.get('ENGINE')
name = connection.settings_dict.get('NAME')

print(f"Motor de base de datos en uso: {engine}")
print(f"Nombre de la conexión: {name}")
