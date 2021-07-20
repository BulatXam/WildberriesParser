from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, TEXT, CHAR
# from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import pandas as pd
import datetime

Base = declarative_base()

username = input('username: ')
password = input('password(если нет, пишите None): ')
host = input('host: ')
port = input('port: ')
db_path = input('Название бд: ')

if password == "None":
    engine = create_engine(f'mysql+pymysql://{username}@{host}:{port}/{db_path}?charset=utf8', echo=True)
else:
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{db_path}?charset=utf8', echo=True)


class Product(Base):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True)
    title = Column(TEXT(300,  collation='utf8_bin'))
    price = Column(Integer)
    article = Column(TEXT(300, collation='utf8_bin'))
    comment_count = Column(Integer)
    sales_count = Column(Integer)
    count_in_stock = Column(Integer)

    def __init__(self, title, price, article, comment_count, sales_count, count_in_stock):
        self.title = title
        self.price = price
        self.article = article
        self.comment_count = comment_count
        self.sales_count = sales_count
        self.count_in_stock = count_in_stock

    def __repr__(self):
        return f"<{self.__class__.__name__}(title={self.title!r}, price={self.price!r})>"

    def get_text(self):
        return f"Название: {self.title}\nЦена: {self.price}\nАртикул: {self.article}\nКоличество отзывов: {self.comment_count}\nКоличество продаж: {self.sales_count}\nКоличество на складе: {self.count_in_stock}"

    def get_in_pandas(self):
        return pd.Series({'title': self.title,
                          'price': self.price,
                          'article': self.article,
                          'comment_count': self.comment_count,
                          'sales_count': self.sales_count,
                          'count_in_stock': self.count_in_stock
                          })

# Base.metadata.create_all(engine) # Как только создали таблицу-убираем эту строчку
