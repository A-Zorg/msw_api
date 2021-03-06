import time
import re
import psycopg2
import configparser
from psycopg2 import extras
from mysql.connector import connection

config = configparser.ConfigParser()
config.read("cred/config.ini")


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


def pgsql_select(request, user, password, port, host, database, param=None):
    with psycopg2.connect(
            user=user,
            host=host,
            port=port,
            password=password,
            database=database
    ) as connect:
        cursor = connect.cursor()
        if request.startswith('SELECT'):
            cursor.execute(query=request, vars=param)
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

def pgsql_insert(request, user, password, port, host, database):
    with psycopg2.connect(
            user=user,
            host=host,
            port=port,
            password=password,
            database=database,
    ) as connect:
        try:
            cursor = connect.cursor()
            if request.startswith('INSERT'):
                cursor.execute(request)
                return cursor.statusmessage
        except:
            return False

def pgsql_touch(query, params='', save=False, rtrn=False):
    try:
        with psycopg2.connect(**config['pg_db_9999']) as conn:
            with conn.cursor() as cur:

                if type(params) == list and save:
                    for p in params:
                        if type(p) == list:
                            cur.execute(query, p)
                        else:
                            cur.execute(query, [p])
                    conn.commit()
                    return True

                cur.execute(query, params)
                if save:
                    conn.commit()
                    if rtrn:
                        return cur.fetchall()
                    else:
                        return True
                else:
                    return cur.fetchall()
    except psycopg2.Error as err:
        return False

def decode_request(context, request, fields):
    key = context.custom_config['pg_key']
    for field in fields:
        request = re.sub(f'(\W){field}(\W)', f"\g<1>pgp_sym_decrypt({field}::bytea,'{key}')\g<2>", request)

    return request

def encode_request(context, request):
    key = context.custom_config['pg_key']
    qty_to_encode = re.findall('=-[a-zA-Z0-9,\.-]*-=', request)
    for part in qty_to_encode:
        request = request.replace(part, f"pgp_sym_encrypt('{part[2:-2]}', '{key}', 'cipher-algo=aes256')")

    return request





























