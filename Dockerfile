FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=2.0.1
ENV PYTHONPATH=/src


RUN apt-get update && apt-get install -y vim && apt-get upgrade -y
RUN pip install --upgrade pip "poetry==$POETRY_VERSION"

COPY ./pyproject.toml /pyproject.toml
COPY ./poetry.lock /poetry.lock

RUN poetry config virtualenvs.create false
RUN poetry config installer.max-workers 1

RUN poetry install
RUN pip install setuptools

RUN mkdir "src"
WORKDIR /src
COPY . /src
