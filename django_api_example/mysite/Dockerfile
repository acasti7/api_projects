sytnax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-alpine as builder
EXPOSE 8000
WORKDIR /app

# install system dependences
RUN apk update
RUN apk add \
    pkgconfig \
    gcc \
    musl-dev \
    bash \
    mariadb-dev

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r -requirements.txt

# Copy the current directory contents in the container at /usr/src/app
COPY . /app

# Run Server
ENTRYPOINT ["python3"]
CMD ["manage.py","runserver","0.0.0.0:8000"] ## this runs the server on a particular port on the docker container

