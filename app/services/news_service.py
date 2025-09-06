"""
Service for fetching data from News API
"""
import requests
from typing import List, Dict, Any, Optional
from app.core.config import settings

class NewsService:
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2"
    
    async def fetch_articles(
        self, 
        query: str, 
        language: str = "en", 
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch articles from News API"""
        if not self.api_key:
            raise ValueError("News API key not configured")
        
        url = f"{self.base_url}/everything"
        params = {
            "q": query,
            "language": language,
            "pageSize": min(page_size, 100),  # News API max is 100
            "apiKey": self.api_key,
            "sortBy": "publishedAt"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "ok":
                return data.get("articles", [])
            else:
                raise Exception(f"News API error: {data.get('message', 'Unknown error')}")
                
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch news data: {str(e)}")
    
    async def fetch_top_headlines(
        self, 
        country: str = "us", 
        category: Optional[str] = None,
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch top headlines from News API"""
        if not self.api_key:
            raise ValueError("News API key not configured")
        
        url = f"{self.base_url}/top-headlines"
        params = {
            "country": country,
            "pageSize": min(page_size, 100),
            "apiKey": self.api_key
        }
        
        if category:
            params["category"] = category
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "ok":
                return data.get("articles", [])
            else:
                raise Exception(f"News API error: {data.get('message', 'Unknown error')}")
                
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch top headlines: {str(e)}")
