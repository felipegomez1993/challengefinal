#importo modulos necesarios para la APP
from flask import Flask, request, Response, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util
# para inicializar flask con conexión a MongoDB son necesarias las siguientes lineas
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://root:meli2022@localhost:27017/coleccion?authSource=admin'

mongo = PyMongo(app)

# a continuación se declara las "rutas" que debe de tomar la API dependiendo de las llamadas GET que realicemos

#esta llamada es cuando invocamos a la api solamente con la ruta colección_2022 
@app.route('/coleccion_2022', methods=['GET'])
#en esta funcion no necesito pasarle parametros
def get_librostotales():
    #busco todos los libros de la colección
    libros = mongo.db.Coleccion_2022.find()
    #cuento cuantos existen
    count = 0
    for x in libros:
        count = count + 1
    #convierto la cuenta a una variable compatible con json
    response = json_util.dumps(count)
    #respuesta
    return Response("La cantidad de documentos en la colección es de " + response, mimetype='application/json')

# la siguiente es cuando brindamos a la API ID de Libro, la palabra que queremos contar y "Case sensitive"
@app.route('/coleccion_2022/<idlibro>/<texto>/cs', methods=['GET'])
# en la siguiente funcion traspaso parametros obtenidos en la ruta
def get_libros_porid_texto_cs(idlibro, texto):
    #filtro en la colección por id de libro y la palabra 
    libros = mongo.db.Coleccion_2022.find({"IDLibro": idlibro, "Texto": {"$regex": texto}})
    #convierto a json
    json = json_util.dumps(libros)
    #cuento las veces que figura la palabra en el string json
    conteo = json.count(texto)
    #la variable anterior devuelve tipo entero
    #convierto a string
    response = str(conteo)
    #respuesta
    return Response("La palabra <<< " + texto +" >>> figura:" + response + " cantidad de veces", mimetype='application/json')

# Esta ruta es igual a la anterior pero sin "Case sensitive"
@app.route('/coleccion_2022/<idlibro>/<texto>', methods=['GET'])
def get_libros_porid_texto(idlibro, texto):
    libros = mongo.db.Coleccion_2022.find({"IDLibro": idlibro, "Texto": {"$regex": texto}})
    json = json_util.dumps(libros)
    #a diferencia de la ruta anterior, tomo la variable json y la convierto a todo minusculas
    jsontolower = json.lower() 
    textotolower = texto.lower()
    conteo = jsontolower.count(textotolower)
    response = str(conteo)
    return Response("La palabra <<< " + texto +" >>> figura:" + response + " cantidad de veces", mimetype='application/json')

# la  siguiente ruta es para cuando queremos contar la palabra pero en todas las colecciones
@app.route('/coleccion_2022/<texto>', methods=['GET'])
def get_libros_totales_texto(texto):
    libros = mongo.db.Coleccion_2022.find({"Texto": {"$regex": texto}})
    json = json_util.dumps(libros)
    jsontolower = json.lower() 
    textotolower = texto.lower()
    conteo = jsontolower.count(textotolower)
    response = str(conteo)
    return Response("La palabra <<< " + texto +" >>> figura:" + response + " cantidad de veces", mimetype='application/json')

# igual que la anterior pero con "Case sensitive"
@app.route('/coleccion_2022/<texto>/cs', methods=['GET'])
def get_libros_totales_cs(texto):
    libros = mongo.db.Coleccion_2022.find({"Texto": {"$regex": texto}})
    json = json_util.dumps(libros)
    conteo = json.count(texto)
    response = str(conteo)
    return Response("La palabra <<< " + texto +" >>> figura:" + response + " cantidad de veces", mimetype='application/json')

# esta es la ruta a tomar, cuando la api recibe parametros incorrectos
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        #devuelvo un mensaje sumado a la ruta mal obtenida
        'message': 'los parametros recibidos por API no son validos, los datos recibidos son: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

#sentencia necesaria para la ejecución de la API
if __name__ == "__main__":
    app.run(debug=True)


