FROM python:3.12-slim-bullseye AS dev

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./src /app/src

CMD ["fastapi", "dev", "--host", "0.0.0.0", "src/main.py"]

FROM dev AS test

RUN pip install pytest \
                httpx
