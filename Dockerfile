FROM python:3.10

# Установка необходимых пакетов
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Создание рабочей директории
WORKDIR library

# Копирование проекта в контейнер
COPY . .

# Настройка переменных окружения
ENV DJANGO_SETTINGS_MODULE=library.settings
ENV DATABASE_URL=sqlite:///db.sqlite3

# Запуск сервера разработки Django
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "collectstatic", "--no-input"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
