from flask_mysqldb import MySQL

mysql = MySQL()

def conectar_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'inventario'
    app.config['MYSQL_PORT'] = 3309

    mysql.init_app(app)
