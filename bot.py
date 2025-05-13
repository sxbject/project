from telegram.ext import Application, CommandHandler, MessageHandler, filters
from database import Session, User, WeatherRequest
from weather_api import get_weather
from config import Config
from datetime import datetime


async def start(update, context):
    user = update.effective_user
    await save_user(user)
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я бот погоды.\n"
        "Просто напиши название города, и я покажу тебе погоду."
    )


async def save_user(user):
    session = Session()
    db_user = session.query(User).filter_by(telegram_id=user.id).first()
    if not db_user:
        db_user = User(
            telegram_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username
        )
        session.add(db_user)
        session.commit()
    session.close()


async def save_request(user_id, location, weather_data):
    session = Session()
    request = WeatherRequest(
        user_id=user_id,
        location=location,
        request_time=datetime.now(),
        weather_data=str(weather_data)
    )
    session.add(request)
    session.commit()
    session.close()


def get_history(user_id):
    session = Session()
    requests = session.query(WeatherRequest).filter_by(user_id=user_id).order_by(
        WeatherRequest.request_time.desc()).limit(5).all()
    session.close()
    return requests


async def weather_handler(update, context):
    location = update.message.text
    weather = get_weather(location)

    if weather:
        response = (
            f"Погода в {location}:\n"
            f"🌡 Температура: {weather['temp']}°C (ощущается как {weather['feels_like']}°C)\n"
            f"☁️ Состояние: {weather['description']}\n"
            f"💧 Влажность: {weather['humidity']}%\n"
            f"🌬 Ветер: {weather['wind']} м/с"
        )
        await save_request(update.effective_user.id, location, weather)
    else:
        response = "Не удалось получить данные о погоде. Проверьте название города."

    await update.message.reply_text(response)


async def history_handler(update, context):
    requests = get_history(update.effective_user.id)
    if requests:
        response = "Ваши последние запросы:\n"
        for req in requests:
            response += f"📍 {req.location} - {req.request_time.strftime('%d.%m.%Y %H:%M')}\n"
    else:
        response = "У вас пока нет истории запросов."

    await update.message.reply_text(response)


def main():
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("history", history_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather_handler))

    application.run_polling()


if __name__ == '__main__':
    main()