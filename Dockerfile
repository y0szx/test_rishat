FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["sh", "-c", "python ./mysite/manage.py migrate && python ./mysite/manage.py runserver 0.0.0.0:8000"]