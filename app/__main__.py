import os
import time

import requests
import datetime
from mysql.connector import connect


def get_posts(order: str, offset: int, limit: int) -> list[dict[str, str]]:
    """
    Парсинг постов

    :param order: сортировка постов по атрибуту
    :param offset: смещение постов
    :param limit: лимит постов
    """

    if offset < 0:
        raise TypeError("Параметр offset отрицательный")
    if limit < 0:
        raise TypeError("Параметр limit отрицательный")
    elif limit > 30:
        raise TypeError("Параметр limit слишком большой")

    params = {
        "offset": offset,
        "limit": limit,
    }

    if order and order not in ("id", "title", "url", "created"):
        raise KeyError("Задан несуществующий атрибут для сортировки")
    elif order:
        params["order"] = order

    return requests.get("http://localhost:8000/posts", params=params).json()


def post_sql(posts: list[dict[str, str | datetime]]):
    """
    Запись постов в базу данных
    :param posts: словарь парсенных постов
    """

    host = os.environ.get('MYSQL_HOST')  # получаем из окружения переменную MYSQL_HOST
    user = os.environ.get('MYSQL_USER')  # получаем из окружения переменную MYSQL_USER
    password = os.environ.get('MYSQL_PASSWORD')  # получаем из окружения переменную MYSQL_PASSWORD

    datetime_now = datetime.datetime.now()  # задаём текущее время и дату

    # Преобразуем список словарей в список кортежей и добавим к каждому текущее время и дату
    posts = [(*tuple(post.values()), datetime_now) for post in posts]

    with connect(host=host, user=user, password=password) as connection:  # подключаемся к базе данных
        with connection.cursor() as cursor:
            # Пусть таблица будет называться posts.
            # Применим метод executemany для вставки сразу множества строк:
            cursor.executemany("INSERT INTO posts (title, url, datetime) VALUES (%s, %s, %s)", posts)
            connection.commit()  # отправляем запрос

    print(f"Количество постов: {len(posts)} успешно записано в базу данных.")


def main():
    order = input("Введите атрибут для сортировки: ") or None
    offset = input("Введите значение для смещения: ") or 0  # по умолчанию не делаем смещения
    limit = input("Введите значение для лимита: ") or 5  # по умолчанию возвращаем 5 постов

    post_sql(get_posts(order, int(offset), int(limit)))

    again = input(
        "Повторить процедуру с заданными параметрами через заданный интервал?\n\n"
        "Введите число для включения таймера, либо нажмите Enter, чтобы выйти:  "
    )

    if again:
        # В тз ничего не было про асинхронность, так что просто усыпляем скрипт на заданное время
        # и повторяем парсинг
        time.sleep(int(again))
        post_sql(get_posts(order, int(offset), int(limit)))


if __name__ == '__main__':
    main()
