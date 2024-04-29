from fastapi import APIRouter, Path, Depends, Query
from fastapi.responses import JSONResponse
from config.database import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middleware.jwt_bearer import JWTBearer

movie_router = APIRouter()


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


# get new route
# response_model it will show us the response model.
# dependencies are the middlewares
# Depends is a class and inside must having the class JWTBearer.

# Make session to our database
DB = Session()

movie_router.get(
    "/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)


def get_movies() -> List[Movie]:

    # Para hacer la consulta necesitamos el método query() adentro le pasamos el modelo y mostramos all()
    result = DB.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# get route with params
movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)


def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:

    # Hacemos la consulta a nuestro modelo pero utilizaremos una filtrado con una condición.
    result = DB.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        return JSONResponse(status_code=404, content={"message": "Not found"})

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# sin pasarlo por la ruta FastAPI lo interpreta como una query
movie_router.get(
    "/movies/", tags=["movies"], response_model=List[Movie], status_code=200
)


def get_movies_by_category(
    category: str = Query(min_length=3, max_length=15)
) -> List[Movie]:
    result = DB.query(MovieModel).filter_by(category=category).all()

    # query = lambda movie: [i for i in movies if i["category"] == movie]
    if not result:
        return JSONResponse(content={"message", "Not found"}, status_code=404)

    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# method post
movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)


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
movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)


def update_movie(id: int, change) -> dict:
    result = DB.query(MovieModel).filter(MovieModel.id == id).first()

    # query = list(filter(lambda el: el["id"] == id, movies))
    # query[0]["title"] = change.title
    # query[0]["overview"] = change.overview

    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=404)

    result.title = change.title
    result.overview = change.overview
    result.year = change.year
    result.rating = change.rating
    result.category = change.category
    DB.commit()

    return JSONResponse(status_code=200, content={"message": "Change success"})


"""
# other form
movie_router.put("/movies/{id}", tags=["movies"])
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


movie_router.delete(
    "/movies/{id}", tags=["movies"], response_model=dict, status_code=200
)


def delete_movie(id: int) -> dict:

    result = DB.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=404)

    DB.delete(result)
    DB.commit()

    # query = list(filter(lambda item: item["id"] == id, movies))
    # query.remove()
    return JSONResponse(status_code=200, content={"message": "Delete movie"})
