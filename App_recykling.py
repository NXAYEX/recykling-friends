from flask import Flask , render_template ,request, redirect , url_for, session, flash
from flaskext.mysql import MySQL
import pymysql
import pymysql.cursors

app= Flask(__name__)
app.secret_key = "1234"
##CONEXIÓN A LA BASE DE DATOS
conexion = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='reciclaje')
                           
#REGISTRO SI ERES NUEVO 
@app.route('/')
def registro():
    return render_template('registrarse.html')
#INSERTAR EN TABLA MYSQL, SE DA UN ID UNICO
@app.route('/', methods=['GET','POST'])
def registrarusu():
    conexion = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='reciclaje')
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
#AHORA PARA INICIAR SESION SE DEBE CORROBORAR EN LA BASE DE DATOS, FALTA LO DEL MENAJE FLASH
@app.route("/iniciarsesion",methods=['GET','POST'])
def iniciarsesion():
    conexion = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='reciclaje')
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
                        flash("Te debes haber equivocado en tu contraseña o usuario")

#PAGINA PRINCIPAL, CON EL GOOGLE MAP PERSONALIZADO DE LOS BASUREROS             
@app.route('/inicio',methods=['GET','POST'])
def principal():
    usuario=session['usuario']
    id=session['id']
    puntos=session['puntos']
    return render_template('principal.html', nombre=usuario, id=id ,puntos=session['puntos'])

#INCREMENTAR EL PUNTAJE
@app.route('/incrementar',methods=['GET','POST'])
def incremento():
    conexion = pymysql.connect(host='localhost',
                              user='root',
                             password='',
                             db='reciclaje') 
    usuario=session['usuario']
    id=session['id']
    i=0
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
            flash("lo lograste")    
            return render_template('principal.html', puntos=session['puntos'])

###
##aqui hare una lista
@app.route('/ranking')
def ranking():
    conexion = pymysql.connect(host='localhost',
                              user='root',
                             password='',
                             db='reciclaje') 
    lista=[]
    with conexion:
        with conexion.cursor() as cursor:
            sql = "SELECT usuario,puntos FROM app_reciclaje ORDER BY puntos DESC"
            cursor.execute(sql)
            result = cursor.fetchone() #me devuelve a solo el mayor *llora*
            conexion.commit()
            primero=result[0]
            puntaje=result[1]
            return render_template('ranking.html',primero=primero, puntaje=puntaje)

#NO ACTUALIZA CORRECTAMENTE LOS PUNTOS
@app.route('/perfil')
def perfil():
    conexion = pymysql.connect(host='localhost',
                              user='root',
                             password='',
                             db='reciclaje')
    usuario=session['usuario']
    id=session['id']
    with conexion:
        with conexion.cursor() as cursor:
            sql = "SELECT puntos FROM app_reciclaje WHERE id=%s"
            cursor.execute(sql,(id))
            result = cursor.fetchone()
            puntaje=result[0]
            conexion.commit()
            return render_template('perfil.html', usuario=session['usuario'], id=session['id'],puntaje=puntaje)

#basureros
@app.route('/basureroverde')
def basureroverde():
    usuario=session['usuario']
    id=session['id']
    puntos=session['puntos']
    return render_template('verde.html', usuario=usuario, id=id, puntos=puntos)

@app.route('/basureroazul')
def basureroazul():
    usuario=session['usuario']
    id=session['id']
    puntos=session['puntos']
    return render_template('azul.html',usuario=usuario, id=id, puntos=puntos)

@app.route('/basurerorojo')
def basurerorojo():
    usuario=session['usuario']
    id=session['id']
    puntos=session['puntos']
    return render_template('rojo.html',usuario=usuario, id=id, puntos=puntos)

@app.route('/basureroamarillo')
def basureroamarillo():
    usuario=session['usuario']
    id=session['id']
    puntos=session['puntos']
    return render_template('amarillo.html',usuario=usuario, id=id, puntos=puntos)
#CERRAR SESION
@app.route("/salir")
def logout():
    session.clear()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(port = 2003, debug=True) 
