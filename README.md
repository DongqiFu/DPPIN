# DPPIN: A Biological Repository of Dynamic Protein-Protein Interaction Network Data

## Overview
DPPIN is a repository of dynamic network datasets, which consists of 12 individual dynamic protein-protein interaction network datasets, stored separately in 12 folders.

In each folder (e.g. DPPIN-Krogan(LCMS)),

- "Dynamic_PPIN.txt" stores temporal connections of the generated dynamic network. To be specific, a node represents a gene coding protein, an edge represents a protein-protein interaction at a certain timestamp, and each edge is timestamped with the format (node_u, node_v, timestamp, weight).

- "Static_PPIN.txt" stores the required static network for generating the dynamic network, each edge is recorded as (node_u, node_v, weight).

- "Node_Features" records the temporal gene expression value of each protein node, and the format is "node_id, node_name, value_at_t_1, value_at_t_2, ..., value_at_t_36".

Moreover, "Node_Labels.xlsx" stores labels (i.e., types) of 6,738 protein nodes shared by twelve dynamic network datasets in DPPIN, which covers the label of each node from each dynamic network. The label of each protein is retrievaled from [Saccharomyces Genome Database](https://www.yeastgenome.org/).

## Paper Link
[Preprint Paper](https://arxiv.org/pdf/2107.02168.pdf)

## Statistics of Generated Datasets in DPPIN
The statistics of the twelve generated dynamic network datasets are shown in Table 1. 

<p align="center"> Table 1. Statistics of DPPIN. </p>
<p align="center"> <img align="center" src="/data_stats.jpg" width="840" height="280"> </p>


## Generation Process of Dynamic Networks
In brief, two inputs are required to construct a dynamic protein-protein interaction network. The **first one** is a static protein-protein interation network and the **second one** is the time-aware gene expression value series of each protein. Through the activity and co-expression analysis (as shown in Figure 1), a dynamic network is constructed.

![pic](/Generation_Process.png)
<p align="center"> Figure 1. Generation of a Dynamic Protein-Protein Interaction Network. </p>

- The static networks for building the corresponding dynamic networks of DPPIN are available at [YeastNet](https://www.inetbio.org/yeastnet/downloadnetwork.php).
- The yeast temporal gene expression value (GSE3431.txt) retrieved from ["Tu et al., Logic of the Yeast Metabolic Cycle: Temporal Compartmentalization of Cellular Processes. Science 2005."](https://science.sciencemag.org/content/310/5751/1152) is also available at [NCBI](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE3431).

The method for constructing a dynamic network is mainly adopted from ["Zhang et al., A method for predicting protein complex in dynamic PPI networks. BMC Bioinformatics 2016."](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-016-1101-y).


## How to Run the Generation Code
The dynamic networks have already been constructed and stored in each folder, users can directly use it. If you want to construct them again on your own and modify some parameters, just run main.py. The main.py program will analyze the GES3431 gene expression value and the static network in each folder to generate the corresponding dynamic network and store it in that folder.

The program is written under Python 3.7, and the prerequisites are listed below.
- numpy 1.20.1
- scipy 1.6.0


## Reference
If you use the materials from this repositiory, please refer to our paper.
```
@inproceedings{DBLP:conf/bigdataconf/FuH22,
  author    = {Dongqi Fu and
               Jingrui He},
  title     = {{DPPIN:} {A} Biological Repository of Dynamic Protein-Protein Interaction
               Network Data},
  booktitle = {{IEEE} International Conference on Big Data, Big Data 2022, Osaka,
               Japan, December 17-20, 2022},
  pages     = {5269--5277},
  publisher = {{IEEE}},
  year      = {2022},
  url       = {https://doi.org/10.1109/BigData55660.2022.10020904},
  doi       = {10.1109/BigData55660.2022.10020904},
  timestamp = {Fri, 10 Feb 2023 18:39:54 +0100},
  biburl    = {https://dblp.org/rec/conf/bigdataconf/FuH22.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
