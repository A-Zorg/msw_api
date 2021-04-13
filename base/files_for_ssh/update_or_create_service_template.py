import datetime
from index.models import CustomUser
from reconciliation.models import Service

user = CustomUser.objects.get(hr_id={USER_ID})
try:
    service_object = Service.objects.get(
        user=user,
        name='{SERV_NAME}'
    )
    service_object.amount = {VALUE}
    service_object.effective_datetime = datetime.datetime.fromtimestamp({DATE})
    service_object.save()
except:
    service_object = Service.objects.create(
        user=user,
        name='{SERV_NAME}',
        service_type='{SERV_TYPE}',
        amount={VALUE},
        effective_datetime=datetime.datetime.fromtimestamp({DATE})
    )
    service_object.save()

