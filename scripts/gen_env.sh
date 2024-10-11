#!/bin/bash

ENV_FILE=".env"
SERVER_NAME=""

if [ -f "$ENV_FILE" ]; then
  echo "Loading variables from $ENV_FILE"
  source "$ENV_FILE"
fi

if [ -n "$SERVER_NAME" ]; then
  echo "Using saved SERVER_NAME=$SERVER_NAME"
  exit 0
else
  # Ask user to choose server mode: host or dev
  while true; do
    read -p "Select server mode: 'host' for remote or 'dev' for localhost: " SERVER_MODE

    case $SERVER_MODE in
      host)
        while true; do
          read -p "Enter the domain for the host (e.g., 34.0.251.246): " SERVER_NAME
          if [ -z "$SERVER_NAME" ]; then
            echo "Error: domain cannot be empty. Please try again."
          else
            echo "Warning: Changing SERVER_NAME later must be done manually in this file."
            break
          fi
        done
        break
        ;;
      dev)
        SERVER_NAME="localhost"
        break
        ;;
      *)
        echo "Error: please enter 'dev' or 'host'."
        ;;
    esac
  done
fi

if [ -f "$ENV_FILE" ]; then
  rm "$ENV_FILE"
fi

touch "$ENV_FILE"

if [ "$SERVER_MODE" = "dev" ]; then
  echo "DEV=true" >> $ENV_FILE
  echo "SERVER_NAME=localhost" >> $ENV_FILE
else
  echo "DEV=false" >> $ENV_FILE
  echo "SERVER_NAME=$SERVER_NAME" >> $ENV_FILE
fi

echo ".env file successfully created"
