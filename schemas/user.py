from pydantic import BaseModel


# class for the users
class User(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_user = {
            "example": {"email": "example@example.com", "password": "hello_world_2024"}
        }
