"""
Pydantic schemas for ingestion requests and responses
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any

class IngestionRequest(BaseModel):
    query: str
    language: Optional[str] = "en"
    page_size: Optional[int] = 100

class IngestionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
