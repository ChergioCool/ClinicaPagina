from config import obtener_conexion, obtener_pacientes

def insertar_usuario(name, paterno, materno, correo, numero, cp, password):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuario(name, paterno, materno, correo, numero, cp, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (name, paterno, materno, correo, numero, cp, password))
    conexion.commit()
    conexion.close()

#cosas del crud XD

def insertar_paciente(Nombres, Apellidos, Tipo_de_sangre, Fecha_de_nacimiento, Telefono, direccion, correo):
    conexion = obtener_pacientes()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO datos(Nombres, Apellidos, Tipo_de_sangre, Fecha_de_nacimiento, Telefono, direccion, correo) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (Nombres, Apellidos, Tipo_de_sangre, Fecha_de_nacimiento, Telefono, direccion, correo))
    conexion.commit()
    conexion.close()


def obtener_datos():
    conexion = obtener_pacientes()
    datos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, Nombres, Apellidos, Tipo_de_sangre, Fecha_de_nacimiento, Telefono, direccion, correo FROM datos")
        datos = cursor.fetchall()
    conexion.close()
    return datos


def eliminar_datos(id):
    conexion = obtener_pacientes()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM datos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_datos_por_id(id):
    conexion = obtener_pacientes()
    dato = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, Nombres, Apellidos, Tipo_de_sangre, Fecha_de_nacimiento, Telefono, direccion, correo FROM datos WHERE id = %s", (id))
        dato = cursor.fetchone()
    conexion.close()
    return dato


def actualizar_datos(Nombres, Apellidos, Tipo_de_sangre, Fecha_de_nacimiento, Telefono, direccion, correo, id):
    conexion = obtener_pacientes()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE datos SET Nombres=%s, Apellidos=%s, Tipo_de_sangre=%s, Fecha_de_nacimiento=%s, Telefono=%s, direccion=%s, correo=%s WHERE id = %s",
                       (Nombres, Apellidos, Tipo_de_sangre, Fecha_de_nacimiento, Telefono, direccion, correo, id))
    conexion.commit()
    conexion.close()

#otras cosas
from config import obtener_conexion, obtener_pacientes

def guardar_citado(Nombre, Numero, Mail, Sintomas, Fecha, Area, Hora, Genero):
    conexion = obtener_pacientes()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO registro(Nombre, Numero, Mail, Sintomas, Fecha, Area, Hora, Genero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (Nombre, Numero, Mail, Sintomas, Fecha, Area, Hora, Genero))
    conexion.commit()
    conexion.close()


