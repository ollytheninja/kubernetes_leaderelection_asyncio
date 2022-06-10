FROM python:alpine

RUN apk add git

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY leaderelection .

CMD [ "python", "example.py" ]
