from functools import lru_cache

from google import genai
from supabase import Client, create_client

from .config import get_settings


@lru_cache
def get_gemini_client() -> genai.Client:
    return genai.Client(api_key=get_settings().gemini_api_key)


@lru_cache
def get_supabase_client() -> Client:
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_role_key)

