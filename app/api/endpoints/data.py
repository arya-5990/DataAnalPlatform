"""
Data endpoints for retrieving stored data
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.data_models import RawData
from app.schemas.data_schemas import DataResponse, DataListResponse

router = APIRouter()

@router.get("/", response_model=DataListResponse)
async def get_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    source: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get stored raw data with optional filtering"""
    query = db.query(RawData)
    
    if source:
        query = query.filter(RawData.source == source)
    
    total = query.count()
    data = query.offset(skip).limit(limit).all()
    
    return DataListResponse(
        data=[DataResponse.from_orm(item) for item in data],
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{data_id}", response_model=DataResponse)
async def get_data_by_id(data_id: int, db: Session = Depends(get_db)):
    """Get specific data entry by ID"""
    data = db.query(RawData).filter(RawData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return DataResponse.from_orm(data)
