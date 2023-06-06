FROM python:3.10-slim

WORKDIR /app

COPY src/requirements ./requirements

RUN pip install -r requirements/base.txt --no-cache-dir

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY src .

ENV PYTHONPATH=/app

ENTRYPOINT [ "/start.sh" ]
