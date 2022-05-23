FROM ubuntu:20.04
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y tzdata && apt install -y python3.8 python3-pip
RUN apt install python3-dev libpq-dev nginx -y
RUN mkdir /app
COPY requirements.txt /
RUN pip install -r requirements.txt
ADD . /app
WORKDIR /app
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "salary_prediction_django.wsgi"]