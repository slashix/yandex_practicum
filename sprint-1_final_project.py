import datetime
from decimal import Decimal


DATE_FORMAT = '%Y-%m-%d'

goods = {}


def add(items, title, amount, expiration_date=None):
    if expiration_date:
        expiration_date = datetime.datetime.strptime(expiration_date, DATE_FORMAT).date()
    if title not in items:
        items[title] = []
    items[title].append({'amount': amount, 'expiration_date': expiration_date})


def add_by_note(items, note):
    if '-' in note.split()[-1]:
        title = ' '.join(note.split()[:-2])
        amount = note.split()[-2]
        expiration_date = datetime.datetime.strptime(note.split()[-1], DATE_FORMAT).date()
    else:
        title = ' '.join(note.split()[:-1])
        amount = note.split()[-1]
        expiration_date = None
    if title not in items:
        items[title] = []
    items[title].append({'amount': Decimal(amount), 'expiration_date': expiration_date})


def find(items, needle):
    goods = []
    for item in items.keys():
        if needle.lower() in item.lower():
            goods.append(item)
    return goods


def amount(items, needle):
    count = Decimal('0')
    for key in items.keys():
        if needle.lower() in key.lower():
            for item in items[key]:
                count = Decimal(count) + item['amount']
    return count


def expire(items, in_advance_days=0):
    expire_list = []
    for item in items:
        last_item = None
        for element in items[item]:
            # print(element)
            if element['expiration_date']:
                difference = (element['expiration_date'] - datetime.date.today()).days
                if difference <= in_advance_days:
                    if item == last_item:
                        # print(item, last_item)
                        # print(expire_list)
                        expire_list[-1] = (item, expire_list[-1][-1] + element['amount'])
                    else:
                        expire_list.append((item, element['amount']))
                    last_item = item

    return (expire_list)

#
# Финальные проверки
#
separator = '#' * 80
print(separator)
print('Положим продукты в холодильник - тест функции add()')
add(goods, 'Пельмени Универсальные', Decimal('3.5'), '2024-03-15')
add(goods, 'Пельмени Универсальные', Decimal('2'), '2024-03-16')
add(goods, 'Яйца утиные', Decimal('1.0'), '2024-04-17')
add(goods, 'Газировка', Decimal('3'))
add(goods, 'Сметана', Decimal('1'), '2024-03-28')
print('Сейчас в холодильнике:')
pprint(goods)

print(f'\r\n{separator}')
print('Добавим продукты в холодильник - с помощью функции add_by_note()')
add_by_note(goods, 'Пицца 1')
add_by_note(goods, 'Пироги с яблоком 10 2024-04-1')
add_by_note(goods, 'Яйца 10 2024-03-19')
print('Сейчас в холодильнике:')
pprint(goods)

print(f'\r\n{separator}')
print('Ищем в холодильнике продукты, содержащие "пи":', find(goods, 'пи'))

print(f'\r\n{separator}')
print('Сколько в холодильнике яиц:', amount(goods, 'яйЦА'))
print('Сколько в холодильнике тортов:', amount(goods, 'торт'))

print(f'\r\n{separator}')
print('Сколько и каких продуктов испортится сегодня:', expire(goods))
print('Завтра:', expire(goods, 1))
print('Послезавтра:', expire(goods, 2))


