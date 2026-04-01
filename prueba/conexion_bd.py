from flask_mysqldb import MySQL

class Conexion_Db:
    def __init__(self,conexion):
        self.conexion=conexion 

        if conexion:
            self.init_app(conexion)

    def init_app(self,app):
        app.config['MYSQL_HOST']= 'localhost'
        app.config['MYSQL_USER']= 'root'
        app.config['MYSQL_PASSWORD']=''
        app.config['MYSQL_DB']='inventario'
        app.config['MYSQL_PORT'] = 3309
        self.conexion = MySQL(app)