from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

"""
* HTMLResponse = useful for send HTML response to the browser.
* JSONResponse = useful for send JSON response to the client.
"""


# Class for the movies
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=2, max_length=15)
    overview: str = Field(min_length=5, max_length=100)
    year: str = Field(min_length=4, max_length=4)
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


# instance of The Class FastAPI
app = FastAPI()

# title of my application and docs
app.title = "My app with FastAPI"

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


# get new route
# response_model it will show us the response model
@app.get("/movies", tags=["movies"], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)


# get route with params
@app.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    def movie_filter(movie_id):
        if movie_id["id"] == id:
            return movie_id

    movie = filter(movie_filter, movies)
    return JSONResponse(content=list(movie)) or JSONResponse(content=[])


# sin pasarlo por la ruta FastAPI lo interpreta como una query
@app.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(
    category: str = Query(min_length=3, max_length=15)
) -> List[Movie]:
    query = lambda movie: [i for i in movies if i["category"] == movie]
    return query(category.capitalize())


# method post
@app.post("/movies", tags=["movies"], response_model=dict)
# params = query
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message": "register success"})


# the params must be both name than the path
@app.put("/movies/{id}", tags=["movies"], response_model=dict)
def update_movie(id: int, change: Movie) -> dict:
    query = list(filter(lambda el: el["id"] == id, movies))
    query[0]["title"] = change.title
    query[0]["overview"] = change.overview
    return JSONResponse(content={"message": [query[0]]})


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


@app.delete("/movies/{id}", tags=["movies"], response_model=dict)
def delete_movie(id: int) -> dict:
    query = list(filter(lambda item: item["id"] == id, movies))
    query.remove()
    return movies
