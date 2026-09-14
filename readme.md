# YaCut

YaCut — сервис для создания коротких ссылок и загрузки файлов на Яндекс Диск.

Сервис позволяет:

- создавать короткие ссылки для длинных URL;
- задавать собственный короткий идентификатор ссылки;
- автоматически генерировать короткий идентификатор;
- переходить по короткой ссылке на исходный ресурс;
- загружать несколько файлов на Яндекс Диск;
- получать короткие ссылки для скачивания загруженных файлов;
- работать с сервисом через API.

## Технологии

Проект написан на Python с использованием следующих технологий:

- Flask;
- Flask-SQLAlchemy;
- Flask-WTF;
- SQLAlchemy;
- aiohttp;
- Jinja2;
- SQLite;
- API Яндекс Диска.

## API

В проекте доступны два API-эндпоинта:

- `POST /api/id/` — создание короткой ссылки;
- `GET /api/id/<short_id>/` — получение оригинального URL по короткому идентификатору.

## Как запустить проект

Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone git@github.com:Zh-zh-k/async-yacut.git
cd yacut
```

Создайте виртуальное окружение:

```bash
python3 -m venv venv
```

Активируйте его.

Для Linux/macOS:

```bash
source venv/bin/activate
```

Для Windows:

```bash
venv\Scripts\activate
```

Обновите `pip`:

```bash
python -m pip install --upgrade pip
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Переменные окружения

Создайте в корневой директории проекта файл `.env`:

```env
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_token
```

Где:

- `SECRET_KEY` — секретный ключ Flask-приложения;
- `DATABASE_URI` — строка подключения к базе данных;
- `DISK_TOKEN` — OAuth-токен для работы с API Яндекс Диска.

## Создание базы данных

Перед первым запуском приложения создайте таблицы базы данных:

```bash
python -m flask --app yacut shell
```

В открывшейся консоли выполните:

```python
from yacut import db

db.create_all()
exit()
```

## Запуск приложения

Запустите Flask:

```bash
python -m flask --app yacut run
```

Для запуска в режиме отладки:

```bash
python -m flask --app yacut run --debug
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:5000/
```

Страница загрузки файлов:

```text
http://127.0.0.1:5000/files
```

## Тестирование

Для запуска тестов выполните:

```bash
python -m pytest
```

## Автор

Жанна Колпакова (github - @Zh-zh-k)
