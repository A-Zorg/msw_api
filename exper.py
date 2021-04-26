import configparser
from base.sql_request import dr
from base.tools.dr_fun import previous_business_day, get_time_param

import numpy

from base.sql_functions import pgsql_select, pgsql_select_as_dict

config = configparser.ConfigParser()
config.read("cred/config.ini")

def test_sql():
    ddd = '2020-08-18'
    request = "SELECT ticker, total_real, total_shares_traded, session " \
                  "FROM review_datapertickeraccount " \
                  f"WHERE account = '34504170' AND review_date = date '{ddd}'"

    raw_result = pgsql_select(request, **config['pg_db_9999'])
    res_pre1 = [[dic[0], dic[1], dic[2]] for dic in raw_result if dic[3] == 'PRE']
    # res_int = {dic[0]: {'total_real': dic[1], 'total_shares_traded': dic[2]}
    #            for dic in raw_result if dic[3] == 'INT'}
    # res_pos = {dic[0]: {'total_real': dic[1], 'total_shares_traded': dic[2]} for dic in raw_result if dic[3] == 'POS'}
    sorted_list = sorted(res_pre1, key=lambda x: x[0])
    print(res_pre1)
    print(sorted_list)

    # if numpy.array_equal(res_pre1, res_pre2): print(numpy.array_equal(res_pre1, res_pre2))

if __name__ == '__main__':
    # review_date = '2020-08-18'
    # session =  'INT'
    # account = '34504016'
    # sql_request = dr['review_datapertickeraccount']
    #
    # raw_result = pgsql_select(sql_request, **config['pg_db_9999'],
    #                           param=[account, review_date])
    #
    # actual = [[dic[0], round(float(dic[1]), 2), dic[2]] for dic in raw_result if dic[3] == session]
    # actual = sorted(actual, key=lambda x: x[0])
    #
    # print(actual)
    #
    # sql_request = dr['calc_data_datapertickeraccount']
    # if session == 'PRE':
    #     review_date = review_date
    # else:
    #     review_date = previous_business_day(review_date)
    # raw_result = pgsql_select(sql_request, **config['pg_db_9999'],
    #                           param=[account, review_date] + get_time_param(session))
    #
    # fact = [[dic[0], round(float(dic[1]), 2), dic[2]] for dic in raw_result]
    # fact = sorted(fact, key=lambda x: x[0])
    if type([1]) == 'list': print(type([1]))
























































