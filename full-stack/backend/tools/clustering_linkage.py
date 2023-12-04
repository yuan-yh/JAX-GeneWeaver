from geneweaver.client.datasets.nci60 import DNACombinedaCGHGeneSummary
# Reproduce the Principal Component Analysis
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
# Draw projection plots 1&2 Removed
# Clustering & Linkage
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram, cut_tree
import pandas as pd

# from .boolean_algebra import boolean_algebra_tool

def initial_processing():
    """
        Perform the initial processing on gene data with PCA, clustering, and filtering based on intensity.
        Returns two sets of genes, which will be analyzed in statistical models.
    """
    try:
        # Initializing the dataset will download the required data from nci.nih.gov
        ds = DNACombinedaCGHGeneSummary()

        # Use the LINKOUT attribute to get a link to the original data download page
        ds.LINKOUT
        # Output: https://discover.nci.nih.gov/cellminer/loadDownload.do

        # Gene Identifiers: gene symbols and entrez ids can be used as possible identifiers.
        # print(ds.gene_names[:5])
        # print(ds.entrez_ids[:5])

        intensity = ds.intensity.transpose()
        # print(intensity[:10])

        # Reproduce the Principal Component Analysis
        scaler = StandardScaler()
        intensity_data_scaled = scaler.fit_transform(intensity)
        pca = PCA()
        pr_out = pca.fit_transform(intensity_data_scaled)
        components = pca.components_
        explained_variance = pca.explained_variance_
        # print(explained_variance)

        # Clustering & Linkage
        data_dist = pdist(intensity_data_scaled)
        # print(data_dist)
        linkage_matrix = linkage(data_dist, method='complete')
        # print(linkage_matrix)

        # User Decision: select the top 4 clusters from the linkage analysis.
        hc_clusters = cut_tree(linkage_matrix, n_clusters=4).flatten()
        # print(hc_clusters)

        table = pd.crosstab(hc_clusters,
                            intensity.index.tolist(),
                            rownames=['clusters'],
                            colnames=['labels'])
        # print(table)

        # After clustered the data by cell line, we can go back and filter our original dataset to just our cluster of interest.
        def get_columns_in_cluster(cluster_idx):
          row_values = table.loc[cluster_idx]
          columns_with_value_1 = row_values[row_values == 1]
          column_names = columns_with_value_1.index.tolist()
          return column_names

        # User Decision: select the second (index 1) and third (index 2) cluster
        # print(len(get_columns_in_cluster(1)))
        # print(len(get_columns_in_cluster(2)))


        # Filter to Columns of Interest
        # Using the cell line labels from our earlier clustering, we can filter the intensity values to include just the cell lines of interest (columns).
        group_1 = ds.intensity.loc[:, get_columns_in_cluster(1)]
        group_2 = ds.intensity.loc[:, get_columns_in_cluster(2)]
        # print(group_1)
        # print(group_2)

        # Filter to Rows of Interest then
        # We can also filter out rows (genes) that don't meet an intensity threshold, or some other criteria. Here we remove any row where each cell line doesn't have an intensity of at least 0.3.
        min_intensity = 0.3
        interest_genes_1 = group_1[group_1.gt(min_intensity).all(axis=1)]
        interest_genes_2 = group_2[group_2.gt(min_intensity).all(axis=1)]
        # print(interest_genes_1)
        # print(interest_genes_2)

        # Label The Gene Identifiers using Entrez IDs or the gene symbols if preference
        interest_genes_1.index = ds.entrez_ids[interest_genes_1.index]
        interest_genes_2.index = ds.entrez_ids[interest_genes_2.index]
        # print(interest_genes_1.index)
        # print(interest_genes_2.index)

        # Remove Rows Without Identifiers
        # Some of the NCI-60 rows don't have identifiers, which are required for use with Geneweaver, so we remove these now.
        # Remove Rows Without a Gene Identifier
        interest_genes_1 = interest_genes_1.drop(0, errors="ignore")
        interest_genes_2 = interest_genes_2.drop(0, errors="ignore")
        # print(interest_genes_1)
        # print(interest_genes_2)
        return interest_genes_1, interest_genes_2

    except Exception as e:
        # Handle exceptions (log or re-raise as needed)
        raise RuntimeError("Error in processing gene data: " + str(e))

# Example usage
# interest_genes_1, interest_genes_2 = initial_processing()
# print(interest_genes_1)
# print(interest_genes_2)