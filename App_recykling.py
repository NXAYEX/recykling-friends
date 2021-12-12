from flask import Flask , render_template ,request, redirect , url_for, session, flash
from flaskext.mysql import MySQL
import pymysql
import pymysql.cursors

app= Flask(__name__)
try:
	conexion = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='reciclaje')
	print("Conexión a base de datos correcta")
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
	print("Ocurrió un error al conectar: ", e)

@app.route('/', methods=['GET','POST'])
def registrar():
    if request.method=='POST':
        nombre= request.form['nombreregister']
        usuario= request.form['Usuarioregister']
        contrasena=request.form['contrasenaregister']
        with conexion:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO app_reciclaje (nombre, usuario, contrasena) VALUES (%s, %s,%s)"
                cursor.execute(sql, (nombre,usuario, contrasena))
            conexion.commit()
        
    return render_template('registrarse.html')


@app.route("/iniciosesion")
def iniciarsesion():
    return render_template('iniciarsesion.html')
    
@app.route('/inicio')
def inicio():
    return render_template('principal.html')


@app.route('/ranking')
def ranking():
    return render_template('ranking.html')
@app.route('/perfil')
def perfil():
    return render_template('perfil.html')
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




if __name__ == '__main__':
    app.run(port = 2003, debug=True) 
