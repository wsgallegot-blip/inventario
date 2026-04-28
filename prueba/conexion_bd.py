
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
    app.config['MYSQL_USER'] = os.getenv("DB_USER")
    app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
    app.config['MYSQL_DB'] = os.getenv("DB_NAME")
    app.config['MYSQL_PORT'] = int(os.getenv("DB_PORT", 3306))

    mysql.init_app(app)
