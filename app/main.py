from flask import Flask, request, render_template, jsonify
from confiDB import connectionBD  # Importando conexión BD
from main2 import enviar_a_arduino, enviar_a_abrir_arduino
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('public/index.html')

@app.route('/form', methods=['GET', 'POST'])
def registrarForm():
    msg = ''
    if request.method == 'POST':
        nombre = request.form['nombre']
        sexo = request.form['sexo']

        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor()

        # Insertar el nuevo usuario
        sql = "INSERT INTO registro_huella(nombre, sexo) VALUES (%s, %s)"
        valores = (nombre, sexo)
        cursor.execute(sql, valores)
        conexion_MySQLdb.commit()

        # Obteniendo el ID del último usuario registrado
        ultimo_id = cursor.lastrowid
        print("1 registro insertado, id:", ultimo_id)

        # Intentar registrar la huella dactilar
        success = enviar_a_arduino(1, ultimo_id)
        
        if not success:
            # Eliminar el usuario si la huella dactilar no se registró correctamente
            sql_delete = "DELETE FROM registro_huella WHERE id_usuario = %s"
            cursor.execute(sql_delete, (ultimo_id,))
            conexion_MySQLdb.commit()
            msg = 'Error al registrar la huella dactilar. Usuario eliminado.'
        else:
            msg = 'Registro con éxito'

        cursor.close()  # Cerrando conexión SQL
        conexion_MySQLdb.close()  # Cerrando conexión de la BD
        
        return render_template('public/index.html', msg=msg)
    else:
        return render_template('public/index.html', msg='Método HTTP incorrecto')

@app.route('/abrir_puerta', methods=['POST'])
def abrir_puerta():
    id_encontrado = enviar_a_abrir_arduino(2)  # Suponiendo que 2 es el comando para abrir la puerta
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()

    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.now()
    fecha_actual = fecha_hora_actual.date()
    hora_actual = fecha_hora_actual.time()

    # Insertar en la tabla de registro de asistencia
    sql = "INSERT INTO registro_asistencia(id_usuario, fecha, hora) VALUES (%s, %s, %s)"
    valores = (id_encontrado, fecha_actual, hora_actual)
    cursor.execute(sql, valores)
    conexion_MySQLdb.commit()

    cursor.close()  # Cerrando conexión SQL
    conexion_MySQLdb.close()  # Cerrando conexión de la BD

    if id_encontrado is not None:
        return jsonify({'status': 'success', 'message': 'Acceso permitido, abriendo puerta', 'id': id_encontrado})
    else:
        return jsonify({'status': 'error', 'message': 'error al tratar de reconocer una huella, inténtelo de nuevo'})

@app.route('/mostrar_registro_huella')
def mostrar_registro_huella():
    conexion_MySQLdb = connectionBD()
    cursor =conexion_MySQLdb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM registro_huella")
    registros = cursor.fetchall()
    cursor.close()
    conexion_MySQLdb.close()
    return render_template('public/registro_huella.html', registros=registros)

@app.route('/mostrar_registro_asistencia')
def mostrar_registro_asistencia():
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM registro_asistencia")
    registros = cursor.fetchall()
    cursor.close()
    conexion_MySQLdb.close()
    return render_template('public/registro_asistencia.html', registros=registros)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
