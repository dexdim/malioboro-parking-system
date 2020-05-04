import mysql
from app import app
from db_config import mysql
from flask import jsonify
from flash import flash, request
from werkzeug import generate_password_hash, check_password_hash


@app.route('/user')
def user():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
