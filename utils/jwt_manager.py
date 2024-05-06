import os
from dotenv import load_dotenv
from jwt import encode, decode

load_dotenv()

secret = os.getenv("SECRET_KEY")


def create_token(data: dict) -> str:
    return encode(payload=data, key=secret, algorithm="HS256")


def validate_token(token: str) -> dict:
    return decode(jwt=token, key=secret, algorithms=["HS256"])
