from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import bcrypt
from functools import wraps

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'DRXENO'
app.config['MYSQL_DB'] = 'sistematitulacion'
app.config['MYSQL_PASSWORD'] = 'DrXeno79TESLA'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

# Decorador para requerir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión primero.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para restringir acceso por rol
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Por favor, inicia sesión primero.', 'danger')
                return redirect(url_for('login'))
            cur = mysql.connection.cursor()
            cur.execute('SELECT Role FROM Users WHERE IdUser = %s', (session['user_id'],))
            user_role = cur.fetchone()[0]
            if user_role not in roles:
                flash('Acceso denegado: No tienes permisos suficientes.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Ruta para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT IdUser, Password, Role FROM Users WHERE Username = %s', (username,))
        user = cur.fetchone()
        
        if user and bcrypt.checkpw(password, user[1].encode('utf-8')):
            session['user_id'] = user[0]
            session['role'] = user[2]
            flash('Inicio de sesión exitoso.', 'success')
            
            if user[2] == 'student':
                return redirect(url_for('estudiante_vista'))
            elif user[2] == 'teacher':
                return redirect(url_for('docentes_vista'))
            elif user[2] == 'admin':
                return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Ruta para registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        email = request.form['email']
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        
        cur = mysql.connection.cursor()
        
        # Validar si el usuario o email ya existe
        cur.execute('SELECT IdUser FROM Users WHERE Username = %s OR Email = %s', (username, email))
        if cur.fetchone():
            flash('El nombre de usuario o correo ya está registrado.', 'danger')
            return redirect(url_for('register'))
        
        if role == 'student':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            codigo_estudiante = request.form['codigo_estudiante']
            telefono = request.form['telefono']
            
            # Insertar en Estudiantes
            cur.execute("INSERT INTO Estudiantes (Nombre, Apellido, CodigoEstudiante, Email, Telefono, EstadoPagos, HabilitadoTitulacion) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (nombre, apellido, codigo_estudiante, email, telefono, 0, 0))
            mysql.connection.commit()
            
            # Obtener el IdEstudiante recién creado
            cur.execute('SELECT IdEstudiante FROM Estudiantes WHERE Email = %s', (email,))
            id_reference = cur.fetchone()[0]
            
        elif role == 'teacher':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            telefono = request.form['telefono']
            habilidades = request.form['habilidades']
            
            # Insertar en Docentes
            cur.execute("INSERT INTO Docentes (Nombre, Apellido, Email, Telefono, Habilidades, HabilitadoGuia, EsJurado) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (nombre, apellido, email, telefono, habilidades, 0, 0))
            mysql.connection.commit()
            
            # Obtener el IdDocente recién creado
            cur.execute('SELECT IdDocente FROM Docentes WHERE Email = %s', (email,))
            id_reference = cur.fetchone()[0]
            
        elif role == 'admin':
            # Para administradores, no se necesita referencia a otra tabla
            id_reference = 0
        
        # Insertar en Users
        cur.execute("INSERT INTO Users (Username, Password, Role, IdReference, Email) VALUES (%s, %s, %s, %s, %s)",
                    (username, hashed_password, role, id_reference, email))
        mysql.connection.commit()
        
        flash('Registro exitoso. Por favor, inicia sesión.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Ruta para logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('login'))

# Páginas (protegidas con login)

@app.route('/docentes_vista')
@login_required
@role_required('admin', 'teacher')
def docentes_vista():
    return render_template('vista_docentes.html')

@app.route('/estudiante_vista')
@login_required
@role_required('admin', 'student')
def estudiante_vista():
    return render_template('vista_estudiantes.html')

@app.route('/')
@login_required
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Estudiantes')
    data = cur.fetchall()
    return render_template('index.html', estudiantes=data)

@app.route('/docentes')
@login_required
def docentes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Docentes')
    data = cur.fetchall()
    return render_template('docentes.html', docentes=data)

@app.route('/pagos')
@login_required
@role_required('admin')
def pagos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Pagos')
    data = cur.fetchall()
    return render_template('pagos.html', pagos=data)

@app.route('/proyectos')
@login_required
@role_required('admin', 'teacher')
def proyectos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Proyectos')
    data = cur.fetchall()
    return render_template('proyectos.html', proyectos=data)

@app.route('/predefensas')
@login_required
@role_required('admin', 'teacher')
def predefensa():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM PreDefensas')
    data = cur.fetchall()
    return render_template('predefensas.html', predefensas=data)

@app.route('/verificaciones')
@login_required
@role_required('admin')
def verificacion():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM VerificacionesSecretaria')
    data = cur.fetchall()
    return render_template('verificaciones.html', verificaciones=data)

@app.route('/cartassolicitudes')
@login_required
@role_required('admin', 'teacher')
def solicitud():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM CartasSolicitud')
    data = cur.fetchall()
    return render_template('cartassolicitud.html', cartassolicitudes=data)

# Guardar
@app.route('/add_estudiante', methods=['POST'])
@login_required
@role_required('admin')
def add_estudiante():
    if request.method == 'POST':
        name = request.form['nombre']
        apellido = request.form['apellido']
        codigo_estudiante = request.form['codigo_estudiante']
        email = request.form['email']
        telefono = request.form['telefono']
        estado_pagos = request.form['estado_pagos']
        habilitado_titulacion = request.form['habilitado_titulacion']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Estudiantes (Nombre, Apellido, CodigoEstudiante, Email, Telefono, EstadoPagos, HabilitadoTitulacion) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, apellido, codigo_estudiante, email, telefono, estado_pagos, habilitado_titulacion))
        mysql.connection.commit()
        flash('Estudiante agregado correctamente', 'success')
        return redirect(url_for('index'))

@app.route('/add_docente', methods=['POST'])
@login_required
@role_required('admin')
def add_docente():
    if request.method == 'POST':
        name = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        habilidades = request.form['habilidades']
        habilitadoGuia = request.form['habilitado_guia']
        esJurado = request.form['es_jurado']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Docentes (Nombre, Apellido, Email, Telefono, Habilidades, HabilitadoGuia, EsJurado) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, apellido, email, telefono, habilidades, habilitadoGuia, esJurado))
        mysql.connection.commit()
        flash('Docente agregado correctamente', 'success')
        return redirect(url_for('docentes'))

@app.route('/add_pago', methods=['POST'])
@login_required
@role_required('admin')
def add_pago():
    if request.method == 'POST':
        IdEstudiante = request.form['idestudiante']
        fecha_pago = request.form['fecha_pago']
        monto = request.form['monto']
        comprobante = request.form['comprobante']
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Pagos (IdEstudiante, FechaPago, Monto, Comprobante, Estado) VALUES (%s, %s, %s, %s, %s)",
                    (IdEstudiante, fecha_pago, monto, comprobante, estado))
        mysql.connection.commit()
        flash('Pago agregado correctamente', 'success')
        return redirect(url_for('pagos'))

@app.route('/add_proyecto', methods=['POST'])
@login_required
@role_required('admin', 'teacher')
def add_proyecto():
    if request.method == 'POST':
        id_estudiante = request.form['idestudiante']
        id_docenteguia = request.form['iddocenteguia']
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_inicio = request.form['fechainicio']
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Proyectos (IdEstudiante, IdDocenteGuia, Titulo, Descripcion, FechaInicio, Estado) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id_estudiante, id_docenteguia, titulo, descripcion, fecha_inicio, estado))
        mysql.connection.commit()
        flash('Proyecto agregado correctamente', 'success')
        return redirect(url_for('proyectos'))

@app.route('/add_predefensa', methods=['POST'])
@login_required
@role_required('admin', 'teacher')
def add_predefensa():
    if request.method == 'POST':
        id_proyecto = request.form['idproyecto']
        fecha_programada = request.form['fechaprogramada']
        reunion = request.form['enlacereunion']
        estado = request.form['estado']
        observaciones = request.form['observaciones']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO PreDefensas (IdProyecto, FechaProgramada, EnlaceReunion, Estado, Observaciones) VALUES (%s, %s, %s, %s, %s)",
                    (id_proyecto, fecha_programada, reunion, estado, observaciones))
        mysql.connection.commit()
        flash('Predefensa agregada correctamente', 'success')
        return redirect(url_for('predefensa'))

@app.route('/add_verificacion', methods=['POST'])
@login_required
@role_required('admin')
def add_verificacion():
    if request.method == 'POST':
        id_carta = request.form['idcarta']
        fecha_verificacion = request.form['fechaverificacion']
        docente_habilitado = request.form['docentehabilitado']
        docente_jurado = request.form['docentesjurado']
        observaciones = request.form['observaciones']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO VerificacionesSecretaria (IdCarta, FechaVerificacion, DocenteHabilitado, DocenteEsJurado, Observaciones) VALUES (%s, %s, %s, %s, %s)",
                    (id_carta, fecha_verificacion, docente_habilitado, docente_jurado, observaciones))
        mysql.connection.commit()
        flash('Verificación agregada correctamente', 'success')
        return redirect(url_for('verificacion'))

@app.route('/add_cartassolicitud', methods=['POST'])
@login_required
@role_required('admin', 'teacher')
def add_solicitud():
    if request.method == 'POST':
        id_estudiante = request.form['idestudiante']
        id_docente = request.form['iddocente']
        fecha_presentacion = request.form['fechapresentacion']
        estado = request.form['estado']
        contenido = request.form['contenido']
        firma_digital_estudiante = request.form['firmadigitalestudiante']
        firma_digital_docente = request.form['firmadigitaldocente']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO CartasSolicitud (IdEstudiante, IdDocente, FechaPresentacion, Estado, Contenido, FirmaDigitalEstudiante, FirmaDigitalDocente) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (id_estudiante, id_docente, fecha_presentacion, estado, contenido, firma_digital_estudiante, firma_digital_docente))
        mysql.connection.commit()
        flash('Solicitud agregada correctamente', 'success')
        return redirect(url_for('solicitud'))

# Editar
@app.route('/edit/<id>')
@login_required
@role_required('admin')
def get_estudiante(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Estudiantes WHERE IdEstudiante = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_Estudiante.html', estudiante=data[0])

@app.route('/docentes/edit_docente/<id>')
@login_required
@role_required('admin')
def get_docente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Docentes WHERE IdDocente = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_docente.html', docente=data[0])

@app.route('/pagos/edit_pago/<id>')
@login_required
@role_required('admin')
def get_pago(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Pagos WHERE IdPago = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_pago.html', pago=data[0])

@app.route('/proyectos/edit_proyecto/<id>')
@login_required
@role_required('admin', 'teacher')
def get_proyecto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Proyectos WHERE IdProyecto = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_proyecto.html', proyecto=data[0])

@app.route('/predefensas/edit_predefensa/<id>')
@login_required
@role_required('admin', 'teacher')
def get_predefensa(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM PreDefensas WHERE IdPreDefensa = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_predefensa.html', predefensa=data[0])

@app.route('/cartassolicitud/edit_cartassolicitud/<id>')
@login_required
@role_required('admin', 'teacher')
def get_solicitud(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM CartasSolicitud WHERE IdCarta = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_cartassolicitud.html', cartassolicitud=data[0])

@app.route('/verificaciones/edit_verificacion/<id>')
@login_required
@role_required('admin')
def get_verificacion(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM VerificacionesSecretaria WHERE IdVerificacion = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_verificacion.html', verificacion=data[0])

# Actualizar
@app.route('/update/<id>', methods=['POST'])
@login_required
@role_required('admin')
def update_estudiante(id):
    if request.method == 'POST':
        name = request.form['nombre']
        apellido = request.form['apellido']
        codigo_estudiante = request.form['codigo_estudiante']
        email = request.form['email']
        telefono = request.form['telefono']
        estado_pagos = request.form['estado_pagos']
        habilitado_titulacion = request.form['habilitado_titulacion']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE Estudiantes SET Nombre = %s, Apellido = %s, CodigoEstudiante = %s, Email = %s, Telefono = %s, EstadoPagos = %s, HabilitadoTitulacion = %s WHERE IdEstudiante = %s""",
                    (name, apellido, codigo_estudiante, email, telefono, estado_pagos, habilitado_titulacion, id))
        mysql.connection.commit()
        flash('Estudiante actualizado correctamente', 'success')
        return redirect(url_for('index'))

@app.route('/docentes/update_docente/<id>', methods=['POST'])
@login_required
@role_required('admin')
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
        cur.execute("""UPDATE Docentes SET Nombre = %s, Apellido = %s, Email = %s, Telefono = %s, Habilidades = %s, HabilitadoGuia = %s, EsJurado = %s WHERE IdDocente = %s""",
                    (name, apellido, email, telefono, habilidades, habilitado_guia, es_jurado, id))
        mysql.connection.commit()
        flash('Docente actualizado correctamente', 'success')
        return redirect(url_for('docentes'))

@app.route('/pagos/update_pago/<id>', methods=['POST'])
@login_required
@role_required('admin')
def update_pago(id):
    if request.method == 'POST':
        IdEstudiante = request.form['idestudiante']
        fecha_pago = request.form['fechapago']
        monto = request.form['monto']
        comprobante = request.form['comprobante']
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE Pagos SET IdEstudiante = %s, FechaPago = %s, Monto = %s, Comprobante = %s, Estado = %s WHERE IdPago = %s""",
                    (IdEstudiante, fecha_pago, monto, comprobante, estado, id))
        mysql.connection.commit()
        flash('Pago actualizado correctamente', 'success')
        return redirect(url_for('pagos'))

@app.route('/proyectos/update_proyecto/<id>', methods=['POST'])
@login_required
@role_required('admin', 'teacher')
def update_proyecto(id):
    if request.method == 'POST':
        idestudiante = request.form['idestudiante']
        id_docenteguia = request.form['iddocenteguia']
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_inicio = request.form['fechainicio']
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE Proyectos SET IdEstudiante = %s, IdDocenteGuia = %s, Titulo = %s, Descripcion = %s, FechaInicio = %s, Estado = %s WHERE IdProyecto = %s""",
                    (idestudiante, id_docenteguia, titulo, descripcion, fecha_inicio, estado, id))
        mysql.connection.commit()
        flash('Proyecto actualizado correctamente', 'success')
        return redirect(url_for('proyectos'))

@app.route('/predefensas/update_predefensa/<id>', methods=['POST'])
@login_required
@role_required('admin', 'teacher')
def update_predefensa(id):
    if request.method == 'POST':
        id_proyecto = request.form['idproyecto']
        fecha_programada = request.form['fechaprogramada']
        reunion = request.form['enlacereunion']
        estado = request.form['estado']
        observaciones = request.form['observaciones']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE PreDefensas SET IdProyecto = %s, FechaProgramada = %s, EnlaceReunion = %s, Estado = %s, Observaciones = %s WHERE IdPreDefensa = %s""",
                    (id_proyecto, fecha_programada, reunion, estado, observaciones, id))
        mysql.connection.commit()
        flash('Predefensa actualizada correctamente', 'success')
        return redirect(url_for('predefensa'))

@app.route('/verificaciones/update_verificacion/<id>', methods=['POST'])
@login_required
@role_required('admin')
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
        flash('Verificación actualizada correctamente', 'success')
        return redirect(url_for('verificacion'))

@app.route('/cartassolicitud/update_cartassolicitud/<id>', methods=['POST'])
@login_required
@role_required('admin', 'teacher')
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
        cur.execute("""UPDATE CartasSolicitud SET IdEstudiante = %s, IdDocente = %s, FechaPresentacion = %s, Estado = %s, Contenido = %s, FirmaDigitalEstudiante = %s, FirmaDigitalDocente = %s WHERE IdCarta = %s""",
                    (id_estudiante, id_docente, fecha_presentacion, estado, contenido, firma_estudiante, firma_docente, id))
        mysql.connection.commit()
        flash('Solicitud actualizada correctamente', 'success')
        return redirect(url_for('solicitud'))

# Eliminar
@app.route('/delete/<string:id>')
@login_required
@role_required('admin')
def delete_estudiante(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Estudiantes WHERE IdEstudiante = %s', (id,))
    mysql.connection.commit()
    flash('Estudiante eliminado correctamente', 'success')
    return redirect(url_for('index'))

@app.route('/docentes/delete_docente/<string:id>')
@login_required
@role_required('admin')
def delete_docente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Docentes WHERE IdDocente = %s', (id,))
    mysql.connection.commit()
    flash('Docente eliminado correctamente', 'success')
    return redirect(url_for('docentes'))

@app.route('/pagos/delete_pagos/<string:id>')
@login_required
@role_required('admin')
def delete_pagos(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Pagos WHERE IdPago = %s', (id,))
    mysql.connection.commit()
    flash('Pago eliminado correctamente', 'success')
    return redirect(url_for('pagos'))

@app.route('/proyectos/delete_proyecto/<string:id>')
@login_required
@role_required('admin', 'teacher')
def delete_proyecto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Proyectos WHERE IdProyecto = %s', (id,))
    mysql.connection.commit()
    flash('Proyecto eliminado correctamente', 'success')
    return redirect(url_for('proyectos'))

@app.route('/predefensas/delete_predefensa/<string:id>')
@login_required
@role_required('admin', 'teacher')
def delete_predefensa(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM PreDefensas WHERE IdPreDefensa = %s', (id,))
    mysql.connection.commit()
    flash('Predefensa eliminada correctamente', 'success')
    return redirect(url_for('predefensa'))

@app.route('/verificaciones/delete_verificacion/<string:id>')
@login_required
@role_required('admin')
def delete_verificacion(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM VerificacionesSecretaria WHERE IdVerificacion = %s', (id,))
    mysql.connection.commit()
    flash('Verificación eliminada correctamente', 'success')
    return redirect(url_for('verificacion'))

@app.route('/cartassolicitud/delete_cartassolicitud/<string:id>')
@login_required
@role_required('admin', 'teacher')
def delete_solicitud(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM CartasSolicitud WHERE IdCarta = %s', (id,))
    mysql.connection.commit()
    flash('Solicitud eliminada correctamente', 'success')
    return redirect(url_for('solicitud'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)