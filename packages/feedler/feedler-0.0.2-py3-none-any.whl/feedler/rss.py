"""
Models based on RSS 2.0 SPECIFICATION
"""
from datetime import datetime
from typing import Optional, List, Union
from xml.etree.ElementTree import ElementTree, Element

from .exceptions import InvalidFeedError

# TODO: parse element attrib and auto cast


class _FeedElementProcessor(object):
    @property
    def _name(self):
        raise NotImplementedError("This property is required")

    @property
    def _required_elements(self):
        raise NotImplementedError("This property is required")

    def __init__(self, XMLElement: Union[ElementTree, Element]):
        self._data = {}
        self._element = XMLElement
        self._sub_elements = []

        self._init(XMLElement=XMLElement)
        self._set_sub_elements()
        self._set_properties()

    @property
    def to_dict(self):
        return self._data

    def _init(self, XMLElement: Union[ElementTree, Element]):
        if hasattr(XMLElement, "_root"):
            self._element = XMLElement.getroot()

        if not self._element:
            raise InvalidFeedError(f"Missing required element {self._name}.")

    def _set_sub_elements(self):
        self._sub_elements.extend(self._required_elements)
        if hasattr(self, "_optional_elements"):
            self._sub_elements.extend(self._optional_elements)

    def _set_properties(self):
        for sub_element in self._sub_elements:
            if "|" in sub_element:
                self._or(sub_element)
                continue

            if hasattr(self, "_many") and sub_element in self._many:
                elements = self._element.findall(sub_element)

                if not elements and sub_element in self._required_elements:
                    raise InvalidFeedError(f"Missing required element {sub_element}.")
                elif not elements and sub_element in self._optional_elements:
                    continue

                if (
                    hasattr(self, "_has_sub_elements_mapping")
                    and sub_element in self._has_sub_elements_mapping
                ):
                    self._set_many(sub_element, elements)
            else:
                element = self._element.find(sub_element)

                if element is None and sub_element in self._required_elements:
                    raise InvalidFeedError(f"Missing required element {sub_element}.")

                if element is None:
                    continue

                self._set_one(sub_element, element)

    def _set_many(self, name: str, elements: List[Element]):
        self._data[name] = [
            self._has_sub_elements_mapping[name](element).to_dict
            for element in elements
        ]

    def _set_one(self, name: str, element: Element):
        if (
            hasattr(self, "_has_sub_elements_mapping")
            and name in self._has_sub_elements_mapping
        ):
            self._data[name] = self._has_sub_elements_mapping[name](element).to_dict
        else:
            if element.text:
                if hasattr(self, "_cast") and name in self._cast:
                    self._data[name] = self._cast[name](element.text.strip())
                else:
                    self._data[name] = element.text.strip()

    def _or(self, elements: str):
        """
        Check that at least one element exist
        """
        count = 0
        sub_elements = elements.split("|")

        for sub_element in sub_elements:
            element = self._element.find(sub_element)

            if element is not None and hasattr(self, sub_element):
                self._data[sub_element] = element.text
            else:
                count += 1

        if count == len(sub_elements):
            raise InvalidFeedError(
                f"Missing required at least one element {sub_elements}."
            )


class RSSImage(_FeedElementProcessor):
    _required_elements = ["url", "title", "link"]
    _optional_elements = ["width", "height"]

    url: str = None
    title: str = None
    link: str = None
    width: Optional[int] = None
    height: Optional[int] = None


class RSSItem(_FeedElementProcessor):
    _required_elements = ["title|description"]
    _optional_elements = [
        "title",
        "link",
        "description",
        "author",
        "category",
        "comments",
        "enclosure",
        "guid",
        "pubDate",
        "source",
    ]

    title: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    category: Optional[List[str]] = None
    comments: Optional[str] = None
    enclosure: Optional[str] = None
    guid: Optional[str] = None
    pubDate: Optional[datetime] = None
    source: Optional[str] = None


class RSSTextInput(_FeedElementProcessor):
    _name = "textInput"
    _required_elements = ["title", "description", "name", "link"]

    title: str = None
    description: str = None
    name: str = None
    link: str = None


class RSSSkipHours(_FeedElementProcessor):
    _name = "skipHours"
    _required_elements = ["hour"]
    _many = ["hour"]

    hour: List[int] = None


class RSSSkipDays(_FeedElementProcessor):
    _name = "skipDays"
    _required_elements = ["day"]
    _many = ["day"]

    day: List[str] = None


class RSSChannel(_FeedElementProcessor):
    _name = "channel"
    # https://validator.w3.org/feed/docs/rss2.html#requiredChannelElements
    _required_elements = ["title", "link", "description"]
    # https://validator.w3.org/feed/docs/rss2.html#optionalChannelElements
    _optional_elements = [
        "language",
        "copyright",
        "managingEditor",
        "webMaster",
        "pubDate",
        "lastBuildDate",
        "category",
        "generator",
        "docs",
        "cloud",
        "ttl",
        "image",
        "item",
        "textInput",
        "skipHours",
        "skipDays",
    ]
    _has_sub_elements_mapping = {
        "image": RSSImage,
        "item": RSSItem,
        "textInput": RSSTextInput,
        "skipHours": RSSSkipHours,
        "skipDays": RSSSkipDays,
    }
    _many = ["category", "item"]

    title: str = None
    link: str = None
    description: str = None
    language: Optional[str] = None
    copyright: Optional[str] = None
    managingEditor: Optional[str] = None
    webMaster: Optional[str] = None
    pubDate: Optional[datetime] = None
    lastBuildDate: Optional[datetime] = None
    category: Optional[List[str]] = None
    generator: Optional[str] = None
    docs: Optional[str] = None
    cloud: Optional[str] = None
    ttl: Optional[int] = None
    image: Optional[RSSImage] = None
    item: Optional[List[RSSItem]] = None
    textInput: Optional[RSSTextInput] = None
    skipHours: Optional[RSSSkipHours] = None
    skipDays: Optional[RSSSkipDays] = None


class RSSRoot(_FeedElementProcessor):
    _name = "root"
    _required_elements = ["channel"]
    _has_sub_elements_mapping = {"channel": RSSChannel}

    channel: List[RSSChannel] = None
