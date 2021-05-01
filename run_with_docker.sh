#!/bin/bash

docker build --pull --rm -f "Dockerfile" -t wordcloudgen:latest "."
clear
docker run -p 8501:8501 wordcloudgen:latest