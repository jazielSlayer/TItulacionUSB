from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'DRXENO'
app.config['MYSQL_DB'] = 'sistematitulacion'
app.config['MYSQL_PASSWORD'] = 'DrXeno79TESLA'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')
    
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


@app.route('/edit')
def edit_estudiante():
    return 'edit_estudiante'
@app.route('/delete')
def delet_estudiante():
    return 'delet_estudiante'

if __name__ == '__main__':
        # Run the Flask app on port 3000
    app.run(port=3000, debug = True)