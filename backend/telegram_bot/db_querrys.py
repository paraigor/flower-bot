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


def get_budgets():
    return Budget.objects.all()


def get_default_motive_id():
    motives = Motive.objects.filter(title="Без повода")
    return motives[0].id


def get_bunch(budget_id, motive_id):
    budget = Budget.objects.get(id=budget_id)
    bunches = Bunch.objects.filter(
        motive__id=motive_id,
        price__gt=budget.value_from,
        price__lt=budget.value_to,
    )
    return bunches[0]


def get_bunch_elements(bunch):
    return BunchAssembly.objects.filter(bunch=bunch)
