FROM python:3.8.3-buster

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "-t", "120", "wsgi:app"]
