import sqlite3

# Conectar a la base de datos (si no existe, la crea)
conn = sqlite3.connect('../database.db')
c = conn.cursor()

# Crear tabla de usuarios
c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Insertar usuario inicial (mgoya)
c.execute('''
    INSERT OR IGNORE INTO usuarios (username, password)
    VALUES ('mgoya', 'mgoya1')
''')

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()