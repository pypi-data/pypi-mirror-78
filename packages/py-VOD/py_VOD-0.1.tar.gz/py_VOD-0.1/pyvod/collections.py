from pyvod import Collection
from os.path import dirname, join


MyTVToGo = Collection(
    name="MyTVToGo",
    logo=join(dirname(__file__), "res", "logo", "MyTVToGo.png"),
    db_path=join(dirname(__file__), "res", "mytvtogo.jsondb"))


Cinemocracy = Collection(
    name="Cinemocracy",
    logo=join(dirname(__file__), "res", "logo", "cinemocracy.jpg"),
    db_path=join(dirname(__file__), "res", "cinemocracy.jsondb"))

SciFiHorror = Collection(
    name="Scifi_Horror",
    logo=join(dirname(__file__), "res", "logo", "SciFi_Horror.png"),
    db_path=join(dirname(__file__), "res", "SciFi_Horror.jsondb"))

ComedyFilms = Collection(
    name="comedy_films",
    logo=join(dirname(__file__), "res", "logo", "Comedy_Films.png"),
    db_path=join(dirname(__file__), "res", "Comedy_Films.jsondb"))

FeatureFilms = Collection(
    name="feature_films",
    logo=join(dirname(__file__), "res", "logo", "feature_films.jpg"),
    db_path=join(dirname(__file__), "res", "feature_films.jsondb"))

FeatureFilmsPicfixer = Collection(
    name="feature_films_picfixer",
    logo=join(dirname(__file__), "res", "logo", "picfixer_films.jpg"),
    db_path=join(dirname(__file__), "res", "feature_films_picfixer.jsondb"))

TheVideoCellarCollection = Collection(
    name="TheVideoCellarCollection",
    logo=join(dirname(__file__), "res", "logo", "VCCollection.jpg"),
    db_path=join(dirname(__file__), "res", "TheVideoCellarCollection.jsondb"))

MovieTrailers = Collection(
    name="movie_trailers",
    db_path=join(dirname(__file__), "res", "movie_trailers.jsondb"))

MovieTrailersPicfixer = Collection(
    name="movie_trailers_picfixer",
    logo=join(dirname(__file__), "res", "logo", "picfixer_trailers.jpg"),
    db_path=join(dirname(__file__), "res", "movie_trailers_picfixer.jsondb"))

ShortFilms = Collection(
    name="short-films",
    db_path=join(dirname(__file__), "res", "short_films.jsondb"))

SilentHallOfFame = Collection(
    name="silent-hall-of-fame",
    logo=join(dirname(__file__), "res", "logo", "silenthalloffame.jpg"),
    db_path=join(dirname(__file__), "res", "silenthalloffame.jsondb"))

MoviesAndFilms = Collection(
    name="movies-and-films",
    db_path=join(dirname(__file__), "res", "moviesandfilms.jsondb"))


SinemaTrailers = Collection(
    name="sinema-trailers",
    db_path=join(dirname(__file__), "res", "sinema-trailers.jsondb"))


NurayPictures = Collection(
    name="nuray-pictures",
    db_path=join(dirname(__file__), "res", "nuraypictures.jsondb"))


StockFootage = Collection(
    name="stock-footage",
    logo=join(dirname(__file__), "res", "logo", "stock_footage-header.gif"),
    db_path=join(dirname(__file__), "res", "stock_footage.jsondb"))

