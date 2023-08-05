import requests
from requests.exceptions import Timeout
import m3u8  # TODO this fails in some cases, need a better parser
from enum import IntEnum


class StreamStatus(IntEnum):
    OK = 200
    DEAD = 404
    FORBIDDEN = 401
    ERROR = 500
    SLOW = 666  # evil
    UNKNOWN = 0


def check_stream(url, timeout=5, verbose=False):
    # verify is url is dead or alive
    # NOTE might be temporarily down but still valid
    try:
        s = requests.get(url, timeout=timeout).status_code
        if s == 200:
            if verbose:
                print("stream OK:", url, s)
            return StreamStatus.OK
        if s == 404:
            if verbose:
                print("stream DEAD:", url, s)
            return StreamStatus.DEAD
        elif str(s).startswith("4"):
            if verbose:
                print("stream FORBIDDEN:", url, s)
            return StreamStatus.FORBIDDEN
        if verbose:
            print("stream ?:", url, s)
    except Timeout as e:
        # error, either a 500 or timeout
        if verbose:
            print("stream SLOW:", url, str(e))
        return StreamStatus.SLOW
    except Exception as e:
        # error, usually a 500
        if verbose:
            print("stream ERROR:", url, str(e))
        return StreamStatus.ERROR
    return StreamStatus.UNKNOWN


def parse_m3u(m3, verify=False, verbose=False):
    movies = {}

    m3u8_obj = m3u8.load(m3)
    for movie in m3u8_obj.segments:

        # verify is url is dead or alive
        if verify:
            # NOTE might be temporarily down but still valid
            # Either way seems to be a bad stream, very slow of server side
            # implementation errors
            if verbose:
                print("Checking movie stream:", movie.title, movie.uri)
            status = check_stream(movie.uri, verbose=verbose)
            if not status == StreamStatus.OK:
                continue

        norm_title = movie.title.replace(" ", " ").strip()

        if norm_title.lower() in movies:
            # add alternate streams to existing entry
            movies[norm_title.lower()]["streams"].append(movie.uri)
            movies[norm_title.lower()]["aliases"].append(norm_title)
        else:
            movies[norm_title.lower()] = {
                "streams": [movie.uri],
                "name": norm_title,
                "aliases": [norm_title]
            }

    for ch in movies:
        # TODO retrieve logo + tags + country automatically somehow
        # remove duplicate entries from fields
        for k in movies[ch]:
            if isinstance(movies[ch][k], list):
                movies[ch][k] = list(set(movies[ch][k]))

    return movies

