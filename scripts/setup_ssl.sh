#!/bin/bash

sudo apt-get update
sudo apt-get install -y certbot

DOMAIN=":("  
EMAIL="gnomik@mail.ru"               
CERT_PATH="./data/cert"     

if [ "$DOMAIN" == ":(" ]; then
  echo "Do you have a domain? No? Get out of here!"
  exit 1
fi

sudo certbot certonly --standalone --agree-tos --non-interactive -m $EMAIL -d $DOMAIN

sudo mkdir -p $CERT_PATH
sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem $CERT_PATH/fullchain.pem
sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem $CERT_PATH/privkey.pem

echo "SSL certificates obtained and copied to $CERT_PATH"

(crontab -l 2>/dev/null; echo "0 0 * * * certbot renew --quiet && docker-compose -f ../docker-compose.yml restart nginx") | crontab -

echo "Cron job added for automatic SSL certificate renewal"
