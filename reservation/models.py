from django.db.models import *


class Order(Model):
    name_surname = CharField(max_length=200)
    email = EmailField()
    phone = CharField(max_length=20)
    date_from = DateField()
    date_to = DateField()
    address = CharField(max_length=100)
    city = CharField(max_length=100)
    postal = CharField(max_length=5)
    price = IntegerField(null=True, blank=True)
    paid = BooleanField(default=False)
