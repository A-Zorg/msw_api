import time
import psycopg2
from psycopg2 import extras
from mysql.connector import connection

def mysql_select(request, user, password, port, host, database):
    with connection.MySQLConnection(
            user=user,
            host=host,
            port=port,
            password=password,
            database=database
    ) as connect:
        cursor = connect.cursor()
        if request.startswith('SELECT'):
            cursor.execute(request)
            response = cursor.fetchall()
            time.sleep(0.5)
            return response

def pgsql_select(request, user, password, port, host, database):
    with psycopg2.connect(
            user=user,
            host=host,
            port=port,
            password=password,
            database=database
    ) as connect:
        cursor = connect.cursor()
        if request.startswith('SELECT'):
            cursor.execute(request)
            response = cursor.fetchall()
            time.sleep(0.5)
            return response

def pgsql_select_as_dict(request, user, password, port, host, database):
    with psycopg2.connect(
            user=user,
            host=host,
            port=port,
            password=password,
            database=database
    ) as connect:
        cursor = connect.cursor(cursor_factory=extras.RealDictCursor)
        if request.startswith('SELECT'):
            cursor.execute(request)
            response = cursor.fetchall()
            time.sleep(0.5)
            return response

def pgsql_del(request, user, password, port, host, database):
    with psycopg2.connect(
            user=user,
            host=host,
            port=port,
            password=password,
            database=database
    ) as connect:
        cursor = connect.cursor()
        if request.startswith('DELETE'):
          cursor.execute(request)
          connect.commit()
          time.sleep(0.5)
          return True
        else:
            return False

def pgsql_update(request, user, password, port, host, database):
    with psycopg2.connect(
            user=user,
            host=host,
            port=port,
            password=password,
            database=database
    ) as connect:
        cursor = connect.cursor()
        if request.startswith('UPDATE'):
            cursor.execute(request)
            connect.commit()
            time.sleep(0.5)
            return True
        else:
            return False