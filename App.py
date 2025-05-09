from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'DRXENO'
app.config['MYSQL_DB'] = 'sistematitulacion'
app.config['MYSQL_PASSWORD'] = 'DrXeno79TESLA'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

#paginas
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM estudiantes')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', estudiantes = data)

@app.route('/docentes')
def docentes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM docentes')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', estudiantes = data)

@app.route('/pagos')
def pagos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pagos')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', estudiantes = data)

#Guardar
@app.route('/add_estudiante', methods=['POST'])
def add_estudiante():
    if request.method == 'POST':
        name = request.form['nombre']
        apellido = request.form['apellido']
        codigo_estudiante = request.form['codigo_estudiante']
        email = request.form['email']
        telefono = request.form['telefono']
        estado_pagos = request.form['estado_pagos']
        habilitado_titulacion = request.form['habilitado_titulacion']
        print(name, apellido, email, telefono, codigo_estudiante, estado_pagos, habilitado_titulacion)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO estudiantes (nombre, apellido, CodigoEstudiante, email, telefono, EstadoPagos, HabilitadoTitulacion) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, apellido, codigo_estudiante, email, telefono, estado_pagos, habilitado_titulacion))
        mysql.connection.commit()
        flash('Estudiante agregado correctamente')
        return redirect(url_for('index'))

#editar
@app.route('/edit/<id>')
def get_estudiante(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM estudiantes WHERE idEstudiante = %s', (id))
    data = cur.fetchall()
    return render_template('edit_Estudiante.html', estudiante = data[0])

#actualisar
@app.route('/update/<id>', methods=['POST'])
def update_estudiante(id):
    if request.method == 'POST':
        name =request.form['nombre']
        apellido = request.form['apellido']
        codigo_estudiante = request.form['codigo_estudiante']
        email = request.form['email']
        telefono = request.form['telefono']
        estado_pagos = request.form['estado_pagos']
        habilitado_titulacion = request.form['habilitado_titulacion']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE estudiantes SET nombre = %s, apellido = %s, CodigoEstudiante = %s, email = %s, telefono = %s, EstadoPagos = %s, HabilitadoTitulacion = %s WHERE idEstudiante = %s""",
                (name, apellido, codigo_estudiante, email, telefono, estado_pagos, habilitado_titulacion, id))
    mysql.connection.commit()
    flash('Estudiante actualizado correctamente')
    return redirect(url_for('index'))
    
#Eliminar
@app.route('/delete/<string:id>')
def delet_estudiante(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM estudiantes WHERE idEstudiante = {0}'.format(id))
    mysql.connection.commit()
    flash('Estudiante eliminado correctamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
        # Run the Flask app on port 3000
    app.run(port=3000, debug = True)