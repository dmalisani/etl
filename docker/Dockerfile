FROM python:3.7.7-buster

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "-t", "120", "wsgi:app"]