FROM python:3.11-slim

RUN python3 -m venv /opt/venv

WORKDIR /opt

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/