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

    if request.method == 'POST':
        direccion = request.form['direccion']
        geolocator = Nominatim(user_agent="mi_aplicacion")
        location = geolocator.geocode(direccion)

        if location:
            lat = location.latitude
            lon = location.longitude
        else:
            flash('No se pudo encontrar la dirección')

    return render_template('home.html', username=session['username'], lat=lat, lon=lon)


# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)