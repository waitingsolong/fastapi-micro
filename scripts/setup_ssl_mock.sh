#!/bin/bash

# Load environment variables from .env file
if [ -f ".env" ]; then
  export $(cat .env | xargs)
fi

if [ "$DEV" = "true" ]; then
  CERT_PATH="./data/cert"
else
  CERT_PATH="/etc/nginx/ssl"
fi

sudo mkdir -p $CERT_PATH

CERT_FILE="$CERT_PATH/selfsigned.crt"
KEY_FILE="$CERT_PATH/selfsigned.key"
DH_FILE="$CERT_PATH/dhparam.pem"

if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ] && [ -f "$DH_FILE" ]; then
  echo "SSL certificate and DH parameters already exist in $CERT_PATH."
else
  echo "Generating mock SSL certificate..."
  sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout $KEY_FILE \
    -out $CERT_FILE \
    -subj "/CN=${SERVER_NAME}" && echo "SSL certificate successfully generated." || echo "Error generating SSL certificate."

  echo "Generating Diffie-Hellman parameters..."
  sudo openssl dhparam -out $DH_FILE 2048 && echo "DH parameters successfully generated." || echo "Error generating DH parameters."

  echo "SSL certificates and DH parameters generated and stored in $CERT_PATH."
fi
