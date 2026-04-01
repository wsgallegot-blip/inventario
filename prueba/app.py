import os 
#os.system('cls'if os.name == 'nt'else 'clear')
from conexion_bd import Conexion_Db
from flask import Flask,redirect,render_template,request


app = Flask(__name__)

# Conexión a la BD
conexion_bd = Conexion_Db(app)
mysql = conexion_bd.conexion


@app.route("/", methods=["GET", "POST"])
def registro():
    mensaje = None

    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO inventario (
                nombre, cantidad, marca, tipo, imei, ram,
                procesador, referencia, capacidad, serial,
                sede, ubicacion, cc, persona
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            request.form["nombre"],
            request.form["cantidad"],
            request.form["marca"],
            request.form["tipo"],
            request.form["imei"],
            request.form["ram"],
            request.form["procesador"],
            request.form["referencia"],
            request.form["capacidad"],
            request.form["serial"],
            request.form["sede"],
            request.form["ubicacion"],
            request.form["cc"],
            request.form["persona"]
        ))
        mysql.connection.commit()
        cursor.close()

        mensaje = "Producto registrado correctamente"

    return render_template("registro.html", mensaje=mensaje)

@app.route("/inventario")
def inventario():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inventario")
    productos = cursor.fetchall()
    cursor.close()

    return render_template("inventario.html", productos=productos)

@app.route("/eliminar/<int:id>", methods=["GET", "POST"])
def eliminar(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM inventario WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    return redirect("/inventario")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    cursor = mysql.connection.cursor()

    if request.method == "POST":
        cursor.execute("""
            UPDATE inventario SET
            nombre=%s, cantidad=%s, marca=%s, tipo=%s,
            imei=%s, ram=%s, procesador=%s, referencia=%s,
            capacidad=%s, serial=%s, sede=%s, ubicacion=%s,
            cc=%s, persona=%s
            WHERE id=%s
        """, (
            request.form["nombre"],
            request.form["cantidad"],
            request.form["marca"],
            request.form["tipo"],
            request.form["imei"],
            request.form["ram"],
            request.form["procesador"],
            request.form["referencia"],
            request.form["capacidad"],
            request.form["serial"],
            request.form["sede"],
            request.form["ubicacion"],
            request.form["cc"],
            request.form["persona"],
            id
        ))
        mysql.connection.commit()
        cursor.close()
        return redirect("/inventario")

    cursor.execute("SELECT * FROM inventario WHERE id = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()

    return render_template("editar.html", producto=producto)

@app.route("/login")
def login():
    lista = ['java', 'python', 'c++', 'js', 'php']
    data = {
        'nombre': 'dorian',
        'saludo': 'bienvenido',
        'Cursos': lista,
        'numero_de_cursos': len(lista)
    }
    return render_template("login.html", data=data)

@app.route("/menu")
def menu():
    lista = ['java', 'python', 'c++', 'js', 'php']
    data = {
        'nombre': 'dorian',
        'saludo': 'bienvenido',
        'Cursos': lista,
        'numero_de_cursos': len(lista)
    }
    return render_template("menu.html", data=data)

if __name__ == "__main__":
    app.run(host="192.168.100.84", port=5000, debug=True)
