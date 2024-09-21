import datetime as dt
import random

from datacenter.models import (
    Budget,
    Bunch,
    BunchAssembly,
    BunchElement,
    Client,
    Motive,
    Order,
)


def check_client(id):
    return Client.objects.filter(id_tg__exact=id).exists()


def create_client(id, first_name, last_name, username=None, phone_number=None):
    Client.objects.create(
        id_tg=id,
        full_name=f"{first_name} {last_name} aka {username}",
        phone_number=phone_number,
    )
    return id


def get_motives():
    return Motive.objects.all()

