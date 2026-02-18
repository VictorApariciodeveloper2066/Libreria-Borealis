# Administrador de Rifas 🎟️

Sistema web para administrar rifas con cuadrícula interactiva de boletos.

## Instalación Local

1. Clonar el repositorio:
```bash
git clone https://github.com/VictorApariciodeveloper2066/Libreria-Borealis.git
cd Libreria-Borealis
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
- ✅ Favicon/logo en el navegador
- ✅ Base de datos SQLite local

## Estructura del proyecto

```
Libreria-Borealis/
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

## Tecnologías utilizadas

- **Backend:** Flask (Python)
- **Base de datos:** SQLite con SQLAlchemy
- **Frontend:** Tailwind CSS, JavaScript
- **Despliegue:** PythonAnywhere
