import random

import numpy as np
import pandas as pd
import networkx as nx

from centality_compare import centrality_compare
from wevi_parser import wevi_parser


def graph_maker():
    list1 = [1 if num < 5 else 5 for num in range(10)]
    graph = nx.configuration_model(list1, seed=123)
    return graph


def get_neighbor(row_index, adj_mat):
    # Select an adjacent node to node 'row_index'
    adjacent_nodes = np.argwhere(adj_mat[row_index] != 0).flatten()
    return random.choice(adjacent_nodes)


def make_random_walks(adj_mat, num_of_walks, len_of_walks):
    # Generate a sentence for each random walk
    random_walks_sentences = []

    num_of_adjacency_matrix_rows = adj_mat.shape[0]
    # Iterate over the rows of the adjacency matrix
    # Variable i represents the starting node of the random walk
    for i in range(num_of_adjacency_matrix_rows):
        for j in range(num_of_walks):
            current_node = i

            # Starting node - always node i
            current_walk = list(["Node" + str(i)])

            # travel to other nodes and append them to the random walk
            for k in range(len_of_walks):
                current_node = get_neighbor(current_node, adj_mat)
                current_walk.append("Node" + str(current_node))

            # append to the result matrix
            current_sentence = ' '.join(current_walk)
            random_walks_sentences.append(current_sentence)
    result = pd.DataFrame({"String": random_walks_sentences})
    return result



def save_to_csv(random_walks, csv_path):
    random_walks.to_csv(csv_path, index=False)


def main():
    number_of_walks = 5
    length_of_walks = 5
    window_size = 2
    csv_path = "C:\Users\Dvir\Desktop\NNftw\words2.csv"

    # make graph
    graph = graph_maker()

    # draw the graph if you want to
    nx.draw_networkx(graph)
    # plt.show()

    # get the adjacency matrix
    adj_matrix = nx.adjacency_matrix(graph)

    # turn it from sparse to regular
    sparse_df = pd.SparseDataFrame(
        [pd.SparseSeries(adj_matrix[x].toarray().ravel()) for x in np.arange(adj_matrix.shape[0])])
    df = sparse_df.to_dense()

    # change the name of the rows
    df.index = ['Node' + str(x) for x in df]
    adj_matrix = df

    # make the random walks
    random_walks = make_random_walks(adj_matrix, number_of_walks, length_of_walks)
    save_to_csv(random_walks, csv_path)

    print "The input to wevi:"
    print wevi_parser(random_walks, window_size)
    print "Please paste here the results from wevi"
    input1 = raw_input()

    centrality_compare(graph, input1)

if __name__ == "__main__":
    main()
