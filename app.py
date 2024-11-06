from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('restaurante.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para mostrar la lista de platos, mesas y pedidos
@app.route('/')
def index():
    conn = get_db_connection()
    platos = conn.execute('SELECT * FROM platos').fetchall()
    mesas = conn.execute('SELECT * FROM mesas').fetchall()
    pedidos = conn.execute('''
    SELECT pedidos.id, platos.nombre AS plato, mesas.numero AS mesa, pedidos.cantidad, pedidos.fecha 
    FROM pedidos
    JOIN platos ON pedidos.plato_id = platos.id
    JOIN mesas ON pedidos.mesa_id = mesas.id
    ''').fetchall()
    conn.close()
    return render_template('index.html', platos=platos, mesas=mesas, pedidos=pedidos)

# Ruta para agregar un nuevo plato
@app.route('/agregar_plato', methods=('GET', 'POST'))
def agregar_plato():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        conn = get_db_connection()
        conn.execute('INSERT INTO platos (nombre, precio) VALUES (?, ?)', (nombre, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('agregar.html', tipo='Plato')

# Ruta para agregar un nuevo pedido
@app.route('/agregar_pedido', methods=('GET', 'POST'))
def agregar_pedido():
    conn = get_db_connection()
    platos = conn.execute('SELECT * FROM platos').fetchall()
    mesas = conn.execute('SELECT * FROM mesas').fetchall()
    conn.close()
    if request.method == 'POST':
        plato_id = request.form['plato_id']
        mesa_id = request.form['mesa_id']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']
        conn = get_db_connection()
        conn.execute('INSERT INTO pedidos (plato_id, mesa_id, cantidad, fecha) VALUES (?, ?, ?, ?)', 
                     (plato_id, mesa_id, cantidad, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('agregar.html', tipo='Pedido', platos=platos, mesas=mesas)

# Ruta para editar un plato
@app.route('/editar_plato/<int:id>', methods=('GET', 'POST'))
def editar_plato(id):
    conn = get_db_connection()
    plato = conn.execute('SELECT * FROM platos WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        conn.execute('UPDATE platos SET nombre = ?, precio = ? WHERE id = ?', (nombre, precio, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('editar.html', item=plato, tipo='Plato')

# Ruta para eliminar un plato
@app.route('/eliminar_plato/<int:id>', methods=('POST',))
def eliminar_plato(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM platos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
