from index.models import CustomUser
from reconciliation.models import Bonus
from accounting_system.models import AccountType


acc_type = AccountType.objects.get(id=8)
try:
    bonus_object = Bonus.objects.get(account_type=acc_type)
    bonus_object.decimal_percentage = 0.13
    bonus_object.save()
except:
    bonus_object = Bonus.objects.create(
        account_type=acc_type,
        decimal_percentage=0.13
    )
    bonus_object.save()

