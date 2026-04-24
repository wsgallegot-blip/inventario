import os 
#os.system('cls'if os.name == 'nt'else 'clear')
import MySQLdb.cursors
from conexion_bd import Conexion_Db
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash ,generate_password_hash

app = Flask(__name__) # vreacion de la aplicacion en flask

app.secret_key = "clave_super_secreta_123"

# Conexión a la BD

conexion_bd = Conexion_Db(app)
mysql = conexion_bd.conexion

#

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM usuario WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        cursor.close()

        print("USER:", user)

        if user and user ["password"]== password:
            session["id_usuario"] = user["id_usuario"]
            session["rol"] = user["rol"]
            print("SESSION CREADA:", session)
            return redirect("/menu")

        return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

#

@app.route("/test_session")
def test_session():
    session["test"] = "ok"
    return str(session)

#

@app.route("/menu")
def menu():
    if "id_usuario" not in session:
        return redirect("/")

    return render_template( "menu.html",rol=session["rol"] )

#

@app.route("/salir")
def salir():
    session.clear()
    return redirect("/")

#

@app.route("/registro", methods=["GET", "POST"])                                #define la ruta del sitio, get=mostrar la pagina del formulario; post=para recibir parametros del formulario# 
def registro():                                                                 #metodo de la ruta
    mensaje = None                                                              #variable vacia

    if request.method == "POST":
        
        id_usuario = session.get("id_usuario")

        if not id_usuario:
            return "Usuario no autenticado"                                     #verificacion de peticion, solo si el usuario la envio
        cursor = mysql.connection.cursor()                                      #cursor de la base de datos quien enviara los datos y hara el registro de dentro de ella                
        cursor.execute("""
            INSERT INTO equipos (
                id_usuario,
                nombre, marca, tipo, imei, ram,
                procesador, referencia, capacidad, serial
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            id_usuario, 
            request.form["nombre"],
            request.form["marca"],
            request.form["tipo"],
            request.form["imei"],
            request.form["ram"],
            request.form["procesador"],
            request.form["referencia"],
            request.form["capacidad"],
            request.form["serial"]
        ))

        mysql.connection.commit() # guarda definitivo los cambios en la base de datos 
        cursor.close() # cierra el cursor

        mensaje = "Producto registrado correctamente" #rectifica el envio de los parametros

    return render_template("registro.html", mensaje=mensaje) #une el html a la ruta

#

@app.route("/inventario")
def inventario():
    if "id_usuario" not in session:
        return redirect("/")

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM equipos")
    productos = cursor.fetchall()
    cursor.close()
    return render_template("inventario.html", productos=productos ,rol=session["rol"])

#

@app.route("/eliminar/<int:id>", methods=["GET", "POST"])
def eliminar(id):
    # 🔐 Seguridad
    if "id_usuario" not in session or session["rol"] != "admin":
        return "Acceso denegado", 403

    cursor = mysql.connection.cursor()

    # ✅ POST → eliminar de verdad
    if request.method == "POST":
        cursor.execute("DELETE FROM equipos WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return redirect("/inventario")

    # ✅ GET → mostrar confirmación
    cursor.execute("SELECT * FROM equipos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()

    return render_template("eliminar.html", producto=producto)

#

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    
    if "id_usuario" not in session or session["rol"] != "admin":
        return "Acceso denegado", 403

    cursor = mysql.connection.cursor()

    if request.method == "POST":
        cursor.execute("""
            UPDATE equipos SET
            nombre=%s, marca=%s, tipo=%s,
            imei=%s, ram=%s, procesador=%s, referencia=%s,
            capacidad=%s, serial=%s
            WHERE id=%s
        """, (
            request.form["nombre"],
            request.form["marca"],
            request.form["tipo"],
            request.form["imei"],
            request.form["ram"],
            request.form["procesador"],
            request.form["referencia"],
            request.form["capacidad"],
            request.form["serial"],
            id
        ))
        mysql.connection.commit()
        cursor.close()
        return redirect("/inventario")

    cursor.execute("SELECT * FROM equipos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()

    return render_template("editar.html", producto=producto)

#


@app.route("/registro_usuarios", methods=["GET", "POST"])
def registro_usuarios():

    if "id_usuario" not in session or session["rol"] != "admin":
        return "Acceso denegado", 403

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO usuario (
                nombre, apellido, cc, correo,
                username, password, rol
            ) VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            request.form["nombre"],
            request.form["apellido"],
            request.form["cc"],
            request.form["correo"],
            request.form["username"],
            request.form["password"],
            request.form["rol"]
        ))
        mysql.connection.commit()
        cursor.close()

        # ✅ CLAVE: redirigir a usuarios
        return redirect("/usuarios")

    return render_template("registro_usuarios.html")

#

@app.route("/usuarios/<int:id_usuario>/equipos")
def inventario_usuario(id_usuario):

    if "id_usuario" not in session or session["rol"] != "admin":
        return "Acceso denegado", 403

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT e.id, e.nombre, e.marca, e.tipo, e.serial,
               u.nombre AS usuario_nombre, u.apellido
        FROM equipos e
        INNER JOIN usuario u ON e.id_usuario = u.id_usuario
        WHERE u.id_usuario = %s
    """, (id_usuario,))

    equipos = cursor.fetchall()
    cursor.close()

    return render_template("inventario_usuarios.html",equipos=equipos)
#
@app.route("/usuarios")
def usuarios():

    if "id_usuario" not in session or session["rol"] != "admin":
        return "Acceso denegado", 403

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT id_usuario, nombre, apellido, username, rol
        FROM usuario
    """)
    usuarios = cursor.fetchall()
    cursor.close()

    return render_template("usuarios.html",usuarios=usuarios)

#

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)