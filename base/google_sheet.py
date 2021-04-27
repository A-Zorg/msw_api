from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
import datetime


GOOGLE_ACCOUNT_CREDS = 'cred/msw-gs-creds.json'
SERVICES_SPREADSHEET_ID_2 = '1AYD-JXNcxd0K9avN9qrOqsiDBJSf8s4mhYNYRTvjET0'

class GSpread:
    """
    Class for interacting with an google spreadsheet
    """

    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id

    def worksheet(self, ws_name):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_ACCOUNT_CREDS, scope)
        gc = gspread.authorize(credentials)
        sh = gc.open_by_key(self.spreadsheet_id)
        try:
            old_worksheet = sh.worksheet(ws_name)
            sh.del_worksheet(old_worksheet)
        except:
            pass
        new_worksheet = sh.add_worksheet(title=ws_name, rows="1000", cols="30")

        df = pd.read_csv('./base/data_set/services.csv')

        services_lis = [df.columns.values.tolist()] + df.values.tolist()
        services_str = str([row[2:] for row in services_lis]).replace('nan', '\'\'')
        new_services_lis = eval(services_str)
        new_worksheet.update(new_services_lis)

        return new_worksheet

    def get_services(self):
        try:
            today = datetime.date.today()
            first = today.replace(day=1)
            last_month = first - datetime.timedelta(days=1)
            last_month_str = last_month.strftime("%m.%Y")
            try:
                ws = self.worksheet(last_month_str)
            except:
                if last_month.month < 10:
                    try:
                        ws = self.worksheet(last_month_str[1:])
                    except:
                        return 'No data for previous month'
                else:
                    return 'No data for previous month'

            data = ws.get_all_values()
            headers = data.pop(0)

            df = pd.DataFrame(data, columns=headers)
            df = df.set_index('UID')
            total_sum = 0

            return df
        except:
            return 'Worksheet load error'

    def get_services_current(self, name):

        ws = self.worksheet(name)
        data = ws.get_all_values()
        return data

def update_gs():
    tod_ay = datetime.datetime.today()
    month = (tod_ay-datetime.timedelta(tod_ay.day+1)).month
    year = (tod_ay - datetime.timedelta(tod_ay.day+1)).year

    gso = GSpread(SERVICES_SPREADSHEET_ID_2)
    df = gso.get_services_current(f'{month}.{year}')

