#!/bin/bash

# echo "Disabled. Placeholder for not-mocked cerficates"
# exit 1

ask_regenerate_certificates() {
    while true; do
        read -p "Do you want to regenerate SSL certificates? (y/n): " yn
        case $yn in
            [Yy]* ) 
                regenerate=true
                break
                ;;       
            [Nn]* ) 
                echo "Skipping SSL certificate regeneration."
                exit 0  
                ;;      
            * ) 
                echo "Please answer 'y' or 'n.'"; 
        esac
    done
}


ask_regenerate_certificates

if [ -f "$CERT_FILE" ]; then
  sudo rm "$CERT_FILE"
  echo "Old certificate removed."
fi

if [ -f "$KEY_FILE" ]; then
  sudo rm "$KEY_FILE"
  echo "Old key file removed."
fi

if [ -f "$DH_FILE" ]; then
  sudo rm "$DH_FILE"
  echo "Old DH parameters removed."
fi

# assert: SERVER_NAME is set
if [ -f ".env" ]; then
  export $(cat .env | xargs)
fi

CERT_PATH="./data/cert"

sudo mkdir -p $CERT_PATH

CERT_FILE="$CERT_PATH/selfsigned.crt"
KEY_FILE="$CERT_PATH/selfsigned.key"
DH_FILE="$CERT_PATH/dhparam.pem"

echo "Generating mock SSL certificate..."
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout $KEY_FILE \
  -out $CERT_FILE \
  -subj "/CN=${SERVER_NAME}" && echo "SSL certificate successfully generated." || echo "Error generating SSL certificate."

echo "Generating Diffie-Hellman parameters..."
sudo openssl dhparam -out $DH_FILE 2048 && echo "DH parameters successfully generated." || echo "Error generating DH parameters."

echo "SSL certificates and DH parameters generated and stored in $CERT_PATH."
