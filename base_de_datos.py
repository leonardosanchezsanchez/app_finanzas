import sqlite3

DB_NAME = 'ledgerly_db.sqlite'

def inicializar_db():
    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS perfiles (
                usuario_id INTEGER PRIMARY KEY,
                nombre TEXT,
                ingreso REAL,
                saldo_actual REAL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')