from django.db.models import *


class Reservation(Model):
    name = CharField(max_length=100)
    date_from = DateField()
    date_to = DateField()
    active = BooleanField(default=True)


class Order(Model):
    name_surname = CharField(max_length=200)
    email = EmailField()
    phone = CharField(max_length=20)
    date_from = DateField()
    date_to = DateField()
    address = CharField(max_length=100)
    city = CharField(max_length=100)
    postal = BigIntegerField()
    paid = BooleanField(default=False)
