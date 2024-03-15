# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /opt

# Install Poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock ./
COPY server ./server
COPY config ./config
COPY files ./files
COPY tests ./tests

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install

# Application entrypoint
CMD ["uvicorn", "server.asgi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
