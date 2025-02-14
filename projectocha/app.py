from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'admin'  

# ruta para volver a la pagina de inicio
@app.route('/')
def redirigir_a_inicio():
    return redirect(url_for('inicio'))

# ruta para la pagina de inicio
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

# crea una coneccion a la base de datos
def get_db_connection():
    conn = sqlite3.connect('registro.db')
    conn.row_factory = sqlite3.Row 
    return conn

# ruta para eliminar un producto
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Eliminar el producto con el ID proporcionado
        cursor.execute('DELETE FROM resgistro_producto WHERE ID = ?', (id,))
        conn.commit()
        flash('Producto eliminado correctamente.', 'success')
    except sqlite3.Error as e:
        flash(f'Error al eliminar el producto: {e}', 'error')
    finally:
        conn.close()

    return redirect(url_for('productos'))  # nos lleva a la página de productos

# ruta para la pagina de productos
@app.route('/productos')
def productos():
    conn = get_db_connection()
    cursor = conn.cursor()

    # obtiene todos los productos
    cursor.execute('SELECT * FROM resgistro_producto')
    productos = cursor.fetchall()

    conn.close()
    return render_template('index.html', productos=productos)

# ruta para agregar un nuevo producto
@app.route('/agregar', methods=['POST'])
def agregar_producto():
    producto = request.form['producto']
    precio = request.form['precio']
    cantidad = request.form['cantidad']

    # verifica que las casillas no esten vacias
    if not producto or not precio or not cantidad:
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('productos'))  
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insertar el nuevo producto
        cursor.execute(
            'INSERT INTO resgistro_producto (producto, precio, cantidad) VALUES (?, ?, ?)',
            (producto, precio, cantidad)
        )
        conn.commit()
        flash('Producto agregado correctamente.', 'success')
    except sqlite3.IntegrityError:
        flash('Error: El nombre del producto ya existe.', 'error')
    except sqlite3.Error as e:
        flash(f'Error al agregar el producto: {e}', 'error')
    finally:
        conn.close()

    return redirect(url_for('productos'))  

if __name__ == '__main__':
    app.run(debug=True)