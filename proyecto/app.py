from flask import Flask, render_template, request, redirect,session
import controlador
import mysql.connector
from flask import make_response
import pdfkit
from flask_mail import Mail, Message


connection = mysql.connector.connect(host='localhost',
                            user='sergio',
                            password='vale',
                            db='login')

cursor = connection.cursor()
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='elmatasanos616@gmail.com'
app.config['MAIL_PASSWORD']='piufppioshcpityz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key="super secret key"


@app.route("/")
def index_():
    return render_template('pagina.html')

@app.route("/pagina.html")
def PedirCita():
    return render_template('pagina.html')

@app.route("/Especialidades.html")
def especialidades():
    return render_template('Especialidades.html')

@app.route("/contactos.html")
def Contactanos():
    return render_template('contactos.html')

@app.route("/QuienesSomos.html")
def QuienesSomos():
    return render_template('QuienesSomos.html')

@app.route("/Servicio.html")
def servicios():
    return render_template('Servicio.html')

@app.route("/cita.html")
def cita():
    return render_template('cita.html')

@app.route("/registro.html")
def registro():
    return render_template('registro.html')

@app.route("/pacientes.html")
def formulario_agregar_dato():
    return render_template('pacientes.html')

@app.route("/citado.html")
def citado():
    return render_template('citado.html')


@app.route("/pre_pdf.html")
def pre_pdf():
    return render_template('pre_pdf.html')

@app.route("/imprimir_pdf.html")
def imprimir_pdf():
    return render_template('pdf.html')

@app.route("/email.html")
def email():
    return render_template('email.html')

@app.route("/guardar_usuario", methods=['POST'])
def guardar_usuario():
    name = request.form["name"]
    paterno = request.form["paterno"]
    materno = request.form["materno"]
    correo = request.form["correo"]
    numero = request.form["numero"]
    cp = request.form["cp"]
    password = request.form["password"]
    controlador.insertar_usuario(name, paterno, materno, correo, numero, cp, password)

    return redirect("/cita.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    msg=''
    if request.method=='POST':
        name =request.form["name"]
        password = request.form["password"]
        cursor.execute("SELECT name, password FROM usuario WHERE name=%s AND password=%s",(name, password))
        record = cursor.fetchone()
        if record:
            session['logeado']=True
            session['nombre']= record[1]
            return redirect("/pagina.html")
        else:
            msg='no se encontró el usuario'
    return render_template('login.html')

@app.route('/salir')
def salir():
    session.pop('logeado', None)
    session.pop('nombre', None)


    return redirect("/login.html")

#cosa del crud 


@app.route("/guardar_paciente", methods=["POST"])
def guardar_paciente():
    Nombres = request.form["Nombres"]
    Apellidos = request.form["Apellidos"]
    Tipo_de_sangre = request.form["Tipo_de_sangre"]
    Fecha_de_nacimiento = request.form["Fecha_de_nacimiento"]
    Telefono = request.form["Telefono"]
    direccion = request.form["direccion"]
    correo = request.form["correo"]
    controlador.insertar_paciente(Nombres, Apellidos, Tipo_de_sangre,Fecha_de_nacimiento, Telefono, direccion, correo)

    return redirect("/datos")


@app.route("/datos")
def datos():
    datos = controlador.obtener_datos()
    return render_template("datos.html", datos=datos)


@app.route("/eliminar_juego", methods=["POST"])
def eliminar_datos():
    controlador.eliminar_datos(request.form["id"])
    return redirect("/datos")


@app.route("/editar_dato/<int:id>")
def editar_dato(id):
    dato = controlador.obtener_datos_por_id(id)
    return render_template("update.html", dato=dato)

@app.route("/pdf/<int:id>")
def pdf(id):
    dato = controlador.obtener_datos_por_id(id)
    return render_template("a_pdf.html", dato=dato)


@app.route("/actualizar_dato", methods=["POST"])
def actualizar_dato():
    id = request.form["id"]
    Nombres = request.form["Nombres"]
    Apellidos = request.form["Apellidos"]
    Tipo_de_sangre = request.form["Tipo_de_sangre"]
    Fecha_de_nacimiento = request.form["Fecha_de_nacimiento"]
    Telefono = request.form["Telefono"]
    direccion = request.form["direccion"]
    correo = request.form["correo"]
    controlador.actualizar_datos(Nombres, Apellidos,Tipo_de_sangre,Fecha_de_nacimiento, Telefono, direccion, correo, id)

    return redirect("/datos")


@app.route('/pdf', methods =["POST"])
def pdf_imprimir():
    id = request.form["id"]
    Nombres = request.form["Nombres"]
    Apellidos = request.form["Apellidos"]
    Tipo_de_sangre = request.form["Tipo_de_sangre"]
    Fecha_de_nacimiento = request.form["Fecha_de_nacimiento"]
    Telefono = request.form["Telefono"]
    direccion = request.form["direccion"]
    correo = request.form["correo"]
    controlador.actualizar_datos(Nombres, Apellidos, Tipo_de_sangre,Fecha_de_nacimiento, Telefono, direccion, correo, id)
    html = render_template("download.html", Nombres=Nombres, Apellidos=Apellidos, Tipo_de_sangre=Tipo_de_sangre,Fecha_de_nacimiento=Fecha_de_nacimiento, Telefono=Telefono, direccion= direccion, correo=correo)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response
    return render_template("pdf_pdf.html")


 #lo de registro

@app.route("/guardar_citado", methods=['POST'])
def guardar_citado():
    Nombre = request.form["Nombre"]
    Numero = request.form["Numero"]
    Mail = request.form["Mail"]
    Sintomas = request.form["Sintomas"]
    Fecha = request.form["Fecha"]
    Area = request.form["Area"]
    Hora = request.form["Hora"]
    Genero = request.form["Genero"]
    controlador.guardar_citado(Nombre, Numero, Mail, Sintomas, Fecha, Area, Hora,Genero)

    msg = Message('CITA REGISTRADA',sender = 'elmatasanos616@gmail.com', recipients=[Mail])
    msg.html = render_template("email.html", Nombre=Nombre, Numero=Numero, Mail=Mail, Sintomas=Sintomas, Fecha=Fecha, Area=Area, Hora=Hora, Genero=Genero)
    mail.send(msg)
    return render_template('pagina.html')
    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
