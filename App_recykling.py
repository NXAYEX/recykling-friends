from flask import Flask , render_template
app= Flask(__name__)
#rutas
@app.route("/")
def ruta1():
    return render_template('principal.html')

@app.route('/basureroverde')
def basureroverde():
    return 'El contenedor verde, también conocido como iglú verde, es el destinado para depositar vidrio. En esta categoría deben reciclarse las botellas de vidrio, tarros, trozos de espejos y cristales rotos, entre otros.'

@app.route('/basureroazul')
def basureroazul():
    return 'El contenedor azul es el correspondiente para depositar papel y cartón. Este tipo de contenedores está diseñado para almacenar cualquier tipo de cartón procedente de cajas, envases de cartón y cualquier tipo de papel como periódicos, revistas, documentos, folletos, papeles de envolver, pancartas de publicación, entre otros. Es importante plegar las cajas de cartón antes de depositarlas en el contenedor azul para que ocupen el menor espacio posible y den cabida a más material para reciclar.'
@app.route('/basurerorojo')
def basurerorojo():
    return 'El contenedor rojo es más especial, no se suele encontrar en los núcleos urbanos con frecuencia, y es el destinado a contener residuos tóxicos y peligrosos, como desechos hospitalarios o baterías. Cuando se habla del contenedor de color rojo, principalmente se están hablando de desechos peligrosos. Entre los desechos que se incluyen en esta categoría se encuentran: desechos hospitalarios, baterías, pilas, insecticidas, aerosoles, aceites o productos tecnológicos.'
@app.route('/basureroamarillo')
def basureroamarillo():
    return 'El contenedor amarillo es el adecuado para reciclar plásticos, latas y envases. En este tipo de contenedores se debe almacenar todo material que esté hecho a base de plástico. Como botellas de plástico, envases de alimentos, bolsas de plástico, briks de leche, etc. También las latas de conserva y de refrescos deben depositarse en el contenedor amarillo.'

@app.route('/registro')
def registrar():
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(port = 2003, debug=True) 
