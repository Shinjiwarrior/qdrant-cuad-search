from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

# Request Models
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Search filters")
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="Number of results to return")
    offset: Optional[int] = Field(default=0, ge=0, description="Number of results to skip")

class SearchFilters(BaseModel):
    jurisdiction: Optional[List[str]] = Field(default=None, description="Filter by jurisdiction")
    court_level: Optional[List[str]] = Field(default=None, description="Filter by court level")
    case_type: Optional[List[str]] = Field(default=None, description="Filter by case type")
    industry: Optional[List[str]] = Field(default=None, description="Filter by industry")
    company_size: Optional[List[str]] = Field(default=None, description="Filter by company size")
    contract_status: Optional[List[str]] = Field(default=None, description="Filter by contract status")
    complexity_level: Optional[List[str]] = Field(default=None, description="Filter by complexity level")
    risk_level: Optional[List[str]] = Field(default=None, description="Filter by risk level")
    renewal_terms: Optional[List[str]] = Field(default=None, description="Filter by renewal terms")
    date_from: Optional[str] = Field(default=None, description="Start date filter (YYYY-MM-DD)")
    date_to: Optional[str] = Field(default=None, description="End date filter (YYYY-MM-DD)")

# Response Models
class LegalCase(BaseModel):
    id: str = Field(..., description="Unique case identifier")
    case_name: str = Field(..., description="Name of the case")
    citation: Optional[str] = Field(default=None, description="Legal citation")
    court: Optional[str] = Field(default=None, description="Court name")
    jurisdiction: Optional[str] = Field(default=None, description="Jurisdiction")
    date_filed: Optional[str] = Field(default=None, description="Date case was filed")
    case_type: Optional[str] = Field(default=None, description="Type of case")
    summary: Optional[str] = Field(default=None, description="Case summary")
    full_text: Optional[str] = Field(default=None, description="Full case text")
    url: Optional[str] = Field(default=None, description="URL to full case")
    score: Optional[float] = Field(default=None, description="Similarity score")
    
    # Enhanced metadata fields for commercial contracts
    industry: Optional[str] = Field(default=None, description="Industry sector")
    company_size: Optional[str] = Field(default=None, description="Company size category")
    contract_status: Optional[str] = Field(default=None, description="Contract status")
    estimated_value: Optional[str] = Field(default=None, description="Estimated contract value")
    complexity_level: Optional[str] = Field(default=None, description="Contract complexity level")
    risk_level: Optional[str] = Field(default=None, description="Risk assessment level")
    renewal_terms: Optional[str] = Field(default=None, description="Contract renewal terms")
    contract_start_date: Optional[str] = Field(default=None, description="Contract start date")
    contract_end_date: Optional[str] = Field(default=None, description="Contract end date")
    court_level: Optional[str] = Field(default=None, description="Court level or business context")

class SearchResponse(BaseModel):
    query: str = Field(..., description="Original search query")
    total: int = Field(..., description="Total number of results")
    results: List[LegalCase] = Field(..., description="Search results")
    filters_applied: Optional[Dict[str, Any]] = Field(default=None, description="Applied filters")
    processing_time: float = Field(..., description="Query processing time in seconds")

class FilterOptions(BaseModel):
    jurisdictions: List[str] = Field(..., description="Available jurisdictions")
    court_levels: List[str] = Field(..., description="Available court levels")
    case_types: List[str] = Field(..., description="Available case types")
    industries: Optional[List[str]] = Field(default=None, description="Available industries")
    company_sizes: Optional[List[str]] = Field(default=None, description="Available company sizes")
    contract_statuses: Optional[List[str]] = Field(default=None, description="Available contract statuses")
    complexity_levels: Optional[List[str]] = Field(default=None, description="Available complexity levels")
    risk_levels: Optional[List[str]] = Field(default=None, description="Available risk levels")
    renewal_terms: Optional[List[str]] = Field(default=None, description="Available renewal terms")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    qdrant_status: str = Field(..., description="Qdrant connection status")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp") 