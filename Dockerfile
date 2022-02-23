# syntax=docker/dockerfile:1

FROM python:3.8.10

WORKDIR /TSA

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py", "--host=0.0.0.0"]
