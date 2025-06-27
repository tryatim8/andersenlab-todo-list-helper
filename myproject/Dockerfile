FROM python:3.12.3-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip 'poetry==2.1.1'
RUN apt-get update && apt-get install -y gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

COPY . .
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "myplatform.wsgi:application", "-b", "0.0.0.0:8000"]