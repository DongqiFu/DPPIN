# D-PPIN
D-PPIN is a dynamic network dataset that consists of 12 different dynamic protein-protein interaction networks of yeast cells.

## Statistics of D-PPIN
In each dynamic network of D-PPIN (e.g. Krogan_LCMS), the node represents a gene coding protein, the edge represents the protein-protein interaction at a certain timestamp, and each edge is timestamped like (node_u, node_v, timestamp, weight).

<p align="center"> Table 1. Generated Dynamic Networks. 
<img align="center" src="/data_stats.png" width="377" height="291"></p>


## Generation of D-PPIN
In brief, two components are needed to construct a dynamic protein-protein interaction network. The first one is a static protein-protein interation network and the second one is the time-aware gene expression value series of each protein in that static network. Through the active and co-expressed protein analysis (as shown in the following figure), a dynamic network is constructed.

![pic](/generation_process.png)
<p align="center"> Figure 1. Dynamic Protein Network Generation Process. </p>

The static networks for building D-PPIN is available at this [link](https://www.inetbio.org/yeastnet/downloadnetwork.php).
The yeast temporal gene expression value from the paper "Tu BP, Kudlicki A, Rowicka M, McKnight SL. Logic of the yeast metabolic cycle: temporal compartmentalization of cellular processes. Science 2005 Nov" is available at this [link](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE3431).
The dynamic network construction is mainly adopted from "Zhang, Yijia, Hongfei Lin, Zhihao Yang, Jian Wang, Yiwei Liu, and Shengtian Sang. "A method for predicting protein complex in dynamic PPI networks." BMC bioinformatics(2016).", which is available at this [link](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-016-1101-y).

The dynamic networks are constructed in each folder. If you want to construct again on your own and modify some parameters, just run main.py, and the prerequisites are listed below.
- numpy 1.20.1
- scipy 1.6.0
