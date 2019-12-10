FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ADD . /src/
WORKDIR /src/
#WORKDIR projement/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#COPY projement /projement/