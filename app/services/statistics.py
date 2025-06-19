import datetime
import json
from functools import lru_cache
from typing import Any, Optional

import pandas as pd
from fastapi import HTTPException

from app.core.config import DATA_PATH
from app.models.responses import (PaginatedDataResponse, PaginationMeta,
                                  PersonRecord)


def calculate_age(born: datetime.datetime) -> int:
    """
    Calculate age from a given birthdate.

    Args:
        born (datetime.datetime): The person's date of birth.

    Returns:
        int: Age in years.
    """
    today = datetime.datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


@lru_cache
def load_dataframe() -> pd.DataFrame:
    """
    Load and preprocess the dataset from JSON.

    Returns:
        pd.DataFrame: Cleaned and augmented DataFrame with additional columns like age.
    """
    with open(DATA_PATH) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
    df["years_of_experience"] = pd.to_numeric(
        df["years_of_experience"], errors="coerce"
    )
    df["date_of_birth"] = pd.to_datetime(
        df["date_of_birth"], format="%d/%m/%Y", errors="coerce"
    )
    df["age"] = df["date_of_birth"].apply(
        lambda x: calculate_age(x) if pd.notnull(x) else None
    )
    return df


def get_paginated_data(offset: int = 0, limit: int = 10) -> PaginatedDataResponse:
    """
    Return a paginated view of the dataset.

    Args:
        offset (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        list[dict[str, Any]]: List of records.
    """
    df = load_dataframe()
    total_records = len(df)

    if offset >= total_records:
        raise HTTPException(status_code=404, detail="Page out of range")

    page_data = (
        df.iloc[offset : offset + limit]
        .replace({float("nan"): None})
        .to_dict(orient="records")
    )

    current_page = (offset // limit) + 1
    total_pages = (total_records + limit - 1) // limit
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    return PaginatedDataResponse(
        data=page_data,
        pagination=PaginationMeta(
            total_records=total_records,
            current_page=current_page,
            total_pages=total_pages,
            next_page=next_page,
            prev_page=prev_page,
        ),
    )


def get_summary() -> dict[str, Any]:
    """
    Generate a summary of the dataset.

    Returns:
        dict[str, Any]: Total record count and missing value statistics.
    """
    df = load_dataframe()
    return {
        "record_count": len(df),
        "missing_values": df.isnull().sum().to_dict(),
    }


def get_industries() -> list[str]:
    """
    Return a list of unique industries found in the dataset.

    Returns:
        list[str]: List of industry names.
    """
    df = load_dataframe()
    return df["industry"].dropna().unique().tolist()


def get_individual_record(first_name: str, last_name: str) -> list[dict[str, Any]]:
    """
    Retrieve a person’s record based on their first and last name.

    Args:
        first_name (str): First name of the person.
        last_name (str): Last name of the person.

    Returns:
        list[dict[str, Any]]: Matching records.
    """
    df = load_dataframe()
    match = df[
        (df["first_name"].str.lower() == first_name.lower())
        & (df["last_name"].str.lower() == last_name.lower())
    ]
    return match[
        ["first_name", "last_name", "salary", "years_of_experience", "industry"]
    ].to_dict(orient="records")


def get_salary_stats(industry: Optional[str] = None) -> dict[str, Any]:
    """
    Compute salary statistics across the dataset or for a specific industry.

    Args:
        industry (Optional[str]): Filter by industry if provided.

    Returns:
        dict[str, Any]: Salary descriptive statistics.
    """
    df = load_dataframe()
    subset = df[df["industry"] == industry] if industry else df
    return subset["salary"].describe().dropna().to_dict()


def get_experience_stats(industry: Optional[str] = None) -> dict[str, Any]:
    """
    Compute experience statistics across the dataset or for a specific industry.

    Args:
        industry (Optional[str]): Filter by industry if provided.

    Returns:
        dict[str, Any]: Experience descriptive statistics.
    """
    df = load_dataframe()
    subset = df[df["industry"] == industry] if industry else df
    return subset["years_of_experience"].describe().dropna().to_dict()


def get_industry_distribution(top_n: int) -> dict[str, int]:
    """
    Get the most common industries by frequency.

    Args:
        top_n (int): Number of top industries to return.

    Returns:
        dict[str, int]: Industry name to count mapping.
    """
    df = load_dataframe()
    return df["industry"].value_counts().head(top_n).to_dict()


def get_gender_distribution() -> dict[str, int]:
    """
    Get the distribution of gender across the dataset.

    Returns:
        dict[str, int]: Gender to count mapping.
    """
    df = load_dataframe()
    return df["gender"].value_counts(dropna=False).to_dict()


def get_age_distribution() -> dict[str, Any]:
    """
    Compute descriptive statistics for age.

    Returns:
        dict[str, Any]: Age statistics including mean, std, and quartiles.
    """
    df = load_dataframe()
    return df["age"].describe().dropna().to_dict()


def get_top_earners(n: int) -> list[PersonRecord]:
    """
    Retrieve the top n earners by salary.

    Args:
        n (int): Number of top earners to return.

    Returns:
        list[PersonRecord]: List of top earners with relevant details.
    """
    df = load_dataframe()
    top = df.sort_values(by="salary", ascending=False).head(n)
    return top[["first_name", "last_name", "salary", "industry"]].to_dict(
        orient="records"
    )


def get_top_experienced(n: int) -> list[dict[str, Any]]:
    """
    Retrieve the top n individuals with the most experience.

    Args:
        n (int): Number of top experienced records to return.

    Returns:
        list[dict[str, Any]]: List of most experienced individuals.
    """
    df = load_dataframe()
    top = df.sort_values(by="years_of_experience", ascending=False).head(n)
    return top[["first_name", "last_name", "years_of_experience", "industry"]].to_dict(
        orient="records"
    )


def get_correlations() -> dict[str, Optional[float]]:
    """
    Compute correlation values between selected numeric columns.

    Returns:
        dict[str, Optional[float]]: Correlation coefficients for salary vs experience, and experience vs age.
    """
    df = load_dataframe()
    corr1 = df[["salary", "years_of_experience"]].corr().iloc[0, 1]
    corr2 = df[["years_of_experience", "age"]].corr().iloc[0, 1]
    return {
        "salary_vs_experience": round(corr1, 4) if pd.notnull(corr1) else None,
        "experience_vs_age": round(corr2, 4) if pd.notnull(corr2) else None,
    }
