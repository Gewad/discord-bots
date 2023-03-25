import shelve  # nosec

from gmovies.entities import Movie


class Database:
    def __init__(self):
        self.s = shelve.open(".db/gmovies.shelve")  # nosec

    def get_movie(self, movie_id: str) -> Movie | None:
        try:
            return self.s[movie_id]
        except KeyError:
            return None

    def add_movie(self, movie: Movie):
        try:
            self.s[movie.movie_id] = movie
        except Exception as e:
            print(f"Error adding movie to database: {e}")

    def close(self):
        self.s.close()
