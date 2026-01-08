# Проект «Music Library» — Лабораторная работа

Проект представляет собой веб-приложение на Django для управления музыкальной библиотекой.  
В рамках лабораторной работы приложение было перенесено с SQLite на PostgreSQL и упаковано в Docker-контейнеры для обеспечения отказоустойчивости, производительности и соответствия промышленным стандартам разработки.

## Технологии

- Backend: Python 3.12, Django 5.1
- База данных: PostgreSQL 15
- Контейнеризация: Docker, Docker Compose

## Безопасность

- Все конфиденциальные данные (пароли, SECRET_KEY) передаются через переменные окружения.
- Файл `.env` не включён в репозиторий (добавлен в `.gitignore`).
- Никакие секреты не хранятся в исходном коде.

## Команды Docker и Docker-Compose.

```bash
# Запустить Docker
docker-compose up --build
 
# Применить миграции
docker-compose exec web python manage.py migrate

# Собрать статические файлы
docker-compose exec web python manage.py collectstatic --noinput

# Положить Docker
docker-compose down
```bash