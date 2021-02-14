FROM tiangolo/uwsgi-nginx-flask:python3.8

LABEL maintainer="The Flask Image Gallery Team"


# Install dependencies for opencv
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y


# Copy the Flask app
COPY ./app /app
COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip install -r requirements.txt


# Copy the React app
COPY ./react-app/build /app/web/static/ui


# Definitions for nginx
ENV STATIC_URL /static
ENV STATIC_PATH /app/web/static
ENV STATIC_INDEX 0