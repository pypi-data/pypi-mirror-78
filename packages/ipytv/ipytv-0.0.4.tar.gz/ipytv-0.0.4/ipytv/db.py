from os.path import dirname, join
import base64
import requests
from json_database import JsonDatabase
from bs4 import BeautifulSoup
import pafy
from ipytv.utils import check_stream, StreamStatus


class Stream:
    def __init__(self, url):
        self.url = url
        self._status = StreamStatus.UNKNOWN

    @property
    def status(self):
        if self._status != StreamStatus.OK:
            try:
                self._status = check_stream(self.url, timeout=1)
            except:
                pass
        return self._status

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url


class Channel:
    def __init__(self, **kwargs):
        self.channel_data = kwargs
        self.name = self.channel_data["name"].strip()
        self._streams = self.channel_data["streams"]
        self.lang = self.channel_data.get("lang", "en")

    @property
    def identifier(self):
        return self.channel_data.get("identifier",
                                     self.name.replace(" ", "_").lower())

    @property
    def best_stream(self):
        for s in self.streams:
            if s.status == StreamStatus.OK:
                return s
        for s in self.streams:
            if s.status == StreamStatus.SLOW:
                return s
        return None

    @property
    def alive(self):
        return self.best_stream is not None

    @staticmethod
    def from_json(data):
        return Channel(**data)

    def as_json(self):
        return self.channel_data

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
            elif "ustvgo.tv" in url:
                url = self.get_ustvgo_stream(url)

            streams.append(Stream(url))
        return streams

    @staticmethod
    def get_youtube_stream(url):
        vid = pafy.new(url)
        stream = vid.getbestvideo()
        if stream:
            return stream.url
        return vid.streams[0].url  # stream fallback

    @staticmethod
    def get_ustvgo_stream(url):
        html = requests.get(url).text
        bsoup = BeautifulSoup(html, 'html.parser')
        for s in bsoup.findAll("script"):
            if "player.setup" in str(s):
                blob = s.next_element
                if blob == "None":
                    continue
                atob = str(blob).split("atob('")[-1].split("');")[0]
                decoded = base64.b64decode(atob).decode("utf-8")
                return decoded
        return None

    def __str__(self):
        return "Channel:" + self.name

    def __repr__(self):
        return "Channel:" + self.name


def total_channels(db_path=None):
    db_path = db_path or join(dirname(__file__), "res",
                              "channels.jsondb")
    with JsonDatabase("channels", db_path) as db:
        return len(db)


def print_channels(db_path=None):
    db_path = db_path or join(dirname(__file__), "res",
                              "channels.jsondb")
    with JsonDatabase("channels", db_path) as db:
        db.print()


def add_channel(channel_data, db_path=None, lang=None, replace=True):
    if isinstance(channel_data, Channel):
        channel_data = channel_data.as_json()
    db_path = db_path or join(dirname(__file__), "res",
                              "channels.jsondb")

    assert "name" in channel_data

    lang = channel_data.get("lang") or lang

    assert lang is not None

    # normalization
    for k in channel_data:
        if isinstance(channel_data[k], list) and k != "streams":
            for idx, i in enumerate(channel_data[k]):
                if isinstance(i, str):
                    channel_data[k][idx] = i.lower()
        elif isinstance(channel_data[k], str):
            channel_data[k] = channel_data[k].lower()

    with JsonDatabase("channels", db_path) as db:

        # search by key/value pair
        channels = db.search_by_value("name", channel_data["name"])

        if len(channels):
            selected = None

            # lang preference

            # i.e, pt-pt matching pt-pt
            for ch in channels:
                if ch.get("lang", "") == lang:
                    selected = ch
                    break

            # 2 letter lang code
            # i.e, pt-pt matching pt
            if not selected:
                for ch in channels:
                    if ch.get("lang", "") == lang.split("-")[0]:
                        selected = ch
                        break

            # 2 letter lang code mismatch
            # i.e, pt-pt matching pt-br, en matching en-us
            if not selected:
                for ch in channels:
                    if ch.get("lang", "").split("-")[0] == lang.split("-")[0]:
                        selected = ch
                        print(selected, channel_data)
                        break

            if not selected:
                print("item found but with alternate language. "
                      "adding new entry")
                print(channel_data)
                print(channels[0])
            else:
                item_id = db.get_item_id(selected)
                if item_id >= 0:
                    if replace:
                        print("replacing item in database")
                        db.update_item(item_id, channel_data)
                    else:
                        print("merging items")

                        # merge fields
                        for k in channel_data:
                            if k in selected and isinstance(selected[k], list):
                                selected[k] += channel_data[k]
                                # remove duplicates
                                selected[k] = list(set(selected[k]))
                            else:
                                selected[k] = channel_data[k]

                        db.update_item(item_id, selected)
                    return
                #else:
                #    print("item not found in database")
        #else:
        #    print("item not found in database")

        print("adding item to database")
        db.add_item(channel_data)


def update_channel(channel_data, db_path=None, lang=None):
    add_channel(channel_data, db_path, lang, False)


def remove_channel(channel_data, db_path=None, lang=None):
    if isinstance(channel_data, Channel):
        channel_data = channel_data.as_json()
    db_path = db_path or join(dirname(__file__), "res",
                              "channels.jsondb")

    assert "name" in channel_data

    lang = channel_data.get("lang") or lang

    assert lang is not None

    # normalization
    for k in channel_data:
        if isinstance(channel_data[k], list) and k != "streams":
            for idx, i in enumerate(channel_data[k]):
                if isinstance(i, str):
                    channel_data[k][idx] = i.lower()
        elif isinstance(channel_data[k], str):
            channel_data[k] = channel_data[k].lower()

    with JsonDatabase("channels", db_path) as db:

        # search by key/value pair
        channels = db.search_by_value("name", channel_data["name"])

        if len(channels):
            selected = None

            # lang preference
            # i.e, pt-pt matching pt-pt
            for ch in channels:
                if ch.get("lang", "") == lang:
                    selected = ch
                    break

            # 2 letter lang code
            # i.e, pt-pt matching pt
            if not selected:
                for ch in channels:
                    if ch.get("lang", "") == lang.split("-")[0]:
                        selected = ch
                        break

            # 2 letter lang code mismatch
            # i.e, pt-pt matching pt-br, en matching en-us
            if not selected:
                for ch in channels:
                    if ch.get("lang", "").split("-")[0] == lang.split("-")[0]:
                        selected = ch
                        print(selected, channel_data)
                        break

            if not selected:
                print("item found but with alternate language. "
                      "not removing entry")
                print(channel_data)
                print(channels[0])
            else:
                item_id = db.get_item_id(selected)
                if item_id >= 0:
                    print("Removing item from db")
                    db.remove_item(item_id)


def get_channels(db_path=None):
    db_path = db_path or join(dirname(__file__), "res",
                              "channels.jsondb")
    with JsonDatabase("channels", db_path) as db:
        for ch in db.db["channels"]:
            yield Channel.from_json(ch)
