FROM python:3.11-alpine

RUN mkdir -p /app/logs

COPY ./dist/*.whl /app

WORKDIR /app

RUN python3 -m pip install *.whl

CMD ["irc2phpbb"]
