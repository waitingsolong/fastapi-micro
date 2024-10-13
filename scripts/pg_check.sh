#!/bin/bash

MICROSERVICES_DIR="./app/microservices"

for microservice in "$MICROSERVICES_DIR"/*; do
    if [ -d "$microservice" ]; then
        microservice_name=$(basename "$microservice")
        
        echo "Connect to: $microservice_name"
        
        docker-compose exec db psql -U postgres -d "$microservice_name" -c "\dt"
        
        echo "-------------------------------------------"
    fi
done
