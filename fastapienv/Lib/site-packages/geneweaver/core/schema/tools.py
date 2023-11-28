"""Schema for tools and tool framework."""
from typing import List

from pydantic import BaseModel

from .geneset import GenesetGenes


class Tool(BaseModel):
    """Tool schema."""

    name: str
    description: str
    version: str
    url: str


class ToolInput(BaseModel):
    """Tool input schema."""

    Metadata: dict
    GeneSets: List[GenesetGenes]


class ToolOutput:
    """Tool output schema."""

    Metadata: dict
    Images: List[str]
    GeneSets: List[GenesetGenes]
