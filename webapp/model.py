from flask_login import UserMixin  # Добавляет доп атрибуты авторицаии, просто надо...
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# Модель (шаблон) нашей базы данных
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # айдишник новости
    title = db.Column(db.String, nullable=False)  # Заголовок новости
    url = db.Column(db.String, unique=True, nullable=False)  # Ссылка на новость
    date = db.Column(db.DateTime, nullable=False)  # Дата публикации
    text = db.Column(db.Text, nullable=True)  # Текст новости

    # Эта борода системные названия переделывает в читаемые данные для человека (вроде хз)
    def __repr__(self):  # sels - обращаемся у экземпляру класса, который сейчас активен
        return '<News {} {}'.format(self.title, self.url)


# Шаблон для базы с пользователями
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    # Метод шифрования присланного паролья
    def set_password(self, password):  # Self - это значит вызвать параметр для текущего "пользователя" (сущности)
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Дикортаор, который вызывает метод как аттрибут
    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User name = {} id = {}'.format(self.username, self.id)
