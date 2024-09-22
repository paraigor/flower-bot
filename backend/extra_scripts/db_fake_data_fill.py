from random import choice, randint

from datacenter.models import (
    Bunch,
    BunchAssembly,
    BunchElement,
    Client,
    Budget,
    Motive,
    Order,
)


IMAGE = [
    "https://krasnodarflora.ru/upload/iblock/ce2/uisicyfvbd33mq75upcb3glng544bykc.jpg",
    "https://krasnodarflora.ru/upload/iblock/c5b/z1s3yybxx8wukdjevpqdklxgibjgwyip.jpg",
    "https://krasnodarflora.ru/upload/iblock/6ed/9f6rgjx59afh2hhwszj7xffkb6ug5xo3.jpg",
    "https://krasnodarflora.ru/upload/iblock/680/6801e2c7d92a51490eb9c1a1f4b26e8f.jpg",
    "https://krasnodarflora.ru/upload/iblock/85f/88drtlyxzdxvlterlrxk0u0e23n8ibid.jpg",
    "https://krasnodarflora.ru/upload/iblock/967/qbs0wbtizlbfenw4al6zmihum2yxvm5o.jpg",
    "https://krasnodarflora.ru/upload/iblock/680/6801e2c7d92a51490eb9c1a1f4b26e8f.jpg",
    "https://krasnodarflora.ru/upload/iblock/c5b/z1s3yybxx8wukdjevpqdklxgibjgwyip.jpg",
    ]
DESCRIPTION = [
    "Окутайте ее лавиной восторга! Этот великолепный букет - это больше, чем просто подарок - это захватывающее дух проявление любви, которое обещает оставить неизгладимое впечатление.",
    "Добавьте нотку изысканности в ваш день с этим букетом!",
    "Букет в нежных тонах с гортензиями и альстромериями.",
    "Яркий и контрастный букет из тюльпанов",
    "Большой букет из розовых лилий и ирисов",
    "Яркий контрастный букет из белых роз, сиреневых ирисов и танацетума",
    "Яркий и контрастный букет из тюльпанов",
    "Добавьте нотку изысканности в ваш день с этим букетом!",
]

STATUS = ["accepted", "confirmed"]
ADDRESSES = [
        "Москва, Тверская, 21, кв. 23",
        "Москва, Краснопресненская, 46, кв. 355",
        "Люберцы, Октябрьский проспект, 101, кв. 123",
        "Химки, Калинина, 4А, кв. 145",
        "Одинцово, Маршала Жукова, 46, кв. 299",
    ]


# Создание Клиентов
def create_clients():
    numbers = [
        "+7(960)985-72-04",
        "+7(960)668-84-67",
        "+7(960)094-42-53",
        "+7(960)498-41-21",
        "+7(960)169-36-31",
        "+7(960)990-45-74",
        "+7(960)790-05-40",
        "+7(960)493-62-48",
        "+7(960)176-71-70",
        "+7(960)715-39-99",
    ]

    names = ["Яна", "Антонина", "Олег", "Михаил", "Анна", "Илья"]

    for id in range(100, 110):
        full_name = choice(names)
        phone_number = numbers[id % 10]
        Client.objects.create(
            id_tg=id, full_name=full_name, phone_number=phone_number
        )


# Создание Поводов
def create_occasions():
    occasions = [
        "Свадьба",
        "День рождения",
        "8 марта",
        "23 февраля",
        "14 февраля",
        "Без повода",
    ]

    for occasion in occasions:
        Motive.objects.create(title=occasion)


# Создание Элементов букета
def create_elements_bouquet():
    elements = [
        "Роза",
        "Пионы",
        "Хризантемы",
        "Тюльпаны",
        "Альстромерии",
        "Герберы",
        "Гортензии",
        "Эустома",
        "Гвоздика",
        "Лилии",
    ]

    for element in elements:
        BunchElement.objects.create(title=element)


# Создание Рссчетной суммы
def create_budget():
    budgets = {
        0: {"title": "до 1500", "value_from": 0, 'value_to': 1499},
        1: {"title": "От 1500 до 3000 ", "value_from": 1500, 'value_to': 2999},
        2: {"title": "От 3000 до 5000", "value_from": 3000, 'value_to': 4999},
        3: {"title": "Свыше 5000", "value_from": 5000, 'value_to': 10000},
        4: {"title": "Не важно", "value_from": 0, 'value_to': 10000},
    }

    for cost in budgets.values():
        title = cost["title"]
        value_from = cost["value_from"]
        value_to = cost["value_to"]
        Budget.objects.create(title=title, value_from=value_from, value_to=value_to)


# Создание Букетов
def create_bouquets():
    cost = {
        0: randint(250, 1499),
        1: randint(1500, 2999),
        2: randint(3000, 4999),
        3: randint(5000, 10000),
    }
    bunch_elements = list(BunchElement.objects.all())
    motives = Motive.objects.all()

    for motive in motives:
        for i in range(4):
            elements = [choice(bunch_elements) for _ in range(2)]
            title = f'Букет из {elements[0]} и {elements[1]}'
            price = cost[i]
            image = choice(IMAGE)
            description = choice(DESCRIPTION)

            bunch = Bunch(
                title=title, price=price, image=image, caption=description
            )
            bunch.save()
            bunch.motive.add(motive)
            
            quantity = [num for num in range(1, 102, 2)]
            for element in elements:
                bunch_assembly = BunchAssembly(
                bunch=bunch, element=element, quantity=choice(quantity)
            )
                bunch_assembly.save()


# Создание Заказов
def create_orders():
    clients = Client.objects.all()
    bouquets = list(Bunch.objects.all())

    for client in clients:
        status = choice(STATUS)
        client = client
        bouquet = choice(bouquets)
        day = randint(1, 28)
        date = f"2024-10-{day:02d}"
        hour = randint(9, 17)
        minute = randint(1, 59)
        time = f"{hour:02d}:{minute:02d}"
        delivery_date = f"2024-10-{day+1:02d}"
        delivery_time = f"{hour:02d}:00"
        address = choice(ADDRESSES)

        Order.objects.create(
            status=status,
            date=date,
            time=time,
            client=client,
            bunch=bouquet,
            delivery_date=delivery_date,
            delivery_time=delivery_time,
            delivery_address=address,
        )


def main():
    create_clients()
    create_occasions()
    create_elements_bouquet()
    create_budget()
    create_bouquets()
    create_orders()
