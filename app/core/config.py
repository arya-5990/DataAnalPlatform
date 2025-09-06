"""
Configuration management for the Data Analytics Platform
"""
import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "DataAnalyticsPlatform"
    DEBUG: bool = True
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./data_analytics.db"
    
    # News API settings
    NEWS_API_KEY: Optional[str] = None
    
    # Twitter API settings
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
