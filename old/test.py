from geneweaver.tools.boolean_algebra import (
    BooleanAlgebra,
    BooleanAlgebraType,
    BooleanAlgebraInput
)
from geneweaver.core.schema.gene import GeneValue
from geneweaver.core import parse
boolean = BooleanAlgebra()

gene_values_1 = parse.iterable.to_gene_value_list_binary(interest_genes_1.index)
gene_values_2 = parse.iterable.to_gene_value_list_binary(interest_genes_2.index)

result = boolean.run(BooleanAlgebraInput(
    type=BooleanAlgebraType.INTERSECTION,
    input_genesets=[gene_values_1, gene_values_2]
))

geneset_values = list(result.result[(0,1)])