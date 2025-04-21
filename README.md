# 🌲 TheForestWiki - Semana 5

Proyecto web desarrollado con Django como parte del ramo de Programación Web.  
Incluye FrontEnd responsivo, sistema de autenticación con roles (cliente y administrador), y panel de administración.

---

##  ¿Qué contiene?

 * Autenticación personalizada con selección de rol  
 * Vistas separadas para cliente y administrador  
 * Información temática del juego **The Forest**  
 * Interfaz responsiva con Bootstrap  
 * Panel de administración (`/admin`)  
 * Archivos organizados con buenas prácticas

---

## ⚙️ Requisitos

- Python 3.9+
- Django 4.2.x (instalado vía `pip`)
- Entorno virtual (recomendado)

---

##  Instrucciones para ejecutar el proyecto

1.  Clona o descomprime este repositorio.
2.  Abre tu terminal y navega a la carpeta principal:

   ```bash
   cd TheForestWiki_Semana5

## Crea y activa un entorno virtual:
   ( en MAc )

 python3 -m venv venv
source venv/bin/activate

## Instala Django:

pip install django

## Aplica las migraciones para construir la base de datos:

python manage.py makemigrations
python manage.py migrate

## Crea un superusuario para acceder al panel admin:

python manage.py createsuperuser

## Ejecuta el servidor local:

python manage.py runserver

## Abre tu navegador en http://127.0.0.1:8000
Accede al panel de administración en http://127.0.0.1:8000/admin

## Archivos incluidos:

📁 core/
📁 static/
📁 templates/
📁 TheForestWiki_Semana5/  # Configuración Django
📄 manage.py
📄 README.md
📄 .gitignore


Desarrollado por:
- Eduardo Guerrero
- Jorge Uribe
- Sebastián Trujillo

---

## 