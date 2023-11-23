import sqlalchemy
from sqlalchemy.orm import sessionmaker
import models
import json
from datetime import datetime

dbms = input('Введите название СУБД: ')
login = input('Введите логин: ')
password = input('Введите пароль: ')
host = input('Введите хост: ')
port = input('Введите порт: ')
db_name = input('Введие название БД: ')

DSN = f'{dbms}://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

models.create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', encoding='utf-8') as test_data_json:
    book_publisher_data = json.load(test_data_json)

for el_with_data in book_publisher_data:
    if el_with_data['model'] == 'publisher':
        publisher = models.Publisher(id=el_with_data['pk'], name=el_with_data['fields']['name'])
        session.add(publisher)
    elif el_with_data['model'] == 'book':
        book = models.Book(id=el_with_data['pk'], title=el_with_data['fields']['title'], id_publisher=el_with_data['fields']['id_publisher'])
        session.add(book)
    elif el_with_data['model'] == 'shop':
        shop = models.Shop(id=el_with_data['pk'], name=el_with_data['fields']['name'])
        session.add(shop)
    elif el_with_data['model'] == 'stock':
        stock = models.Stock(id=el_with_data['pk'], id_book=el_with_data['fields']['id_book'], id_shop=el_with_data['fields']['id_shop'], count=el_with_data['fields']['count'])
        session.add(stock)
    else:
        sale = models.Sale(id=el_with_data['pk'], price=el_with_data['fields']['price'], date_sale=el_with_data['fields']['date_sale'], id_stock=el_with_data['fields']['id_stock'], count=el_with_data['fields']['count'])
        session.add(sale)
session.commit()

publisher_name = input('Введите имя автора: ')

join_query = session.query(models.Book.title, models.Shop.name, models.Sale.price, models.Sale.date_sale).join(models.Publisher).join(models.Stock).join(models.Shop).join(models.Sale).filter(models.Publisher.name == publisher_name)

list_of_ouput = []
for tuple in join_query.all():
    list_of_ouput.append(list(tuple))

for el in list_of_ouput:
    for index, el_ in enumerate(el):
        if type(el_) == str:
            pass
        elif type(el_) == float:
            el[index] = str(el_)
        else:
            el[index] = datetime.strftime(el_, '%d-%m-%Y')

for el in list_of_ouput:
    print(' | '.join(el))

session.close()