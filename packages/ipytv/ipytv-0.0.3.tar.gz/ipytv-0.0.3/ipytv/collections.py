from ipytv import IPTV
from os.path import dirname, join

MyTVToGo = IPTV(db_path=join(dirname(__file__), "res", "mytvtogo.jsondb"))

MusicChannels = IPTV(db_path=join(dirname(__file__), "res", "music.jsondb"))

NewsChannels = IPTV(db_path=join(dirname(__file__), "res", "news.jsondb"))

PortugueseChannels = IPTV(db_path=join(dirname(__file__), "res", "pt.jsondb"))
