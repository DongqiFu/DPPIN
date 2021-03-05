import math
import numpy as np
from scipy.stats import pearsonr


def get_common_proteins(gene_expression, PPIN_network):
    expressed_gene_set = set()
    PPIN_gene_set = set()

    gene_expression_file = open(gene_expression, 'r')
    for line in gene_expression_file.readlines():
        items = line.strip().split('  ')
        expressed_gene_set.add(str(items[1]))
    gene_expression_file.close()

    PPIN_network_file = open(PPIN_network, 'r')
    for line in PPIN_network_file.readlines():
        items = line.strip().split('\t')
        PPIN_gene_set.add(str(items[0]))
        PPIN_gene_set.add(str(items[1]))
    PPIN_network_file.close()

    common_protein_set = expressed_gene_set.intersection(PPIN_gene_set)

    protein2id = {}
    id2protein = {}
    idx = 0
    for protein in common_protein_set:
        protein2id[protein] = idx
        id2protein[idx] = protein
        idx += 1
    num_proteins = idx

    return common_protein_set, protein2id, id2protein, num_proteins


def get_temporal_act_prob(time_interval, num_cycles, num_proteins, protein2id, gene_expression):
    # - lifelong expression value - #
    gene_expression_value = np.zeros((num_proteins, time_interval * num_cycles), dtype=np.float32)
    gene_expression_file = open(gene_expression, 'r')
    for line in gene_expression_file.readlines():
        items = line.strip().split('  ')
        if items[1] in protein2id.keys():
            for t in range(time_interval * num_cycles):
                gene_expression_value[protein2id[items[1]], t] = items[t + 2]
    gene_expression_file.close()

    # - periodical expression value mean and std - #
    avg_gene_expression_value = np.zeros((num_proteins, num_cycles), dtype=float)
    std_gene_expression_value = np.zeros((num_proteins, num_cycles), dtype=float)
    for idx in protein2id.values():
        for i in range(num_cycles):
            avg_gene_expression_value[idx, i] = np.mean(gene_expression_value[idx, i*time_interval:(i+1)*time_interval])
            std_gene_expression_value[idx, i] = np.std(gene_expression_value[idx, i*time_interval:(i+1)*time_interval])

    # - Get active probability of each protein at each time (total 36 time stamps) - #
    act_vec_list = []
    for i in range(num_cycles):
        for t in range(time_interval):
            act_prob_vec = np.zeros((num_proteins,), dtype=float)
            for idx in protein2id.values():
                if gene_expression_value[idx, t + i * time_interval] >= avg_gene_expression_value[idx, i] + 3 * std_gene_expression_value[idx, i] * (1 - 1/(1 + math.pow(std_gene_expression_value[idx, i], 2))):
                    act_prob_vec[idx] = 0.99
                elif gene_expression_value[idx, t + i * time_interval] >= avg_gene_expression_value[idx, i] + 2 * std_gene_expression_value[idx, i] * (1 - 1/(1 + math.pow(std_gene_expression_value[idx, i], 2))):
                    act_prob_vec[idx] = 0.95
                elif gene_expression_value[idx, t + i * time_interval] >= avg_gene_expression_value[idx, i] + 1 * std_gene_expression_value[idx, i] * (1 - 1/(1 + math.pow(std_gene_expression_value[idx, i], 2))):
                    act_prob_vec[idx] = 0.68
            act_vec_list.append(act_prob_vec)

    return act_vec_list, gene_expression_value


def load_static_PPI(num_proteins, PPIN_network, protein2id):
    adj_matrix = np.zeros((num_proteins, num_proteins), dtype=int)

    PPIN_network_file = open(PPIN_network, 'r')
    for line in PPIN_network_file.readlines():
        items = line.strip().split('\t')
        if items[0] in protein2id.keys() and items[1] in protein2id.keys():
            adj_matrix[protein2id[items[0]], protein2id[items[1]]] = 1
            adj_matrix[protein2id[items[1]], protein2id[items[0]]] = 1
    PPIN_network_file.close()

    return adj_matrix


if __name__ == '__main__':
    gene_expression = 'GSE3431.txt'
    PPIN_network_list = ['Yu/Static_PPIN.txt', 'Babu/Static_PPIN.txt', 'Breitkreutz/Static_PPIN.txt', 'Gavin/Static_PPIN.txt',
                         'Hazbun/Static_PPIN.txt', 'Ho/Static_PPIN.txt', 'Ito/Static_PPIN.txt',
                         'Krogan_LCMS/Static_PPIN.txt', 'Krogan_MALDI/Static_PPIN.txt', 'Lambert/Static_PPIN.txt',
                         'Tarassov/Static_PPIN.txt', 'Uetz/Static_PPIN.txt']

    for PPIN_network in PPIN_network_list:
        # - Get common appeared proteins (i.e., genes) from PPI network and GSE3431 gene expression data - #
        common_protein_set, protein2id, id2protein, num_proteins = get_common_proteins(gene_expression, PPIN_network)
        print('----------------------------------------------------------------------------------------------------')
        print('Static PPI network: ' + PPIN_network.split('/')[0])
        print('Number of appeared proteins: ' + str(num_proteins))
        print('Not every protein has to be active, actual number of nodes may be fewer than ' + str(num_proteins))

        # - GSE3431 has totally 36 time intervals (i.e., time stamps) - #
        time_interval = 12  # - GSE3431 has 12 time intervals per cycle, 25 min per time interval - #
        num_cycles = 3  # - GSE3431 has 3 consecutive cycles - #

        # - Get the active prob. of each gene at each time stamp via expression values - #
        act_vec_list, gene_expression_value = get_temporal_act_prob(time_interval, num_cycles, num_proteins, protein2id, gene_expression)

        # - Output node features - #
        output_node_features = open(PPIN_network.split('/')[0] + '/Node_Features.txt', 'w+')
        for idx in range(num_proteins):
            output_node_features.write(str(idx) + ',' + str(id2protein[idx]) + ',' + ','.join(map(str, gene_expression_value[idx, :])) + '\n')
        output_node_features.close()

        # - Load static PPI network - #
        adj_matrix = load_static_PPI(num_proteins, PPIN_network, protein2id)

        # - Build temporal PPI network at each time stamp - #
        output_temporal_graph = open(PPIN_network.split('/')[0] + '/Dynamic_PPIN.txt', 'w+')
        for i in range(num_cycles):
            for t in range(time_interval):
                time_stamp = t + i * time_interval
                print('Current timestamp: ' + str(time_stamp))

                # - Build activity prob matrix - #
                act_prob_matrix = np.dot(act_vec_list[time_stamp].reshape((num_proteins, 1)), act_vec_list[time_stamp].reshape((num_proteins, 1)).transpose())

                # - Build co-expression matrix - #
                coe_matrix = np.zeros((num_proteins, num_proteins), dtype=float)
                if t == 0:
                    for node_u in range(num_proteins):
                        for node_v in range(node_u + 1, num_proteins):
                            x = [gene_expression_value[node_u, time_stamp], gene_expression_value[node_u, time_stamp + 1]]
                            y = [gene_expression_value[node_v, time_stamp], gene_expression_value[node_v, time_stamp + 1]]
                            pcc = pearsonr(x, y)
                            if pcc[0] >= 0.5:
                                coe_matrix[node_u, node_v] = pcc[0]
                                coe_matrix[node_v, node_u] = pcc[0]
                if t == 11:
                    for node_u in range(num_proteins):
                        for node_v in range(node_u+1, num_proteins):
                            x = [gene_expression_value[node_u, time_stamp - 1], gene_expression_value[node_u, time_stamp]]
                            y = [gene_expression_value[node_v, time_stamp - 1], gene_expression_value[node_v, time_stamp]]
                            pcc = pearsonr(x, y)
                            if pcc[0] >= 0.5:
                                coe_matrix[node_u, node_v] = pcc[0]
                                coe_matrix[node_v, node_u] = pcc[0]
                if t != 0 and t != 11:
                    for node_u in range(num_proteins):
                        for node_v in range(node_u+1, num_proteins):
                            x = [gene_expression_value[node_u, time_stamp - 1], gene_expression_value[node_u, time_stamp], gene_expression_value[node_u, time_stamp + 1]]
                            y = [gene_expression_value[node_v, time_stamp - 1], gene_expression_value[node_v, time_stamp], gene_expression_value[node_v, time_stamp + 1]]
                            pcc = pearsonr(x, y)
                            if pcc[0] >= 0.5:
                                coe_matrix[node_u, node_v] = pcc[0]
                                coe_matrix[node_v, node_u] = pcc[0]

                # - Build temporal adjacency matrix - #
                temporal_adj_matrix = np.multiply(np.multiply(act_prob_matrix, coe_matrix), adj_matrix)

                # - Write to output file at time t in the time interval of a cycle #
                for j in range(num_proteins):
                    for k in range(j + 1, num_proteins):
                        if temporal_adj_matrix[j, k] > 0:
                            output_temporal_graph.write(str(j) + ',' + str(k) + ',' + str(time_stamp) + ',' + str(temporal_adj_matrix[j, k]) + '\n')
        output_temporal_graph.close()