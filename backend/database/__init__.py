"""Database package for Supabase integration."""

from .supabase_client import get_supabase_client
from .repositories import NewsRepository

__all__ = ["get_supabase_client", "NewsRepository"]
