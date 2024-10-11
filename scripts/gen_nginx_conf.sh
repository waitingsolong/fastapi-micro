#!/bin/bash

TEMPLATE_PATH="./conf/nginx.conf.template"
NGINX_CONF_PATH="./conf/nginx.conf"

if [ ! -f "$TEMPLATE_PATH" ]; then
  echo "Error: nginx.conf.template not found. Please specify the template file."
  exit 1
fi

if ! command -v envsubst &> /dev/null; then
  echo "envsubst is not installed. Installing..."
  sudo apt-get update
  sudo apt-get install -y gettext
fi

export SERVER_NAME=""
source ".env"

if [ -z "$SERVER_NAME" ]; then
  echo "Error: SERVER_NAME is not set. Please run gen_env.sh first."
  exit 1
fi

envsubst '${SERVER_NAME}' < "$TEMPLATE_PATH" > "$NGINX_CONF_PATH"
echo "nginx.conf successfully generated with SERVER_NAME=$SERVER_NAME."
