from flask import render_template, request, redirect, url_for, jsonify, session, current_app as app
from . import db
from .models import Usuario, Rifa, Boleto
from .utils import seleccionar_ganador
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            session['user_id'] = usuario.id
            return redirect(url_for('dashboard_rifas'))
        return render_template('login.html', error='Email o contraseña incorrectos')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        password = request.form['password']
        
        if Usuario.query.filter_by(email=email).first():
            return render_template('register.html', error='El email ya está registrado')
        
        usuario = Usuario(nombre=nombre, email=email, telefono=telefono)
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()
        
        session['user_id'] = usuario.id
        return redirect(url_for('dashboard_rifas'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('dashboard_rifas'))

@app.route('/dashboard/rifas')
@login_required
def dashboard_rifas():
    usuario = Usuario.query.get(session['user_id'])
    rifas = Rifa.query.all()
    return render_template('dashboard_rifas.html', rifas=rifas, usuario=usuario)

@app.route('/dashboard/agregar')
@login_required
def dashboard_agregar():
    return render_template('dashboard_agregar.html')

@app.route('/dashboard/boletos')
@login_required
def dashboard_boletos():
    rifa_id = request.args.get('rifa_id')
    if not rifa_id:
        return redirect(url_for('dashboard_rifas'))
    rifa = Rifa.query.get_or_404(rifa_id)
    boletos = Boleto.query.filter_by(rifa_id=rifa_id).order_by(Boleto.numero).all()
    return render_template('dashboard_boletos.html', rifa=rifa, boletos=boletos)

@app.route('/dashboard/pagos')
@login_required
def dashboard_pagos():
    from sqlalchemy import func
    
    rifa_id = request.args.get('rifa_id')
    if not rifa_id:
        return redirect(url_for('dashboard_rifas'))
    
    rifa = Rifa.query.get_or_404(rifa_id)
    rifas = Rifa.query.all()
    
    # Obtener todos los boletos pagados de esta rifa específica
    boletos_pagados = db.session.query(Boleto, Rifa).join(Rifa).filter(
        Boleto.estatus_pago == 'Pagado',
        Boleto.rifa_id == rifa_id
    ).order_by(Boleto.id.desc()).all()
    
    # Calcular totales para esta rifa
    total_recaudado = sum(boleto.Rifa.precio for boleto in boletos_pagados)
    total_pagados = len(boletos_pagados)
    
    # Contar pendientes de esta rifa
    total_pendientes = Boleto.query.filter_by(rifa_id=rifa_id, estatus_pago='Pendiente').count()
    
    # Agrupar por método de pago para esta rifa
    pagos_por_metodo = db.session.query(
        Boleto.metodo_pago,
        func.count(Boleto.id).label('cantidad'),
        func.sum(Rifa.precio).label('total')
    ).join(Rifa).filter(
        Boleto.estatus_pago == 'Pagado',
        Boleto.metodo_pago.isnot(None),
        Boleto.rifa_id == rifa_id
    ).group_by(Boleto.metodo_pago).all()
    
    return render_template('dashboard_pagos.html', 
                         rifa=rifa,
                         rifas=rifas,
                         boletos_pagados=boletos_pagados,
                         total_recaudado=total_recaudado,
                         total_pagados=total_pagados,
                         total_pendientes=total_pendientes,
                         pagos_por_metodo=pagos_por_metodo)

@app.route('/dashboard/ganador')
@login_required
def dashboard_ganador():
    rifas = Rifa.query.all()
    return render_template('dashboard_ganador.html', rifas=rifas)

@app.route('/sortear_ganador/<int:rifa_id>', methods=['POST'])
@login_required
def sortear_ganador(rifa_id):
    from datetime import date
    
    rifa = Rifa.query.get_or_404(rifa_id)
    
    # Verificar si es el día del sorteo
    if rifa.fecha_sorteo and rifa.fecha_sorteo > date.today():
        return jsonify({
            'success': False,
            'error': 'fecha',
            'message': f'El sorteo está programado para el {rifa.fecha_sorteo.strftime("%d/%m/%Y")}'
        })
    
    # Verificar si todos los boletos están pagados
    total_boletos = Boleto.query.filter_by(rifa_id=rifa_id).count()
    boletos_pagados = Boleto.query.filter_by(rifa_id=rifa_id, estatus_pago='Pagado').count()
    
    if boletos_pagados < total_boletos:
        return jsonify({
            'success': False,
            'error': 'pagos',
            'message': f'Faltan {total_boletos - boletos_pagados} boletos por pagar',
            'pagados': boletos_pagados,
            'total': total_boletos
        })
    
    # Seleccionar ganador
    boletos = Boleto.query.filter_by(rifa_id=rifa_id, estatus_pago='Pagado').all()
    ganador = seleccionar_ganador(boletos)
    
    # Guardar ganador en la rifa (sin cerrar la rifa)
    rifa.boleto_ganador_id = ganador.id
    db.session.commit()
    
    return jsonify({
        'success': True,
        'ganador': {
            'numero': ganador.numero,
            'nombre': ganador.nombre_comprador,
            'telefono': ganador.telefono
        }
    })

@app.route('/eliminar_ganador/<int:rifa_id>', methods=['POST'])
@login_required
def eliminar_ganador(rifa_id):
    rifa = Rifa.query.get_or_404(rifa_id)
    rifa.boleto_ganador_id = None
    db.session.commit()
    return jsonify({'success': True})

@app.route('/rifa/<int:rifa_id>/boletos')
@login_required
def boletos(rifa_id):
    rifa = Rifa.query.get_or_404(rifa_id)
    boletos = Boleto.query.filter_by(rifa_id=rifa_id).all()
    return render_template('boletos.html', rifa=rifa, boletos=boletos)

@app.route('/reservar/<int:boleto_id>', methods=['POST'])
@login_required
def reservar_boleto(boleto_id):
    boleto = Boleto.query.get_or_404(boleto_id)
    data = request.get_json()
    
    boleto.nombre_comprador = data.get('nombre')
    boleto.telefono = data.get('telefono')
    boleto.estatus_pago = 'Pendiente'
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/actualizar_boleto/<int:boleto_id>', methods=['POST'])
@login_required
def actualizar_boleto(boleto_id):
    from werkzeug.utils import secure_filename
    import os
    
    boleto = Boleto.query.get_or_404(boleto_id)
    
    boleto.estatus_pago = request.form.get('estatus_pago')
    boleto.nombre_comprador = request.form.get('nombre_comprador')
    boleto.telefono = request.form.get('telefono')
    
    if boleto.estatus_pago == 'Pagado':
        boleto.metodo_pago = request.form.get('metodo_pago')
        boleto.banco = request.form.get('banco')
        
        comprobante = request.files.get('comprobante')
        if comprobante and comprobante.filename:
            filename = secure_filename(comprobante.filename)
            upload_folder = os.path.join(app.root_path, 'static', 'comprobantes')
            os.makedirs(upload_folder, exist_ok=True)
            comprobante.save(os.path.join(upload_folder, filename))
            boleto.comprobante = filename
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/pagar/<int:boleto_id>', methods=['POST'])
@login_required
def pagar_boleto(boleto_id):
    boleto = Boleto.query.get_or_404(boleto_id)
    boleto.estatus_pago = 'Pagado'
    db.session.commit()
    return jsonify({'success': True})

@app.route('/sorteo/<int:rifa_id>')
@login_required
def sorteo(rifa_id):
    rifa = Rifa.query.get_or_404(rifa_id)
    boletos_pagados = Boleto.query.filter_by(rifa_id=rifa_id, estatus_pago='Pagado').all()
    
    ganador = None
    if boletos_pagados:
        ganador = seleccionar_ganador(boletos_pagados)
        rifa.estado = 'Cerrada'
        db.session.commit()
    
    return render_template('sorteo.html', rifa=rifa, ganador=ganador)

@app.route('/crear_rifa', methods=['POST'])
@login_required
def crear_rifa():
    from werkzeug.utils import secure_filename
    from datetime import datetime
    import os
    
    data = request.form
    imagen = request.files.get('imagen')
    imagen_filename = None
    
    if imagen and imagen.filename:
        filename = secure_filename(imagen.filename)
        upload_folder = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        imagen_path = os.path.join(upload_folder, filename)
        imagen.save(imagen_path)
        imagen_filename = filename
    
    fecha_sorteo = None
    if data.get('fecha_sorteo'):
        fecha_sorteo = datetime.strptime(data['fecha_sorteo'], '%Y-%m-%d').date()
    
    rifa = Rifa(
        nombre=data['nombre'],
        precio=float(data['precio']),
        cantidad_numeros=int(data['cantidad_numeros']),
        imagen=imagen_filename,
        fecha_sorteo=fecha_sorteo
    )
    db.session.add(rifa)
    db.session.commit()
    
    for i in range(1, rifa.cantidad_numeros + 1):
        boleto = Boleto(numero=i, rifa_id=rifa.id)
        db.session.add(boleto)
    
    db.session.commit()
    return redirect(url_for('dashboard_rifas'))

@app.route('/editar_rifa/<int:rifa_id>')
@login_required
def editar_rifa(rifa_id):
    rifa = Rifa.query.get_or_404(rifa_id)
    return render_template('dashboard_editar.html', rifa=rifa)

@app.route('/actualizar_rifa/<int:rifa_id>', methods=['POST'])
@login_required
def actualizar_rifa(rifa_id):
    from werkzeug.utils import secure_filename
    import os
    
    rifa = Rifa.query.get_or_404(rifa_id)
    data = request.form
    imagen = request.files.get('imagen')
    
    rifa.nombre = data['nombre']
    rifa.precio = float(data['precio'])
    
    if imagen and imagen.filename:
        filename = secure_filename(imagen.filename)
        upload_folder = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        imagen_path = os.path.join(upload_folder, filename)
        imagen.save(imagen_path)
        rifa.imagen = filename
    
    db.session.commit()
    return redirect(url_for('dashboard_rifas'))

@app.route('/borrar_rifa/<int:rifa_id>')
@login_required
def borrar_rifa(rifa_id):
    rifa = Rifa.query.get_or_404(rifa_id)
    Boleto.query.filter_by(rifa_id=rifa_id).delete()
    db.session.delete(rifa)
    db.session.commit()
    return redirect(url_for('dashboard_rifas'))
