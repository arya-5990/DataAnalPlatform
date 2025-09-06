"""
Sample data ingestion script
"""
import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.services.ingestion_service import IngestionService

async def ingest_sample_data():
    """Ingest sample data from configured sources"""
    db = SessionLocal()
    try:
        ingestion_service = IngestionService(db)
        
        print("Starting data ingestion...")
        
        # Ingest news data
        try:
            print("Ingesting news data...")
            news_result = await ingestion_service.ingest_news_data(
                query="artificial intelligence",
                language="en",
                page_size=50
            )
            print(f"News ingestion completed: {news_result}")
        except Exception as e:
            print(f"News ingestion failed: {e}")
        
        # Ingest Twitter data
        try:
            print("Ingesting Twitter data...")
            twitter_result = await ingestion_service.ingest_twitter_data(
                query="AI OR artificial intelligence",
                count=50
            )
            print(f"Twitter ingestion completed: {twitter_result}")
        except Exception as e:
            print(f"Twitter ingestion failed: {e}")
        
        print("Data ingestion completed!")
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(ingest_sample_data())
