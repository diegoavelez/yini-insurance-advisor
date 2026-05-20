"""Optimization contracts for future DSPy-based work."""

from __future__ import annotations

from pydantic import BaseModel, Field

from contracts.evaluation import ExpectedBehavior


class QueryClassificationOptimizationInput(BaseModel):
    """One typed optimization input for query classification."""

    user_query: str = Field(min_length=1)


class QueryClassificationOptimizationOutput(BaseModel):
    """One typed optimization output for query classification."""

    expected_behavior: ExpectedBehavior
    rationale: str = Field(min_length=1)
