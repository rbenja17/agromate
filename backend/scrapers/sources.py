"""RSS feed sources for Argentine agricultural news."""

from typing import TypedDict


class RSSSource(TypedDict):
    """Type definition for RSS source configuration."""
    name: str
    url: str
    enabled: bool


RSS_SOURCES: list[RSSSource] = [
    {
        "name": "Bichos de Campo",
        "url": "https://bichosdecampo.com/feed/",
        "enabled": True,
    },
    {
        "name": "Agrofynews",
        "url": "https://news.agrofy.com.ar/rss.xml",
        "enabled": True,
    },
    {
        "name": "Infocampo",
        "url": "https://www.infocampo.com.ar/feed/",
        "enabled": True,
    },
]


def get_active_sources() -> list[RSSSource]:
    """
    Get only the enabled RSS sources.
    
    Returns:
        List of active RSS source configurations
    """
    return [source for source in RSS_SOURCES if source["enabled"]]
