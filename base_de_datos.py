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
def registrar_usuario(usuario, password):
    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            # Usamos el comando INSERT para guardar los datos
            cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (usuario, password))
            conexion.commit()
            return True
    except sqlite3.IntegrityError:
        # Esto pasa si el nombre de usuario ya existe
        return False
def validar_login(usuario, password):
    with sqlite3.connect(DB_NAME) as conexion:
        cursor = conexion.cursor()
        # Buscamos si existe alguien con ese nombre Y esa contraseña
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (usuario, password))
        resultado = cursor.fetchone()
        return resultado # Si encuentra algo, devuelve los datos; si no, devuelve None