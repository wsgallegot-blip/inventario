from flask_mysqldb import MySQL
import os

class Conexion_Db:
    def __init__(self, app=None):
        self.conexion = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'flaskuser'
        app.config['MYSQL_PASSWORD'] = 'password_segura'
        app.config['MYSQL_DB'] = 'inventario'
        app.config['MYSQL_PORT'] = 3306

        self.conexion = MySQL(app)
