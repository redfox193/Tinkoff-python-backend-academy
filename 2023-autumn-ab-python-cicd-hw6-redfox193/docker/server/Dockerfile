FROM python:3.10 AS builder

WORKDIR /opt/build

RUN pip install poetry

COPY pyproject.toml poetry.lock server ./

RUN poetry config virtualenvs.create false && poetry install --no-dev

FROM python:3.10-slim

WORKDIR /opt/app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY ./ /opt/app/

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
