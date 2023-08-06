from pyvod.utils import StreamStatus, check_stream, parse_m3u8, url2stream
from os.path import join, dirname
from json_database.utils import match_one, fuzzy_match
from tempfile import gettempdir
from json_database import JsonDatabase


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


class Media:
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
        return Media(**data)

    def as_json(self):
        return self.data

    @property
    def streams(self):
        streams = []
        for url in self._streams:
            url = url2stream(url)
            if not url:
                continue
            streams.append(Stream(url))
        return streams

    @property
    def alive(self):
        for s in self.streams:
            if s.status == StreamStatus.OK:
                return True
        for s in self.streams:
            if s.status == StreamStatus.SLOW:
                return True
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Collection:
    def __init__(self, name="pyVOD", logo=None, db_path=None):
        self.db_path = db_path or join(gettempdir(), name + ".jsondb")
        self.name = name
        self.logo = logo or join(dirname(__file__), "res",
                                 "logo", "moviesandfilms.png")

    @property
    def m3u8(self):

        m3u8_str = "#EXTM3U pyvod\n"
        m3u8_str += "#PLAYLIST: " + self.name + "\n"
        entry_template = "#EXTINF:-1 group-title=\"{group}\" tvg-id=\"{identifier}\""
        # #EXT-X-PLAYLIST-TYPE: 	VOD or EVENT
        # #EXT-X-MEDIA: 	NAME="English", TYPE=AUDIO, GROUP-ID="audio-stereo-64", LANGUAGE="en", DEFAULT=YES, AUTOSELECT=YES, URI="english.m3u8"
        for ch in self.entries:
            group = self.name

            total = len(ch.streams)
            for idx, stream in enumerate(ch.streams):
                stream = str(ch.streams[0])
                if stream == "None":
                    continue
                entry = entry_template.format(group=group,
                                              identifier=ch.identifier)
                if total > 1:
                    name = ch.name + " " + str(idx + 1) + "/" + str(total)
                else:
                    name = ch.name
                m3u8_str += entry + ", " + name + "\n" + stream + "\n"

        m3u8_str += "#EXT-X-ENDLIST"
        return m3u8_str

    def dump_m3u8(self, path):
        with open(path, "w") as f:
            f.write(self.m3u8)

    def add_entry(self, data, replace=True, normalize=False):
        if isinstance(data, Media):
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

        with JsonDatabase(self.name, self.db_path) as db:

            selected, item_id = self.match_entry(data)
            if selected:
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

    def match_entry(self, data):
        if isinstance(data, Media):
            data = data.as_json()
        with JsonDatabase(self.name, self.db_path) as db:

            # search by key/value pair
            movies = db.search_by_value("title", data["title"])

            if len(movies):
                selected = movies[0]
                item_id = db.get_item_id(selected)
                if item_id >= 0:
                    return selected, item_id
        return None, -1

    def replace_entry(self, data):
        self.add_entry(data, replace=True)

    def update_entry(self, data):
        self.add_entry(data, replace=False)

    def remove_entry(self, data, normalize=False):
        if isinstance(data, Media):
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

        with JsonDatabase(self.name, self.db_path) as db:

            # search by key/value pair
            movies = db.search_by_value("title", data["title"])

            if len(movies):
                selected = movies[0]
                item_id = db.get_item_id(selected)
                if item_id >= 0:
                    print("Removing item from db")
                    db.remove_item(item_id)

    def print_collection(self):
        with JsonDatabase(self.name, self.db_path) as db:
            db.print()

    @property
    def entries(self):
        entries = []
        with JsonDatabase(self.name, self.db_path) as collection:
            for ch in collection.db[self.name]:
                if not ch.get("streams") and not ch.get("stream"):
                    continue
                entries.append(Media.from_json(ch))
        return entries

    @property
    def stream_names(self):
        return list(set([ch.name for ch in self.entries]))

    @property
    def total_entries(self):
        with JsonDatabase(self.name, self.db_path) as db:
            return len(db)

    def remove_bad_entries(self):
        for ch in self.entries:
            if not ch.alive:
                self.remove_entry(ch)
                print(ch.name, "DEAD")

    def search(self, query, max_res=5,
               tag_whitelist=None):
        scores = []
        query = query.lower()
        words = query.split(" ")
        tag_whitelist = tag_whitelist or []
        tag_whitelist = [t.lower().strip() for t in tag_whitelist]

        def common(l1, l2):
            return list(set(l1).intersection(l2))

        for ch in self.entries:

            # check allowed tags
            if tag_whitelist:
                i = common(tag_whitelist, ch.data["tags"])
                if not len(i):
                    continue

            # fuzzy match name for base score
            score = fuzzy_match(query, ch.name)

            # partial match name
            if ch.name in query:
                score += 0.4
            elif ch.name.lower() in query.lower():
                score += 0.25

            if query in ch.name:
                score += 0.5
            elif query.lower() in ch.name.lower():
                score += 0.35

            # count word overlap with movie tags
            tags = [t.strip() for t in ch.data["tags"]]

            word_intersection = common(words, tags)
            pct = len(word_intersection) / len(words)
            score += pct

            # fuzzy match tags

            if len(tags):
                _, _score = match_one(query, tags)
                score += _score * 0.5
                for t in tags:
                    if t in query:
                        score += 0.3

            # re-scale score values
            score = score / 4

            # name match bonus
            # we really want to increase score in this case
            name = ch.name.replace("_", " ")
            word_intersection = common(words, name.split())
            pct = len(word_intersection) / len(words)
            if pct > 0:
                score += 0.4 * pct

            scores.append((ch, min(1, score)))

        scores = sorted(scores, key=lambda k: k[1], reverse=True)
        return scores[:max_res]
