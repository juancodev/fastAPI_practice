from pydantic import BaseModel, Field
from typing import Optional


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
                "title": "Title of the movie",
                "overview": "Description of the movie",
                "year": 2024,
                "rating": 9.9,
                "category": "Category of the movie",
            }
        }
