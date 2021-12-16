from flask import Flask , render_template ,request, redirect , url_for, session, flash
from flaskext.mysql import MySQL
import pymysql
import pymysql.cursors

app= Flask(__name__)
app.secret_key = "1234"
##CONEXIÓN A LA BASE DE DATOS
try:
	conexion = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='reciclaje')
	print("Conexión a base de datos correcta")
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
	print("Ocurrió un error al conectar: ", e)
#REGISTRO SI ERES NUEVO 
@app.route('/')
def registro():
    return render_template('registrarse.html')
#INSERTAR EN TABLA MYSQL, SE DA UN ID UNICO
@app.route('/', methods=['GET','POST'])
def registrarusu():
    if request.method=='POST':
        nombre= request.form['nombreregister']
        usuario= request.form['Usuarioregister']
        contrasena=request.form['contrasenaregister']
        with conexion:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO app_reciclaje (nombre, usuario, contrasena) VALUES (%s, %s,%s)"
                cursor.execute(sql, (nombre,usuario, contrasena))
            conexion.commit()
            return redirect(url_for('login'))
#SI YA ERES USUARIO, DEBES INICIAR SESIÓN
@app.route("/iniciarsesion")
def login():
    return render_template("iniciarsesion.html")
#ESTE SIRVE PARA MANTENER SESION ABIERTA
@app.before_request
def session_management():
  session.permanent = True
#AHORA OARA INICIAR SESION SE DEBE CORROBORAR EN LA BASE DE DATOS, FALTA LO DEL MENAJE FLASH
@app.route("/iniciarsesion",methods=['GET','POST'])
def iniciarsesion():
    msg=''
    if request.method=='POST':
        usuario=request.form['usuario']
        contrasena=request.form['contrasena']
        with conexion:
            with conexion.cursor() as cursor:
                sql = "SELECT id, usuario, puntos FROM app_reciclaje WHERE contrasena=%s"
                cursor.execute(sql, (contrasena))
                result = cursor.fetchone()
                print(result)
                conexion.commit()
                if result is None:
                    flash("Usuario no existe o contraseña incorrecta","alert-warning")
                    return redirect(url_for(registro))
                else:
                    if usuario==result[1]:
                        session['usuario']= result[1]
                        session['id']=result[0]
                        session['puntos']=result[2]
                        return render_template('principal.html', usuario=session['usuario'], id=session['id'], puntos=session['puntos'])
                    else:
                        return ("Te debes haber equivocado en tu contraseña o usuario")
                
    else:
        return redirect(url_for('login'))
#PAGINA PRINCIPAL, CON EL GOOGLE MAP PERSONALIZADO DE LOS BASUREROS             
@app.route('/inicio',methods=['GET','POST'])
def principal():
    usuario=session['usuario']
    id=session['id']
    puntos=session['puntos']
    return render_template('principal.html', nombre=usuario, id=id ,puntos=session['puntos'])
#puntaje
@app.route('/incrementar',methods=['GET','POST'])
def incremento():
    conexion = pymysql.connect(host='localhost',
                              user='root',
                             password='',
                             db='reciclaje')      
    
    usuario=session['usuario']
    id=session['id']
    with conexion:
        with conexion.cursor() as cursor:
            sql = "SELECT puntos FROM app_reciclaje WHERE id=%s"
            cursor.execute(sql, (id))
            result = cursor.fetchone()
            session['puntos']=result[0]
            puntos=session['puntos']
            i=puntos+1
            sql='UPDATE app_reciclaje SET puntos=%s WHERE usuario=%s AND id=%s'
            cursor.execute(sql,(i,usuario,id))
            result = cursor.fetchone()
            conexion.commit()      
            return render_template('principal.html', puntos=session['puntos'])

###
##aqui hare una lista
@app.route('/ranking')
def ranking():
    return render_template('ranking.html')
#NO ACTUALIZA CORRECTAMENTE LOS PUNTOS
@app.route('/perfil')
def perfil():
    puntos=session['puntos']
    usuario=session['usuario']
    id=session['id']
    return render_template('perfil.html', usuario=session['usuario'], id=session['id'],puntos=session['puntos'])
@app.route('/puntaje')
def puntaje():
    return render_template('puntaje.html')


#basureros
@app.route('/basureroverde')
def basureroverde():
    return render_template('verde.html')

@app.route('/basureroazul')
def basureroazul():
    return render_template('azul.html')

@app.route('/basurerorojo')
def basurerorojo():
    return render_template('rojo.html')

@app.route('/basureroamarillo')
def basureroamarillo():
    return render_template('amarillo.html')
#CERRAR SESION
@app.route("/salir")
def logout():
    session.clear()
    return redirect(url_for('iniciarsesion'))



if __name__ == '__main__':
    app.run(port = 2003, debug=True) 
