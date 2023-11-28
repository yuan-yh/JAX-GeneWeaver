from pydantic import BaseModel
from typing import List

class PreprocessedGeneData(BaseModel):
    gene_set_1: List[str]  # List of gene identifiers for the first set
    gene_set_2: List[str]  # List of gene identifiers for the second set
