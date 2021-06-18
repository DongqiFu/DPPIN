# DPPIN
DPPIN is a collection of dynamic networks, which consists of 12 generated dynamic protein-protein interaction networks of yeast cells in 12 folders.

In each folder (e.g. Krogan_LCMS),

- "Dynamic_PPIN.txt" stores temporal connections of the generated dynamic network. To be specific, a node represents a gene coding protein, an edge represents a protein-protein interaction at a certain timestamp, and each edge is timestamped like (node_u, node_v, timestamp, weight).

- "Static_PPIN.txt" stores connections of the input static network, each edge is shown as (node_u, node_v, weight).

- "Node_Features" records the temporal gene expression value of each protein node, and the format is "node_id, node_name, value_at_t_1, value_at_t_2, ..., value_at_t_36".

Moreover, "Node_Labels.xlsx" stores labels (i.e., types) of 6,738 protein nodes shared by 12 folders, which covers the label of each node from 12 generated dynamic protein-protein interaction networks. The label of each protein is retrievaled from the [Saccharomyces Genome Database](https://www.yeastgenome.org/).


## Statistics of DPPIN
The statistics of all 12 generated dynamic networks are shown in Table 1. 

<p align="center"> Table 1. Generated Dynamic Networks in DPPIN. </p>
<p align="center"> <img align="center" src="/data_stats.jpg" width="1200" height="291"> </p>


## Generation Process of DPPIN
In brief, two components are needed to construct a dynamic protein-protein interaction network. The first one is a static protein-protein interation network and the second one is the time-aware gene expression value series of each protein. Through the activity and co-expression analysis (as shown in Figure 1), a dynamic network is constructed.

![pic](/generation_process.png)
<p align="center"> Figure 1. Dynamic Protein Network Generation Process. </p>

The static networks for building DPPIN are available at this [link](https://www.inetbio.org/yeastnet/downloadnetwork.php).
The yeast temporal gene expression value (GSE3431.txt) from the paper "Tu BP, Kudlicki A, Rowicka M, McKnight SL. Logic of the yeast metabolic cycle: temporal compartmentalization of cellular processes. Science 2005." is available at this [link](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE3431).

The dynamic network construction method is mainly adopted from "Zhang, Yijia, Hongfei Lin, Zhihao Yang, Jian Wang, Yiwei Liu, and Shengtian Sang. A method for predicting protein complex in dynamic PPI networks. BMC bioinformatics 2016.", which is available at this [link](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-016-1101-y).

## How to Run
The dynamic networks have already been constructed in each folder, users can directly use it. If you want to construct them again on your own and modify some parameters, just run main.py. The main.py program will analyze the GES3431 gene expression value and the static network in each folder to generate the corresponding dynamic network and store it in that folder.

The program is written under Python 3.7, and the prerequisites are listed below.
- numpy 1.20.1
- scipy 1.6.0
