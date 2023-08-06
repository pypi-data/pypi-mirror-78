import requests
from requests.exceptions import Timeout
from enum import IntEnum
import youtube_dl
from tempfile import gettempdir
from os.path import join


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


def parse_m3u8(m3, verify=False, verbose=False):
    if m3.startswith("http"):
        content = requests.get(m3).content
        m3 = join(gettempdir(), "pyvod.m3u8")
        with open(m3, "wb") as f:
            f.write(content)
    with open(m3) as f:
        m3ustr = f.read().split("\n")
        m3ustr = [l for l in m3ustr if l.strip()]

    movies = []
    for idx, line in enumerate(m3ustr):
        if not line.strip():
            continue
        next_line = m3ustr[idx + 1] if idx + 1 < len(m3ustr) else None
        if not next_line:
            break
        if line.startswith("#EXTINF:"):
            data = {
                "stream": next_line
            }
            fields, data["name"] = line.replace("#EXTINF:", "").split(
                ",")

            fields = fields.split("=")
            k, val = None, None
            for idx, entry in enumerate(fields):
                if idx == 0:
                    if len(entry.split(" ")) == 1:
                        data["duration"] = entry
                    else:
                        data["duration"], k = entry.split(" ")
                    data["duration"] = float(data["duration"])
                else:
                    _ = entry.split(" ")
                    new_k = _[-1]
                    val = " ".join(_[:-1])

                    if val.startswith("\""):
                        val = val[1:].strip()
                    if val.endswith("\""):
                        val = val[:-1].strip()

                    if k and val:
                        data[k] = val
                        k, val = new_k, None
            if "identifier" not in data:
                data['identifier'] = data["name"].lower().strip().replace(" ", "_")
            movies.append(data)

    entries = {}
    for movie in movies:
        name = movie["name"]
        entries[movie['identifier']] = movie

        # verify is url is dead or alive
        if verify:
            # NOTE might be temporarily down but still valid
            # Either way seems to be a bad stream, very slow of server side
            # implementation errors
            stream = movie["stream"]
            if verbose:
                print("Checking stream:", name, stream)
            status = check_stream(stream, verbose=verbose)
            if not status == StreamStatus.OK:
                continue

    return entries


def ydl(url, verbose=False):
    ydl_opts = {
        "no_color": True,
        'quiet': not verbose
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url,
                                  download=False
                                  # We just want to extract the info
                                  )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        return video['url']


def url2stream(url):
    try:
        stream = ydl(url)
        if stream:
            url = stream
    except:
        # specific implementations can be added here
        pass
    return url

