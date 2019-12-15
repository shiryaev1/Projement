FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ADD . /src/
WORKDIR /src/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

