from django.db.models import *
from django.contrib.auth.models import User


class Reservation(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    date_from = DateField()
    date_to = DateField()
