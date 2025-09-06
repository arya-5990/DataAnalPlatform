"""
Database models for storing raw data from various sources
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class RawData(Base):
    """Model for storing raw data from various sources"""
    __tablename__ = "raw_data"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, index=True)  # e.g., 'news', 'twitter'
    source_id = Column(String(100), nullable=True, index=True)  # Original ID from source
    title = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    author = Column(String(200), nullable=True)
    url = Column(String(1000), nullable=True)
    published_at = Column(DateTime, nullable=True, index=True)
    raw_metadata = Column(JSON, nullable=True)  # Store original API response
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class DataSource(Base):
    """Model for tracking data sources and their configurations"""
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    source_type = Column(String(50), nullable=False)  # e.g., 'news_api', 'twitter'
    is_active = Column(String(10), default='true')
    last_fetch = Column(DateTime, nullable=True)
    config = Column(JSON, nullable=True)  # Store source-specific configuration
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
