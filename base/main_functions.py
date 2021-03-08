import random
from datetime import date, timedelta
import re
from telethon import TelegramClient
import imaplib
import email
from email.header import decode_header


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

# def prev_current_date():
#     current_month = date.today().month
#     current_year = date.today().year
#     prev_month = current_month - 1
#     prev_year = current_year
#     if prev_month == 0:
#         prev_month = 12
#         prev_year = current_year - 1
#     date_dict = {
#                  'current_month':current_month,
#                  'current_year':current_year,
#                  'prev_month':prev_month,
#                  'prev_year':prev_year,
#                  'current_day': date.today().day,
#                  }
#     return date_dict
def prev_current_date():
    current_date = date.today()
    prev_month_date = current_date.replace(day=1) - timedelta(days=1)
    date_dict = {
        'current_month' : current_date.month,
        'current_year' : current_date.year,
        'prev_month' : prev_month_date.month,
        'prev_year' : prev_month_date.year,
        'current_day' : current_date.day,
        "prev_month_day" : prev_month_date.day
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

def get_last_email(username, password):

    with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
        imap.login(username, password)

        status, messages = imap.select("INBOX")
        N = 1
        messages = int(messages[0])

        for i in range(messages, messages - N, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    print("Subject:", subject)
                    print("From:", From)
                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                                print(body)
                                return body
                            except:
                                pass

"""divide the number to the list of number which sum is equal to the initial number"""
def get_parts_from_number(number, qty):
    numbers_list=[]
    for i in range(qty-1):
        x_number = random.randint(1,number//2)
        numbers_list.append(x_number)
        number-=x_number
    numbers_list.append(number)

    return numbers_list





























