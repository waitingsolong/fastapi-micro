#!/bin/bash

ask_install_docker() {
    if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
        echo "Docker and Docker Compose are already installed."
        exit 0
    fi

    while true; do
        read -p "Install Docker, Docker Compose? (y/n): " yn
        case $yn in
            [Yy] ) break;; 
            [Nn] ) echo "Docker installation canceled."; exit;;
            * ) echo "Please answer 'y' or 'n'.";  
        esac
    done
}

ask_install_docker

sudo apt-get update

sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker GPG key and repository
sudo mkdir -m 0755 -p /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl start docker
sudo systemctl enable docker

sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "Docker and Docker Compose have been installed successfully!"
