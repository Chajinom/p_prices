from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.secret_key = 'supersecretkey'


# Función para conectarse a la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Esto devuelve filas como diccionarios
    return conn


# Ruta principal (Login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?',
                            (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrecta')

    return render_template('login.html')


# Página de inicio donde se ingresa la dirección
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    lat = None
    lon = None

    conn = get_db_connection()
    paises = conn.execute('SELECT * FROM paises').fetchall()
    ciudades = None

    if request.method == 'POST':
        pais_id = request.form['pais']
        ciudad_id = request.form['ciudad']
        direccion = request.form['direccion']

        # Obtener el nombre del país y la ciudad seleccionados
        pais = conn.execute('SELECT nombre FROM paises WHERE id = ?', (pais_id,)).fetchone()
        ciudad = conn.execute('SELECT nombre FROM ciudades WHERE id = ?', (ciudad_id,)).fetchone()

        # Construir la dirección completa
        direccion_completa = f"{direccion}, {ciudad['nombre']}, {pais['nombre']}"
        geolocator = Nominatim(user_agent="mi_aplicacion")
        location = geolocator.geocode(direccion_completa)

        if location:
            lat = location.latitude
            lon = location.longitude
        else:
            flash('No se pudo encontrar la dirección completa')

    if request.args.get('pais'):
        # Cargar las ciudades cuando un país es seleccionado
        pais_id = request.args.get('pais')
        ciudades = conn.execute('SELECT * FROM ciudades WHERE pais_id = ?', (pais_id,)).fetchall()

    conn.close()

    return render_template('home.html', username=session['username'], paises=paises, ciudades=ciudades, lat=lat,
                           lon=lon)


# Ruta para obtener las ciudades basadas en el país seleccionado
@app.route('/obtener_ciudades', methods=['GET'])
def obtener_ciudades():
    pais_id = request.args.get('pais_id')
    conn = get_db_connection()
    ciudades = conn.execute('SELECT * FROM ciudades WHERE pais_id = ?', (pais_id,)).fetchall()
    conn.close()
    return render_template('ciudades_dropdown.html', ciudades=ciudades)


# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)