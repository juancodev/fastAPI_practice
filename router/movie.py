from fastapi import APIRouter, Path, Depends, Query
from fastapi.responses import JSONResponse
from config.database import Session
from typing import List
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middleware.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

# get new route
# response_model it will show us the response model.
# dependencies are the middlewares
# Depends is a class and inside must having the class JWTBearer.

# Make session to our database
DB = Session()


@movie_router.get(
    "/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:

    # Para hacer la consulta necesitamos el método query() adentro le pasamos el modelo y mostramos all()
    result = MovieService(DB).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# get route with params
@movie_router.get(
    "/movies/{id}", tags=["movies"], response_model=Movie, status_code=200
)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:

    # Hacemos la consulta a nuestro modelo pero utilizaremos una filtrado con una condición.
    result = MovieService(DB).get_movie(id)

    if not result:
        return JSONResponse(status_code=404, content={"message": "Not found"})

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# sin pasarlo por la ruta FastAPI lo interpreta como una query
@movie_router.get(
    "/movies/", tags=["movies"], response_model=List[Movie], status_code=200
)
def get_movies_by_category(
    category: str = Query(min_length=3, max_length=15)
) -> List[Movie]:
    result = MovieService(DB).get_movie_by_category(category)

    # query = lambda movie: [i for i in movies if i["category"] == movie]
    if not result:
        return JSONResponse(content={"message", "Not found"}, status_code=404)

    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# method post
@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
# params = query
def create_movie(movie: Movie) -> dict:
    MovieService(DB).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "register success"})


# the params must be both name than the path
@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, change_movie: Movie) -> dict:

    try:
        MovieService(DB).update_movie(id, change_movie)
        return JSONResponse(status_code=200, content={"message": "Change success"})
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=404)


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


@movie_router.delete(
    "/movies/{id}", tags=["movies"], response_model=dict, status_code=200
)
def delete_movie(id: int) -> dict:
    try:
        MovieService(DB).delete_movie(id)
        return JSONResponse(status_code=200, content={"message": "Delete movie"})
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=404)

    # query = list(filter(lambda item: item["id"] == id, movies))
    # query.remove()
