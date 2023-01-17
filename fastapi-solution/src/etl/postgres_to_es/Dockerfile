FROM python:3.10

WORKDIR /fastapi-solution

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip \
    & pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD python fastapi-solution/src/etl/postgres_to_es/load_data.py