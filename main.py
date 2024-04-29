from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token
from config.database import engine, Base
from middleware.error_handler import ErrorHandler
from router.movie import movie_router

"""
* HTMLResponse = useful for send HTML response to the browser.
* JSONResponse = useful for send JSON response to the client.
* Path = useful for send a limit and offset in params.
* Query = useful for query in route
* Status = useful for all status code.
* HTTPException = useful for send error Message and don't stop the app.
* Request = util para la solicitud que vamos a requerir desde la petición
* jsonable_encoder = nos sirve para convertir la respuesta del modelo de la clase en respuesta json
"""
# instance of The Class FastAPI
app = FastAPI()

# title of my application and docs
app.title = "My app with FastAPI"

# version of my API
app.version = "0.0.1"

# use middleware in all the app for handle error.
app.add_middleware(ErrorHandler)

# include all routing of our app
app.include_router(movie_router)

# create database
Base.metadata.create_all(bind=engine)


# class for the users
class User(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_user = {
            "example": {"email": "example@example.com", "password": "hello_world_2024"}
        }


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción",
    },
    {
        "id": 2,
        "title": "End Game",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2018",
        "rating": 9.5,
        "category": "Ficción",
    },
    {
        "id": 3,
        "title": "End Game",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2018",
        "rating": 9.5,
        "category": "Drama",
    },
]


# change tags
@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello World</h1>")


# .dict() is deprecated. Now use .__dict__ or .model_dump()
@app.post("/login", tags=["auth"], response_model=User)
def login_user(user: User):
    if user.email == "admin@admin.com" and user.password == "admin":
        token: str = create_token(user.__dict__)
        return JSONResponse(status_code=201, content=token)
