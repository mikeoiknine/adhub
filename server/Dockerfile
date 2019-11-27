FROM python:3.8-alpine


ADD . /app
WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "app.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True


RUN apk add build-base
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask run --host=0.0.0.0

