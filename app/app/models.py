from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    table_number = Column(String, nullable=False)
    guests = Column(Integer, nullable=False)
    dishes = Column(Text, nullable=False)  # Список блюд в виде строки
    status = Column(String, default='Принят')  # Статус заказа
    is_paid = Column(Boolean, default=False)  # Статус оплаты (по умолчанию не оплачен)


# Модель для пользователей
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)  # Уникальное имя пользователя
    role = Column(String, nullable=False)  # Роль пользователя, например: "Официант", "Повар", "Администратор"

# Создаем базу данных и сессии
DATABASE_URL = "sqlite:///cafe.db"  # Используем SQLite для простоты
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
