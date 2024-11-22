# MultiNetPy
MultiNetPy is a Python package for analyzing multiplex networks. It provides functionalities for importing multiplex network data and computing centrality measures
Installation

Install the dependencies using pip:
pip install -r requirements.txt

# Import a multiplex network dataset
mg = gm.Import_Graph.make_graph(
    "YourPath_nodes.txt",
    "YourPath_nodes.edges",
    "YourPath_nodes_layers.txt"
)

# Compute centrality measures
# First define desires centrality measure, including betweenness and closeness
aggregated_centralities_CC1 = mg.aggregated_CC()
weighted_centralities_CC1 = mg.weighted_CC()
aggregated_centralities_BC1 = mg.aggregated_BC()
weighted_centralities_BC1 = mg.weighted_BC()

# Use some other centrality measures in networkX
test = mg.Centralities(nx.degree_centrality) # define desired centrality measure
mg.aggregated_centralityTest(nx.degree_centrality)

# Code used for comparing a table with calculated centralities
file_path1 =' path_BC.xlsx.'
file_path2 ='path_CC.xlsx'

# Load the table ranks 
table_rank1 = mg.load_table_ranks_from_excel(file_path1)
table_rank2 = mg.load_table_ranks_from_excel(file_path2)

# kendall's tau
print("kendall's tau in betweenness:")
mg.plot_kendall_tau(aggregated_centralities_BC1, weighted_centralities_BC1, table_rank1)
print("\nkendall's tau in Closeness Centrality:\n")
mg.plot_kendall_tau(aggregated_centralities_CC1, weighted_centralities_CC1, table_rank1)

# isim
a, b, c = mg2.intersection_similarity(table_rank2, aggregated_centralities_CC1, weighted_centralities_CC1, max_k=20)
print("\nisim in closeness:\n")
mg2.display_isim_table(a, b, c)

# rank difference
print("\nrank difference in betweenness in your dataset:\n")
Rb, R2b, R3b = mg.Rank_Difference(table_rank1, aggregated_centralities_BC1, weighted_centralities_BC1)
mg.plot_rank_difference(Rb, R2b, R3b)
print("\nrank difference in closeness:\n")
R, R2, R3 = mg.Rank_Difference(table_rank2, aggregated_centralities_CC1, weighted_centralities_CC1)
mg.plot_rank_difference(R, R2, R3)

Documentation
Detailed documentation for each function and class can be found in the source code.

