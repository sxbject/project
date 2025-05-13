import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN = "5135504370:AAFUU3kEQpuUZG-L2w8XYJvueDUj5TlbHSs"
    OPENWEATHER_API_KEY = "1e80b9f61248cf8dbd2968957482e48b"
    DATABASE_URI = 'sqlite:///weather_bot.db'