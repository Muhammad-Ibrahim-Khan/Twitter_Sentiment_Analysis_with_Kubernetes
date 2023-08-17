FROM python:3.9-slim-buster

WORKDIR /.

COPY requirements.txt requirements.txt

RUN python3 -m pip install --no-cache-dir --upgrade pip

RUN python3 -m pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

EXPOSE 4000

COPY . .

CMD ["python", "main.py"]
