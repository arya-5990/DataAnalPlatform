"""
Service for handling data ingestion from various sources
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from app.models.data_models import RawData
from app.services.news_service import NewsService
from app.services.twitter_service import TwitterService
from app.core.config import settings

class IngestionService:
    def __init__(self, db: Session):
        self.db = db
        self.news_service = NewsService()
        self.twitter_service = TwitterService()

    async def ingest_news_data(
        self, 
        query: str, 
        language: str = "en", 
        page_size: int = 100
    ) -> Dict[str, Any]:
        """Ingest data from News API"""
        if not settings.NEWS_API_KEY:
            raise ValueError("News API key not configured")
        
        articles = await self.news_service.fetch_articles(
            query=query,
            language=language,
            page_size=page_size
        )
        
        count = 0
        for article in articles:
            # Check if article already exists
            existing = self.db.query(RawData).filter(
                RawData.source == "news",
                RawData.source_id == article.get("url")
            ).first()
            
            if not existing:
                raw_data = RawData(
                    source="news",
                    source_id=article.get("url"),
                    title=article.get("title"),
                    content=article.get("description", "") + " " + article.get("content", ""),
                    author=article.get("author"),
                    url=article.get("url"),
                    published_at=article.get("publishedAt"),
                    raw_metadata=article
                )
                self.db.add(raw_data)
                count += 1
        
        self.db.commit()
        return {"count": count, "query": query}

    async def ingest_twitter_data(
        self, 
        query: str, 
        count: int = 100
    ) -> Dict[str, Any]:
        """Ingest data from Twitter API"""
        if not settings.TWITTER_BEARER_TOKEN:
            raise ValueError("Twitter API credentials not configured")
        
        tweets = await self.twitter_service.fetch_tweets(
            query=query,
            count=count
        )
        
        count = 0
        for tweet in tweets:
            # Check if tweet already exists
            existing = self.db.query(RawData).filter(
                RawData.source == "twitter",
                RawData.source_id == tweet.get("id")
            ).first()
            
            if not existing:
                raw_data = RawData(
                    source="twitter",
                    source_id=tweet.get("id"),
                    title=None,
                    content=tweet.get("text"),
                    author=tweet.get("author_id"),
                    url=f"https://twitter.com/user/status/{tweet.get('id')}",
                    published_at=tweet.get("created_at"),
                    raw_metadata=tweet
                )
                self.db.add(raw_data)
                count += 1
        
        self.db.commit()
        return {"count": count, "query": query}
