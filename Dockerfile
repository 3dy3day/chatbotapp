FROM python:alpine

RUN git clone https://github.com/sandy-sunday/chatbotapp.git .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "server.py"]
