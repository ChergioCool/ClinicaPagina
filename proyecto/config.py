import pymysql


def obtener_conexion():
    return pymysql.connect(host='localhost',
                                user='sergio',
                                password='vale',
                                db='login')

def obtener_pacientes():
    return pymysql.connect(host='localhost',
                           user='sergio',
                           password='vale',
                           db='data_pacientes')
