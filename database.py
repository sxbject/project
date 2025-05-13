from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()
engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)

class WeatherRequest(Base):
    __tablename__ = 'weather_requests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    location = Column(String)
    request_time = Column(DateTime)
    weather_data = Column(String)

# Создаем таблицы
Base.metadata.create_all(engine)