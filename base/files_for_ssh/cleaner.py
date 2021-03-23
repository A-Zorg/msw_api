import logging
from index.models import CustomUser
from reconciliation.models import UserData, ReconciliationUserPropAccount, Service, UserPropAccount
from accounting_system.models import \
    UserMainData, UserBillTypes, \
    UserBill,CompanyBill, HistoryUserBill, HistoryCompanyBill, Transaction, Entry, ErrorReport


logging.basicConfig(
                    filename="dataset_log.log",
                    format='%(asctime)s (%(filename)s:%(lineno)d  %(threadName)s) %(name)s - %(levelname)s: %(message)s'
                   )
logger=logging.getLogger()

logger.setLevel(logging.INFO)

logger.info('start destroing of datasets')

users = CustomUser.objects.filter(hr_id__in=range(90000, 91000))
bills = UserBill.objects.filter(user__in=users)
user_transactions = Transaction.objects.filter(user_bill__in=bills)
ErrorReport.objects.all().delete()
for trans in user_transactions:
    try:
        entry = trans.entry
        Transaction.objects.filter(entry=entry).delete()
        HistoryUserBill.objects.filter(entry=entry).delete()
        HistoryCompanyBill.objects.filter(entry=entry).delete()
        entry.delete()
    except:
        pass
bills.delete()
HistoryUserBill.objects.filter(user__in=users).delete()
UserMainData.objects.filter(user__in=users).delete()
UserData.objects.filter(user__in=users).delete()
UserPropAccount.objects.filter(user__in=users).delete()
ReconciliationUserPropAccount.objects.filter(user__in=users).delete()
Service.objects.filter(user__in=users).delete()
users.delete()


logger.info('finish destroing of datasets')

