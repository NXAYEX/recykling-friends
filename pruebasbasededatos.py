try:
	conexion = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='reciclaje')

    print("Conexión correcta")

except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
    print("Ocurrió un error al conectar: ", e)
    
def insertar_juego(nombre, descripcion, precio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO juegos(nombre, descripcion, precio) VALUES (%s, %s, %s)",
                       (nombre, descripcion, precio))
    conexion.commit()
    conexion.close()

#######


    @app.route('/')
def registrar():
    db = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='reciclaje')
    cursor=db.cursor()
    print("conexión a base de datos correcta")
    sql = "SELECT * FROM app_reciclaje WHERE user="+request.form.get('nombre')+" AND password="+request.form.get('Usuario')+")"
    try:
        # Ejecutar declaración sql
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results)==1:
            return 'Inicio de sesión correcto'
        else:
            return 'Nombre de usuario o contraseña incorrecta'
        # Enviar a la base de datos para su ejecución
        db.commit()
    except:
        # Si ocurre un error, retroceda
        traceback.print_exc()
        db.rollback()
    # Cerrar la conexión a la base de datos
    db.close()
    return render_template('registrarse.html',results=results)


#####
#iniiciar sesion
@application.before_request
def session_management():
  session.permanent = True
@application.route("/iniciosesion")
def login():
  session.clear()
  session["Usuario"] = Usuario
  session["contrasena"] = contrasena
  return index()

       '''
                if result:
                    session.clear()
                    sesion['usuario']=result['usuario']
                    session['id']=result['id']
                    return inicio()
                else:
                    return ("naaa")
                '''
'''
                sql = "SELECT `id`, `usuario` FROM `app_reciclaje` WHERE `usuario`=%s AND 'contrasena'=%s"
                cursor.execute(sql, (usuario,contrasena))
                result = cursor.fetchone()
                if result:
                    session.clear()
                    session["usuario"] = True
                    sesion['id']=result['id']
                    session["contrasena"] = result['contrasena']
                    msg='bienvenido'
                    return inicio()
                else:
                    return("no eres un usuario")
'''
        