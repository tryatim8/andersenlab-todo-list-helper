FROM python:3.12.3-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip 'poetry==2.1.3' \
    && poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./
# RUN poetry install --no-root --no-dev
RUN poetry install --no-root

COPY . .

COPY myproject/entrypoint.sh /app/myproject/entrypoint.sh
RUN chmod +x /app/myproject/entrypoint.sh

CMD ["gunicorn", "mysite.wsgi:application", "-b", "0.0.0.0:8000"]
ENTRYPOINT ["/app/myproject/entrypoint.sh"]
