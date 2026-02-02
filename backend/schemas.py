"""Pydantic schemas (DTOs) for API request/response serialization."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NewsResponse(BaseModel):
    """
    Response model for a single news article.
    
    This is the JSON structure that the frontend will receive.
    """
    id: str = Field(..., description="Unique identifier (UUID)")
    title: str = Field(..., description="Article headline")
    source: str = Field(..., description="News source name")
    url: str = Field(..., description="Article URL")
    published_at: Optional[datetime] = Field(None, description="Publication timestamp")
    
    # Sentiment analysis fields
    sentiment: Optional[str] = Field(None, description="ALCISTA, BAJISTA, or NEUTRAL")
    confidence: Optional[float] = Field(None, description="Confidence score (0.00-1.00)")
    
    # Metadata
    commodity: Optional[str] = Field("SOJA", description="Related commodity")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record update timestamp")
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Soja alcanza precios récord en Chicago",
                "source": "Bichos de Campo",
                "url": "https://bichosdecampo.com/soja-record",
                "published_at": "2026-01-31T15:30:00Z",
                "sentiment": "ALCISTA",
                "confidence": 0.92,
                "commodity": "SOJA",
                "created_at": "2026-01-31T18:00:00Z",
                "updated_at": "2026-01-31T18:00:00Z"
            }
        }


class NewsListResponse(BaseModel):
    """Response model for a list of news articles."""
    total: int = Field(..., description="Total number of articles returned")
    articles: list[NewsResponse] = Field(..., description="List of news articles")


class SentimentStats(BaseModel):
    """Response model for sentiment statistics."""
    total: int = Field(..., description="Total number of articles")
    alcista: int = Field(..., description="Number of ALCISTA (bullish) articles")
    bajista: int = Field(..., description="Number of BAJISTA (bearish) articles")
    neutral: int = Field(..., description="Number of NEUTRAL articles")
    null: int = Field(..., description="Number of articles without sentiment")
    
    # Percentages
    alcista_percentage: float = Field(..., description="Percentage of ALCISTA articles")
    bajista_percentage: float = Field(..., description="Percentage of BAJISTA articles")
    neutral_percentage: float = Field(..., description="Percentage of NEUTRAL articles")
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "total": 100,
                "alcista": 45,
                "bajista": 30,
                "neutral": 25,
                "null": 0,
                "alcista_percentage": 45.0,
                "bajista_percentage": 30.0,
                "neutral_percentage": 25.0
            }
        }


class PipelineResponse(BaseModel):
    """Response model for pipeline execution."""
    status: str = Field(..., description="Pipeline execution status")
    message: str = Field(..., description="Human-readable message")
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "status": "running",
                "message": "Pipeline started in background. Check /api/stats for updates."
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current server timestamp")
    database: str = Field(..., description="Database connection status")
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-01-31T18:00:00Z",
                "database": "connected"
            }
        }
