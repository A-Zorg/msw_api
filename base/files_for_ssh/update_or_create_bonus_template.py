from index.models import CustomUser
from reconciliation.models import Bonus
from accounting_system.models import AccountType


acc_type = AccountType.objects.get(id={ACC_ID})
try:
    bonus_object = Bonus.objects.get(account_type=acc_type)
    bonus_object.decimal_percentage = {VALUE}
    bonus_object.save()
except:
    bonus_object = Bonus.objects.create(
        account_type=acc_type,
        decimal_percentage={VALUE}
    )
    bonus_object.save()

