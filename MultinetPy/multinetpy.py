from MultinetPy import multinetx
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import kendalltau

class MultiNetPy(multinetx.MultilayerGraph):
    def __init__(self, **attr):
        super().__init__(**attr)
        self.node_sums = None 
        self.create_adjacency_matrix()  

    def load_table_ranks_from_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            if 'ID' not in df.columns or 'Order' not in df.columns:
                raise ValueError("Excel file must contain 'ID' and 'Order' columns.")
            table_ranks = df.set_index('ID')['Order'].to_dict()
            return table_ranks
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}
            
    def degree_centrality(self, i=None):
        vectors = {}
        layers = self.list_of_layers
        if i is not None:
            vectors[i] = []
        for layer in layers:
            degrees = layer.degree
            if i is not None:
                vectors[i].append(degrees[i])
            else:
                for degree in degrees:
                    if not degree[0] in vectors:
                        vectors[degree[0]] = []
                    vectors[degree[0]].append(degree[1])
        result = {}
        for vector in vectors:
            vector_sum = sum(vectors[vector])
            result[vector] = vector_sum

        sorted_centrality = sorted(result.items(), key=lambda x: x[1], reverse=True)
        # Extract the top 20 values
        top_12_values = sorted_centrality[:12]
        # Create a table using matplotlib
        fig, ax = plt.subplots()
        table_data = [['Number', 'Node ID', 'Degree Centrality Value']]
        for i, (node_id, centrality_value) in enumerate(top_12_values, start=1):
            centrality_value_formatted = format(centrality_value, ".4f")
            table_data.append([i, node_id, centrality_value_formatted])
    
        table = ax.table(cellText=table_data, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        ax.axis('off')
        plt.show()

    # All the centralities in networkX
    def Centralities(self, centrality_type):
        Centrality = {}
        for layer_graph in self.list_of_layers:
            try:
                Centrality[layer_graph] = centrality_type(layer_graph)
            except Exception as e:
                print(f"Error calculating {centrality_type} centrality for layer {layer_graph}: {e}")
        return Centrality 
    
    def aggregated_centralityTest(self, centrality_type):
        # Calculate betweenness centrality for each layer
        C_centralities = self.Centralities(centrality_type)
        # Initialize dictionary to store aggregate centrality measures
        aggregated_centrality = {}      
        # Initialize number of layers
        num_layers = len(self.list_of_layers)       
        # Iterate over nodes in each layer and aggregate betweenness centrality
        for layer_graph, centrality_dict in C_centralities.items():
            for node, centrality_value in centrality_dict.items():
                if node not in aggregated_centrality:
                    aggregated_centrality[node] = 1 * centrality_value
                else:
                    aggregated_centrality[node] += 1 * centrality_value
        
        # Compute the aggregate centrality for each node
        for node in aggregated_centrality:
            aggregated_centrality[node] /= num_layers        
        # Sort the aggregated centrality values
        sorted_centrality = sorted(aggregated_centrality.items(), key=lambda x: x[1], reverse=True)   
        # Extract the top 20 values
        top_20_values = sorted_centrality[:20]
        print(f"centrality type:{centrality_type}")
        fig, ax = plt.subplots()
        table_data = [['Number', 'Node ID', ' Value']]
        for i, (node_id, centrality_value) in enumerate(top_20_values, start=1):
            centrality_value_formatted = format(centrality_value, ".4f")
            table_data.append([i, node_id, centrality_value_formatted])
    
        table = ax.table(cellText=table_data, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        ax.axis('off')
        plt.show()

    def Closeness_centrality(self):
        ClosenessCentrality = {}
        for layer_graph in self.list_of_layers:
            try:
                ClosenessCentrality[layer_graph] = nx.closeness_centrality(layer_graph)
            except Exception as e:
                print(f"Error calculating closeness centrality for layer {layer_graph}: {e}")
        return ClosenessCentrality
    
    def aggregated_CC(self):
            # Calculate betweenness centrality for each layer
            C_centralities = self.Closeness_centrality()
            aggregated_centrality = {}
            # Initialize number of layers
            num_layers = len(self.list_of_layers)
            
            # Iterate over nodes in each layer and aggregate betweenness centrality
            for layer_graph, centrality_dict in C_centralities.items():
                for node, centrality_value in centrality_dict.items():
                    if node not in aggregated_centrality:
                        aggregated_centrality[node] = 1 * centrality_value
                    else:
                        aggregated_centrality[node] += 1 * centrality_value

            for node in aggregated_centrality:
                aggregated_centrality[node] /= num_layers

            sorted_centrality = sorted(aggregated_centrality.items(), key=lambda x: x[1], reverse=True)
            top_20_values = sorted_centrality[:20]

            return top_20_values

    def weighted_CC(self):
        C_centralities = self.Closeness_centrality()
        aggregated_centrality = {}
        # Compute normalization constant W
        W = sum(self.node_sums.values())
        # Iterate over nodes in each layer and aggregate betweenness centrality
        for layer_graph, centrality_dict in C_centralities.items():
            for node, centrality_value in centrality_dict.items():
                weight = self.node_sums.get(node, 0)
                if node not in aggregated_centrality:
                    aggregated_centrality[node] = weight * centrality_value / W
                else:
                    aggregated_centrality[node] += weight * centrality_value / W

        sorted_centrality = sorted(aggregated_centrality.items(), key=lambda x: x[1], reverse=True)
        top_20_values = sorted_centrality[:20]
        return top_20_values

    def betweenness_centrality(self):
        betweennessCentrality = {}
        for layer_graph in self.list_of_layers:
            try:
                betweennessCentrality[layer_graph] = nx.betweenness_centrality(layer_graph)
            except Exception as e:
                print(f"Error calculating betweenness centrality for layer {layer_graph}: {e}")
        return betweennessCentrality
    
        
    def aggregated_BC(self):
        B_centralities = self.betweenness_centrality()
        aggregated_centrality = {}
        num_layers = len(self.list_of_layers)

        for layer_graph, centrality_dict in B_centralities.items():
            for node, centrality_value in centrality_dict.items():
                if node not in aggregated_centrality:
                    aggregated_centrality[node] = centrality_value
                else:
                    aggregated_centrality[node] += centrality_value

        for node in aggregated_centrality:
            aggregated_centrality[node] /= num_layers
        sorted_centrality = sorted(aggregated_centrality.items(), key=lambda x: x[1], reverse=True)
        top_20_values = sorted_centrality[:20]

        return top_20_values

    def weighted_BC(self):
        B_centralities = self.betweenness_centrality()
        aggregated_centrality = {}
        W = sum(self.node_sums.values())

        for layer_graph, centrality_dict in B_centralities.items():
            for node, centrality_value in centrality_dict.items():
                weight = self.node_sums.get(node, 0)
                if node not in aggregated_centrality:
                    aggregated_centrality[node] = weight * centrality_value / W
                else:
                    aggregated_centrality[node] += weight * centrality_value / W

        sorted_centrality = sorted(aggregated_centrality.items(), key=lambda x: x[1], reverse=True)
        top_20_values = sorted_centrality[:20]
        return top_20_values

    
    # Create adjacency matrix
    def create_adjacency_matrix(self):
        layers = self.list_of_layers
        # Find unique nodes across all layers
        all_nodes = set()
        for layer in layers:
            all_nodes.update(layer.nodes())
        # Sort nodes based on their IDs (assuming IDs are strings)
        all_nodes = sorted(all_nodes)
        # Check if all_nodes is empty
        if not all_nodes:
            print("No nodes found in the layers.")
            return
        # Create an empty adjacency matrix
        num_nodes = len(all_nodes)
        adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        # Populate the adjacency matrix with connections based on the edges in each layer
        for layer in layers:
            for u, v in layer.edges():
                index1 = all_nodes.index(u)
                index2 = all_nodes.index(v)
                adj_matrix[index1, index2] += 1
                adj_matrix[index2, index1] += 1  # Assuming undirected edges
        # Calculate the sum of connections for each node
        node_sums = {}
        for i, node_id in enumerate(all_nodes):
            connections_sum = np.sum(adj_matrix[i])
            node_sums[node_id] = connections_sum
        # Create an adjacency matrix with node IDs and sum of connections
        adj_matrix_with_ids = np.zeros((num_nodes + 1, num_nodes + 2), dtype=object)
        adj_matrix_with_ids[0, 1:num_nodes+1] = all_nodes
        adj_matrix_with_ids[1:num_nodes+1, 0] = all_nodes
        adj_matrix_with_ids[1:num_nodes+1, 1:num_nodes+1] = adj_matrix
        # Add the sum of connections to the last column
        for i, node_id in enumerate(all_nodes, start=1):
            adj_matrix_with_ids[i, num_nodes+1] = node_sums[node_id]
        # Set the header for the last column
        adj_matrix_with_ids[0, num_nodes+1] = "Sum"
        df = pd.DataFrame(adj_matrix_with_ids[1:, 1:], index=adj_matrix_with_ids[1:, 0], columns=adj_matrix_with_ids[0, 1:])
        print(df)
        if df.empty:
            print("The DataFrame is empty.")
            return
        plt.figure(figsize=(20, 16))  
        sns.heatmap(df.astype(int), annot=True, fmt="d", cmap="YlGnBu", linewidths=.5, cbar_kws={"label": "Sum of Connections"}, annot_kws={"size": 8})
        plt.title("Adjacency Matrix with Node IDs and Sum of Connections")
        plt.xlabel("Node IDs")
        plt.ylabel("Node IDs")
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.show()
        self.node_sums = node_sums
        return adj_matrix
        
    def plot_kendall_tau(self, aggregated_centralities, weighted_centralities, table_ranks):
        # Check for None inputs   
        if aggregated_centralities is None:
            raise ValueError("The input 'aggregated_centralities' is None. Please provide a valid list.")
        if weighted_centralities is None:
            raise ValueError("The input 'weighted_centralities' is None. Please provide a valid list.")
        if table_ranks is None:
            raise ValueError("The input 'Source Value_ranks' is None. Please provide a valid dictionary.")

        def convert_to_int(node):
            try:
                return int(node)
            except ValueError:
                return None
        aggregated_ranks = {
            convert_to_int(node): rank
            for rank, (node, _) in enumerate(aggregated_centralities, start=1)
            if convert_to_int(node) is not None
        }

        weighted_ranks = {
            convert_to_int(node): rank
            for rank, (node, _) in enumerate(weighted_centralities, start=1)
            if convert_to_int(node) is not None
        }

        table_ranks = {
            int(node): rank
            for node, rank in table_ranks.items()
        }

        common_nodes_agg_table = set(aggregated_ranks.keys()).intersection(table_ranks.keys())
        common_nodes_weighted_table = set(weighted_ranks.keys()).intersection(table_ranks.keys())
        common_nodes_weighted_agg = set(weighted_ranks.keys()).intersection(aggregated_ranks.keys())

        agg_ranks = [aggregated_ranks[node] for node in common_nodes_agg_table]
        table_ranks_for_agg = [table_ranks[node] for node in common_nodes_agg_table]
        weighted_ranks_common = [weighted_ranks[node] for node in common_nodes_weighted_table]
        table_ranks_for_weighted = [table_ranks[node] for node in common_nodes_weighted_table]
        # Exploit ranks for comparing weighted and aggregated
        weighted_ranks_for_agg = [weighted_ranks[node] for node in common_nodes_weighted_agg]
        agg_ranks_for_weighted = [aggregated_ranks[node] for node in common_nodes_weighted_agg]
        results = []
        # Compute Kendall's Tau
        if agg_ranks and table_ranks_for_agg:
            tau_agg, p_value_agg = kendalltau(agg_ranks, table_ranks_for_agg)
            results.append(['Aggregated vs Wang mothod 2023', round(tau_agg, 4), round(p_value_agg, 4)])

        if weighted_ranks_common and table_ranks_for_weighted:
            tau_weighted, p_value_weighted = kendalltau(weighted_ranks_common, table_ranks_for_weighted)
            results.append(['Weighted vs Wang mothod 2023', round(tau_weighted, 4), round(p_value_weighted, 4)])

        if weighted_ranks_for_agg and agg_ranks_for_weighted:
            tau_weighted_agg, p_value_weighted_agg = kendalltau(weighted_ranks_for_agg, agg_ranks_for_weighted)
            results.append(['Weighted vs Aggregated', round(tau_weighted_agg, 4), round(p_value_weighted_agg, 4)])
        df = pd.DataFrame(results, columns=['Comparison', "Kendall's Tau", 'p-value'])
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)  
        plt.title("Kendall's Tau Rank Correlation Results")
        plt.show()
            
    def Rank_Difference(self, table_ranks, aggregated_ranks, weighted_ranks):
        def convert_to_int(node):
            try:
                return int(node)
            except ValueError:
                return None

        agg_rank_dict = {convert_to_int(node): rank for rank, (node, _) in enumerate(aggregated_ranks, start=1) if convert_to_int(node) is not None}
        weight_rank_dict = {convert_to_int(node): rank for rank, (node, _) in enumerate(weighted_ranks, start=1)}
        table_rank_dict = table_ranks
        print("Aggregated Rank Dictionary:", agg_rank_dict)
        print("Weighted Rank Dictionary:", weight_rank_dict)
        print("Table Rank Dictionary:", table_rank_dict)

        common_nodes_aggandTable = set(agg_rank_dict.keys()).intersection(table_rank_dict.keys())
        common_nodes_weightedandTable = set(weight_rank_dict.keys()).intersection(table_rank_dict.keys())
        common_nodes_aggandWeighted = set(agg_rank_dict.keys()).intersection(weight_rank_dict.keys())
        
        print("Common nodes between Aggregated and Table:", common_nodes_aggandTable)
        print("Common nodes between Weighted and Table:", common_nodes_weightedandTable)
        print("Common nodes between Aggregated and Weighted:", common_nodes_aggandWeighted)

        R, R2, R3 = None, None, None
        # Calculation between aggregated and Wang method 2023
        n_agg = len(common_nodes_aggandTable)
        if n_agg > 1:
            sum_d = sum(abs(agg_rank_dict[node] - table_rank_dict[node]) for node in common_nodes_aggandTable)
            R = round(1 - (3 * sum_d) / (n_agg**2 - 1), 4)
            print(f"Rank correlation in aggregated Betweenness Centrality and Wang mothod 2023: {R}")
        else:
            print("Insufficient common nodes to compare ranks between aggregated and Wang mothod 2023.")
        
        # Calculation between weighted and Wang method 2023
        n_weighted = len(common_nodes_weightedandTable)
        if n_weighted > 1:
            sum_d = sum(abs(weight_rank_dict[node] - table_rank_dict[node]) for node in common_nodes_weightedandTable)
            R2 = round(1 - (3 * sum_d) / (n_weighted**2 - 1), 4)
            print(f"Rank correlation in weighted Betweenness Centrality and Wang mothod 2023: {R2}")
        else:
            print("Insufficient common nodes to compare ranks between weighted and Wang mothod 2023.")
        # Calculation between aggregated and weighted
        n_agg_weighted = len(common_nodes_aggandWeighted)
        R3 = None
        if n_agg_weighted > 1:
            sum_d = sum(abs(agg_rank_dict[node] - weight_rank_dict[node]) for node in common_nodes_aggandWeighted)
            R3 =round (1 - (3 * sum_d) / (n_agg_weighted**2 - 1),4)
            print(f"Rank correlation in aggregated and weighted Betweenness Centrality: {R3}")
        else:
            print("Insufficient common nodes to compare ranks between aggregated and weighted.")
        
        return R, R2, R3

    def plot_rank_difference(self, R, R2, R3):
        labels = [
            'Aggregated vs Wang method 2023',
            'Weighted vs Wang method 2023',
            'Aggregated vs Weighted'
        ]
        data = {
            'Comparison': labels,
            'Rank Correlation': [R, R2, R3],
        }
        df = pd.DataFrame(data)
        fig, ax = plt.subplots(figsize=(8, 3))  
        ax.axis('off')
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            cellLoc='center',
            loc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2) 
        plt.show()
            
    # Intersection similarity
    def intersection_similarity(self, table_ranks, aggregated_ranks, weighted_ranks, max_k=20):
        def convert_to_int(node):
            try:
                return int(node)
            except ValueError:
                return None
        # Create dictionaries for the ranks, filtering out invalid nodes (non-integers)
        agg_rank_dict = {convert_to_int(node): rank for rank, (node, _) in enumerate(aggregated_ranks, start=1) if convert_to_int(node) is not None}
        weight_rank_dict = {convert_to_int(node): rank for rank, (node, _) in enumerate(weighted_ranks, start=1) if convert_to_int(node) is not None}
        table_rank_dict = {convert_to_int(node): rank for rank, (node, _) in enumerate(table_ranks.items(), start=1) if convert_to_int(node) is not None}
        # Sort nodes by their rank in each ranking method
        agg_nodes_sorted_by_rank = sorted(agg_rank_dict.items(), key=lambda x: x[1])
        table_nodes_sorted_by_rank = sorted(table_rank_dict.items(), key=lambda x: x[1])
        weighted_nodes_sorted_by_rank = sorted(weight_rank_dict.items(), key=lambda x: x[1])
        # Initialize lists to store similarities for each K
        isim_k_values = []
        isim_k2_values = []
        isim_k3_values = []
        # Get the minimum length to avoid index errors if fewer nodes than max_k
        min_length = min(len(agg_nodes_sorted_by_rank), len(table_nodes_sorted_by_rank), len(weighted_nodes_sorted_by_rank))
        # Ensure we don't exceed available nodes when calculating up to K
        max_k = min(max_k, min_length)

        for K in range(1, max_k + 1):
            # Calculate intersection similarity with aggregated ranks
            isim_k = 0.0
            for i in range(K):
                table_node = table_nodes_sorted_by_rank[i][0] if i < len(table_nodes_sorted_by_rank) else None
                agg_node = agg_nodes_sorted_by_rank[i][0] if i < len(agg_nodes_sorted_by_rank) else None
                if table_node is not None and agg_node is not None:
                    delta = 0 if table_node == agg_node else 1
                else:
                    delta = 1  # If either node is missing
                isim_k += delta / (2 * (i + 1))

            isim_k = (1 / K) * isim_k
            normalized_isim_k = 1 - isim_k
            isim_k_values.append(round(normalized_isim_k,4))

            # Calculate intersection similarity with weighted ranks
            isim_k2 = 0.0
            for i in range(K):
                table_node = table_nodes_sorted_by_rank[i][0] if i < len(table_nodes_sorted_by_rank) else None
                weight_node = weighted_nodes_sorted_by_rank[i][0] if i < len(weighted_nodes_sorted_by_rank) else None
                if table_node is not None and weight_node is not None:
                    delta = 0 if table_node == weight_node else 1
                else:
                    delta = 1  # If either node is missing
                isim_k2 += delta / (2 * (i + 1))

            isim_k2 = (1 / K) * isim_k2
            normalized_isim_k2 = 1 - isim_k2
            isim_k2_values.append(round(normalized_isim_k2,4))

            # Calculate intersection similarity between aggregated and weighted ranks
            isim_k3 = 0.0
            for i in range(K):
                agg_node = agg_nodes_sorted_by_rank[i][0] if i < len(agg_nodes_sorted_by_rank) else None
                weight_node = weighted_nodes_sorted_by_rank[i][0] if i < len(weighted_nodes_sorted_by_rank) else None
                if agg_node is not None and weight_node is not None:
                    delta = 0 if agg_node == weight_node else 1
                else:
                    delta = 1  # If either node is missing
                isim_k3 += delta / (2 * (i + 1))

            isim_k3 = (1 / K) * isim_k3
            normalized_isim_k3 = 1 - isim_k3
            isim_k3_values.append(round(normalized_isim_k3,4))
            
        print(f"Normalized Similarity (Wang mothod 2023 vs Aggregated): {normalized_isim_k}")
        print(f"Normalized Similarity (Wang mothod 2023 vs Weighted): {normalized_isim_k2}")
        print(f"Normalized Similarity (Aggregated vs Weighted): {normalized_isim_k3}")
        return isim_k_values, isim_k2_values, isim_k3_values          
  
    def display_isim_table(self, isim_k_values, isim_k2_values, isim_k3_values):
        # Create a DataFrame to hold the ISIM values
        data = {
            'Top-K': range(1, len(isim_k_values) + 1),
            'Normalized ISIM (Wang method 2023 vs Unweighted)': isim_k_values,
            'Normalized ISIM (Wang method 2023 vs Weighted)': isim_k2_values,
            'Normalized ISIM (Unweighted vs Weighted)': isim_k3_values
        }
        df = pd.DataFrame(data)
        df = df.round(4)  
        df.set_index('Top-K', inplace=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot(kind='bar', alpha=0.7, ax=ax)
        ax.set_title('Normalized ISIM Values')
        ax.set_xlabel('Top-K')
        ax.set_ylabel('Normalized ISIM Values')
        ax.set_xticklabels(df.index, rotation=0)  
        ax.legend(title='ISIM Comparisons', bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=1)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        fig.subplots_adjust(bottom=0.25)
        plt.show()
       
