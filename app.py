from flask import Flask, request, jsonify #importar librerias
from flask_mysqldb import MySQL #configuracion de la base de datos
from requests import post #configuracion de la base de datos
from sympy import hn1#configuracion de la base de datos

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'#configuracion de la base de datos host
app.config['MYSQL_USER'] = 'bbd292aa23aeaf'#configuracion de la base de datos usuario
app.config['MYSQL_PASSWORD'] = 'ece55924'#configuracion de la base de datos contraseña
app.config['MySQL_DB'] = 'heroku_978ea61906c2949'#configuracion de la base de datos

mysql = MySQL(app) #se usa para mostrar los datos de la tabla vehiculo

def obtener_id(correo): #se usa para mostrar los datos de la tabla persona
    try:
        print(correo)
        cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
        cursor.execute("select Cedula from heroku_978ea61906c2949.usuario where Correo = '{0}' ".format(correo))#se ejecuta la consulta
        datos = cursor.fetchone()
        print(datos[0])
        return datos[0]
    except Exception as e:
        print("no se pudo")
        return False

#leer los vehiculos por el Id_vehiculo
@app.route('/venta/<correo>', methods=['GET'])
def get_vehiculo_venta(correo):#funcion de la pagina leer los vehiculos por el Id_vehiculo
    codigo = obtener_id(correo)
    try:#el try es para que si hay un error no se caiga el programa
        cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
        sql = """select Nombre, Modelo , Tipo, Caracteristica, Precio
                from heroku_978ea61906c2949.vehiculos as vehiculo
                inner join heroku_978ea61906c2949.ventas as venta
                on vehiculo.Id_vehiculo = venta.id_vehiculo
                where venta.id_user =   '{0}' """.format(codigo)
        cursor.execute(sql)#se ejecuta la consulta
        datos = cursor.fetchone()#el fetchone es para que se muestren solo los datos de la consulta
        #imprimiendo todos los datos de la consulta echa
        if datos != None: #en caso de que el codigo no exista
            vehiculo = {'Nombre': datos[0], 'Modelo': datos[1], 'Tipo': datos[2], 'Caracteristica': datos[3], 'Precio': datos[4]}
            print(datos)
            return jsonify({'vehiculo': vehiculo, 'message': 'ok'})#se retorna los datos del vehiculo y un mensaje de ok
        else:#en caso de que no se encuentre el vehiculo se retorna un mensaje de error
            return jsonify({'message': 'error 1'})#en caso de que haya un error se retorna un mensaje de error
    except Exception as e:#el except es para que si hay un error no se caiga el programa
        return jsonify({'message': 'error'})#en caso de que haya un error se retorna un mensaje de error
#funcion para insertar vehiculos a la base de datos    
def insertar_vehiculo(nombre,modelo,caracteristica,precio):
    try:
        cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
        sql = """INSERT INTO heroku_978ea61906c2949.vehiculos(Nombre , Modelo , Tipo , Caracteristica, Precio) 
        VALUES ('{0}','{1}','usado','{2}',{3})""".format(nombre, modelo, caracteristica, precio)
        cursor.execute(sql)#se ejecuta la consulta
        mysql.connection.commit()#guardar los cambios
        return True
    except Exception as e:
        return False
#funcion para insertar ventas a la base de datos    

#extarer el ultimo valor de la base la tabla vehiculos
def extraer():
    try:
        cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
        cursor.execute("select Id_vehiculo from heroku_978ea61906c2949.vehiculos order by Id_vehiculo desc LIMIT 1")#se ejecuta la consulta
        datos = cursor.fetchone()
        return datos[0]
    except Exception as e:
        return False
#registrar un vehiculo
@app.route('/venta/<correo>', methods=['POST'])
def venta_vehiculos(correo):#funcion de la pagina registrar un vehiculo
    cedula = obtener_id(correo)
    cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
    try:# el try es para que si hay un error no se caiga el programa
        if insertar_vehiculo(request.json['Nombre'], request.json['Modelo'], request.json['Caracteristica'], request.json['Precio']) == True:#se inserta el vehiculo
            if extraer() != False:#se extrae el ultimo valor de la tabla vehiculos
                id_vehiculo = extraer()#se guarda el ultimo valor de la tabla vehiculos
                cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
                print("la cedula es: ", cedula, "el tipo es: ",type(cedula) ," el id del vehiculo es: ", id_vehiculo, "el tipo es: ",type(id_vehiculo) )
                insertar = f"INSERT INTO heroku_978ea61906c2949.ventas(id_user , id_vehiculo) VALUES('{cedula}',{id_vehiculo})"#se inserta el id del usuario y el id del vehiculo en la tabla ventas
                cursor.execute(insertar)#se ejecuta la consulta
                mysql.connection.commit()#guardar los cambios    
                return jsonify({'message': 'vehiculo vendido'})#se retorna un mensaje de vehiculo añadido
            return jsonify({'message': 'error 1!'})#en caso de que haya un error se retorna un mensaje de error
        return jsonify({'message': 'error 2!'})#en caso de que haya un error se retorna un mensaje de error
    except Exception as e:#el except es para que si hay un error no se caiga el programa
        return jsonify({'message': 'error 3!'})#en caso de que haya un error se retorna un mensaje de error
    
if __name__ == '__main__':#se ejecuta el programa
    app.run(debug=True, port=5000)#se ejecuta el programa en el puerto 5000 y en modo debug