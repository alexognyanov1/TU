import requests
from prettytable import PrettyTable

OMDB_API_KEY = "d8801073"

BASE_URL = "http://www.omdbapi.com/"

PARAMS = {'apiKey': OMDB_API_KEY}


def search_movie_by_title(title):
    PARAMS['t'] = title
    r = requests.get(url=BASE_URL, params=PARAMS)

    data = r.json()

    return data


def organize_movies_by_rating(movies):
    movie_dict = {}

    for movie, rating in movies:
        if rating not in movie_dict:
            movie_dict[rating] = []

        movie_dict[rating].append(movie)

    sorted_movie_dict = {rating: sorted(
        movie_dict[rating]) for rating in sorted(movie_dict)}

    return sorted_movie_dict


def get_data_for_movies(movies):
    PROPERTIES = ["Title", "Year", "Rated", "Released", "Genre",
                  "Director", "Country"]

    movie_data = []

    for movie, _ in movies:
        data = search_movie_by_title(movie)
        filtered_data = {key: data[key] for key in PROPERTIES if key in data}

        movie_data.append(filtered_data)

    return movie_data


def print_pretty_table(movie_data):
    t = PrettyTable(movie_data[0].keys())
    for movie in movie_data:
        t.add_row(movie.values())

    print(t)


movies = [
    ("The Shawshank Redemption", 9.3),
    ("The Godfather", 9.2),
    ("The Dark Knight", 9.0),
    ("12 Angry Men", 9.0),
    ("Schindler's List", 8.9),
    ("Pulp Fiction", 8.9)
]

organized_movies = organize_movies_by_rating(movies)
movie_data = get_data_for_movies(movies)

# print(organized_movies)
# print(movie_data)

print_pretty_table(movie_data)
