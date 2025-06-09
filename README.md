🚀 Guía de Inicio Rápido: Sistema de Gestión PLAZOS
¡Bienvenido al sistema de gestión de pagos PLAZOS! Sigue estos pasos para configurar y ejecutar la aplicación en tu entorno local.

📋 Requisitos Previos
Antes de comenzar, asegúrate de tener instalado:

Python 3.8+

PostgreSQL (o cualquier base de datos compatible con Django)

Git (opcional, pero recomendado)

🛠️ Configuración Inicial
1. Clonar el Repositorio
Si usas Git, ejecuta:

bash
git clone https://github.com/tu-usuario/sistema-plazos.git
cd sistema-plazos
Si no usas Git, descarga el código fuente manualmente y descomprímelo.

2. Preparar la Base de Datos
Crea una base de datos en PostgreSQL llamada plazos_db.

Ejecuta el script SQL proporcionado en /scripts/plazos_schema.sql para generar las tablas necesarias.

3. Entorno Virtual
Crea y activa un entorno virtual para evitar conflictos de dependencias:

bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
4. Instalar Dependencias
Instala los paquetes requeridos:

bash
pip install -r requirements.txt
5. Configurar Variables de Entorno
Crea un archivo .env en la raíz del proyecto con estos datos (ajústalos según tu entorno):

ini
DB_NAME=plazos_db
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
6. Migraciones y Datos Iniciales
Ejecuta las migraciones para crear las tablas en Django:

bash
python manage.py migrate
python manage.py loaddata datos_iniciales.json  # Opcional: carga datos de prueba
🖥️ Ejecutar la Aplicación
Inicia el servidor de desarrollo con:

bash
python manage.py runserver
🔹 Accede a la aplicación desde: http://localhost:8000

🔧 Funcionalidades Adicionales
Panel de Administración:
Crea un superusuario para acceder al panel de Django:

bash
python manage.py createsuperuser
Luego visita: http://localhost:8000/admin

API REST:
Explora los endpoints en: http://localhost:8000/api/

