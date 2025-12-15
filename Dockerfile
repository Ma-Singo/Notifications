FROM python:alpine-14

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "manage.py", "runserver"]