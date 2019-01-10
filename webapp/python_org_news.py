from datetime import datetime

import requests
from bs4 import BeautifulSoup

from webapp.model import db, News  # импортируем модель


# Обращаемся к странице и тупо ее скачиваем как текст
def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text  # Возвращаем контент в виде текста
    except(requests.RequestException, ValueError):
        print("Network error")
        return False


def get_python_news():
    html = get_html('https://www.python.org/')
    if html:
        # Возьме и сделаем дерево элеметов из нашего html
        soup = BeautifulSoup(html, 'html.parser')
        # Дерево готого, теперь делаем понему поиск
        all_news = soup.find('div', class_='shrubbery').findAll('li')
        # result_news = []
        for news in all_news:
            title = news.find('a').text  # Берем текст
            url = news.find('a')['href']  # Берем атрибут html
            date = news.find('time').text
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                date = datetime.now()

            save_news(title, url, date)
            '''    
            # Эта часть более не требуется, т.к. теперь данные хронятся в БД
            result_news.append({
                'title': title,
                'url': url,
                'date': date
            })
            '''
        # return result_news
    return False


# Метод для добавления данных в базу данных
def save_news(title, url, date):
    # Проверям, есть ли такая новость
    news_exists = News.query.filter(News.url == url).count()  # Это счетчик, ищет в БД запись, и если есть, то +1
    # Проверяем на наличие, и если url нет, то добавляем новое
    if not news_exists:
        # Объект класса News()
        new_news = News(title=title, url=url, date=date)
        # Кладем в БД
        db.session.add(new_news)
        # Подтверждаем добавление (комитим как в гит)
        db.session.commit()

# Если программа вызвана отдельно, то обратиться к главной странице ресурса
# и вызвать метод для скачки страницы. Скаченная страница записывается в отдельный
# файлик html, т.е. как бы скачали html страницу
