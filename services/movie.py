from models.movie import Movie as MovieModel
from schemas.movie import Movie


class MovieService:

    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie(self, id: int):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result

    def get_movie_by_category(self, category: str):
        result = self.db.query(MovieModel).filter_by(category=category).all()
        return result

    def create_movie(self, movie: Movie):
        # Create an instance of class MovieModel giving the arguments with **
        new_movie = MovieModel(**movie.__dict__)
        # add to the DB the new register.
        self.db.add(new_movie)
        # saving the changes with commit()
        self.db.commit()
        return

    def update_movie(self, id: int, data: Movie):
        movie = self.get_movie(id)
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        self.db.commit()
        return

    def delete_movie(self, id: int):
        movie = self.get_movie(id)
        self.db.delete(movie)
        self.db.commit()
        return
