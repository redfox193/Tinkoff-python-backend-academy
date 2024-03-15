FROM python:3.12-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY homework_app/ ./homework_app/
COPY tests/ ./tests/

CMD ["uvicorn", "homework_app.main:app", "--host", "0.0.0.0", "--port", "80"]