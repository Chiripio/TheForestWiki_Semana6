import django
import os
import sys

# Asegura el entorno Django y la conexión a Oracle usando el módulo oracledb
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TheForestWiki_Semana5.settings")

# ⚠️ Forzamos definición de rutas como en settings.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.join(BASE_DIR, 'oracle_wallet', 'lib')
wallet_dir = os.path.join(BASE_DIR, 'oracle_wallet', 'network', 'admin')
os.environ['TNS_ADMIN'] = wallet_dir

try:
    print("⏳ Inicializando Django...")
    print("📁 TNS_ADMIN actual:", os.environ.get("TNS_ADMIN"))
    print("📁 Intentando usar el alias:", os.environ['TNS_ADMIN'] + "/tnsnames.ora")

    with open(os.environ['TNS_ADMIN'] + "/tnsnames.ora", "r") as f:
        print("\n📄 Contenido de tnsnames.ora:")
        print(f.read())

    django.setup()

    from django.db import connection

    print("🔌 Verificando conexión con Oracle...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM user_tables")
        tablas = cursor.fetchall()
        if tablas:
            print("✅ Conexión exitosa. Tablas encontradas:")
            for tabla in tablas:
                print(f"   - {tabla[0]}")
        else:
            print("⚠️ Conectado, pero no se encontraron tablas.")
except Exception as e:
    print("❌ Error al conectar con Oracle:", e)
    sys.exit(1)
