import sqlite3
import os

db_path = 'instance/rifas.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    columns_to_add = [
        ("metodo_pago", "VARCHAR(50)"),
        ("banco", "VARCHAR(100)"),
        ("comprobante", "VARCHAR(200)")
    ]
    
    for column_name, column_type in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE boleto ADD COLUMN {column_name} {column_type}")
            print(f"Columna '{column_name}' agregada exitosamente")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"La columna '{column_name}' ya existe")
            else:
                print(f"Error en {column_name}: {e}")
    
    conn.commit()
    conn.close()
else:
    print("Base de datos no encontrada")
