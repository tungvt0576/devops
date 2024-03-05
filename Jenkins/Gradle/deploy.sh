#!/bin/bash

# Set default values
SSH_USER=dep
SSH_HOST=192.168.0.86

# Check if IMAGE_TAG and PORT are provided as command-line arguments
if [[ -n "$1" ]]; then
  IMAGE_TAG=$1
fi

if [[ -n "$2" ]]; then
  PORT=$2
fi

# Check if IMAGE_TAG and PORT are not empty
if [[ -z "$IMAGE_TAG" || -z "$PORT" ]]; then
  echo "Please provide both IMAGE_TAG and PORT."
  exit 1
fi

# Remove old container and old version image
ssh $SSH_USER@$SSH_HOST "docker rm -f $IMAGE_TAG && docker rmi -f $IMAGE_TAG"
# Load Docker image
docker save $IMAGE_TAG | ssh $SSH_USER@$SSH_HOST " docker load"
# Start Docker container
ssh $SSH_USER@$SSH_HOST "docker run -d -p $PORT:8099  --name $IMAGE_TAG --restart always $IMAGE_TAG"
# Remove old version image from local machine
docker rmi -f $IMAGE_TAG