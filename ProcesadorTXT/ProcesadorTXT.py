#importamos las funciones necesarias para la ejecucion
from pymongo import MongoClient
import glob, os
try:
    # ruta definida para la coleccion de datos
    os.chdir("coleccion_2022")
except:
    print("No se pudo acceder a la colección")
    print("Debe existir en la raiz una carpeta coleccion_2022")
try:
    # conexion con mongoDB, definición de DB y coleccion
    client = MongoClient('localhost', port=27017, username = 'root', password ='meli2022')
    db = client['coleccion']
    collection = db['Coleccion_2022']
    txtcargados = 0
except:
    print("No se pudo conectar con la MongoDB")
try:
        # recorremos todo el directorio de la colección tomando los .txt que cumplan con la nomeclatura 999-999
        for file in glob.glob("*-*.txt"):
            # cargo la variable idlibro con el nombre del archivo
            idlibro= file 
            # le quito la extensión para poder guardar como numero identificativo en la DB
            idsinext = idlibro.replace(".txt","") 
            # busco en la DB si existe ese numero de ID
            find = {"IDLibro": idsinext}
            existe = collection.find(find)
            resultado = list(existe)
            # Si no existe ese id proceso a impactar en la base de datos
            if len(resultado)==0:
                # leo el txt y lo cargo dentro de una variable
                with open(file, 'r', encoding= "utf8") as file:
                    data = file.read()
                #procedo a impactar en la DB guardando el ID relacionado con la información contenida en los TXT 
                insert = {"IDLibro": idsinext, "Texto": data }
                collection.insert_one(insert)
                #cuento la cantidad de TXT que fueron cargados para informar en la salida estandard
                txtcargados = txtcargados + 1
        print("Se cargaron " + str(txtcargados) + " TXT nuevos a mongoDB")
except:
    print("Hubo un error en la ejecución del codigo")