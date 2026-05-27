# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # No flight/hotel API keys needed — static data used
    supabase_url: str = ""
    supabase_key: str = ""
    database_url: str = ""

    redis_url: str   = "redis://localhost:6379"
    redis_token: str = ""

    # Upstash uses REST API — derived from redis_url
    @property
    def upstash_rest_url(self) -> str:
        return self.redis_url

    @property
    def upstash_rest_token(self) -> str:
        return self.redis_token

    anthropic_api_key: str = ""

    environment: str        = "development"
    cache_ttl_seconds: int  = 21600
    allowed_origins: str    = "*"

    open_meteo_url: str = "https://api.open-meteo.com/v1/forecast"

    # ── Destination catalogue (launch set) ──────────────────
    DESTINATIONS: dict = {
        "HAN": {"name": "Hanoi",     "country": "Vietnam",   "lat": 21.0285, "lon": 105.8542, "timezone": "Asia/Ho_Chi_Minh"},
        "BKK": {"name": "Bangkok",   "country": "Thailand",  "lat": 13.7563, "lon": 100.5018, "timezone": "Asia/Bangkok"},
        "DPS": {"name": "Bali",      "country": "Indonesia", "lat": -8.3405, "lon": 115.0920, "timezone": "Asia/Makassar"},
        "NRT": {"name": "Tokyo",     "country": "Japan",     "lat": 35.6762, "lon": 139.6503, "timezone": "Asia/Tokyo"},
        "MEL": {"name": "Melbourne", "country": "Australia", "lat": -37.8136,"lon": 144.9631, "timezone": "Australia/Melbourne"},
    }

    ORIGIN: dict = {
        "SIN": {"name": "Singapore", "lat": 1.3521, "lon": 103.8198}
    }

    class Config:
        env_file = ".env"
        extra    = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()
