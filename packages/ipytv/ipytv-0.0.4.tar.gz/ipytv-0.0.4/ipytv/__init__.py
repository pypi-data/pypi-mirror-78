import ipytv.db
from os.path import join, dirname
from json_database.utils import match_one, fuzzy_match
from tempfile import gettempdir


class IPTV:
    def __init__(self, lang="en", db_path=None):
        self.db_path = db_path or join(gettempdir(), "ipytv.jsondb")
        self.lang = lang

    @property
    def m3u8(self):

        m3u8_str = "#EXTM3U ipytv\n"
        m3u8_str += "#PLAYLIST: " + self.db_path + "\n"
        entry_template = "#EXTINF:-1 group-title=\"{group}\" tvg-id=\"{identifier}\""
        # #EXT-X-PLAYLIST-TYPE: 	VOD or EVENT
        # #EXT-X-MEDIA: 	NAME="English", TYPE=AUDIO, GROUP-ID="audio-stereo-64", LANGUAGE="en", DEFAULT=YES, AUTOSELECT=YES, URI="english.m3u8"
        for ch in self.channels:
            group = ch.channel_data.get("tags") or ["TV"]
            group = group[0]
            stream = str(ch.best_stream)
            if stream == "None":
                continue
            entry = entry_template.format(
                group=group, lang=ch.lang,
                identifier=ch.identifier)

            for k in ch.channel_data:
                if isinstance(ch.channel_data[k], str):
                    entry += " " + k + "=\"" + ch.channel_data[k] + "\""
                elif isinstance(ch.channel_data[k], list):
                    tags = " | ".join(ch.channel_data[k])
                    entry += " " + k + "=\"" + tags + "\""

            m3u8_str += entry + ", " + ch.name + "\n" + stream + "\n"

        m3u8_str += "#EXT-X-ENDLIST"
        return m3u8_str

    def dump_m3u8(self, path):
        with open(path, "w") as f:
            f.write(self.m3u8)

    def add_channel(self, channel):
        ipytv.db.add_channel(channel, self.db_path, self.lang)

    def replace_channel(self, channel):
        self.add_channel(channel)

    def update_channel(self, channel):
        ipytv.db.update_channel(channel, self.db_path, self.lang)

    def remove_channel(self, channel):
        ipytv.db.remove_channel(channel, self.db_path, self.lang)

    def print_channels(self):
        ipytv.db.print_channels(self.db_path)

    @property
    def channels(self):
        return list(set(ipytv.db.get_channels(self.db_path)))

    @property
    def channel_names(self):
        return list(set([ch.name for ch in self.channels]))

    @property
    def total_channels(self):
        return ipytv.db.total_channels(self.db_path)

    def search(self, query, max_res=5,
               tag_whitelist=None, lang_whitelist=None):
        scores = []
        query = query.lower()
        words = query.split(" ")
        tag_whitelist = tag_whitelist or []
        tag_whitelist = [t.lower().strip() for t in tag_whitelist]
        lang_whitelist = lang_whitelist or []
        lang_whitelist = [t.lower().split("-")[0] for t in lang_whitelist]

        def common(l1, l2):
            return list(set(l1).intersection(l2))

        for ch in self.channels:
            # check allowed langs
            if lang_whitelist:
                i = common(lang_whitelist, [ch.lang.split("-")[0]])
                if not len(i):
                    continue

            # check allowed tags
            tags = ch.channel_data.get("tags", [])
            if tag_whitelist:
                i = common(tag_whitelist, tags)
                if not len(i):
                    continue

            # fuzzy match name for base score
            score = fuzzy_match(query, ch.name)

            # partial match name
            if ch.name in query:
                score += 0.4
            if query in ch.name:
                score += 0.3

            # fuzzy match aliases
            name, _score = match_one(query, ch.channel_data.get("aliases", []))

            score += _score

            # language of TV
            if ch.lang == self.lang:
                score += 0.5  # base lang bonus  (full code)
            elif ch.lang == self.lang.split("-")[0]:
                score += 0.4  # base lang bonus (short code)
            elif ch.lang.split("-")[0] == self.lang.split("-")[0]:
                score += 0.3  # base lang bonus (short code mismatch)
            else:
                score -= 0.5

            # count word overlap with channel tags
            word_intersection = common(words, tags)
            pct = len(word_intersection) / len(words)
            score += pct

            # fuzzy match tags
            if len(tags):
                _, _score = match_one(query, tags)
                score += _score * 0.5
                for t in tags:
                    if t in query:
                        score += 0.15

            # match country
            if "country" in ch.channel_data:
                if ch.channel_data["country"] in query:
                    score += 0.2

            # fuzzy match region
            if "region" in ch.channel_data:
                _, _score = match_one(query, ch.channel_data.get("region", []))
                score += _score * 0.5

            # re-scale score values
            score = score / 4

            # name match bonus
            # we really want to increase score in this case
            name = name.replace("_", " ")
            word_intersection = common(words, name.split())
            pct = len(word_intersection) / len(words)
            if pct > 0:
                score += 0.4 * pct

            scores.append((ch, min(1, score)))

        scores = sorted(scores, key=lambda k: k[1], reverse=True)
        return scores[:max_res]
