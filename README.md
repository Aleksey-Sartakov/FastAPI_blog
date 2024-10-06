# <span style="color: #5c8aff">Блог для публикации статей (только backend часть)</span>

## <span style="color: #7230ff">Описание проекта</span>
- Это ***pet-проект***, представляющий из себя ***backend*** часть для блога, в которой реализован основной необходимый функционал.
- ***Целью*** проекта является ***демонстрация навыков*** использования некоторого набора инструментов, а также ***примеров*** написания ***кода***.
- Полное ***доведение*** проекта ***до конца***, т. е. реализация всевозможных необходимых функций, ***НЕ является необходимым*** для достижения
поставленной цели

### 1. Что реализовано?
- контейнеризация с использованием ***Docker и Docker-compose***
- описаны модели БД с использованием ***SQLAlchemy ORM***
- миграция БД с использованием ***alembic***
- валидация данных с использованием ***Pydantic***
- система аутентификации с использованием ***FastAPI Users***. Есть 2 роли пользователя: администратор, обычный пользователь:
  + возможности обычного пользователя:
    1) Создание/Удаление/Редактирование собственной статьи
    2) Просмотр списка всех статей по категориям
    3) Прочтение статьи и комментариев к ней
    4) Создание категории
    5) Написание комментария к любой статье
    6) Создание жалобы на статью
    7) Регистрация на сайте
    8) Авторизация с использованием JWT токена
  + возможности администратора:
    1) Все вышеперечисленное
    2) Просмотр всех жалоб
    3) Просмотр статей, на которые есть жалобы
    4) Просмотр жалоб на одну конкретную статью
    5) Удаление всех статей / жалоб / категорий / пользователей
    6) Назначение другого пользователя администратором
    7) Бан / разбан пользователя
  + возможности незарегистрированных или забаненных пользователей:
    1) Просмотр списка всех статей по категориям
    2) Прочтение статьи и комментариев к ней
- пагинация
- сортировка

## <span style="color: #f00">Как запустить?</span>
### 1. Запуск в контейнере:
```
    docker-compose up --build --force-recreate -d
```


### 2. Запуск без контейнера:
1) Необходимо создать и запустить БД PostgreSQL со следующими настройками:
     - *порт:* 5432
     - *пароль:* root
     - *имя пользователя:* postgres
     - *имя БД:* postgres

2) Находясь в каталоге проекта выполнить в терминале следующую команду:
```
    alembic upgrade head
```

3) Далее необходимо запустить сервер используя следующую команду:
```
    uvicorn src.main:app --reload
```

4) При первом запуске миграций в бд будут добавлены 2 роли: "admin" и "user" (по итогу не используются)
5) Также будет создан пользователь, обладающий правами администратора. Логин и пароль для этого пользователя: root, root


## <span style="color: #00ff1a">Документация и тестирование API</span>

- Документация к API и возможность его протестировать будет доступна по адресу: http://localhost:8000/docs


## <span style="color: #fbff00">Используемый стек</span>
- Python 3.10
- PostgreSQL 16.3
- SQLAlchemy
- FastAPI
- FastAPI Users
- Alembic
- Локальная ОС:
    + Windows 10
- Образ ОС в docker-контейнере:
    + python:3.10.14-alpine3.20


