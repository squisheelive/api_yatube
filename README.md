# Yatube API
##### В этом проекте реализован API для небольшой социальной сети Yatube.
##### В Yatube пользователи могут создавать и комментировать публикации, а также подписываться на других авторов.

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/squisheelive/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
### Примеры запросов:
```
GET http://.../api/v1/posts/?limit=3&offset=6
```
##### HTTP_200_OK
```
{
    "count": 100500,
    "next": "http://.../api/v1/posts/?limit=3&offset=9",
    "previous": "http://.../api/v1/posts/?limit=3&offset=3",
    "results": [
        {
            "id": 123,
            "author": "username",
            "text": "Некторый текст",
            "pub_date": "2021-09-17T20:48:53.093050Z",
            "image": "http://.../api/v1/posts/posts/image.jpg",
            "group": some_group
        },
        {
            ...
        },
    ]
}
```
```
POST http://.../api/v1/posts/

{
    "text": "Некоторый текст"
}
```
##### HTTP_201_CREATED
```
{
    "id": 1234,
    "author": "username",
    "text": "Некоторый текст",
    "pub_date": "2021-09-17T21:28:12.998465Z",
    "image": null,
    "group": null
}
```
### Больше информации:
Подробную документацию к API вы можете найти после запуска проекта по адресу http://127.0.0.1:8000/redoc/
