"""Functions for parsing pandas dataframes.

The top-level functions are (in-order):
- dataframe_to_gene_values
- dataframe_to_gene_values_by_name
- dataframe_to_gene_values_by_idx
"""
from typing import List, Tuple

import pandas as pd
from geneweaver.core.parse.numpy import (
    SYMBOL_KEYS,
    VALUE_KEYS,
    ndarray_to_gene_values_by_idx,
)
from geneweaver.core.schema.batch import GenesetValueInput


def dataframe_to_gene_values(geneset_df: pd.DataFrame) -> List[GenesetValueInput]:
    """Convert a pandas dataframe to a list of GeneValueInput objects.

    This function will try to map via labels first, then by index.

    :param geneset_df: The pandas dataframe to convert.
    :raises ValueError: If there's a problem mapping the dataframe.
    :return: A set of the values in the dataframe.
    """
    check_input_shape_and_type(geneset_df)
    try:
        return dataframe_to_gene_values_named(geneset_df)
    except ValueError:
        return dataframe_to_gene_values_by_idx(geneset_df)


def dataframe_to_gene_values_by_idx(
    geneset_df: pd.DataFrame,
) -> List[GenesetValueInput]:
    """Convert a pandas dataframe to a list of GeneValueInput objects.

    The pandas dataframe must be a 2-dimensional dataframe with 2 columns. The first
    column will be mapped to the GenesetValueInput.symbol attribute, and the second
    column will be mapped to the GenesetValueInput.value attribute.

    :param geneset_df: The pandas dataframe to convert.
    :return: A set of the values in the dataframe.
    """
    return ndarray_to_gene_values_by_idx(geneset_df.values)


def dataframe_to_gene_values_named(geneset_df: pd.DataFrame) -> List[GenesetValueInput]:
    """Convert a pandas dataframe to a list of GeneValueInput objects using labels.

    :param geneset_df: The pandas dataframe to convert.
    :raises ValueError: If there's a problem mapping the dataframe using labels.
    :return: A set of the values in the dataframe.
    """
    symbol_key, value_key = map_dataframe_labels_to_gene_value_attr(geneset_df)

    return [
        GenesetValueInput(symbol=row[symbol_key], value=row[value_key])
        for _, row in geneset_df.iterrows()
    ]


def dataframe_to_gene_values_binary(
    geneset_df: pd.DataFrame,
) -> List[GenesetValueInput]:
    """"""


def check_input_shape_and_type(input_df: pd.DataFrame) -> None:
    """Check the shape and type of the input dataframe.

    :raises ValueError: If the input dataframe is not a pandas dataframe or if it is not
    at least 2-dimensional.
    """
    if not isinstance(input_df, pd.DataFrame):
        raise ValueError("Input is not a pandas dataframe")

    if input_df.ndim < 2:
        raise ValueError("Input must be at least a 2-dimensional dataframe")


def map_dataframe_labels_to_gene_value_attr(
    geneset_dataframe: pd.DataFrame,
) -> Tuple[str, str]:
    """Map DataFrame column names to GenesetValueInput attributes.

    This function checks if a DataFrame has certain column names, and if it does,
    it maps these to a GenesetValueInput object.

    In order, it will map ("Symbol", "GeneID", "Gene_ID", "Gene ID") to the
    GenesetValueInput symbol attribute.

    In order, it will map
    ("Value", "Score", "PValue", "QValue", "Effect", "Correlation") to the
    GenesetValueInput value attribute.

    If it cannot map to both symbol and value, it will raise an error.

    :param geneset_dataframe: The pandas DataFrame to map.

    :raises ValueError: If the DataFrame column names cannot be mapped to
    GenesetValueInput attributes.
    :return: A tuple, where the first value is the key mapping to the symbol attribute
    and the second value is the key mapping to the value attribute.
    """
    symbol_key, value_key = None, None
    for key in SYMBOL_KEYS:
        if key in geneset_dataframe.columns:
            symbol_key = key
            break

    for key in VALUE_KEYS:
        if key in geneset_dataframe.columns:
            value_key = key
            break

    if symbol_key is None or value_key is None:
        raise ValueError(
            "Could not map DataFrame column names to GenesetValueInput attributes"
        )

    return symbol_key, value_key
