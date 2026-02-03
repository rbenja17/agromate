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
    {
        "name": "Clarín Rural",
        "url": "https://www.clarin.com/rss/rural/",
        "enabled": True,
    },
    {
        "name": "La Nación Campo",
        "url": "https://servicios.lanacion.com.ar/herramientas/rss/categoria_id=30",
        "enabled": True,
    },
    {
        "name": "Agrovoz",
        "url": "https://www.lavoz.com.ar/rss/agro/",
        "enabled": True,
    },
    {
        "name": "Bolsa de Comercio de Rosario",
        "url": "https://www.bcr.com.ar/es/rss-news",
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
