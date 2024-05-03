from fastapi import APIRouter
from fastapi.responses import JSONResponse
from jwt_manager import create_token
from schemas.user import User

auth_router = APIRouter()


# .dict() is deprecated. Now use .__dict__ or .model_dump()
@auth_router.post("/login", tags=["auth"], response_model=User)
def login_user(user: User):
    if user.email == "admin@admin.com" and user.password == "admin":
        token: str = create_token(user.__dict__)
        return JSONResponse(status_code=201, content=token)
