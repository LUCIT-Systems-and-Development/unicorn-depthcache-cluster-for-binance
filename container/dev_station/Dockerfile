FROM python:3.12.3-slim

RUN apt-get update && apt-get install -y \
    curl \
    iputils-ping \
    net-tools \
    vim \
    bash \
    telnet \
    && apt-get clean

WORKDIR /app/dev_station

COPY ./container/dev_station/ /app/dev_station

RUN python3.12 -m venv /app/venv

CMD ["/bin/sh", "-c", "python -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt"]
