#!/bin/bash

echo "> ./scripts/gen_env.sh"
./scripts/gen_env.sh

echo "> ./scripts/gen_nginx_conf.sh"
./scripts/gen_nginx_conf.sh

echo "> ./scripts/setup_ssl_mock.sh"
./scripts/setup_ssl_mock.sh

echo "> ./scripts/install_docker.sh"
./scripts/install_docker.sh

echo "Success! You can run docker-compose now: docker-compose up --build -d"
