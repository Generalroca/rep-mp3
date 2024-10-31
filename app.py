from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'base_de_datos.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS canciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                artista TEXT,
                ruta TEXT NOT NULL
            )
        ''')

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM canciones')
    canciones = cursor.fetchall()
    conn.close()
    return render_template('index.html', canciones=canciones)

@app.route('/subir', methods=['POST'])
def subir():
    archivo = request.files['cancion']
    if archivo:
        ruta = os.path.join('static', archivo.filename)
        archivo.save(ruta)
        nombre = archivo.filename
        artista = request.form.get('artista', 'Desconocido')

        with sqlite3.connect(DATABASE) as conn:
            conn.execute('INSERT INTO canciones (nombre, artista, ruta) VALUES (?, ?, ?)',
                         (nombre, artista, ruta))
    return index()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=35304, debug=True)
