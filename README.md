# Administrador de Rifas 🎟️

Sistema web para administrar rifas con cuadrícula interactiva de boletos.

## Instalación Local

1. Clonar el repositorio:
```bash
git clone https://github.com/TU_USUARIO/MariaRifa.git
cd MariaRifa
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
python app.py
```

4. Abrir en el navegador: `http://localhost:5000`

## Características

- ✅ Crear rifas con cantidad personalizada de números
- ✅ Cuadrícula visual con colores por estado (Verde=Disponible, Amarillo=Pendiente, Rojo=Pagado)
- ✅ Reservar boletos con nombre y teléfono
- ✅ Marcar boletos como pagados
- ✅ Sorteo aleatorio entre boletos pagados
- ✅ Eliminar rifas pasadas
- ✅ Base de datos SQLite local

## Despliegue en PythonAnywhere

### Opción 1: Subir archivos directamente

1. **Crear cuenta en PythonAnywhere**
   - Ve a [pythonanywhere.com](https://www.pythonanywhere.com/)
   - Crea una cuenta gratuita (o premium si necesitas más características)

2. **Subir archivos**
   - En la pestaña "Files" de PythonAnywhere, crea una carpeta llamada `MariaRifa`
   - Sube todos los archivos del proyecto a esa carpeta:
     - `app/` (carpeta completa)
     - `app.py`
     - `config.py`
     - `wsgi.py`
     - `requirements.txt`
     - La carpeta `instance/` con tu base de datos existente (si tienes datos)

3. **Instalar dependencias**
   - Ve a la pestaña "Consoles" y crea una nueva consola bash
   - Ejecuta:
   ```bash
   pip install -r ~/MariaRifa/requirements.txt
   ```

4. **Configurar la aplicación web**
   - Ve a la pestaña "Web"
   - Click en "Add a new web app"
   - Selecciona "Manual configuration" y luego "Python 3.11"
   - En la sección "WSGI configuration file", edita el archivo y reemplaza el contenido con el de `wsgi.py`

5. **Configurar rutas de archivos estáticos**
   - En la pestaña "Web", busca "Static files"
   - Añadir:
     - URL: `/static/` → Directory: `/home/TU_USUARIO/MariaRifa/app/static/`

6. **Recargar la aplicación**
   - Click en el botón "Reload" en la pestaña "Web"
   - Tu aplicación debería estar disponible en `https://TU_USUARIO.pythonanywhere.com`

### Opción 2: Deploy desde GitHub (Recomendado)

Esta opción es más fácil para actualizaciones futuras.

#### Paso 1: Subir código a GitHub

1. Crea un repositorio en GitHub:
   - Ve a [github.com](https://github.com) e inicia sesión
   - Click en "New repository"
   - Nombre: `MariaRifa`
   - Click en "Create repository"

2. En tu computadora local, inicializa git y sube el código:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/MariaRifa.git
git push -u origin main
```

#### Paso 2: Configurar PythonAnywhere con GitHub

1. **En PythonAnywhere - Consoles**
   - Ve a la pestaña "Consoles" y abre una Bash console
   - Clona el repositorio:
   ```bash
   cd ~
   git clone https://github.com/TU_USUARIO/MariaRifa.git
   ```

2. **Instalar dependencias**
   ```bash
   cd ~/MariaRifa
   pip install -r requirements.txt
   ```

3. **Configurar la aplicación web**
   - Ve a la pestaña "Web"
   - Click en "Add a new web app"
   - Selecciona "Manual configuration" y luego "Python 3.11"
   - Edita el WSGI configuration file y reemplaza el contenido con:
   ```python
   import os
   import sys

   # Add your project directory to the Python path
   project_home = os.path.expanduser('~/MariaRifa')
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   # Set environment to production
   os.environ['FLASK_ENV'] = 'production'

   # Create the application
   from app import create_app
   application = create_app('production')
   ```

4. **Configurar rutas de archivos estáticos**
   - En la pestaña "Web", busca "Static files"
   - Añadir:
     - URL: `/static/` → Directory: `/home/TU_USUARIO/MariaRifa/app/static/`

5. **Recargar la aplicación**
   - Click en el botón "Reload"

#### Paso 3: Actualizar el código desde GitHub

Cuando hagas cambios en tu código:

1. Haz los cambios localmente
2. Sube a GitHub:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

3. En PythonAnywhere, actualiza el código:
```bash
cd ~/MariaRifa
git pull origin main
```

4. Recarga la aplicación web desde la pestaña "Web"

### Notas importantes:

- La base de datos se guardará en `/home/TU_USUARIO/MariaRifa/instance/rifas.db`
- Si tienes una base de datos existente, súbela a la carpeta `instance/`
- El archivo `wsgi.py` ya está configurado para producción

### Solución de problemas:

- Si ves errores, revisa los logs en la pestaña "Web" → "View logs"
- Asegúrate de que la ruta en WSGI apunte correctamente a tu carpeta
- Verifica que las rutas de archivos estáticos estén configuradas correctamente

## Estructura del proyecto

```
MariaRifa/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── utils.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── img/
│   │   ├── uploads/
│   │   └── comprobantes/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard_rifas.html
│       ├── dashboard_boletos.html
│       ├── dashboard_pagos.html
│       ├── dashboard_agregar.html
│       ├── dashboard_editar.html
│       └── dashboard_ganador.html
├── app.py
├── config.py
├── wsgi.py
├── requirements.txt
├── instance/
│   └── rifas.db (base de datos)
└── README.md
```
