from typing import Any, Optional

from fastapi import APIRouter, Query

from app.models.responses import (AgeDistributionResponse, CorrelationResponse,
                                  GenderDistributionResponse,
                                  IndustryDistributionResponse,
                                  IndustryListResponse, PaginatedDataResponse,
                                  PersonRecord, StatsResponse, SummaryResponse)
from app.services.statistics import (get_age_distribution, get_correlations,
                                     get_experience_stats,
                                     get_gender_distribution,
                                     get_individual_record, get_industries,
                                     get_industry_distribution,
                                     get_paginated_data, get_salary_stats,
                                     get_summary, get_top_earners,
                                     get_top_experienced)

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/summary", response_model=SummaryResponse)
def summary() -> dict[str, Any]:
    return get_summary()


@router.get("/employees", response_model=PaginatedDataResponse)
def get_all(
    page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)
) -> PaginatedDataResponse:
    offset = (page - 1) * limit
    return get_paginated_data(offset=offset, limit=limit)


@router.get("/industries", response_model=IndustryListResponse)
def industries():
    return {"industries": get_industries()}


@router.get("/person", response_model=list[PersonRecord])
def person(first_name: str = Query(...), last_name: str = Query(...)) -> list[dict]:
    return get_individual_record(first_name, last_name)


@router.get("/salary/stats", response_model=StatsResponse)
def salary_stats(industry: Optional[str] = Query(None)) -> dict[str, Any]:
    return get_salary_stats(industry)


@router.get("/experience/stats", response_model=StatsResponse)
def experience_stats(industry: Optional[str] = Query(None)) -> dict[str, Any]:
    return get_experience_stats(industry)


@router.get("/industry/distribution", response_model=IndustryDistributionResponse)
def industry_distribution(top_n: int = Query(10, ge=1)) -> dict[str, int]:
    return get_industry_distribution(top_n)


@router.get("/gender/distribution", response_model=GenderDistributionResponse)
def gender_distribution() -> dict[str, int]:
    return get_gender_distribution()


@router.get("/age/distribution", response_model=AgeDistributionResponse)
def age_distribution() -> dict[str, Any]:
    return get_age_distribution()


@router.get("/top-earners", response_model=list[PersonRecord])
def top_earners(n: int = Query(10, ge=1)) -> list[dict[str, Any]]:
    return get_top_earners(n)


@router.get("/top-experienced", response_model=list[PersonRecord])
def top_experienced(n: int = Query(10, ge=1)) -> list[dict[str, Any]]:
    return get_top_experienced(n)


@router.get("/correlations", response_model=CorrelationResponse)
def correlations() -> dict[str, Optional[float]]:
    return get_correlations()
