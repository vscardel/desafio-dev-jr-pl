FROM python:3.8

EXPOSE 8080

WORKDIR /TransportAPI

COPY requirements.txt /TransportAPI

RUN pip3 install -r requirements.txt


COPY db.py /TransportAPI
COPY app.py /TransportAPI
COPY main.py /TransportAPI

CMD python3 main.py