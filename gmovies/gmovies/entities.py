from dataclasses import dataclass
from datetime import datetime


@dataclass
class Movie:
    movie_id: str
    title: str
    year: int
    directors: list[str]
    genres: list[str]
    rating: float
    runtime: int
    streaming_platforms: list[str]
    added: datetime = datetime.now()
