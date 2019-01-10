import requests
from bs4 import BeautifulSoup


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
        result_news = []
        for news in all_news:
            title = news.find('a').text  # Берем текст
            url = news.find('a')['href']  # Берем атрибут html
            date = news.find('time').text
            result_news.append({
                'title': title,
                'url': url,
                'date': date
            })
        return result_news
    return False


# Если программа вызвана отдельно, то обратиться к главной странице ресурса
# и вызвать метод для скачки страницы. Скаченная страница записывается в отдельный
# файлик html, т.е. как бы скачали html страницу
