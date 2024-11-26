FROM python:3.10-slim

# Установим зависимости для PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

WORKDIR /app

# Скопируем зависимости
COPY requirements.txt .

# Установим зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем приложение
COPY app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
