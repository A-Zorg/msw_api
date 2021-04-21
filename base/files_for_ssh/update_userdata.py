from index.models import CustomUser
from reconciliation.models import UserData

user = CustomUser.objects.get(hr_id=234275)
userdata_object = UserData.objects.get(user=user)
userdata_object.custom_payout_rate = 0.66
userdata_object.save()

