set dotenv-load

SERVER_IMAGE_NAME := "ghcr.io/casualcodersprojects/smarthome-server-server:main"
FRONTEND_IMAGE_NAME := "ghcr.io/casualcodersprojects/smarthome-server-web:main"

default:
  just --list --unsorted

build-server:
  #!/bin/bash
  cd server
  docker build -t {{SERVER_IMAGE_NAME}} .
  cd ..

build-frontend:
  #!/bin/bash
  cd frontend
  docker build -t {{FRONTEND_IMAGE_NAME}} .
  cd ..

build: build-server build-frontend

run-services:
  docker compose -f docker/docker-compose-dev.yml up

run-server:
  #!/bin/bash
  cd server
  python main.py
  cd ..

run-frontend:
  #!/bin/bash
  cd frontend
  PORT=5200 yarn dev
  cd ..

run-mock:
  #!/bin/bash
  cd server
  python mock_device.py
  cd ..

dev:
  overmind start

start:
  docker compose up

up:
  docker compose up -d

down:
  docker compose down
