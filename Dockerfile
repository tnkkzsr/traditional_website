FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y \
    build-essential \
    graphviz

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/