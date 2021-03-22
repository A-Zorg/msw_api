from datetime import datetime, timedelta
import pandas
from index.models import CustomUser
from reconciliation.models import UserPropAccount, ReconciliationUserPropAccount
from accounting_system.models import UserMainData, UserBillTypes, \
    UserBill,CompanyBill, HistoryCompanyBill, HistoryUserBill, Transaction

#get users
users = [
    CustomUser.objects.get(hr_id = 90000),
    CustomUser.objects.get(hr_id = 90001)
]

active_accounts = set()
for acc_day in UserPropAccount.objects.all():
    if acc_day.daily_adj_net:
        active_accounts.add(acc_day.account)

active_accounts = list(active_accounts)

month_result = {
    "hr_id":[],
    "account_id" : active_accounts,
}

for index in range(len(active_accounts)):
    account = active_accounts[index]
    user = users[index%2]

    month_result['hr_id'].append(user.hr_id)

    for acc in UserPropAccount.objects.filter(account=account):
        acc.user = user
        acc.save()

        if month_result.get(acc.effective_date):
            amount = acc.daily_adj_net if acc.daily_adj_net else 0
            month_result[acc.effective_date].append(amount)
        else:
            amount = acc.daily_adj_net if acc.daily_adj_net else 0
            month_result[acc.effective_date] = [amount]
    account_rec_user_prop = ReconciliationUserPropAccount.objects.get(account=account)
    account_rec_user_prop.user = user
    account_rec_user_prop.save()

for key in month_result:
    print(str(key)+'-'+str(len(month_result[key])))
to_userdata_file = pandas.DataFrame(data=month_result)
to_userdata_file.to_excel('/home/alex_zatushevkiy/3/month_propreports_template.xlsx')
to_userdata_file.to_excel('/home/alex_zatushevkiy/3/month_propreports.xlsx')