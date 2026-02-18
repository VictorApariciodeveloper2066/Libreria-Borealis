from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Rifa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad_numeros = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default='Abierta')
    imagen = db.Column(db.String(200))
    fecha_sorteo = db.Column(db.Date)
    boleto_ganador_id = db.Column(db.Integer)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    boletos = db.relationship('Boleto', backref='rifa', lazy=True)

class Boleto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    nombre_comprador = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    estatus_pago = db.Column(db.String(20), default='Disponible')
    metodo_pago = db.Column(db.String(50))
    banco = db.Column(db.String(100))
    comprobante = db.Column(db.String(200))
    rifa_id = db.Column(db.Integer, db.ForeignKey('rifa.id'), nullable=False)
