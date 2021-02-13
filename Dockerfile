FROM tiangolo/uwsgi-nginx-flask:python3.8

LABEL maintainer="The Flask Image Gallery Team"

COPY ./app /app
# COPY ./react-app /react-app
COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip install -r requirements.txt

# Install dependencies for opencv
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# TODO: initialize react-app


# Run Flask app from nginx
ENV STATIC_URL /static
ENV STATIC_PATH /app/web/static
ENV STATIC_INDEX 0