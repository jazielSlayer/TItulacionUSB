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
    return render_template('docentes.html', docentes = data)

@app.route('/pagos')
def pagos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pagos')
    data = cur.fetchall()
    print(data)
    return render_template('pagos.html', pagos = data)

@app.route('/proyectos')
def proyectos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyectos')
    data = cur.fetchall()
    print(data)
    return render_template('proyectos.html', proyectos = data)

@app.route('/predefensas')
def predefensa():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM predefensas')
    data = cur.fetchall()
    print(data)
    return render_template('predefensas.html', predefensas = data)

@app.route('/verificaciones')
def verificacion():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM VerificacionesSecretaria')
    data = cur.fetchall()
    print(data)
    return render_template('verificaciones.html', verificaciones = data)

@app.route('/cartassolicitudes')
def solicitud():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM CartasSolicitud')
    data = cur.fetchall()
    print(data)
    return render_template('cartassolicitud.html', cartassolicitudes = data)

#Guardar////////////////
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
    
@app.route('/add_docente', methods=['POST'])
def add_docente():
    if request.method == 'POST':
        name = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        habilidades = request.form['habilidades']
        habilitadoGuia = request.form['habilitado_guia']
        esJurado = request.form['es_jurado']
        print(name, apellido, email, telefono, habilidades, habilitadoGuia, esJurado)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO docentes (nombre, apellido, email, telefono, Habilidades, HabilitadoGuia, EsJurado) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, apellido, email, telefono, habilidades, habilitadoGuia, esJurado))
        mysql.connection.commit()
        flash('Docente agregado correctamente')
        return redirect(url_for('docentes'))
    
@app.route('/add_pago', methods=['POST'])
def add_pago():
    if request.method == 'POST':
        IdEstudiante = request.form['idestudiante']
        fecha_pago = request.form['fecha_pago']
        monto = request.form['monto']
        comprobante = request.form['comprobante']
        estado = request.form['estado']
        print(IdEstudiante, fecha_pago, monto, comprobante, estado)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pagos (IdEstudiante, FechaPago, Monto, Comprobante, Estado) VALUES (%s, %s, %s, %s, %s)", (IdEstudiante, fecha_pago, monto, comprobante, estado))
        mysql.connection.commit()
        flash('Pago agregado correctamente')
        return redirect(url_for('pagos'))

@app.route('/add_proyecto', methods=['POST'])
def add_proyecto():
    if request.method == 'POST':
        id_estudiante = request.form['idestudiante']
        id_docenteguia = request.form['iddocenteguia']
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_inicio = request.form['fechainicio']
        estado = request.form['estado']
        print(id_estudiante, id_docenteguia, titulo, descripcion, fecha_inicio, estado)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO proyectos (IdEstudiante, IdDocenteGuia, Titulo, Descripcion, FechaInicio, Estado) VALUES (%s, %s, %s, %s, %s, %s)", (id_estudiante, id_docenteguia, titulo, descripcion, fecha_inicio, estado))
        mysql.connection.commit()
        flash('Proyecto agregado correctamente')
        return redirect(url_for('proyectos'))

@app.route('/add_predefensa', methods=['POST'])
def add_predefensa():
    if request.method == 'POST':
        id_proyecto = request.form['idproyecto']
        fecha_programada = request.form['fechaprogramada']
        reunion = request.form['enlacereunion']
        estado = request.form['estado']
        observaciones = request.form['observaciones']
        print(id_proyecto, fecha_programada, reunion, estado, observaciones)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO PreDefensas (IdProyecto, FechaProgramada, EnlaceReunion, Estado, Observaciones) VALUES (%s, %s, %s, %s, %s)", (id_proyecto, fecha_programada, reunion, estado, observaciones))
        mysql.connection.commit()
        flash('Predefensa agregado correctamente')
        return redirect(url_for('predefensas'))

@app.route('/add_verificacion', methods=['POST'])
def add_verificacion():
    if request.method == 'POST':
        id_carta = request.form['idcarta']
        fecha_verificacion = request.form['fechaverificacion']
        docente_habilitado = request.form['docentehabilitado']
        docente_jurado = request.form['docentesjurado']
        observaciones = request.form['observaciones']
        print(id_carta, fecha_verificacion, docente_habilitado, docente_jurado, observaciones)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO VerificacionesSecretaria (IdCarta, FechaVerificacion, DocenteHabilitado, DocenteEsJurado, Observaciones) VALUES (%s, %s, %s, %s, %s)", (id_carta, fecha_verificacion, docente_habilitado, docente_jurado, observaciones))
        mysql.connection.commit()
        flash('Verificacion agregado correctamente')
        return redirect(url_for('verificacion'))

@app.route('/add_cartassolicitud', methods=['POST'])
def add_solicitud():
    if request.method == 'POST':
        id_estudiante = request.form['idestudiante']
        id_docente = request.form['iddocente']
        fecha_presentacion = request.form['fechapresentacion']
        estado = request.form['estado']
        contenido = request.form['contenido']
        firma_digital_estudiante = request.form['firmadigitalestudiante']
        firma_digital_docente = request.form['firmadigitaldocente']
        print(id_estudiante, id_docente, fecha_presentacion, estado, contenido, firma_digital_estudiante, firma_digital_docente)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO CartasSolicitud (IdEstudiante, IdDocente, FechaPresentacion, Estado, Contenido, FirmaDigitalEstudiante, FirmaDigitalDocente) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id_estudiante, id_docente, fecha_presentacion, estado, contenido, firma_digital_estudiante, firma_digital_docente))
        mysql.connection.commit()
        flash('Verificacion agregado correctamente')
        return redirect(url_for('solicitud'))


#editar//////////////
@app.route('/edit/<id>')
def get_estudiante(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM estudiantes WHERE idEstudiante = %s', (id))
    data = cur.fetchall()
    return render_template('edit_Estudiante.html', estudiante = data[0])

@app.route('/docentes/edit_docente/<id>')
def get_docente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM docentes WHERE idDocente = %s', (id))
    data = cur.fetchall()
    return render_template('edit_docente.html', docente = data[0])

@app.route('/pagos/edit_pago/<id>')
def get_pago(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pagos WHERE IdPago = %s', (id))
    data = cur.fetchall()
    return render_template('edit_pago.html', pago = data[0])

@app.route('/proyectos/edit_proyecto/<id>')
def get_proyecto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyectos WHERE IdProyecto = %s', (id))
    data = cur.fetchall()
    return render_template('edit_proyecto.html', proyecto = data[0])

@app.route('/predefensas/edit_predefensa/<id>')
def get_predefensa(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM PreDefensas WHERE IdPreDefensa = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_predefensa.html', predefensa = data[0])

@app.route('/cartassolicitud/edit_cartassolicitud/<id>')
def get_solicitud(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM CartasSolicitud WHERE IdCarta = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_cartassolicitud.html', cartassolicitud = data[0])

@app.route('/verificaciones/edit_verificacion/<id>')
def get_verificacion(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM VerificacionesSecretaria WHERE IdVerificacion = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_verificacion.html', verificacion = data[0])

#actualisar/////////////////////////////
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

@app.route('/docentes/update_docente/<id>', methods=['POST'])
def update_docente(id):
    if request.method == 'POST':
        name = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        habilidades = request.form['habilidades']
        habilitado_guia = request.form['habilitado_guia']
        es_jurado = request.form['es_jurado']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE docentes SET nombre = %s, apellido = %s, email = %s, telefono = %s, Habilidades = %s, HabilitadoGuia = %s, EsJurado = %s WHERE idDocente = %s""",
                (name, apellido, email, telefono, habilidades, habilitado_guia, es_jurado, id))
    mysql.connection.commit()
    flash('Docente actualizado correctamente')
    return redirect(url_for('docentes'))

@app.route('/pagos/update_pago/<id>', methods=['POST'])
def update_pago(id):
    if request.method == 'POST':
        IdEstudiante = request.form['idestudiante']
        fecha_pago = request.form['fechapago']
        monto = request.form['monto']
        comprobante = request.form['comprobante']
        estado = request.form['estado']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE pagos SET IdEstudiante = %s, FechaPago = %s, Monto = %s, Comprobante = %s, Estado = %s WHERE IdPago = %s""",
                (IdEstudiante, fecha_pago, monto, comprobante, estado, id))
    mysql.connection.commit()
    flash('Pago actualizado correctamente')
    return redirect(url_for('pagos'))

@app.route('/proyectos/update_proyecto/<id>', methods=['POST'])
def update_proyecto(id):
    if request.method == 'POST':
        idestudiante = request.form['idestudiante']
        id_docenteguia = request.form['iddocenteguia']
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_inicio = request.form['fechainicio']
        estado = request.form['estado']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE proyectos SET IdEstudiante = %s, IdDocenteGuia = %s, Titulo = %s, Descripcion = %s, FechaInicio = %s, Estado = %s WHERE IdProyecto = %s""",
                (idestudiante, id_docenteguia, titulo, descripcion, fecha_inicio, estado, id))
    mysql.connection.commit()
    flash('Proyecto actualizado correctamente')
    return redirect(url_for('proyectos'))

@app.route('/predefensas/update_predefensa/<id>', methods=['POST'])
def update_predefensa(id):
    if request.method == 'POST':
        id_proyecto = request.form['idproyecto']
        fecha_programada = request.form['fechaprogramada']
        reunion = request.form['enlacereunion']
        estado = request.form['estado']
        observaciones = request.form['observaciones']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE predefensas SET IdProyecto = %s, FechaProgramada = %s, EnlaceReunion = %s, Estado = %s, Observaciones = %s WHERE IdPredefensa = %s""",
                (id_proyecto, fecha_programada, reunion, estado, observaciones, id))
    mysql.connection.commit()
    flash('Predefensa actualizada correctamente')
    return redirect(url_for('predefensa'))

@app.route('/verificaciones/update_verificacion/<id>', methods=['POST'])
def update_verificacion(id):
    if request.method == 'POST':
        id_carta = request.form['idcarta']
        fecha_verificacion = request.form['fechaverificacion']
        docente_habilitado = request.form['docentehabilitado']
        docente_jurado = request.form['docenteesjurado']
        observaciones = request.form['observaciones']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE VerificacionesSecretaria SET IdCarta = %s, FechaVerificacion = %s, DocenteHabilitado = %s, DocenteEsJurado = %s, Observaciones = %s WHERE IdVerificacion = %s""",
                (id_carta, fecha_verificacion, docente_habilitado, docente_jurado, observaciones, id))
    mysql.connection.commit()
    flash('Verificacion actualizada correctamente')
    return redirect(url_for('verificacion'))

@app.route('/cartassolicitud/update_cartassolicitud/<id>', methods=['POST'])
def update_solicitud(id):
    if request.method == 'POST':
        id_estudiante = request.form['idestudiante']
        id_docente = request.form['iddocente']
        fecha_presentacion = request.form['fechapresentacion']	
        estado = request.form['estado']
        contenido = request.form['contenido']
        firma_estudiante = request.form['firmadigitalestudiante']
        firma_docente = request.form['firmadigitaldocente']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE CartasSolicitud SET IdEstudiante = %s, IdDocente = %s, FechaPresentacion = %s, Estado = %s, Contenido = %s, FirmaDigitalEstudiante = %s, FirmaDigitalDocente  = %s WHERE IdCarta = %s""",
                (id_estudiante, id_docente, fecha_presentacion, estado, contenido,firma_estudiante, firma_docente, id))
    mysql.connection.commit()
    flash('Solicitud actualizada correctamente')
    return redirect(url_for('solicitud'))

#Eliminar//////////////////////////
@app.route('/delete/<string:id>')
def delet_estudiante(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM estudiantes WHERE idEstudiante = {0}'.format(id))
    mysql.connection.commit()
    flash('Estudiante eliminado correctamente')
    return redirect(url_for('index'))
@app.route('/docentes/delete_docente/<string:id>')
def delet_docente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM docentes WHERE IdDocente = {0}'.format(id))
    mysql.connection.commit()
    flash('Docente eliminado correctamente')
    return redirect(url_for('docentes'))

@app.route('/pagos/delete_pagos/<string:id>')
def delet_pagos(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pagos WHERE IdPago = {0}'.format(id))
    mysql.connection.commit()
    flash('Pago eliminado correctamente')
    return redirect(url_for('pagos'))

@app.route('/proyectos/delete_proyecto/<string:id>')
def delet_proyecto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM proyectos WHERE IdProyecto = {0}'.format(id))
    mysql.connection.commit()
    flash('Proyecto eliminado correctamente')
    return redirect(url_for('proyectos'))

@app.route('/predefensas/delete_predefensa/<string:id>')
def delet_predefensa(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM predefensas WHERE IdPredefensa = {0}'.format(id))
    mysql.connection.commit()
    flash('Predefensa eliminada correctamente')
    return redirect(url_for('predefensa'))

@app.route('/verificaciones/delete_verificacion/<string:id>')
def delet_verificacion(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM VerificacionesSecretaria WHERE IdVerificacion = {0}'.format(id))
    mysql.connection.commit()
    flash('Verificacion eliminada correctamente')
    return redirect(url_for('verificacion'))

@app.route('/cartassolicitud/delete_cartassolicitud/<string:id>')
def delet_dolicitud(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM CartasSolicitud WHERE IdCarta = {0}'.format(id))
    mysql.connection.commit()
    flash('Solicitud eliminada correctamente')
    return redirect(url_for('solicitud'))


if __name__ == '__main__':
        # Run the Flask app on port 3000
    app.run(port=3000, debug = True)