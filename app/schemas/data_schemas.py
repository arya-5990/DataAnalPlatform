"""
Pydantic schemas for data models
"""
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime

class DataResponse(BaseModel):
    id: int
    source: str
    source_id: Optional[str]
    title: Optional[str]
    content: str
    author: Optional[str]
    url: Optional[str]
    published_at: Optional[datetime]
    raw_metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DataListResponse(BaseModel):
    data: List[DataResponse]
    total: int
    skip: int
    limit: int
