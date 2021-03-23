import random
import configparser
from datetime import date, timedelta
import re
import imaplib
import email
from email.header import decode_header


config = configparser.ConfigParser()
config.read("cred/config.ini")

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

    def check_json(self, keys_list):
        for key in keys_list[:-5]:
            index = 0
            for part in self.json_list:
                if all([str(i) in str(part) for i in key]):
                    index += 1
            if index != 1:
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

def find_button(messages, button_name):
    for message in messages:
        if message.buttons == None:
            continue
        for butt_row in message.buttons:
            for button in butt_row:
                if re.search(button_name,button.text ):
                    return button

def run_periodic_task(session, task_name):#sdfsdfsdfsdfsdf
    """run periodic task"""
    url = config['host']['host']+ '/admin/django_celery_beat/periodictask/'
    token = get_token(session, url)
    task_id = config['periodic_tasks'][task_name]

    recon_dict = {
        'csrfmiddlewaretoken': token,
        'action': 'run_tasks',
        'select_across': '0',
        'index': '0',
        '_selected_action': task_id,
    }
    response = session.post(url, data=recon_dict, headers={"Referer": url})

    return response.ok

def correct_py_file(file_name, old_new_parts):
    """change part in file"""
    with open(f'./base/files_for_ssh/{file_name}_template.py', 'r') as file:
        text = file.read()
        for old_part, new_part in old_new_parts.items():
            text = text.replace(old_part, new_part)
        with open(f'./base/files_for_ssh/{file_name}.py', 'w') as file2:
            file2.write(text)
    return True


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

def get_custom_config(context, host):
    if host == "test":
        context.custom_config = {
            "super_user": config['super_user'],
            "fin_user": config['fin_user'],
            "manager_user": config['manager_user'],
            "manager_id": config['manager_id'],
            "server": config['server'],
            "pg_db": config['pg_db'],
            "holidays_api": config['holidays_api'],
            "email": config['email'],
            "host": config['host']['host'],
            "dir_django_proj": config['dir_django_proj']['path'],
            "server_dir": config['server_dir']['path'],
            "telegram_user": config['telegram_user'],
            "periodic_task": config['periodic_tasks']['test'],
            "risk_bot": config['risk_bot']['name'],
        }
    elif host == "test_9999":
        context.custom_config = {
            "super_user": config['super_user_9999'],
            "fin_user": config['fin_user_9999'],
            "manager_user": config['manager_user_9999'],
            "manager_id": config['manager_id_9999'],
            "server": config['server'],
            "pg_db": config['pg_db_9999'],
            "holidays_api": config['holidays_api'],
            "email": config['email'],
            "host": config['host']['host_9999'],
            "dir_django_proj": config['dir_django_proj']['path_9999'],
            "server_dir": config['server_dir']['path'],
            "telegram_user": config['telegram_user'],
            "periodic_task": config['periodic_tasks']['test_9999'],
            "risk_bot": config['risk_bot']['name'],
        }

"""divide the number to the list of number which sum is equal to the initial number"""
def get_parts_from_number(number, qty):
    numbers_list=[]
    for i in range(qty-1):
        x_number = random.randint(1,number//2)
        numbers_list.append(x_number)
        number-=x_number
    numbers_list.append(number)

    return numbers_list






















