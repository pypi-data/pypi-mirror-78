from json_database import JsonDatabase
import pafy
from pyvod.utils import check_stream, StreamStatus


class Stream:
    def __init__(self, url):
        self.url = url
        self._status = StreamStatus.UNKNOWN

    @property
    def status(self):
        return check_stream(self.url)

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url


class Movie:
    def __init__(self, **kwargs):
        self.data = kwargs
        if "title" not in self.data and "name" in self.data:
            self.data["title"] = self.data.pop("name")
        self.name = str(self.data["title"]).strip()
        self._streams = self.data.get("streams") or [self.data["stream"]]

    @property
    def identifier(self):
        return self.data.get("identifier", self.name.replace(" ", "_").lower())

    @staticmethod
    def from_json(data):
        return Movie(**data)

    def as_json(self):
        return self.data

    @property
    def streams(self):
        streams = []
        for url in self._streams:

            if not url:
                continue

            if "www.youtube.com" in url:
                try:
                    url = self.get_youtube_stream(url)
                except:
                    print("youtube-dl failed, try updating it")
                    continue
            streams.append(Stream(url))
        return streams

    @staticmethod
    def get_youtube_stream(url):
        vid = pafy.new(url)
        stream = vid.getbestvideo()
        if stream:
            return stream.url
        return vid.streams[0].url  # stream fallback

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def total_movies(db_path):
    with JsonDatabase("VOD", db_path) as db:
        return len(db)


def print_movies(db_path):
    with JsonDatabase("VOD", db_path) as db:
        db.print()


def add_movie(data, db_path, replace=True, normalize=True):
    if isinstance(data, Movie):
        data = data.as_json()

    title = data.get("title") or data.get("name")
    assert title is not None
    data["title"] = title

    # normalization
    if normalize:
        for k in data:
            if isinstance(data[k], list) and k != "streams":
                for idx, i in enumerate(data[k]):
                    if isinstance(i, str):
                        data[k][idx] = i.lower()
            elif isinstance(data[k], str):
                data[k] = data[k].lower()

    with JsonDatabase("VOD", db_path) as db:

        # search by key/value pair
        movies = db.search_by_value("title", data["title"])

        if len(movies):
            selected = movies[0]
            item_id = db.get_item_id(selected)
            if item_id >= 0:
                if replace:
                    print("replacing item in database")
                    db.update_item(item_id, data)
                else:
                    print("merging items")

                    # merge fields
                    for k in data:
                        if k in selected and isinstance(selected[k], list):
                            selected[k] += data[k]
                            # remove duplicates
                            selected[k] = list(set(selected[k]))
                        else:
                            selected[k] = data[k]

                    db.update_item(item_id, selected)
                return
        db.add_item(data)


def update_movie(data, db_path):
    add_movie(data, db_path, False)


def remove_movie(data, db_path, normalize=True):
    if isinstance(data, Movie):
        data = data.as_json()

    title = data.get("title") or data.get("name")
    assert title is not None
    data["title"] = title

    # normalization
    if normalize:
        for k in data:
            if isinstance(data[k], list) and k != "streams":
                for idx, i in enumerate(data[k]):
                    if isinstance(i, str):
                        data[k][idx] = i.lower()
            elif isinstance(data[k], str):
                data[k] = data[k].lower()

    with JsonDatabase("VOD", db_path) as db:

        # search by key/value pair
        movies = db.search_by_value("title", data["title"])

        if len(movies):
            selected = movies[0]
            item_id = db.get_item_id(selected)
            if item_id >= 0:
                print("Removing item from db")
                db.remove_item(item_id)


def get_movies(db_path):
    with JsonDatabase("VOD", db_path) as db:
        for ch in db.db["VOD"]:
            if not ch.get("streams") and not ch.get("stream"):
                continue
            yield Movie.from_json(ch)
