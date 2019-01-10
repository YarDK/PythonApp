from flask import Flask, render_template

from webapp.model import db, News
from webapp.python_org_news import get_python_news
from webapp.weather import weather_by_city

'''
Мы создаем переменную app, которая и будет являться Flask приложением. __name__ - это имя
текущего приложения. Т.е. app = приложением Flask является файл server.py 

Файл был переименован в __init__.py, что бы при импорте корневой папки, происходил импорт всех файлов как 
отдельный мобуль

Проект строится по принцепу патерна проектирования "Фабрика", тем самым мы упаковываем всю работу
по инициализации сервера внутрь функции
'''


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)  # Инициализируем базу данных

    @app.route('/')
    def index():
        page_title = 'PythonApp'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.date.desc()).all()
        # БД_новости.запрос.при_этом_отфильтровать_по(БД_новости.дата_пудликации.в_обратном_порядке()).все_данные()

        return render_template('index.html', weather=weather, page_title=page_title, news_list=news_list)

    return app
