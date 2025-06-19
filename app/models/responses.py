from typing import Dict, List, Optional

from pydantic import BaseModel, Field, RootModel


class SummaryResponse(BaseModel):
    record_count: int
    missing_values: Dict[str, int]


class StatsResponse(BaseModel):
    count: float
    mean: float
    std: float
    min: float
    p25: Optional[float] = Field(None, alias="25%")
    p50: Optional[float] = Field(None, alias="50%")
    p75: Optional[float] = Field(None, alias="75%")
    max: float


class IndustryListResponse(BaseModel):
    industries: List[str]


class IndustryDistributionResponse(RootModel[Dict[str, int]]):
    pass


class GenderDistributionResponse(RootModel[Dict[str, int]]):
    pass


class AgeDistributionResponse(BaseModel):
    count: float
    mean: float
    std: float
    min: float
    p25: Optional[float] = Field(None, alias="25%")
    p50: Optional[float] = Field(None, alias="50%")
    p75: Optional[float] = Field(None, alias="75%")
    max: float


class PersonRecord(BaseModel):
    first_name: str
    last_name: str
    salary: Optional[float] = None
    years_of_experience: Optional[float] = None
    industry: Optional[str] = None


class CorrelationResponse(BaseModel):
    salary_vs_experience: Optional[float]
    experience_vs_age: Optional[float]


class PaginationMeta(BaseModel):
    total_records: int
    current_page: int
    total_pages: int
    next_page: Optional[int]
    prev_page: Optional[int]


class PaginatedDataResponse(BaseModel):
    data: List[PersonRecord]
    pagination: PaginationMeta
