from app import create_app, db

app = create_app()

with app.app_context():
    # Agregar columnas de ganador a la tabla rifa
    with db.engine.connect() as conn:
        try:
            conn.execute(db.text('ALTER TABLE rifa ADD COLUMN boleto_ganador_id INTEGER'))
            conn.commit()
            print("Columna boleto_ganador_id agregada exitosamente")
        except Exception as e:
            print(f"Error al agregar boleto_ganador_id: {e}")
