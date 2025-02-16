#!/bin/bash

# container docker
docker run -d --name redis -p 6379:6379 redis

# fastapi
fastapi dev main.py --reload --port 8000
