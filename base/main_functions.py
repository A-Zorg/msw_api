import random
from datetime import date, timedelta
import re
from telethon import TelegramClient

class GetRequest():

    def __init__(self, session, url):
        self.request = session.get(url)
        self.text = self.request.text
        try:
            text = self.text
            text = text.replace('null', 'None')
            text = text.replace('false', 'False')
            text = text.replace('true', 'True')

            self.json_list = eval(text)
        except:
            self.json_list = None

    def check_text(self, name_list):
        check_list = [i in self.text for i in name_list]
        return all(check_list)

    def check_json(self, keys_list ):
        for key in keys_list[:-5]:
            index = 0
            for part in self.json_list:
                if all([str(i) in str(part) for i in key]):
                    index+=1
            if index!=1:
                return False
        return True

def random_filter_generator(item_list, patern):
    copy_list = item_list[:]
    qty = random.randint(1,len(copy_list))
    new_list=[]
    for i in range(qty):
        new_list.append(random.choice(copy_list))
        copy_list.remove(new_list[-1])
    url_parts = [f'{patern}[]={i}&' for i in new_list]
    return ''.join(url_parts), new_list

def prev_current_date():
    current_month = date.today().month
    current_year = date.today().year
    prev_month = current_month - 1
    prev_year = current_year
    if prev_month == 0:
        prev_month = 12
        prev_year = current_year - 1
    date_dict = {
                 'current_month':current_month,
                 'current_year':current_year,
                 'prev_month':prev_month,
                 'prev_year':prev_year,
                 'current_day': date.today().day,
                 }
    return date_dict
def check_comming_entries(entries, subject_dict, key):
    for entry in entries:
        count = 0
        for part in subject_dict:
            str_enytr = str(part)
            result = all([str(i) in str_enytr for i in entry])
            if result:
                count+=1
        if count!=1 and key == 'appropriate':
            return False
        elif count!=0 and key == 'inappropriate':
            return False
    return True

def get_token(session, url, key='csrftoken'):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                  'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    html = session.get(url, headers=headers)
    if key == 'csrftoken':
        token = re.findall('name="csrfmiddlewaretoken" value="([a-zA-Z0-9]*)">', html.text)[0]
    elif key == 'X-CSRFToken':
        token = re.findall('csrfToken: "([a-zA-Z0-9]*)"', html.text)[0]
    return token

def find_button( messages, button_name):
    for message in messages:
        if message.buttons==None:
            continue
        for butt_row in message.buttons:
            for button in butt_row:
                if re.search(button_name,button.text ):
                    return button

