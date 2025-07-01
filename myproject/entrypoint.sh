#!/bin/sh

echo "Ожидаем базу данных PostgreSQL..."

while ! nc -z db_postgres 5432; do
  sleep 1
done

echo "База доступна, запускаем миграции..."

python manage.py migrate

echo "Загружаем фикстуры..."

python manage.py loaddata fixtures/*.json

echo "Готово, запускаем приложение..."

exec "$@"
