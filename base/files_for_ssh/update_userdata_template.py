from index.models import CustomUser
from reconciliation.models import UserData

user = CustomUser.objects.get(hr_id={USER_ID})
userdata_object = UserData.objects.get(user=user)
userdata_object.{FIELD} = {VALUE}
userdata_object.save()

