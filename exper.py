import configparser
from base.sql_functions import pgsql_select, pgsql_select_as_dict

config = configparser.ConfigParser()
config.read("cred/config.ini")

def test_sql():
    request = "SELECT DISTINCT(ticker) FROM public.review_propreportsdata " \
              f"WHERE execution_date = '2020-08-18'"
    raw_result = pgsql_select(request, **config['pg_db_9999'])
    print(raw_result)

if __name__ == '__main__':
    test_sql()
























































