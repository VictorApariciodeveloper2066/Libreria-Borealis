import sqlite3
import os

db_path = 'instance/rifas.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE rifa ADD COLUMN imagen VARCHAR(200)")
        conn.commit()
        print("Columna 'imagen' agregada exitosamente")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("La columna 'imagen' ya existe")
        else:
            print(f"Error: {e}")
    finally:
        conn.close()
else:
    print("Base de datos no encontrada")
