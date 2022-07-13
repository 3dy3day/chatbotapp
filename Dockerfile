FROM python:alpine

WORKDIR /app

ADD ./requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "server.py"]