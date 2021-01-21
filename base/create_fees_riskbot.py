from openpyxl import Workbook
from openpyxl import load_workbook
import py7zr
import pandas
from datetime import datetime, timedelta, date
def update_fees(from_data, to_data):
    for i in range(len(to_data)):
        for j in range(len(to_data[i])):
            to_data[i][j].value=from_data[i][j].value

def create_riskbot_fees():
    """------------------------create fees file for riskbot----------------------------"""
    fees = pandas.read_csv('base/data_set/fees.csv')
    rows = fees.index.stop
    wb_from = load_workbook('base/data_set/fees.xlsx')
    ws_from = wb_from.active
    wb_to = load_workbook('generator/december.xlsx')
    ws_to = wb_to.active

    from_data = ws_from['D2':f'H{rows + 1}']
    to_data = ws_to['K5':f'O{rows + 4}']
    update_fees(from_data, to_data)

    from_user_id = ws_from['B2':f'B{rows + 1}']
    to_user_id = ws_to['B5':f'B{rows + 4}']
    update_fees(from_user_id, to_user_id)

    tod_ay = datetime.today()
    month = (tod_ay-timedelta(tod_ay.day+1)).month
    year = (tod_ay - timedelta(tod_ay.day+1)).year

    ws_to['C2'] = month-2
    ws_to['C3'] = date(year, month, 11)

    wb_to.save('base/data_set/fees_riskbot.xlsx')

    """------------------------create fees archive for riskbot----------------------------"""

    with py7zr.SevenZipFile('base/data_set/fees.7z', 'w', password='123456') as archive:
        archive.writeall('base/data_set/fees_riskbot.xlsx', 'month.xlsx',)