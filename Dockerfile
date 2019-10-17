FROM python:3-alpine

COPY . /app
RUN mkdir -p /app
WORKDIR /app

RUN python3 -m pip install -r .requirements.txt

CMD ["python", "/app/main.py"]
