from flask import Flask, jsonify
from bot import main as run_bot
from threading import Thread
from config import Config

app = Flask(__name__)


@app.route('/')
def index():
    return "Weather Bot Server is running"


@app.route('/api/health')
def health_check():
    return jsonify({"status": "ok"})


def run_flask():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Запускаем бота в основном потоке
    run_bot()