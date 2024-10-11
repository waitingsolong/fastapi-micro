## Description
Microservices on FastAPI

## Steps to Run

### Run the command
```bash
./scripts/run.sh
```

### Then
```bash
sudo docker-compose up --build -d
```

## If something went wrong, follow these steps manually:

### 1. Retrieve Environment Variables
First, you need to retrieve the environment variables:
```bash
./scripts/get_env.sh
```

### 2. Generate nginx.conf
To generate the nginx.conf based on the environment variables:
```bash
./scripts/gen_nginx_conf.sh
```

### 3. Set Up SSL Certificates
To set up self-signed SSL certificates:
```bash
./scripts/setup_ssl_mock.sh
```

### 4. Install Docker
If Docker is not yet installed on the host, run the script to install it via dcpkg (or install it manually):
```bash
./scripts/install_docker.sh
```

### 5. Start the Project
Now you can start the project using Docker Compose:
```bash
sudo docker-compose up --build -d
```

### Notes

- Ensure that ports 80 and 443 on the host are not being used by other processes.