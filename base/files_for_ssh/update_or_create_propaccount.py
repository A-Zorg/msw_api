from index.models import CustomUser
from reconciliation.models import ReconciliationUserPropAccount
from accounting_system.models import AccountType


user = CustomUser.objects.get(hr_id=90000)
acc_type = AccountType.objects.get(id=4)
try:
    bonus_object = ReconciliationUserPropAccount.objects.get(
        user=user,
        account='bonus_acc'
    )
    bonus_object.month_adj_net = 0
    bonus_object.save()
except:
    bonus_object = ReconciliationUserPropAccount.objects.create(
        user=user,
        account='bonus_acc',
        account_type=acc_type,
        month_adj_net=0
    )
    bonus_object.save()

