from datetime import datetime, timezone
import json
from typing import Dict

from xml.etree.ElementTree import ElementTree

from .rss import RSSRoot
from .constants import RSS_DATE_FORMAT


def cast_string_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, RSS_DATE_FORMAT).replace(tzinfo=timezone.utc)


def convert_rss_feed_to_dict(rss: ElementTree) -> Dict:
    return RSSRoot(rss).to_dict


def convert_rss_feed_to_json(rss: ElementTree) -> str:
    return json.dumps(convert_rss_feed_to_dict(rss))
