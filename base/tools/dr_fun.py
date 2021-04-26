import holidays
import datetime as dt

def write_log(text):
    with open('./logs/dr_log.txt', 'a') as file:
        datetime = '[' + str(dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + '] '
        f_text = ''
        if isinstance(text, list):
            for t in text:
                f_text += str(t) + '; '
            file.write(datetime + f_text[:-2] + '\n')
            return True
        elif isinstance(text, str):
            file.write(datetime + text + '\n')
            return True
        else: return False

def get_time_param(session):
    if session == 'INT':
        execution_time_s = '10:00:00'
        execution_time_e = '16:00:00'
    elif session == 'POS':
        execution_time_s = '16:00:00'
        execution_time_e = '20:00:01'
    else:
        execution_time_s = '4:00:00'
        execution_time_e = '10:00:00'
    return [execution_time_s, execution_time_e]

def previous_business_day(day, str_type='%Y-%m-%d', n=-1):
    day = dt.datetime.strptime(day, str_type)
    next_day = day + dt.timedelta(days=n)
    while next_day.weekday() in holidays.WEEKEND:
        next_day += dt.timedelta(days=n)
    return next_day.strftime(str_type)
