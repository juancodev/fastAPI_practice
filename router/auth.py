from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token

auth_router = APIRouter()


# class for the users
class User(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_user = {
            "example": {"email": "example@example.com", "password": "hello_world_2024"}
        }


# .dict() is deprecated. Now use .__dict__ or .model_dump()
@auth_router.post("/login", tags=["auth"], response_model=User)
def login_user(user: User):
    if user.email == "admin@admin.com" and user.password == "admin":
        token: str = create_token(user.__dict__)
        return JSONResponse(status_code=201, content=token)
