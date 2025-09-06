"""
Data ingestion endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.ingestion_service import IngestionService
from app.schemas.ingestion_schemas import IngestionRequest, IngestionResponse

router = APIRouter()

@router.post("/news", response_model=IngestionResponse)
async def ingest_news_data(
    request: IngestionRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Trigger news data ingestion"""
    try:
        ingestion_service = IngestionService(db)
        result = await ingestion_service.ingest_news_data(
            query=request.query,
            language=request.language,
            page_size=request.page_size
        )
        return IngestionResponse(
            success=True,
            message=f"Successfully ingested {result['count']} news articles",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/twitter", response_model=IngestionResponse)
async def ingest_twitter_data(
    request: IngestionRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Trigger Twitter data ingestion"""
    try:
        ingestion_service = IngestionService(db)
        result = await ingestion_service.ingest_twitter_data(
            query=request.query,
            count=request.page_size
        )
        return IngestionResponse(
            success=True,
            message=f"Successfully ingested {result['count']} tweets",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
