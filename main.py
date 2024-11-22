from MultinetPy import multinetpy as mp
from MultinetPy import multinetx as mx
from MultinetPy import graph_mng as gm
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
from pyvis.network import Network
from io import StringIO

#Import dataset
mg = gm.Import_Graph.make_graph("path_nodes.txt", "path.edges", "path_layers.txt")
# fig = plt.figure(figsize=(15,5))
# ax1 = fig.add_subplot(121)
# ax1.imshow(mx.adjacency_matrix(mg,weight='weight').todense(),
#         origin='upper',interpolation='nearest',cmap=plt.cm.jet_r)
# ax1.set_title('supra adjacency matrix')
# plt.show()

aggregated_centralities_CC1 = mg.aggregated_CC()
weighted_centralities_CC1 = mg.weighted_CC()

# Calculate some centrality measures in networkX
mg.aggregated_centralityTest(nx.betweenness_centrality)

# Code used for comparing a tabel with calculated centralities
file_path1 =' path_BC.xlsx.'
file_path2 ='path_CC.xlsx'

# Load the table ranks 
table_rank1 = mg.load_table_ranks_from_excel(file_path1)
table_rank2 = mg.load_table_ranks_from_excel(file_path2)

# kendall's tau
print("\nkendall's tau in Closeness Centrality:\n")
mg.plot_kendall_tau(aggregated_centralities_CC1, weighted_centralities_CC1, table_rank1)

# isim
a, b, c = mg.intersection_similarity(table_rank2, aggregated_centralities_CC1, weighted_centralities_CC1, max_k=20)
print("\nisim in closeness:\n")
mg.display_isim_table(a, b, c)

# rank difference
print("\nrank difference in closeness:\n")
R, R2, R3 = mg.Rank_Difference(table_rank2, aggregated_centralities_CC1, weighted_centralities_CC1)
mg.plot_rank_difference(R, R2, R3)