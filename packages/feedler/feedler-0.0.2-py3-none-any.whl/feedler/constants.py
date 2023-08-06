from enum import Enum


class FeedTypes(Enum):
    rss = "rss"
    atom = "atom"


RSS_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +%f"
