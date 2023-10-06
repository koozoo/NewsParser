FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade setuptools && \
    pip3 install -r requirements.txt && \
    chmod 755 .
COPY . .
