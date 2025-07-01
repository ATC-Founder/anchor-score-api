FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip &&     pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
