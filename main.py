from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middleware.error_handler import ErrorHandler
from router.movie import movie_router
from router.auth import auth_router

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
# app.version = "0.0.1"

# use middleware in all the app for handle error.
app.add_middleware(ErrorHandler)

# include all routing of our app
app.include_router(movie_router)
app.include_router(auth_router)

# create database
Base.metadata.create_all(bind=engine)

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
