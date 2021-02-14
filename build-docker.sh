#!/bin/bash

# package the React app for deployment
cd react-app
yarnpkg build

# create Docker image
cd ..
docker build -t imagegallery:latest .
