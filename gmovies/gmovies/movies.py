import os
from datetime import datetime, timedelta

import requests

from gmovies.db.shelve import Database
from gmovies.entities import Movie

url = "https://streaming-availability.p.rapidapi.com/v2/get/basic"

headers = {
    "X-RapidAPI-Key": "b235aac6e4msh9c481db9b415412p17f846jsn34b5f0cce4bd",
    "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com",
}


def movie_info(movie_id: str) -> Movie | None:
    database = Database()
    movie = database.get_movie(movie_id)
    if movie and movie.added - datetime.now() < timedelta(days=31):
        print(f"Movie info for {movie_id} found in database")
        return movie

    querystring = {}
    querystring["imdb_id"] = movie_id
    querystring["country"] = os.getenv("COUNTRY") or "us"

    print(f"Getting movie info for {movie_id}...")
    response = requests.request("GET", url, headers=headers, params=querystring)
    if not response.ok:
        print(f"Error getting movie info for {movie_id}: {response.status_code}")
        return None

    response_dict = response.json()["result"]

    movie = Movie(
        movie_id=movie_id,
        title=response_dict["title"],
        year=response_dict["year"],
        directors=response_dict["directors"],
        genres=response_dict["genres"],
        rating=response_dict["tmdbRating"],
        runtime=response_dict["runtime"],
        streaming_platforms=get_subscription_platforms(
            response_dict["streamingInfo"][os.getenv("COUNTRY")]
        ),
    )

    database.add_movie(movie)
    database.close()
    return movie


def get_subscription_platforms(streaming_info: dict) -> list[str]:
    services = []
    for service, offers in streaming_info.items():
        for offer in offers:
            if offer["type"] == "subscription":
                services.append(service)

    return services
