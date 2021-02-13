FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app
COPY ./react-app /react-app
COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip install -r requirements.txt

# Install dependencies for opencv
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# TODO: initialize react-app

EXPOSE 5000

# TODO: run flask app not from dev server but from nginx
CMD ["python", "-m", "app"]

# TODO: run react-app
