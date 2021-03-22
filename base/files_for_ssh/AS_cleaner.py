import logging
from index.models import CustomUser
from reconciliation.models import UserData, ReconciliationUserPropAccount, Service
from accounting_system.models import \
    UserMainData, UserBillTypes, \
    UserBill,CompanyBill, HistoryUserBill, HistoryCompanyBill, Transaction, \
    Entry, MonthPropreportsTransaction, ErrorReport





ErrorReport.objects.all().delete()
Transaction.objects.all().delete()
HistoryUserBill.objects.all().delete()
UserBill.objects.all().delete()
UserMainData.objects.all().delete()
HistoryUserBill.objects.all().delete()
HistoryCompanyBill.objects.all().delete()
Entry.objects.all().delete()
MonthPropreportsTransaction.objects.all().delete()


