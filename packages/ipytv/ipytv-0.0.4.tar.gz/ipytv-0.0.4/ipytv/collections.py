from ipytv import IPTV
from os.path import dirname, join

MyTVToGo = IPTV(db_path=join(dirname(__file__), "res", "mytvtogo.jsondb"))

MusicChannels = IPTV(db_path=join(dirname(__file__), "res", "music.jsondb"))

NewsChannels = IPTV(db_path=join(dirname(__file__), "res", "news.jsondb"))

Portugal = IPTV(db_path=join(dirname(__file__), "res", "pt.jsondb"))

Spain = IPTV(db_path=join(dirname(__file__), "res", "es.jsondb"))

Italy = IPTV(db_path=join(dirname(__file__), "res", "it.jsondb"))

France = IPTV(db_path=join(dirname(__file__), "res", "fr.jsondb"))

US = IPTV(db_path=join(dirname(__file__), "res", "us.jsondb"))
