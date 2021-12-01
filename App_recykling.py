from flask import Flask , render_template
app= Flask(__name__)
#rutas
@app.route("/")
def iniciarsesion():
    return render_template('iniciarsesion.html')
    
@app.route('/inicio')
def inicio():
    return render_template('principal.html')

@app.route('/registro')
def registrar():
    return render_template('registrarse.html')
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
