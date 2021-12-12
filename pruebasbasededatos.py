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
