from flask_sqlalchemy import SQLAlchemy

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
