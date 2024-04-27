from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

"""
* HTMLResponse = useful for send HTML response to the browser.
* JSONResponse = useful for send JSON response to the client.
* Path = useful for send a limit and offset in params.
* Query = useful for query in route
* Status = useful for all status code.
* HTTPException = useful for send error Message and don't stop the app.
* Request = util para la solicitud que vamos a requerir desde la petición
"""
# instance of The Class FastAPI
app = FastAPI()

# title of my application and docs
app.title = "My app with FastAPI"

# create database
Base.metadata.create_all(bind=engine)


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # super() es la función superior que en este caso sería HTTPBearer y tiene un método llamado .__call__() que hace la solicitud de forma asíncrona.
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@admin.com":
            raise HTTPException(status_code=403, detail="credentials invalid")


# class for the users
class User(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_user = {
            "example": {"email": "example@example.com", "password": "hello_world_2024"}
        }


# Class for the movies
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=2, max_length=15)
    overview: str = Field(min_length=5, max_length=100)
    year: int = None
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=3, max_length=15)

    # class config example
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Title of the movie",
                "overview": "Description of the movie",
                "year": "2024",
                "rating": 9.9,
                "category": "Category of the movie",
            }
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


# get new route
# response_model it will show us the response model.
# dependencies are the middlewares
# Depends is a class and inside must having the class JWTBearer.
@app.get(
    "/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


# get route with params
@app.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    def movie_filter(movie_id):
        if movie_id["id"] == id:
            return movie_id

    movie = filter(movie_filter, movies)
    return JSONResponse(status_code=200, content=list(movie)) or JSONResponse(
        status_code=404, content=[]
    )


# sin pasarlo por la ruta FastAPI lo interpreta como una query
@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(
    category: str = Query(min_length=3, max_length=15)
) -> List[Movie]:
    query = lambda movie: [i for i in movies if i["category"] == movie]
    return JSONResponse(status_code=200, content=query(category.capitalize()))


# method post
@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
# params = query
def create_movie(movie: Movie) -> dict:
    # Session is the connection to the DB.
    db = Session()
    # Create an instance of class MovieModel giving the arguments with **
    new_movie = MovieModel(**movie.__dict__)
    # add to the DB the new register.
    db.add(new_movie)
    # saving the changes with commit()
    db.commit()
    return JSONResponse(status_code=201, content={"message": "register success"})


# the params must be both name than the path
@app.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, change: Movie) -> dict:
    query = list(filter(lambda el: el["id"] == id, movies))
    query[0]["title"] = change.title
    query[0]["overview"] = change.overview
    return JSONResponse(status_code=200, content={"message": [query[0]]})


"""
# other form
@app.put("/movies/{id}", tags=["movies"])
def update_movie(
    id: int, title: str, overview: str, year: str, rating: float, category: str
):
    for item in movies:
        if item["id"] == id:
            item["title"] = title
            item["overview"] = overview
            item["year"] = year
            item["rating"] = rating
            item["category"] = category
            return movies
"""


@app.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    query = list(filter(lambda item: item["id"] == id, movies))
    query.remove()
    return JSONResponse(status_code=200, content=movies)
