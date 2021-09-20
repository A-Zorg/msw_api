import random
import math
import pandas
from base64 import b64decode
from dateutil.relativedelta import relativedelta
import holidays
from behave import *

from datetime import date, datetime, timedelta
from base.db_interactions.trader_profile import TraderProfile, RiskBlockPeriod, Log
from base.db_interactions.index import User
from base.db_interactions.reconciliation import UserPropaccounts, ReconciliationUserPropaccounts, Services
from base.db_interactions.accounting_system import HistoryUserBill, UserBill
from base.main_functions import get_token


def to_float(text):
    return float(text)


def to_list(text):
    return eval(text)


register_type(Number=to_float, List=to_list)


@step("Delete manager's row from TraderProfile table")
def step_impl(context):
    context.user_id = context.custom_config['manager_id']['user_id']
    profile_layout = TraderProfile.get(user_id=context.user_id)
    if profile_layout:
        profile_layout.delete()


@step("Delete manager's row from RiskBlockPeriod table")
def step_impl(context):
    context.user_id = context.custom_config['manager_id']['user_id']
    admin_username = context.custom_config['super_user']['username']
    admin = User.get(username=admin_username)
    context.admin_id = admin.id
    user_period = RiskBlockPeriod.get(user_id=context.user_id, risk_manager_id=context.admin_id )
    if user_period:
        user_period.delete()


@step("Make PUT request to api/trader/layout/ by manager")
def step_impl(context):
    url = context.custom_config["host"] + f"api/trader/layout/"
    random_list = [True, False]
    session = context.manager_user
    token = get_token(session=session, url=url, key='X-CSRFToken')

    context.body = [
            {'id': 'R3', 'isHidden': random.choice(random_list)},
            {'id': 'R2', 'isHidden': random.choice(random_list)},
            {'id': 'LP', 'isTall': True, 'isHidden': random.choice(random_list)},
            {'id': 'HR', 'isHidden': random.choice(random_list)},
            {'id': 'R1', 'isHidden': random.choice(random_list)},
            {'id': 'PR', 'isHidden': random.choice(random_list)}
        ]
    random.shuffle(context.body)

    session.put(
        url,
        json={
            'layout': context.body
        },
        headers={
            "Referer": 'https://mytest.sg.com.ua/',
            'X-CSRFToken': token,
        }
    )


@step("Make PUT request to api/trader/risk_block2_period/ by {person}")
def step_impl(context, person):
    url = context.custom_config["host"] + f"api/trader/risk_block2_period/{context.user_id}/"
    if person == 'manager':
        session = context.manager_user
    elif person == 'admin':
        session = context.super_user
    else:
        session = None

    token = get_token(session=session, url=url, key='X-CSRFToken')

    context.body = {
            'riskblock2_period': random.randint(0, 1000)
        }

    response = session.put(
        url,
        json=context.body,
        headers={
            "Referer": 'https://mytest.sg.com.ua/',
            'X-CSRFToken': token,
        }
    )


@step("Check created TraderProfile row: {endpoint}")
def step_impl(context, endpoint):
    if endpoint == 'api/trader/risk_block2_period/':
        url = context.custom_config["host"] + endpoint + f'{context.user_id}/'
    elif endpoint == 'api/trader/layout/':
        url = context.custom_config["host"] + endpoint
    else:
        url = None

    session = context.manager_user
    response = session.get(url)

    if response.json() != context.body:
        context.txt_writer(f'CHECK - {endpoint}')
        context.txt_writer(response.json())
        context.txt_writer(context.body)
        assert False

@step("Check created RiskBlockPeriod row")
def step_impl(context):
    url = context.custom_config["host"] + f'api/trader/risk_block2_period/{context.user_id}/'
    session = context.super_user
    response = session.get(url)

    if response.json() != context.body:
        context.txt_writer(f'CHECK - admin api/trader/risk_block2_period')
        context.txt_writer(response.json())
        context.txt_writer(context.body)
        assert False


def create_log(user_id, manager_id, expired):
    month_active = random.randint(1, 6)
    today = datetime.today()
    if today.month - month_active < 1:
        month = 12 + (today.month - month_active)
        year = today.year - 1
    else:
        month = today.month - month_active
        year = today.year

    created_date = today.replace(month=month, year=year) + \
                   timedelta(days=random.choice([1, 10, 30]) * (1 - 2 * expired))
    log_template = {
        'created_date': created_date,
        'log_type': random.randint(0, 2),
        'reason': random.randint(1, 3),
        'duration': 15,
        'c_loss': random.randint(-10, 99),
        'auto_close': random.randint(-10, 99),
        'poss_loss': random.randint(-10, 99),
        'pos_auto_cls': random.randint(-10, 99),
        'pos_inv': random.randint(-10, 99),
        'months_active': month_active,
        'big_input': 'test: some comment',
        'risk_manager_id': manager_id,
        'user_id': user_id,
    }
    Log.create(**log_template)

    return [expired, log_template]


@step("Create user's logs: {type_creation}")
def step_impl(context, type_creation):
    user_id = context.custom_config['manager_id']['user_id']
    admin_username = context.custom_config['super_user']['username']
    admin = User.get(username=admin_username)
    admin_id = admin.id

    Log.filter(user_id=user_id).delete()

    variants_dict = {
        'one expired and one actual': [True, False],
        'two expired': [True, True],
        'two actual': [False, False],
    }
    context.created_logs = []
    for i in variants_dict[type_creation]:
        context.created_logs.append(
            create_log(
                user_id=user_id,
                manager_id=admin_id,
                expired=i
            )
        )


@step("Log-status of user should be {answer}")
def step_impl(context, answer):
    user_id = context.custom_config['manager_id']['user_id']
    url = context.custom_config["host"] + f'api/trader/main_info/{user_id}/'

    session = context.super_user
    response = session.get(url).json()

    if answer == 'null':
        assert response['status'] == None
    elif answer == 'not null':
        assert response['status'] != None
    elif answer == 'null or not':
        first_log = context.created_logs[0]
        second_log = context.created_logs[1]
        # context.txt_writer(context.created_logs[0])
        # context.txt_writer(context.created_logs[1])
        if first_log[1]['created_date'] > second_log[1]['created_date']:
            if first_log[0]:
                assert response['status'] == None
            else:
                assert response['status'] != None
        else:
            if second_log[0]:
                assert response['status'] == None
            else:
                assert response['status'] != None


@step("get user's data from DB")
def step_impl(context):
    context.exp_data = {}

    user_id = context.custom_config['manager_id']['user_id']
    user = User.get(id=user_id)
    context.exp_data['first_name'] = user.first_name
    context.exp_data['second_name'] = user.last_name
    context.exp_data['hr_id'] = user.hr_id

    session = context.sb
    url = f'https://hrtest-server.sg.com.ua/api/contact/{user.sb_id}'
    photo_id = session.get(url).json()['photo']['id']
    photo_url = url + f'/photo/{photo_id}/download'
    context.exp_data['photo'] = session.get(photo_url).content

    profile = TraderProfile.get(user_id=user_id)
    profile.risk_note = 'risk_note text'
    profile.save()
    context.exp_data['risk_note'] = profile.risk_note


@step("get user's data through api/trader/main_info/")
def step_impl(context):
    user_id = context.custom_config['manager_id']['user_id']
    url = context.custom_config["host"] + f'api/trader/main_info/{user_id}/'
    session = context.super_user

    response = session.get(url).json()
    image = response['photo']
    head, body = image.split(',', 1)
    response['photo'] = b64decode(body)
    del response['status']

    context.act_data = response


@step("Main-info: compare actual and expected data")
def step_impl(context):
    if context.act_data != context.exp_data:
        context.txt_writer("trader/main_info/: data is not matched")
        assert False


def get_math_average(array):
    array = [i for i in array if i != None]
    if len(array):
        return round(sum(array)/len(array), 2)


def get_win_loss(positive_ar, negative_ar):
    if negative_ar:
        return abs(round(sum(positive_ar)/sum(negative_ar), 2))
    else:
        abs(round(sum(positive_ar), 2))


def get_sigma(array):
    array = [i for i in array if i != None]
    math_average = get_math_average(array)
    if math_average:
        return round((sum([(part-math_average)**2 for part in array])/(len(array)-1))**0.5, 2)


def get_adj_net_per_days(user_id, date_from):
    days = (datetime.today() - date_from).days
    adj_net_dict = dict()
    for day in range(days):
        curr_date = date_from + timedelta(day)
        adj_net_per_day = UserPropaccounts.filter(
            user_id=user_id,
            effective_date=curr_date.date()
        )
        result = [i.daily_adj_net for i in adj_net_per_day if i.daily_adj_net]

        if result:
            adj_net_dict[curr_date] = float(sum([i.daily_adj_net for i in adj_net_per_day if i.daily_adj_net]))
        else:
            adj_net_dict[curr_date] = None

    return adj_net_dict


def get_adj_net_per_days2(user_id, date_from, date_to=datetime.today()):
    days = (date_to - date_from).days + 1
    adj_net_per_days = UserPropaccounts.filter(
        user_id=user_id,
        effective_date__gte=date_from.date(),
        effective_date__lte=date_to.date()
    )

    adj_net_dict = dict()
    for day in range(days):
        curr_date = (date_from + timedelta(day)).date()
        adj_net_dict[curr_date] = None

    for adj_net_per_day in adj_net_per_days:
        if adj_net_per_day.daily_adj_net:
            if not adj_net_dict[adj_net_per_day.effective_date]:
                adj_net_dict[adj_net_per_day.effective_date] = 0
            adj_net_dict[adj_net_per_day.effective_date] += float(adj_net_per_day.daily_adj_net)

    return adj_net_dict


def get_total_net(user_id, date_from):
    adj_nets = UserPropaccounts.filter(
        user_id=user_id,
        effective_date__gte=date_from
    )
    return float(sum([part.daily_adj_net for part in adj_nets if part.daily_adj_net]))


def get_total_service(user_id, date_from):
    services = Services.filter(
        user_id=user_id,
        service_type__in=['compensation', 'service'],
        effective_datetime__gte=date_from
    )
    return float(sum([part.amount for part in services if part.amount]))


def first_day_curr_month():
    today = datetime.now()
    return today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def calculate_deadline(account):
    if account < 1000:
        deadline = 2500
    elif 1000 <= account <= 2499:
        deadline = account + 5000
    elif 2500 <= account <= 4999:
        deadline = account + 7500
    else:
        deadline = account + 15000

    return deadline


def get_last_holiday(holiday_name):
    today = datetime.today()
    us_holidays = holidays.UnitedStates(years=[today.year, today.year - 1])
    last_holidays = us_holidays.get_named(holiday_name)
    if today.date() >= last_holidays[1]:
        last_holiday = last_holidays[1]
    else:
        last_holiday = last_holidays[0]

    return last_holiday


def get_pb_sigma(user_id, from_date):
    adj_net_per_days = get_adj_net_per_days(user_id, from_date)
    sigma = get_sigma(adj_net_per_days.values())

    max_net = - math.inf
    curr_net = 0
    for adj_net_per_day in adj_net_per_days.values():
        if adj_net_per_day != None:
            curr_net += adj_net_per_day
            if curr_net > max_net:
                max_net = curr_net
    return round((max_net - curr_net) / sigma, 2)


def get_rate_of_user(user_id, users):
    thanksgiving_date = get_last_holiday('Thanksgiving')
    users_rate = []
    for user in users:
        ur_id = user['id']
        total_net = get_total_net(ur_id, thanksgiving_date)
        total_services = get_total_service(ur_id, thanksgiving_date)
        users_rate.append((ur_id, total_net + total_services))

    users_rate = sorted(users_rate, key=lambda key: key[1], reverse=True)
    actual_rate = None
    for rate, user in enumerate(users_rate):
        if user[0] == user_id:
            actual_rate = rate + 1

    return actual_rate


@step("get expected PRIMARY RISK BLOCK data of user: {user_id:Number}")
def step_impl(context, user_id=193):
    today = datetime.today()
    from_date = today - timedelta(days=40)

    pb_sigm = get_pb_sigma(user_id, from_date)

    curr_net_balance_bill = UserBill.get(user_id=user_id, bill_id__name='Current Net balance')
    cur_net_balance = curr_net_balance_bill.amount

    account_bill = UserBill.get(user_id=user_id, bill_id__name='Account')
    account = account_bill.amount

    histories = HistoryUserBill.filter(
        user_id=user_id,
        model_id=curr_net_balance_bill.id,
        history_date__lt=first_day_curr_month()
    ).sorted_by('history_date', desc=True)
    last_month_net = histories[0].amount

    left = calculate_deadline(account_bill.amount) + curr_net_balance_bill.amount

    url = context.custom_config["host"] + 'api/index/users/'
    session = context.super_user
    users = session.get(url).json()
    rating = get_rate_of_user(user_id, users)

    context.exp_data = {
        "data":
            {
                "user_id": user_id,
                "cur_net_balance": f'{cur_net_balance:.2f}',
                "account": f'{account:.2f}',
                "last_month_net": f'{last_month_net:.2f}',
                "month_net": f'{(cur_net_balance - last_month_net):.2f}',
                "pb_sigm": f'{pb_sigm:.2f}',
                "left": f'{left:.2f}',
                "rating": rating
            },
        "errors": []
    }


@step("get user's HR BLOCK data from smartbase")
def step_impl(context):
    user_id = context.custom_config['manager_id']['user_id']
    user = User.get(id=user_id)
    context.txt_writer('context.exp_data')
    session = context.sb
    url = f'https://hrtest-server.sg.com.ua/api/contact/{user.sb_id}'
    smart_base_user_data = session.get(url).json()
    birthday = datetime.strptime(smart_base_user_data['birthday'], '%d.%m.%Y %H:%M:%S')
    who_brought = smart_base_user_data['whatLedInCompany']
    phone = smart_base_user_data['phone']
    first_working_date = datetime.strptime(smart_base_user_data['firstWorkingDate'], '%d.%m.%Y %H:%M:%S')

    profile = TraderProfile.get(user_id=user_id)
    profile.trading_partners = 'my partner'
    profile.save()

    context.exp_data = {
        'birthday': birthday.strftime('%Y-%m-%d'),
        'date_of_start': first_working_date.strftime('%Y-%m-%d'),
        'phone': phone,
        'trading_partners': profile.trading_partners,
        'who_brought': who_brought,
    }


@step("get expected LAST PERFORMANCE BLOCK data of user: {user_id}")
def step_impl(context, user_id):
    from_date = datetime.today() - timedelta(days=23)

    adj_net_per_days = get_adj_net_per_days2(user_id, from_date)

    result = []
    counter = 0
    for effective_date, amount in adj_net_per_days.items():
        result.append(
            {
                'effective_date': effective_date.strftime('%Y-%m-%d'),
                'adj_net': amount
            }
        )
        counter += 1
    context.exp_data = result


def get_total_net_per_account(user_id, date_from):
    trading_accounts = ReconciliationUserPropaccounts.filter(user_id=user_id)
    results = {account.account: 0 for account in trading_accounts}
    adj_nets = UserPropaccounts.filter(
        user_id=user_id,
        effective_date__gte=date_from.date()
    )

    refine_adj_nets = [part for part in adj_nets if part.daily_adj_net]
    for adj_net in refine_adj_nets:
        results[adj_net.account] += adj_net.daily_adj_net

    return [{'account': acc_name, 'month_adj_net': f'{amount:.2f}'} for acc_name, amount in results.items()]


@step("get expected PROPREPORTS BLOCK data of user: {user_id}")
def step_impl(context, user_id):
    from_date = first_day_curr_month()
    context.exp_data = get_total_net_per_account(user_id, from_date)


@step("get expected RISK BLOCK I data of user: {user_id:Number}")
def step_impl(context, user_id):
    from_date = datetime.today() - relativedelta(months=6)
    adj_net_per_days = get_adj_net_per_days2(user_id, from_date)

    all_adj_net = [adj_net for adj_net in adj_net_per_days.values() if adj_net != None]
    positive_adj_net = list(filter(lambda x: x > 0, all_adj_net))
    negative_adj_net = list(filter(lambda x: x <= 0, all_adj_net))

    context.exp_data = {
        'data':
            {
                'user_id': user_id,
                'average_day': f'{get_math_average(all_adj_net):.2f}',
                'sigma': f'{get_sigma(all_adj_net):.2f}',
                'win_loss': f'{get_win_loss(positive_adj_net, negative_adj_net):.2f}',
                'avg_up': f'{get_math_average(positive_adj_net):.2f}',
                'avg_down': f'{get_math_average(negative_adj_net):.2f}',
                'up_count': len(positive_adj_net),
                'down_count': len(negative_adj_net),
            },
        'errors': []
    }


def get_last_quarters(start_date, quarter_qty):
    quarters = {
        0: {'date_from': (1, 1), 'date_to': (3, 31)},
        1: {'date_from': (4, 1), 'date_to': (6, 30)},
        2: {'date_from': (7, 1), 'date_to': (9, 30)},
        3: {'date_from': (10, 1), 'date_to': (12, 31)},
    }
    quarter_number = pandas.Timestamp(start_date).quarter - 1
    start_year = start_date.year
    quarters_result = {}
    for i in range(quarter_qty):
        from_date = quarters[quarter_number]['date_from']
        to_date = quarters[quarter_number]['date_to']
        quarters_result[quarter_qty-i] = {
            'from_quarter': datetime(year=start_year, month=from_date[0], day=from_date[1]),
            'to_quarter': datetime(year=start_year, month=to_date[0], day=to_date[1])
        }
        quarter_number = (quarter_number + 3) % 4
        if quarter_number == 3:
            start_year -= 1
    return quarters_result


def get_quarters(user_id, qty=5):
    today = datetime.today()
    curr_quarters = get_last_quarters(today, qty)
    quarters = {}
    for key, dates in curr_quarters.items():
        adj_net_per_days = get_adj_net_per_days2(user_id, dates['from_quarter'], dates['to_quarter'])

        all_adj_net = [adj_net for adj_net in adj_net_per_days.values() if adj_net != None]
        positive_adj_net = list(filter(lambda x: x > 0, all_adj_net))
        negative_adj_net = list(filter(lambda x: x <= 0, all_adj_net))
        quarters[str(key)] = {
            'win_loss': get_win_loss(positive_adj_net, negative_adj_net),
            'average_day': get_math_average(all_adj_net),
            'sigma': get_sigma(all_adj_net),
            'date_from': dates['from_quarter'].strftime('%Y-%m-%d'),
            'date_to': dates['to_quarter'].strftime('%Y-%m-%d'),
        }

    return quarters


def get_chart(user_id):
    today = datetime.today()
    today_year_ago = today - relativedelta(years=1)
    all_time = today - relativedelta(years=2)
    days = (today - all_time).days + 1
    adj_net_per_days = get_adj_net_per_days2(user_id, all_time, today)

    start_adj_net = 0
    total_chart = {}
    for day in range(days):
        curr_day = (all_time + timedelta(days=day)).date()
        if adj_net_per_days.get(curr_day):
            start_adj_net += adj_net_per_days[curr_day]
        total_chart[curr_day.strftime('%Y-%m-%d')] = start_adj_net

    chart = {datum: amount for datum, amount in total_chart.items()
             if datetime.strptime(datum, '%Y-%m-%d').date() >= today_year_ago.date()}

    return chart


@step("get PERFORMANCE CHART data of user: {user_id:Number}")
def step_impl(context, user_id):
    context.exp_data = {
        'data': {
            'user_id': user_id,
            'quarters': get_quarters(user_id),
            'chart': get_chart(user_id),
        },
        'errors': []
    }


@step("get expected RISK BLOCK II of user: {user_id:Number} data as {role}")
def step_impl(context, user_id, role):
    if role == 'risk':
        admin_username = context.custom_config['super_user']['username']
        admin = User.get(username=admin_username)
        period = RiskBlockPeriod.get(user_id=user_id, risk_manager_id=admin.id).riskblock2_period
    else:
        period = TraderProfile.get(user_id=user_id).riskblock2_period

    from_date = datetime.today() - timedelta(days=360)
    adj_net_per_days = get_adj_net_per_days2(user_id, from_date)

    all_adj_net = [adj_net for adj_net in adj_net_per_days.values() if adj_net != None]
    period_positive_adj_net = list(filter(lambda x: x > 0, all_adj_net))[-period:]
    period_negative_adj_net = list(filter(lambda x: x <= 0, all_adj_net))[-period:]

    period_adj_net = all_adj_net[-period:]
    positive_adj_net = list(filter(lambda x: x > 0, period_adj_net))
    negative_adj_net = list(filter(lambda x: x <= 0, period_adj_net))

    context.exp_data = {
        'data':
            {
                'user_id': user_id,
                'average_day': f'{get_math_average(period_adj_net):.2f}',
                'sigma': f'{get_sigma(period_adj_net):.2f}',
                'win_loss': f'{get_win_loss(positive_adj_net, negative_adj_net):.2f}',
                'avg_up': f'{get_math_average(period_positive_adj_net):.2f}',
                'avg_down': f'{get_math_average(period_negative_adj_net):.2f}',
                'up_count': len(positive_adj_net),
                'down_count': len(negative_adj_net),
            },
        'errors': []
    }


@step("get expected RISK BLOCK III data")
def step_impl(context):
    today = date.today()
    user_id = context.custom_config['manager_id']['user_id']
    all_logs = Log.filter(user_id=user_id).sorted_by('created_date', desc=True)
    actual_logs = []
    for log in all_logs:
        end_date = log.created_date + relativedelta(months=log.months_active)
        if end_date > today:
            actual_logs.append(log)

    if actual_logs:
        shown_log = actual_logs[0]
        expired = False
    elif all_logs:
        shown_log = all_logs[0]
        expired = True
    else:
        assert False

    context.exp_data = {
        'c_loss': shown_log.c_loss,
        'auto_close': shown_log.auto_close,
        'poss_loss': shown_log.poss_loss,
        'pos_auto_cls': shown_log.pos_auto_cls,
        'pos_inv': shown_log.pos_inv,
        'overdue': expired,
    }


@step("get actual PRIMARY RISK BLOCK data of user: {user_id}")
def step_impl(context, user_id):
    session = context.super_user
    url = context.custom_config["host"] + f'api/trader/risk_block/{user_id}/'

    context.act_data = session.get(url).json()


@step("get actual HR BLOCK data")
def step_impl(context):
    user_id = context.custom_config['manager_id']['user_id']
    url = context.custom_config["host"] + f'api/trader/hr_block/{user_id}/'
    session = context.super_user

    context.act_data = session.get(url).json()


@step("get actual LAST PERFORMANCE BLOCK data of user: {user_id}")
def step_impl(context, user_id):
    url = context.custom_config["host"] + f'api/trader/last_performance/{user_id}/'
    session = context.super_user

    context.act_data = session.get(url).json()


@step("get actual PROPREPORTS BLOCK data of user: {user_id}")
def step_impl(context, user_id):
    url = context.custom_config["host"] + f'api/trader/propreports/{user_id}/'
    session = context.super_user

    context.act_data = session.get(url).json()


@step("get actual RISK BLOCK I data of user: {user_id}")
def step_impl(context, user_id):
    url = context.custom_config["host"] + f'api/trader/risk_block1/{user_id}/'
    session = context.super_user

    context.act_data = session.get(url).json()


@step("get actual PERFORMANCE CHART data of user: {user_id}")
def step_impl(context, user_id):
    url = context.custom_config["host"] + f'api/trader/performance_chart/{user_id}/'
    session = context.super_user

    context.act_data = session.get(url).json()


@step("get actual RISK BLOCK II data of user: {user_id}")
def step_impl(context, user_id):
    url = context.custom_config["host"] + f'api/trader/risk_block2/{user_id}/'
    session = context.super_user

    context.act_data = session.get(url).json()


@step("get actual RISK BLOCK III data")
def step_impl(context):
    user_id = context.custom_config['manager_id']['user_id']
    url = context.custom_config["host"] + f'api/trader/risk_block3/{user_id}/'
    session = context.super_user

    context.act_data = session.get(url).json()


@step("{endpoint}: compare actual and expected data")
def step_impl(context, endpoint):
    if context.act_data != context.exp_data:
        context.txt_writer(endpoint.upper())
        context.txt_writer(context.act_data)
        context.txt_writer(context.exp_data)
        assert False
