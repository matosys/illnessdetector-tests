# Dockerfile
FROM python:3.9-slim

RUN pip install flask

COPY app.py /app/app.py
COPY index.html /app/index.html

WORKDIR /app

EXPOSE 5000

CMD ["python", "app.py"]