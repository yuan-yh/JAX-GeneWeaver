"""Parse iterables into Geneweaver objects."""
from typing import Iterable, List, Any
from geneweaver.core.schema.gene import GeneValue


def to_gene_value_list_binary(gene_ids: Iterable) -> List[GeneValue]:
    """Parse a list of Gene IDs to GeneValue objects.

    :param gene_ids: Iterable of Gene IDs.
    :return: List of GeneValue objects.
    """
    return [GeneValue(symbol=gene_id, value=1) for gene_id in gene_ids]


def to_gene_value_list(gene_ids: Iterable, values: Iterable) -> List[GeneValue]:
    """Parse a list of Gene IDs to GeneValue objects.

    :param gene_ids: Iterable of Gene IDs.
    :param values: Iterable of Gene values.
    :return: List of GeneValue objects.
    """
    return [
        GeneValue(symbol=gene_id, value=value)
        for gene_id, value in zip(gene_ids, values)
    ]


def to_gene_value_list_zipped(gene_ids: Iterable) -> List[GeneValue]:
    """Parse a list of Gene IDs to GeneValue objects.

    This function takes an iterable of items where each item can be unpacked into a
    gene ID and a value. For example, if the iterable is a list of tuples, the first
    item in each tuple is the gene ID and the second item is the value.

    :param gene_ids: Iterable of Gene IDs and values.
    :return: List of GeneValue objects.
    """
    return [GeneValue(symbol=gene_id, value=value) for gene_id, value in gene_ids]
