from flask import Flask, make_response 
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from io import BytesIO
import pandas as pd


app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index2.html')   

@app.route('/admin')
def admin():
 if session.get('id_rol') == 1:
    return render_template('admin.html')   
 else:
        return "Acceso no autorizado"
@app.route('/usuario')
def usuario():
    if session.get('id_rol') == 2:
        perfil = obtener_informacion_de_usuario()
        return render_template('usuario.html', usuario=perfil)
    else:
        return "Acceso no autorizado"
       

# ACCESO---LOGIN
@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:

        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

    
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s ', (_correo, _password,))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['Id']=account['Id']
            session['id_rol']=account['id_rol']
     # Obtén información de perfil del usuario
            usuario = obtener_informacion_de_usuario()
            if session['id_rol']== 1:
                return render_template("admin.html")
            elif session ['id_rol']== 2:
                return render_template("usuario.html",usuario=usuario)
        else:
            return render_template('index2.html',mensaje="Usuario O Contraseña Incorrectas")
# Asegúrate de que haya una declaración de retorno para el caso en que no se cumplan las condiciones previas.     
    return render_template('index2.html',)

#registro---
@app.route('/registro')
def registro():
    return render_template('registro.html')  

def obtener_informacion_de_usuario():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM perfil WHERE usuario_id = %s", (session['Id'],))
    usuario = cur.fetchone()
    cur.close()
    return usuario

##perfil
@app.route('/perfil')
def ver_perfil():
    if 'logueado' in session:
        # Obtén el ID del usuario desde la sesión
        usuario_id = session.get('Id')
        # Obtén el nombre del usuario desde la sesión (asegúrate de configurarlo al iniciar sesión)
        nombre_usuario = session.get('nombre_usuario')

        # Realiza una consulta para obtener la información del perfil del usuario
        cur = mysql.connection.cursor()
        cur.execute("SELECT nombre, correo FROM perfil WHERE usuario_id = %s", (usuario_id,))
        perfil = cur.fetchone()
        cur.close()

        if perfil:
            # Si se encontró un perfil, muestra la información en la plantilla
            return render_template('perfil.html', nombre=nombre_usuario, perfil=perfil)
        else:
            # Si no se encontró un perfil, muestra un mensaje o realiza otra acción
            return "Perfil no encontrado"
    else:
        return redirect('/acceso-login')
    
@app.route('/perfill')
def ver_perfill():
    if 'logueado' in session:
        # Obtén el ID del usuario desde la sesión
        usuario_id = session.get('Id')
        # Obtén el nombre del usuario desde la sesión (asegúrate de configurarlo al iniciar sesión)
        nombre_usuario = session.get('nombre_usuario')

        # Realiza una consulta para obtener la información del perfil del usuario
        cur = mysql.connection.cursor()
        cur.execute("SELECT nombre, correo FROM perfil WHERE usuario_id = %s", (usuario_id,))
        perfil = cur.fetchone()
        cur.close()

        if perfil:
            # Si se encontró un perfil, muestra la información en la plantilla
            return render_template('perfill.html', nombre=nombre_usuario, perfil=perfil)
        else:
            # Si no se encontró un perfil, muestra un mensaje o realiza otra acción
            return "Perfil no encontrado"
    else:
        return redirect('/acceso-login')
##editar perfil
@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'logueado' in session:
        if request.method == 'POST':
            # Obtén los datos del formulario enviado por el usuario
            nuevo_nombre = request.form['nuevo_nombre']
            nuevo_correo = request.form['nuevo_correo']
            # Actualiza el perfil del usuario en la base de datos
            cur = mysql.connection.cursor()
            cur.execute("UPDATE perfil SET nombre = %s, correo = %s WHERE usuario_id = %s",
                        (nuevo_nombre, nuevo_correo, session['Id']))
            mysql.connection.commit()
            cur.close()
            return redirect('/perfil')
        else:
            # Carga los datos actuales del perfil del usuario
            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre, correo FROM perfil WHERE usuario_id = %s", (session['Id'],))
            perfil = cur.fetchone()
            cur.close()
            return render_template('editar_perfil.html', perfil=perfil)
    else:
        return redirect('/acceso-login')

## editar contraseña
@app.route('/cambiar_contrasena', methods=['GET', 'POST'])
def cambiar_contrasena():
    if 'logueado' in session:
        if request.method == 'POST':
            # Obtén la contraseña actual y la nueva contraseña del formulario
            contrasena_actual = request.form['contrasena_actual']
            nueva_contrasena = request.form['nueva_contrasena']
            # Verifica la contraseña actual en la base de datos
            cur = mysql.connection.cursor()
            cur.execute("SELECT password FROM usuarios WHERE Id = %s", (session['Id'],))
            usuario = cur.fetchone()
            cur.close()
            if usuario and usuario['password'] == contrasena_actual:
                # Actualiza la contraseña en la base de datos
                cur = mysql.connection.cursor()
                cur.execute("UPDATE usuarios SET password = %s WHERE Id = %s",
                            (nueva_contrasena, session['Id']))
                mysql.connection.commit()
                cur.close()
                return redirect('/perfil')
            else:
                return render_template('cambiar_contrasena.html', error_message="Contraseña actual incorrecta")

        else:
            return render_template('cambiar_contrasena.html')
    else:
        return redirect('/acceso-login')
@app.route('/crear-registro', methods=["GET", "POST"])
def crear_registro():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form and 'rol' in request.form:
        nombre = request.form['txtnombre']
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']
        rol = request.form['rol']

        if not nombre or not correo or not password or not rol:
            mensaje = "Todos los campos son obligatorios."
            return render_template("registro.html", mensaje=mensaje)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (correo, password, id_rol) VALUES (%s, %s, %s)", (correo, password, rol))
        mysql.connection.commit()

        # Obtén el ID del usuario recién insertado
        nuevo_usuario_id = cur.lastrowid

        # Inserta un registro en la tabla de perfil relacionando al usuario con su perfil
        cur.execute("INSERT INTO perfil (usuario_id, nombre, correo, contraseña) VALUES (%s, %s, %s, %s)",
                    (nuevo_usuario_id, nombre, correo, password))
        mysql.connection.commit()

        return render_template("index2.html", mensaje2="Usuario Registrado Exitosamente")
    else:
        return render_template("registro.html", mensaje2="Falta información para el registro")

@app.route('/agregar-persona', methods=['GET', 'POST'])
def agregar_persona():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        rol = request.form['rol']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO perfil (nombre, correo, contraseña, id_rol) VALUES (%s, %s, %s, %s)", (nombre, correo, contraseña, rol))
        mysql.connection.commit()
        # Obtén el ID de la persona recién insertada en la tabla de perfil
        nueva_persona_id = cur.lastrowid
        # Inserta un registro en la tabla de usuarios relacionando la persona con un rol
        cur.execute("INSERT INTO usuarios (correo, password, id_rol) VALUES (%s, %s, %s)", (correo, contraseña, rol))
        mysql.connection.commit()
        # Asocia la persona a su usuario
        cur.execute("UPDATE perfil SET usuario_id = %s WHERE id = %s", (nueva_persona_id, nueva_persona_id))
        mysql.connection.commit()
        return redirect('/listar-usuarios')
    else:
        return render_template('agregar_persona.html', usuario=usuario)

@app.route('/guardar-persona', methods=['POST'])
def guardar_persona():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        id_rol = request.form['id_rol']
        # Insertar en la tabla "usuarios"
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (correo, password, id_rol, nombre) VALUES (%s, %s, %s, %s)",
                    (correo, contraseña, id_rol, nombre))
        mysql.connection.commit()
        # Obtén el ID del usuario recién insertado
        nuevo_usuario_id = cur.lastrowid
        # Insertar en la tabla "perfil"
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO perfil (nombre, correo, contraseña, usuario_id) VALUES (%s, %s, %s, %s)",
                    (nombre, correo, contraseña, nuevo_usuario_id))
        mysql.connection.commit()
        return redirect('/listar-usuarios')
    else:
        return "Método no permitido"
@app.route('/listar-usuarios')
def listar_usuarios():
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    usuarios = cur.fetchall()
    return render_template('listar_usuarios.html', usuarios=usuarios)

#EDITAR USUARIOS
@app.route('/editar-usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if request.method == 'POST':
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']
        nombre = request.form['txtnombre']
        id_rol = request.form['id_rol']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET correo=%s, password=%s, nombre=%s, id_rol=%s WHERE Id=%s",
                    (correo, password, nombre, id_rol, id))
        mysql.connection.commit()

        return redirect('/listar-usuarios')

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE Id = %s', (id,))
    usuario = cur.fetchone()

    return render_template('editar_usuario.html', usuario=usuario)
#ELIMINAR USUARIOS
@app.route('/eliminar-usuario/<int:id>')
def eliminar_usuario(id):
    cur = mysql.connection.cursor()
    # Obtén el ID del usuario que se va a eliminar
    cur.execute('SELECT Id FROM usuarios WHERE Id = %s', (id,))
    usuario = cur.fetchone()
    # Elimina el perfil asociado al usuario
    cur.execute('DELETE FROM perfil WHERE usuario_id = %s', (usuario['Id'],))
    # Luego, elimina el usuario
    cur.execute('DELETE FROM usuarios WHERE Id = %s', (id,))
    mysql.connection.commit()
    return redirect('/listar-usuarios')
def obtener_informacion_de_usuario():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s", (session['Id'],))
    usuario = cur.fetchone()
    cur.close()
    return usuario
@app.route('/activar-usuario/<int:usuario_id>')
def activar_usuario(usuario_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET activo = 1 WHERE Id = %s", (usuario_id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/listar-usuarios')  # Redirige de nuevo a la lista de usuarios

@app.route('/desactivar-usuario/<int:usuario_id>')
def desactivar_usuario(usuario_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET activo = 0 WHERE Id = %s", (usuario_id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/listar-usuarios')  # Redirige de nuevo a la lista de usuarios

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/mediciones')
def mostrar_mediciones():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mediciones")
    mediciones = cur.fetchall()
    cur.close()
    return render_template('mediciones.html', mediciones=mediciones, usuario=usuario)

# Ruta y vista para agregar una medición
@app.route('/agregar_medicion', methods=['GET', 'POST'])
def agregar_medicion():
    if request.method == 'POST':
        puntodemed = request.form['puntodemed']
        medicion = float(request.form['medicion'])
        fecha_tomada = request.form['fecha_tomada']


        # Obtener el usuario_id de la sesión
        usuario_id = session.get('usuario_id', None)

        # Obtener el id_lugar del formulario HTML
        id_lugar = int(request.form['id_lugar'])

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO mediciones (puntodemed, medicion, fecha_tomada, usuario_id, id_lugar) VALUES (%s, %s, %s, %s, %s)',
                       (puntodemed, medicion, fecha_tomada, usuario_id, id_lugar))
        mysql.connection.commit()
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_lugar, nombre, latitud, longitud FROM lugares")
        lugares = cursor.fetchall()
        return render_template('agregar_medicion.html', lugares=lugares)



##Ver medicones    
@app.route('/ver-mediciones-agregadas', methods=['GET'])
def ver_mediciones_agregadas():
    try:
        # Conecta con la base de datos
        cur = mysql.connection.cursor()

        # Realiza una consulta SQL para obtener todas las mediciones
        consulta = "SELECT * FROM mediciones"
        cur.execute(consulta)

        # Obtiene todas las filas resultantes de la consulta
        mediciones = cur.fetchall()

        # Cierra el cursor después de usarlo
        cur.close()

        # Renderiza una plantilla HTML y pasa los datos de las mediciones como argumento
        return render_template('mediciones_agregadas.html', mediciones=mediciones)

    except Exception as e:
        # Maneja errores de conexión a la base de datos u otros errores
        return "Error: " + str(e)

@app.route('/confirmacion-registro')
def confirmacion_registro():
    return render_template('confirmacion_registro.html')
@app.route('/registrar_lugar', methods=['GET', 'POST'])
def registrar_lugar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        latitud = request.form['latitud']
        longitud = request.form['longitud']

        # Conecta con la base de datos
        cur = mysql.connection.cursor()

        # Inserta los datos del lugar en la base de datos (sin especificar el id_lugar)
        cur.execute("INSERT INTO lugares (nombre, latitud, longitud) VALUES (%s, %s, %s)",
                    (nombre, latitud, longitud))
        mysql.connection.commit()

        # Cierra el cursor después de usarlo
        cur.close()

        # Redirige a una página de confirmación o a donde desees
        return redirect(url_for('confirmacion_registro'))

    # Renderiza el formulario para registrar lugares (puede ser un archivo HTML)
    return render_template('registrar_lugar')


@app.route('/generar-informe', methods=['GET'])
def generar_informe():
    # Obtén las mediciones desde la base de datos (ajusta esto según tu estructura de base de datos)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM mediciones")
    mediciones = cursor.fetchall()
    
    # Convierte los datos de mediciones en un DataFrame de pandas
    df = pd.DataFrame(mediciones)

    # Genera el informe en formato CSV y Excel (puedes ajustar los nombres de los archivos)
    csv_file = "reporte_mediciones.csv"
    excel_file = "reporte_mediciones.xlsx"
    
    df.to_csv(csv_file, index=False)
    df.to_excel(excel_file, index=False)

    # Retorna una respuesta que incluye los archivos generados
    response = make_response(render_template('informe.html', csv_file=csv_file, excel_file=excel_file))
    return response
# Ruta para procesar el archivo Excel
@app.route('/procesar-excel', methods=['POST'])
def procesar_excel():
    if 'archivo' not in request.files:
        return 'No se seleccionó ningún archivo.'

    archivo = request.files['archivo']
    if archivo.filename == '':
        return 'No se seleccionó ningún archivo.'

    if archivo:
        # Leer el archivo Excel
        df = pd.read_excel(archivo)

        # Conectar a la base de datos
        cursor = mysql.connection.cursor()

        # Iterar a través de las filas del DataFrame y agregarlas a la base de datos
        for _, row in df.iterrows():
            medicion = row['Medición']
            indice_uv = row['Índice UV']
            fecha = row['Fecha']

            # Agregar la fila a la base de datos
            cursor.execute("INSERT INTO mediciones (medicion, indice_uv, fecha) VALUES (%s, %s, %s)",
                           (medicion, indice_uv, fecha))
            mysql.connection.commit()

        cursor.close()
        return 'Datos del archivo Excel agregados correctamente.'
@app.route('/obtener_datos_temperatura', methods=['GET'])
def obtener_datos_temperatura():
    cur = mysql.connection.cursor()
    cur.execute("SELECT fecha_tomada, medicion, indice_uv FROM mediciones ORDER BY id DESC LIMIT 1")
    datos_temperatura = cur.fetchone()
    cur.close()

    if datos_temperatura:
        fecha = datos_temperatura['fecha']
        medicion = datos_temperatura['medicion']
        indice_uv = datos_temperatura['indice_uv']
    else:
        fecha = 'N/A'
        temperatura = 'N/A'
        indice_uv = 'N/A'

    return {'fecha': fecha, 'medicion': medicion, 'indice_uv': indice_uv}


if __name__ == '__main__':
   app.secret_key = "pinchellave"
   app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)