FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh


RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip


RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

# Production
CMD ["gunicorn", "notifications.wsgi:application", "--bind", "0.0.0.0:8000"]
# Development
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]