import requests
from bs4 import BeautifulSoup
import random
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product
import datetime

username = input('username: ')
password = input('password(если нет, пишите None): ')
host = input('host: ')
port = input('port: ')
db_path = input('Название бд: ')

if password == "None":
    engine = create_engine(f'mysql+pymysql://{username}@{host}:{port}/{db_path}?charset=utf8', echo=True)
else:
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{db_path}?charset=utf8', echo=True)


Session = sessionmaker(bind=engine)
session = Session()


class Category:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def iter_paginate(self):
        i = 0
        while True:
            i += 1
            page = requests.get(self.url, params={'page': i})
            soup_page = BeautifulSoup(page.text, 'html.parser')
            if soup_page.find('a', class_='ref_goods_n_p j-open-full-product-card'):
                yield soup_page.find_all('a', class_='ref_goods_n_p j-open-full-product-card')

    def get_paginate(self):
        return [page for page in self.iter_paginate()]

    def get_product(self, url) -> Product:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        title = soup.find('span', class_='name').text
        price = soup.find('div', class_='final-price-block').find('span', class_='final-cost').text.replace(" ", "").replace("\xa0", "").replace("\n", "")[:-1]
        article = soup.find('div', class_='article').span.text
        comments_count = soup.find('a', id='a-Comments').text[6:]
        sales_count = random.randint(25, 10000)
        count_in_stock = random.randint(1, 1000)

        return Product(title, price, article, comments_count, sales_count, count_in_stock)

    def iter_products(self, products):
        for product in products:
            yield self.get_product('https://www.wildberries.ru' + product['href'])

    def get_products(self, products):
        return [self.get_product('https://www.wildberries.ru' + product['href']) for product in self.iter_products(products)]


def pars_category(url, title=None):
    category = Category(title, url)
    for page in category.iter_paginate():
        for product in category.iter_products(page):
            # print(product.title)
            session.add(product)
            session.commit()


def iter_categories(r):
    catalogs = BeautifulSoup(r.text, 'html.parser').find_all('li',
                                                             class_='menu-burger__main-list-item j-menu-main-item')
    for catalog in catalogs:
        r = requests.get(catalog.a['href'])
        cat = BeautifulSoup(r.text, 'html.parser').find('ul', class_='maincatalog-list-2')
        if cat:
            categories = cat.find_all('li')
            for category in categories:
                yield 'https://www.wildberries.ru' + category.a['href']


def main():
    r = requests.get('https://www.wildberries.ru')
    for category_url in iter_categories(r):
        pars_category(category_url)


if __name__ == '__main__':
    main()
