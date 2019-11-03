from python:3.8-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["server.py"]

