from geneweaver.tools.boolean_algebra import (
    BooleanAlgebra,
    BooleanAlgebraType,
    BooleanAlgebraInput
)
from geneweaver.core.schema.gene import GeneValue
from geneweaver.core import parse
from geneweaver.core.render.gene_list import gene_list_str

# database operation
from ..database.db import AnalysisRun, Session
import uuid
import json


def boolean_algebra_tool(interest_genes_1, interest_genes_2):
    # !Process in the server side!
    boolean = BooleanAlgebra()

    gene_values_1 = parse.iterable.to_gene_value_list_binary(interest_genes_1.index)
    gene_values_2 = parse.iterable.to_gene_value_list_binary(interest_genes_2.index)

    result = boolean.run(BooleanAlgebraInput(
        type=BooleanAlgebraType.INTERSECTION,
        input_genesets=[gene_values_1, gene_values_2]
    ))

    geneset_values = list(result.result[(0,1)])
    geneset_values_str = gene_list_str(geneset_values)
    # print(type(geneset_values_str))

    # Store in the database
    # Convert geneset_values to a string for storage
    # geneset_values_str = json.dumps(geneset_values)

    # Create a unique run ID
    run_id = str(uuid.uuid4())

    # Start a new database session
    session = Session()
    try:
        new_run = AnalysisRun(run_id=run_id, geneset_values=geneset_values_str)
        session.add(new_run)
        session.commit()
    finally:
        session.close()

    return run_id   # Return the run ID for reference



# Example usage
# Assuming interest_genes_1 and interest_genes_2 are defined and contain data
# run_id = boolean_algebra_tool(interest_genes_1, interest_genes_2)
# print(f"Analysis run completed. Run ID: {run_id}")
