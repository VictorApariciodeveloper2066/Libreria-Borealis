from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Import config
    from config import config
    app.config.from_object(config.get(config_name, config['default']))
    
    db.init_app(app)
    
    with app.app_context():
        from . import routes
        db.create_all()
    
    return app
