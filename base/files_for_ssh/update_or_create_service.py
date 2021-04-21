import datetime
from index.models import CustomUser
from reconciliation.models import Service

user = CustomUser.objects.get(hr_id=90000)
try:
    service_object = Service.objects.get(
        user=user,
        name='fee_2'
    )
    service_object.amount = -0.2
    service_object.effective_datetime = datetime.datetime.fromtimestamp(1616235008.551759)
    service_object.save()
except:
    service_object = Service.objects.create(
        user=user,
        name='fee_2',
        service_type='fee',
        amount=-0.2,
        effective_datetime=datetime.datetime.fromtimestamp(1616235008.551759)
    )
    service_object.save()

