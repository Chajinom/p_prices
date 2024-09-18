import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('../database.db')
c = conn.cursor()

# Crear tabla de países
c.execute('''
    CREATE TABLE IF NOT EXISTS paises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
''')

# Crear tabla de ciudades
c.execute('''
    CREATE TABLE IF NOT EXISTS ciudades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        pais_id INTEGER NOT NULL,
        FOREIGN KEY (pais_id) REFERENCES paises (id)
    )
''')

# Insertar datos de países
c.execute("INSERT OR IGNORE INTO paises (nombre) VALUES ('Argentina')")
c.execute("INSERT OR IGNORE INTO paises (nombre) VALUES ('Colombia')")

# Insertar ciudades principales de Argentina
c.execute("INSERT OR IGNORE INTO ciudades (nombre, pais_id) VALUES ('Buenos Aires', 1)")
c.execute("INSERT OR IGNORE INTO ciudades (nombre, pais_id) VALUES ('Córdoba', 1)")
c.execute("INSERT OR IGNORE INTO ciudades (nombre, pais_id) VALUES ('Rosario', 1)")

# Insertar ciudades principales de Colombia
c.execute("INSERT OR IGNORE INTO ciudades (nombre, pais_id) VALUES ('Bogotá', 2)")
c.execute("INSERT OR IGNORE INTO ciudades (nombre, pais_id) VALUES ('Medellín', 2)")
c.execute("INSERT OR IGNORE INTO ciudades (nombre, pais_id) VALUES ('Cali', 2)")

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()