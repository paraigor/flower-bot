import datetime as dt

from datacenter.models import (
    Budget,
    Bunch,
    BunchAssembly,
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
    motive = Motive.objects.filter(title="Без повода").first()
    return motive.id


def get_bunch(budget_id, motive_id):
    budget = Budget.objects.get(id=budget_id)
    return Bunch.objects.filter(
        motive__id=motive_id,
        price__gt=budget.value_from,
        price__lt=budget.value_to,
    ).first()


def get_random_bunch():
    return Bunch.objects.all().order_by("?").first()


def get_bunch_elements(bunch):
    return BunchAssembly.objects.filter(bunch=bunch)


def check_and_add_phone_number(id, phone_num):
    if not Client.objects.filter(id_tg=id, phone_number=phone_num).exists():
        client = Client.objects.get(id_tg=id)
        client.phone_number = phone_num
        client.save()


def get_client(id):
    return Client.objects.get(id_tg__exact=id)


def create_order(
    client,
    bunch,
    delivery_date,
    delivery_time,
    delivery_address,
    comment,
):
    order = Order.objects.create(
        client=client,
        bunch=bunch,
        delivery_date=dt.datetime.strptime(delivery_date, "%Y-%m-%d").date(),
        delivery_time=dt.datetime.strptime(delivery_time, "%H").time(),
        delivery_address=delivery_address,
        comment=comment,
    )
    return order
