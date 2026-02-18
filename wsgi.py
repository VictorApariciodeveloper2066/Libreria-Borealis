"""
WSGI config for MariaRifa project on PythonAnywhere.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

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

# For debugging (comment out in production)
# application = create_app('development')
