## Dockerfile for Flask app intended for production with gunicorn
FROM python:3.11.1-alpine3.16

ENV FLASK_APP=app.py

WORKDIR /usr/app
RUN mkdir -p deps/calculator
RUN mkdir src

COPY deps/calculator/calculator.py deps/calculator
COPY src/app.py src
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0", "--workers", "10", "src.app:create_app()"]
