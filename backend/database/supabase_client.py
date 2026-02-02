"""Supabase client configuration and initialization."""

import os
import logging
from supabase import create_client, Client
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def get_supabase_client(use_service_key: bool = False) -> Client:
    """
    Initialize and return a Supabase client.
    
    Args:
        use_service_key: If True, use service role key for elevated permissions.
                        If False, use anon key for normal operations (default).
    
    Returns:
        Configured Supabase client
        
    Raises:
        ValueError: If required environment variables are not set
    """
    url = os.getenv("SUPABASE_URL")
    
    if not url:
        raise ValueError(
            "SUPABASE_URL not found in environment variables. "
            "Please check your .env file."
        )
    
    # Choose which key to use
    if use_service_key:
        key = os.getenv("SUPABASE_SERVICE_KEY")
        if not key:
            raise ValueError(
                "SUPABASE_SERVICE_KEY not found in environment variables. "
                "Falling back to anon key."
            )
        logger.info("Initializing Supabase client with service role key")
    else:
        key = os.getenv("SUPABASE_ANON_KEY")
        if not key:
            raise ValueError(
                "SUPABASE_ANON_KEY not found in environment variables. "
                "Please check your .env file."
            )
        logger.info("Initializing Supabase client with anon key")
    
    try:
        client = create_client(url, key)
        logger.info(f"Supabase client initialized successfully: {url}")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        raise


# Global client instance (lazy initialization)
_client: Client = None


def get_client() -> Client:
    """
    Get or create a global Supabase client instance.
    
    Returns:
        Shared Supabase client instance
    """
    global _client
    if _client is None:
        _client = get_supabase_client()
    return _client
