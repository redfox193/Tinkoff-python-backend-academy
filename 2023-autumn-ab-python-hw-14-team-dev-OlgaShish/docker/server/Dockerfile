FROM python:3.11 AS builder

WORKDIR /opt/build

RUN pip install poetry

COPY pyproject.toml poetry.lock src config.json ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

FROM python:3.11-slim

WORKDIR /opt

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src ./src
COPY config.json ./

CMD ["uvicorn", "src.homework.main:app", "--host", "0.0.0.0", "--port", "8000"]
