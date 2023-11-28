from typing import List

from geneweaver.core.schema.batch import (
    HEADER_CHARACTERS,
    IGNORE_CHARACTERS,
    INV_CHAR_MAP,
    SPACE_SEPARATED_HEADER_CHARACTERS,
    BatchUploadGeneset,
)

CHAR_MAP = HEADER_CHARACTERS | SPACE_SEPARATED_HEADER_CHARACTERS | IGNORE_CHARACTERS


def format_batch_file(genesets: List[BatchUploadGeneset]) -> str:
    """Format a batch upload file from a list of genesets."""


def format_geneset(geneset: BatchUploadGeneset) -> str:
    geneset_dict = geneset.dict(exclude={"values", "curation_id"})
    "\n".join(
        (
            f"{INV_CHAR_MAP[key] if key in INV_CHAR_MAP else key}={value}"
            for key, value in geneset_dict.items()
        )
    )
