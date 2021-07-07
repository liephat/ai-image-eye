FROM tiangolo/uwsgi-nginx-flask:python3.8

LABEL maintainer="The Flask Image Gallery Team"


# Install dependencies for opencv
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

# Install dependencies for face-recognition
RUN apt-get install cmake -y

WORKDIR /

# Install Python Environment
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Flask app
COPY ./app app

# Copy the React app
COPY ./react-app/build app/web/static/ui


# Definitions for nginx
ENV STATIC_URL /static
ENV STATIC_PATH /app/web/static
ENV STATIC_INDEX 0