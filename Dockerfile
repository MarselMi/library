FROM python:3.10

# Установка необходимых пакетов
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Создание рабочей директории
WORKDIR library

# Копирование проекта в контейнер
COPY . .
