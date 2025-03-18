# Сборка
# =======
FROM python:3.9-slim as builder

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --user -r requirements.txt

# Финальный образ
# ===============
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local

# Копируем исходный код
COPY . .
ENV PATH=/root/.local/bin:$PATH

# Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
