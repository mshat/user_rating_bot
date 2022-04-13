# user_rating_bot

## Описание
Учебный проект: чат-бот для телеграм, отслеживающий реакции на сообщения в группе.
Бот находится в стадии разработки

## Технологии
**Бэкенд**:
* Api на Django Rest Framework
* Для получения пользовательских реакций на сообщения используется кастомный телеграм-клиент (пакет Pyrogram). Обновление этих данных реализовано как периодическая Celery задача (пакет django-celery-beat).
* Бэкенд, воркер Selery и брокер задач Redis работают Docker контейнерах
**Фронт** - телеграм бот, используется пакет PySimpleGUI
**Тесты** - на данный момент есть набор позитивных апи тестов в виде Postman коллекции   

