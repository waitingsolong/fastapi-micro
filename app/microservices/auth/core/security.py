from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from .config import settings

def get_password_hash(password: str) -> str:
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
    return salt.hex() + key.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    salt = bytes.fromhex(hashed_password[:32])
    stored_key = bytes.fromhex(hashed_password[32:])
    new_key = PBKDF2(plain_password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
    return new_key == stored_key

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
