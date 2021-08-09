FROM python:3.8

EXPOSE 8080

WORKDIR /desafio-dev-jr-pl

COPY requirements.txt /desafio-dev-jr-pl

RUN pip3 install -r requirements.txt

COPY test.py /desafio-dev-jr-pl
COPY test_objects.py /desafio-dev-jr-pl
COPY graph.py /desafio-dev-jr-pl
COPY app.py /desafio-dev-jr-pl
COPY db.py /desafio-dev-jr-pl
COPY main.py /desafio-dev-jr-pl

CMD python3 main.py