from index.models import CustomUser
from reconciliation.models import ReconciliationUserPropAccount
from accounting_system.models import AccountType


user = CustomUser.objects.get(hr_id={USER_ID})
acc_type = AccountType.objects.get(id={ACC_ID})
try:
    bonus_object = ReconciliationUserPropAccount.objects.get(
        user=user,
        account='{ACC_NAME}'
    )
    bonus_object.month_adj_net = {VALUE}
    bonus_object.save()
except:
    bonus_object = ReconciliationUserPropAccount.objects.create(
        user=user,
        account='{ACC_NAME}',
        account_type=acc_type,
        month_adj_net={VALUE}
    )
    bonus_object.save()

