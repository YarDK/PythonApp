from getpass import getpass  # Поле импут не печает вводимое символы
import sys

from webapp import create_app
from webapp.model import db, User

app = create_app()

with app.app_context():
    new_username = input('Введите имя: ')

    if User.query.filter(User.username == new_username).count():
        print('Такой пользователь уже существует')
        sys.exit(0)

    new_password = getpass('Введите пароль: ')
    password_check_on_correct = getpass('Повторите пароль: ')
    if not new_password == password_check_on_correct:
        print('Пароли не одинаковые')
        sys.exit(0)

    new_user = User(username=new_username, role='admin')
    new_user.set_password(new_password)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь {} c id {}'.format(new_user.username, new_user.id))