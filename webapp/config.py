import os

basedir = os.path.abspath(os.path.dirname(__file__))  # Автоматически определяет путь к файлу

WEATHER_DEFAULT_CITY = "Moscow, Russia"
WEATHER_API_KEY = "9a4977c06d964b588ef163935190901"
WEATHER_URL = "http://api.worldweatheronline.com/premium/v1/weather.ashx"

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "webapp.db")

SECRET_KEY = "asdb*&Sdh@jashdbNK@aksjdh*"
