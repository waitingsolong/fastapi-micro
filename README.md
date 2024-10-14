## Description
Microservices on FastAPI

## Pre-setup
1. Convert Line Endings
Run dos2unix to ensure that the scripts have the correct line endings:
```bash
dos2unix -R ./scripts/*.sh
```

2. Add Environment Variable
Add the following line to ./app/microservices/media/env.py:
```python
YANDEX_DISK_API_KEY=...
```
Else media will be stored in filesystem in folder data/media/

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

- Ensure that ports 80 and 443 on the host are not being used by other processes
- It sometimes necessary restart ./scripts/setup_ssl_mock.sh
- When writing nginx.conf just copy final result to nginx.conf.template and replace your host (e.g. "localhost") with $SERVER_NAME

## How to Create a New Microservice

1. **Select a Similar Microservice**  
   Choose an existing microservice as a analogue. You can copy "media" based on Postgres or "news" based on MongoDB.

2. **Copy the File Structure**  
   Use the following command to copy the file structure from the old service to the new service:
   ```bash
   python ./scripts/copymicro.py <old_service> <new_service>
   ```
   **Note:** This script simply replaces occurrences of `<old_service>` with `<new_service>`, so it is best suited for microservices where the object names match the service name (e.g., "AuthModel" == "auth", but "MatchModel" != "matches").

3. **Database Migration (if using Postgres)**  
   If you are using Postgres, create a migrations directory for your new service:
   - Create the directory: `migrations/<new_service>` based on your analogue
   - Update `script_location` in `alembic.ini` to point to the new migrations directory.
   - Import the necessary models and `declarative_base` in `env.py`.

4. **Update `docker-compose.yml`**  
   Add the new service to your `docker-compose.yml` file based on your analogue

5. **Update Nginx Configuration**  
   Add the new service to `nginx.conf.template` based on your analogue. After making the changes, run:
   ```bash
   ./scripts/gen_nginx_conf.sh
   ```
