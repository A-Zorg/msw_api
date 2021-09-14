from index.models import CustomUser
from reconciliation.models import UserData

user = CustomUser.objects.get(hr_id=90000)
userdata_object = UserData.objects.get(user=user)
userdata_object.custom_podushka = True
userdata_object.save()

