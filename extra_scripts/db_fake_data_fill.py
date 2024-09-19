"""
with open('extra_scripts/db_fake_data_fill.py') as f:
    exec(f.read())
"""

import os
from random import choice, randint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

from datacenter.models import (
    Client,
    Motive,
    BunchElement,
    EstimatedCost,
    Bunch,
    Order
)


# Создание Клиентов

numbers = [
    '+7(960)985-72-04',
    '+7(960)668-84-67',
    '+7(960)094-42-53',
    '+7(960)498-41-21',
    '+7(960)169-36-31',
    '+7(960)990-45-74',
    '+7(960)790-05-40',
    '+7(960)493-62-48',
    '+7(960)176-71-70',
    '+7(960)715-39-99'
]

names = [
    'Яна',
    'Антонина',
    'Олег',
    'Михаил',
    'Анна',
    'Илья'
]

for id in range(100, 110):
    full_name = choice(names)
    phone_number = numbers[id%10]
    Client.objects.create(
        id_client = id,
        full_name = full_name,
        phone_number = phone_number
    )

# Создание Поводов

occasions = [
    'Свадьба',
    'День рождения',
    '8 марта',
    '23 февраля',
    '14 февраля',
    'Без повода',
    'Другой повод'
]

for occasion in occasions:
    Motive.objects.create(title = occasion)

# Создание Элементов букета

elements = [
    'Роза',
    'Пионы',
    'Хризантемы',
    'Тюльпаны',
    'Альстромерии',
    'Герберы',
    'Гортензии',
    'Эустома',
    'Гвоздика',
    'Лилии'
]

for element in elements:
    BunchElement.objects.create(title = element)

# Создание Рссчетной суммы

estimated_cost = {
    0: {'title': 'До 1000', 'price': 1000},
    1: {'title': 'До 2500 ', 'price': 2500},
    2: {'title': 'До 5000', 'price': 5000},
    3: {'title': 'Свыше 5000', 'price': 10000}
}

for cost in estimated_cost.values():
    title = cost['title']
    value = cost['price']
    EstimatedCost.objects.create(
        title = title, 
        value = value
    )

# Создание Букетов

bouquets = {
    0: {'title': 'Sarah Bernardt', 'price': randint(250, 10000),
        'image': 'https://krasnodarflora.ru/upload/iblock/ce2/uisicyfvbd33mq75upcb3glng544bykc.jpg',
        'description': 'Окутайте ее лавиной восторга! Этот великолепный букет - это больше, чем просто подарок - это захватывающее дух проявление любви, которое обещает оставить неизгладимое впечатление.'},
    1: {'title': 'Букет из 25 гортензии', 'price': randint(250, 10000),
        'image': 'https://krasnodarflora.ru/upload/iblock/c5b/z1s3yybxx8wukdjevpqdklxgibjgwyip.jpg',
        'description': 'Добавьте нотку изысканности в ваш день с этим букетом!'},
    2: {'title': 'Букет "Гортензии и Альстромерии"', 'price': randint(250, 10000),
        'image': 'https://krasnodarflora.ru/upload/iblock/6ed/9f6rgjx59afh2hhwszj7xffkb6ug5xo3.jpg',
        'description': 'Букет в нежных тонах с гортензиями и альстромериями.'},
    3: {'title': 'Букет из 51 тюльпана "Солнце и Небо"', 'price': randint(250, 10000),
        'image': 'https://krasnodarflora.ru/upload/iblock/680/6801e2c7d92a51490eb9c1a1f4b26e8f.jpg',
        'description': 'Яркий и контрастный букет из 51 тюльпана'},
    4: {'title': 'Букет из 10 лилий и 15 ирисов', 'price': randint(250, 10000),
        'image': 'https://krasnodarflora.ru/upload/iblock/85f/88drtlyxzdxvlterlrxk0u0e23n8ibid.jpg',
        'description': 'Большой букет из 10 розовых лилий и 15 ирисов'},
    5: {'title': 'Букет из белых роз, ирисов и ромашек', 'price': randint(250, 10000),
        'image': 'https://krasnodarflora.ru/upload/iblock/967/qbs0wbtizlbfenw4al6zmihum2yxvm5o.jpg',
        'description': 'Яркий контрастный букет из 21 белой розы, 14 сиреневых ирисов и танацетума'}
}

bunch_elements = list(BunchElement.objects.all())
motives = list(Motive.objects.all())

for bouquet in bouquets.values():
    title = bouquet['title']
    price = bouquet['price']
    image = bouquet['image']
    description = bouquet['description']
    motive = choice(motives)
    element = choice(bunch_elements)
    
    Bunch.objects.create(
        title = title,
        price = price,
        caption = description,
        motive = motive,
        elements = element
    )

# Создание Заказов

status = [
    "Принят",
    "Подтвержден"
    ]

addresses = [
    "Москва, Тверская, 21, кв. 23",
    "Москва, Краснопресненская, 46, кв. 355",
    "Люберцы, Октябрьский проспект, 101, кв. 123",
    "Химки, Калинина, 4А, кв. 145",
    "Одинцово, Маршала Жукова, 46, кв. 299"
]

client = list(Client.objects.all())
bouquets = Bunch.objects.all()

for bouquet in bouquets:
    status = choice(status)
    client = choice(client)
    bouquet = choice(bouquets)
    day = randint(1, 28)
    date = f"2024-10-{day:02d}"
    hour = randint(9, 17)
    minute = randint(1, 59)
    time = f"{hour:02d}:{minute:02d}"
    delivery_date = f"2024-10-{day+1:02d}"
    delivery_time = f"{hour:02d}:00"
    address = choice(addresses)
    
    Order.objects.create(
        status = status,
        date = date,
        time = time,
        client = client,
        bunch = bouquet,
        delivery_date = delivery_date,
        delivery_time = delivery_time,
        delivery_address = address
    )
