import os
import argparse
from shutil import copyfile

def mkdir(path):
    os.makedirs(path, exist_ok=True)

def create_main_file(base_dir, name):
    with open(f'{base_dir}/main.py', 'w') as f:
        f.write(f"""from .utils.logging import setup_logging
import grpc
from concurrent import futures
from app.microservices.{name.lower()}.grpc import {name.lower()}_pb2
from app.microservices.{name.lower()}.grpc import {name.lower()}_pb2_grpc
from fastapi import FastAPI
from .api.v1.{name.lower()} import router
from .core.config import settings


app = FastAPI()

app.include_router(router, prefix="/api/v1/{name.lower()}")

class {name}Service({name.lower()}_pb2_grpc.{name}ServiceServicer):
    def Get{name}(self, request, context):
        return {name.lower()}_pb2.{name}Response(message="Hello from {name} via gRPC!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    {name.lower()}_pb2_grpc.add_{name}ServiceServicer_to_server({name}Service(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
""")

def create_utils_and_logging_file(base_dir):
    utils_dir = f'{base_dir}/utils'
    mkdir(utils_dir)

    with open(f'{utils_dir}/logging.py', 'w') as f:
        f.write("""import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

setup_logging()
""")

def create_config_file(base_dir):
    with open(f'{base_dir}/core/config.py', 'w') as f:
        f.write("""from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET: str = "SECRET"

settings = Settings()
""")

def create_grpc_files(base_dir, name):
    grpc_dir = f'{base_dir}/grpc'
    mkdir(grpc_dir)
    
    # Create .proto file
    with open(f'{grpc_dir}/{name.lower()}.proto', 'w') as f:
        f.write(f"""syntax = "proto3";

package {name.lower()};

// The {name} service definition.
service {name}Service {{
  rpc Get{name}({name}Request) returns ({name}Response);
}}

// The request message for the Get{name} RPC.
message {name}Request {{}}

// The response message containing the {name} message.
message {name}Response {{
  string message = 1;
}}
""")

def create_env(base_dir):
    with open(f'{base_dir}/.env', 'w') as f:
        f.write(f"""SECRET=SECRET""")

# CLI functions
def create_db_files(base_dir, db_type):
    if db_type == 'postgres':
        mkdir(f'{base_dir}/models')
        mkdir(f'{base_dir}/schemas')
        print(f"PostgreSQL setup completed for {base_dir}")
    elif db_type == 'mongo':
        mkdir(f'{base_dir}/models')
        mkdir(f'{base_dir}/schemas')
        print(f"MongoDB setup completed for {base_dir}")
    else:
        print("No database configuration chosen.")

def handle_database_choice(base_dir):
    db_type = input("Enter database type (PG for PostgreSQL, MONGO for MongoDB, or leave empty to skip): ").strip().upper()

    if db_type == 'PG':
        create_db_files(base_dir, 'postgres')
    elif db_type == 'MONGO':
        create_db_files(base_dir, 'mongo')
    else:
        print('No database chosen.')

def create_microservice(name):
    base_dir = f'app/microservices/{name.lower()}'

    mkdir(base_dir)
    mkdir(f'{base_dir}/api/v1')
    mkdir(f'{base_dir}/core')

    create_env(base_dir)
    create_main_file(base_dir, name)
    create_utils_and_logging_file(base_dir)
    create_config_file(base_dir)
    create_grpc_files(base_dir, name)

    handle_database_choice(base_dir)

    print(f'Microservice {name} created successfully!')

def create_copyme_file():
    tmp_dir = 'tmp'
    mkdir(tmp_dir)

    with open(f'{tmp_dir}/copyme.txt', 'w') as f:
        f.write("""bar:  
    build:  
      context: ./bar  
      dockerfile: Dockerfile  
    hostname: bar  
    container_name: bar  
    ports:  
      - "50052:50051"  
    env_file:  
      - bar/.env  
    volumes:  
      - ./bar:/home/bar  
    networks:  
      - my-net
""")
    print("copyme.txt created in tmp/")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Microservice creation tool")
    parser.add_argument("name", help="Name of the microservice")
    args = parser.parse_args()

    create_microservice(args.name)
    create_copyme_file()
