# Administrador de Rifas 🎟️

Sistema web para administrar rifas con cuadrícula interactiva de boletos.

## Instalación Local

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
python app.py
```

3. Abrir en el navegador: `http://localhost:5000`

## Características

- ✅ Crear rifas con cantidad personalizada de números
- ✅ Cuadrícula visual con colores por estado (Verde=Disponible, Amarillo=Pendiente, Rojo=Pagado)
- ✅ Reservar boletos con nombre y teléfono
- ✅ Marcar boletos como pagados
- ✅ Sorteo aleatorio entre boletos pagados
- ✅ Eliminar rifas pasadas
- ✅ Base de datos SQLite local

## Despliegue en PythonAnywhere

### Pasos para desplegar:

1. **Crear cuenta en PythonAnywhere**
   - Ve a [pythonanywhere.com](https://www.pythonanywhere.com/)
   - Crea una cuenta gratuita (o premium si necesitas más características)

2. **Subir archivos**
   - En la pestaña "Files" de PythonAnywhere, crea una carpeta llamada `MariaRifa`
   - Sube todos los archivos del proyecto a esa carpeta:
     - `app/` (carpeta completa)
     - `app.py`
     - `config.py`
     - `wsgi.py` (este archivo es nuevo y necesario para PythonAnywhere)
     - `requirements.txt`
     - La carpeta `instance/` con tu base de datos existente (si tienes datos)

3. **Crear entorno virtual (opcional pero recomendado)**
   - Ve a la pestaña "Consoles" y crea una nueva consola bash
   - Ejecuta:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 rifas-venv
   workon rifas-venv
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

### Notas importantes:

- La base de datos se guardará en `/home/TU_USUARIO/MariaRifa/instance/rifas.db`
- Si tienes una base de datos existente, súbela a la carpeta `instance/`
- El archivo `wsgi.py` ya está configurado para producción

### Solución de problemas:

- Si ves errores, revisa los logs en la pestaña "Web" → "View logs"
- Asegúrate de que la ruta en WSGI apunte correctamente a tu carpeta

## Estructura

- `app/models.py` - Modelos de base de datos
- `app/routes.py` - Rutas y lógica
- `app/utils.py` - Función de sorteo
- `app/templates/` - Vistas HTML
- `app/static/` - CSS, JS e imágenes
- `wsgi.py` - Archivo de configuración para PythonAnywhere
- `config.py` - Configuración de la aplicación
