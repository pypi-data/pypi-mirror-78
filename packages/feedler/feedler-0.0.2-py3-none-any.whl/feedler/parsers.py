from io import BytesIO
from typing import Union, Dict

import requests
from defusedxml.ElementTree import parse

from .constants import FeedTypes
from .utils import convert_rss_feed_to_dict, convert_rss_feed_to_json


def _parser(file: str, type=FeedTypes.rss, format=None) -> Union[str, Dict]:
    xml = file

    if "http" in file:
        try:
            response = requests.get(file)
            xml = BytesIO(response.content)
        except requests.exceptions.ConnectionError:
            raise FileNotFoundError(f"Invalid URL: '{file}'")

    rss = parse(xml)
    if format == "json":
        return convert_rss_feed_to_json(rss)
    return convert_rss_feed_to_dict(rss)


def rss_parser(xmlfile, format=None) -> Union[str, Dict]:
    return _parser(xmlfile, format=format)
