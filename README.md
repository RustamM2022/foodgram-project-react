# Foodrgam
Foodrgam

## Описание:
Продуктовый помощник - дипломный проект курса Backend-разработки Яндекс.Практикум. Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список избранного, а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Проект реализован на Django и DjangoRestFramework. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием Redoc.

## Особенности реализации
  - Проект завернут в Docker-контейнеры;
  - Образы infra-frontend и foodgram_backend запушены на DockerHub;
  - Реализован workflow c автодеплоем на удаленный сервер и отправкой сообщения в Telegram;
  - Проект был развернут на сервере: http://130.193.41.207/recipes

## Развертывание проекта
  - Установите на сервере docker и docker-compose.
  - Выполните команду docker-compose up -d --buld.
  - Выполните миграции docker-compose exec backend python manage.py migrate.
  - Создайте суперюзера docker-compose exec backend python manage.py createsuperuser.
  - Соберите статику docker-compose exec backend python manage.py collectstatic --no-input.
  - Заполните базу ингредиентами docker-compose exec backend python manage.py load_ingredients.
  - Для корректного создания рецепта через фронт, надо создать пару тегов в базе через админку.

## Документация
Полная документация проeкта (redoc) доступна по адресу http://130.193.41.207/api/docs/redoc.html.

## Системные требования
- Python 3.9
- Django 3.12.18
- djangorestframework 3.12.4
