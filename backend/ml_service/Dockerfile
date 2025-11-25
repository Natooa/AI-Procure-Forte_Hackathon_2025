# --- Используем официальный Python образ ---
FROM python:3.11-slim

# --- Рабочая директория ---
WORKDIR /app

# --- Системные зависимости ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# --- Устанавливаем зависимости Python ---
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# --- Копируем весь проект ---
COPY . .

# --- Прокидываем порт ---
EXPOSE 8000

# --- Команда запуска ---
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
