import pyvod.db
from os.path import join, dirname
from json_database.utils import match_one, fuzzy_match
from tempfile import gettempdir


class Collection:
    def __init__(self, name=None, logo=None, db_path=None):
        self.db_path = db_path or join(gettempdir(), "pyvod.jsondb")
        self.name = name or self.db_path.split("/")[-1]
        self.logo = logo or join(dirname(__file__), "res",
                                 "logo", "moviesandfilms.png")

    @property
    def m3u8(self):

        m3u8_str = "#EXTM3U pyvod\n"
        m3u8_str += "#PLAYLIST: " + self.db_path + "\n"
        entry_template = "#EXTINF:-1 group-title=\"{group}\" tvg-id=\"{identifier}\""
        # #EXT-X-PLAYLIST-TYPE: 	VOD or EVENT
        # #EXT-X-MEDIA: 	NAME="English", TYPE=AUDIO, GROUP-ID="audio-stereo-64", LANGUAGE="en", DEFAULT=YES, AUTOSELECT=YES, URI="english.m3u8"
        for ch in self.movies:
            group = self.name

            # TODO all streams

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

    def add_movie(self, movie):
        pyvod.db.add_movie(movie, self.db_path)

    def replace_movie(self, movie):
        self.add_movie(movie)

    def update_movie(self, movie):
        pyvod.db.update_movie(movie, self.db_path)

    def remove_movie(self, movie):
        pyvod.db.remove_movie(movie, self.db_path)

    def print_movies(self):
        pyvod.db.print_movies(self.db_path)

    @property
    def movies(self):
        return list(set(pyvod.db.get_movies(self.db_path)))

    @property
    def movie_names(self):
        return list(set([ch.name for ch in self.movies]))

    @property
    def total_movies(self):
        return pyvod.db.total_movies(self.db_path)

    def search(self, query, max_res=5,
               tag_whitelist=None):
        scores = []
        query = query.lower()
        words = query.split(" ")
        tag_whitelist = tag_whitelist or []
        tag_whitelist = [t.lower().strip() for t in tag_whitelist]

        def common(l1, l2):
            return list(set(l1).intersection(l2))

        for ch in self.movies:

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
