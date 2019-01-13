from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from webapp.forms import LoginForm
from webapp.model import db, News, User
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

    # Атрибуты логин менеджмента
    login_manager = LoginManager()
    login_manager.init_app(app)  # Инициализируем логин менежера
    login_manager.login_view = 'login'  # Указываем какая функция отвечает за авторизацию

    # Проверяем кеш пользователя на момент наличия авторизации, дабы всякие не шлялись
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        # не пускаем на главную страницу, если нет авторизации
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        page_title = 'PythonApp'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.date.desc()).all()
        # БД_новости.запрос.при_этом_отфильтровать_по(БД_новости.дата_пудликации.в_обратном_порядке()).все_данные()

        return render_template('index.html', weather=weather, page_title=page_title, news_list=news_list)

    @app.route('/login')
    def login():
        # Если пользователь уже авторизован, то не нужно его деражать на странице авторизации,
        # а сразу перекидываем его на главную страницу. Иначе же, запрашиваем форму авторизации
        print(current_user)
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        # Запрашиваем пользователя из базы данных
        if form.validate_on_submit():
            # Пытаемся получить такого пользователя по имени из базы данных
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)  # Авторизуем пользователя на странице
                flash('Вы успешно вошли на сайт')  # Говорим ему, что он красавчег
                return redirect(url_for('index'))  # Редирект на главную страницу программы
        # Если авторизация не корректная
        flash('Неправильное имя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинелись')
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required  # Дикортаор, для проверки ролей
    def admin_index():
        if current_user.is_admin:
            return 'Hello, ADMIN !!!'
        flash('Административный доступ запрещен!')
        return redirect(url_for('login'))

    return app
