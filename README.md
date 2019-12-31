# GeneSet MAPR

Two methods are provided for running GeneSet MAPR. The script mapr.py will complete all steps at once. Alternatively, the scripts can be run individually. This latter option is useful in the event one wishes to re-use a network that has already been processed.

Expected network and gene set file formats are described at the end of this document.

## Approach 1: Using the MAPR wrapper


## Approach 2: Running scripts manually

The primary steps to GeneSet MAPR are as follows:
1. Pre-process the network
2. Create meta-path features from gene set(s)
3. Learn the gene ranking

### Pre-processing the network

Network pre-processing is handled by the script: MAPR_networkPrep.py

The script requires 1 argument giving the path (relative or fixed) to the two network files provided by the user. It will create the meta-path matrices and other supporting files, such as lists of all unique genes or non-gene terms in the network. By default this will be created in the same directory as the network location, but can be changed with an optional flag.

Optional arguments are specified with flags, and include
- '-k' An alternative keep file. Otherwise assumed to be in same directory as the edge file, named with the same name (ie: network_name.keep.txt).
- '-l' The maximum length of meta-paths to calculate. Currently, the script will calculate paths up to lengths of 3 edges, but this can be set to 2 or 1.
- '-v' How much feedback to receive at the command line. Default value is 0, but can be set to 1 or 2.
- '-n' An alternative output location for the processed network. By default the processed network is saved in the same directory as the provided edge file.
- '-s' Whether to save each single-edge sub-network. Default value is False. If set to True, then an edge file will be saved for each individual edge type in the original network file.

An example of calling the script using default options and the included example network:
```
$ python MAPR_networkPrep.py ./networks/example_network.edge.txt

Running GeneSet MAPR pre-processing ...

Done.
```

An example specifying a different output location, limiting meta-paths to lengths of no greater than 2 edges, saving .txt sub-network edge lists, and specifying verbose terminal output:
```
$ python MAPR_networkPrep.py ./networks/example_network.edge.txt -o ./alternative_net_output -l 2 -s True -v 1

Running GeneSet MAPR pre-processing ...

Reading in the following edge & keep files ...
    ./networks/example_network.edge.txt
    ./networks/example_network.keep.txt
Applying restrictions specified in keep file ...
Saving network files to ./alternative_net_output/example_network/
doSaveSubNets True
  saving subnetwork edge list: example_network-GO_BioProc.txt
  saving subnetwork edge list: example_network-GO_CelComp.txt
  saving subnetwork edge list: example_network-GO_MolFunc.txt
  saving subnetwork edge list: example_network-kegg_pathway.txt
  saving subnetwork edge list: example_network-pfam_domain.txt
  saving subnetwork edge list: example_network-PPI_direct_interaction.txt
  saving subnetwork edge list: example_network-PPI_genetic_interaction.txt
  saving subnetwork edge list: example_network-PPI_physical_association.txt
  saving subnetwork edge list: example_network-STRING_coexpression.txt
  saving subnetwork edge list: example_network-STRING_textmining.txt
  saving subnetwork edge list: example_network-blastp_homology.txt
All 1-length paths already computed ...
WARNING: maximum value == 0 for saved matrix 000044.gz
    Meta-path PPI_direct_interaction-STRING_coexpression does not connect any nodes.

WARNING: maximum value == 0 for saved matrix 000051.gz
    Meta-path PPI_genetic_interaction-STRING_coexpression does not connect any nodes.


Done.
```
The warnings here indicate meta-paths that fail to connect any nodes. This may happen when very sparse sub-networks are combined, and no nodes use edges from both edge types. Such meta-paths won't influence the final prediction.


### Creating the meta-path features

Meta-path connections for gene sets are calculated by: MAPR_buildFeatures.py

The script requires 1 argument specifying the name of the network to use. By default, it assumes the processed network is stored in './networks', the gene sets to be processed are in './samples', and the resulting output will be saved in './output'.

The script will calculate meta-path connections for all gene sets in the samples directory.

Optional arguments are specified with flags, and include
- '-v' How much feedback to receive at the command line. Default value is 0, but can be set to 1 or 2.
- '-n' Directory where the processed network is stored. Default is './network'
- '-s' Directory where one or more gene set text files are stored. Default is './samples'
- '-o' Directory where the output will be saved. Default is './output'

An example of the script with default options and the processed example network:
```
$ python MAPR_buildFeatures.py example_network

-----------------------------------------
Building feature vectors from network ...
  network: example_network
  sample set: samples
-----------------------------------------

Creating path: ./output/results_0006/char01-batch-000/
Features stored at: ./output/results_0006/char01-batch-000/

Done.
```

An example specifying a network saved to an alternative location, an alternative output folder, and verbose terminal feedback:
```
python MAPR_buildFeatures.py example_network -n ./alternative_net_output -o ./alternative_output -v 1

-----------------------------------------
Building feature vectors from network ...
  network: example_network
  sample set: samples
-----------------------------------------

Files will be saved to char01-batch-001/
Creating path: ./alternative_output/char01-batch-001/
Creating the gene-index dictionary.
Checking what paths are available ...
Finding the matrix dimensions ...
Collecting sample: 1, sample01
Collecting sample: 2, sample02
  Examined 0 of 77 paths...
    --time per path: 0.012 (s)
  Examined 25 of 77 paths...
    --time per path: 0.012 (s)
  Examined 50 of 77 paths...
    --time per path: 0.00799 (s)
  Examined 75 of 77 paths...
    --time per path: 0.012 (s)
Finished examining matrix similarity matrices.
Finished writing Z-Score Similarity feature vector files.
    --time to write: 0.912 (s)
Features stored at: ./alternative_output/char01-batch-001/

Done.
```

### Learning the ranked gene list

Characterization of gene sets based on meta-paths is performed by MAPR_characterizeSet

The script requires 1 argument specifying the location of the meta-path features. This is the directory output by the MAPR_buildFeatures script. This script builds multiple models of the processed gene sets to learn how they are interconnected and create a ranked list of all genes by patterns of connectedness. This is done both for the full gene set and several folds. The cross-folds are used to determine how well the learned models predict the original gene set -- or how well they fit the data.
Each fold is scored by how well the concealed genes are predicted using the Area Under the Curve (AUC) metric. The mean is taken over all folds for each sample to illustrate how well each sample can be predicted by GeneSet MAPR using the provided network (how well the set can be uniquely identified by MAPR).

Optional arguments are specified with flags, and include
- '-i' Path and filename of a text file containing edge types to omit from consideration. Default is 'NONE'.
- '-l' Maximum meta-path length to consider. Default is 3.
- '-m' Number of models to create, affects stability of results. Default is 101.
- '-p' Whether to save the Area Under the Curve (AUC) plots as PNG files. Default is 'False'.
- '-v' How much feedback to receive at the command line. Default value is 0, but can be set to 1 or 2.

An example of the script with default options and the processed example network:
```
$ python MAPR_characterizeSet.py ./output/char01-batch-000
```

An example of the script specifying a maximum considered meta-path length of 2, the creation of only 31 models per set, and verbose terminal feedback.
```
$ python MAPR_characterizeSet.py ./alternative_output/char01-batch-000 -l 2 -n 31 -v 1

Running GeneSet MAPR set characterization ...

Performing regression(s) on ./alternative_output/char01-batch-000
Using label: Iter1V31_cLas_aA_wRS2_m1_fZ12
Reading gene and path dictionaries for example_network
After removing ignored edges and lengths, using 77 metapaths

char01-batch-000/full-sample01/
    ... using 77 features
known: 0, unknown: 0; exiting loop
  Saving ranked genes to file ranked_genes-Iter1V31_cLas_aA_wRS2_m1_fZ12_Avg.txt
  Saving ranked genes to file ranked_all_genes-Iter1V31_cLas_aA_wRS2_m1_fZ12_Avg.txt
  Saving feature scores to file scored_features-Iter1V31_cLas_aA_wRS2_m1_fZ12.txt
--1 of 10
--elapsed time: 0.00 (h)

char01-batch-000/full-sample02/
    ... using 77 features
known: 0, unknown: 0; exiting loop
  Saving ranked genes to file ranked_genes-Iter1V31_cLas_aA_wRS2_m1_fZ12_Avg.txt
  Saving ranked genes to file ranked_all_genes-Iter1V31_cLas_aA_wRS2_m1_fZ12_Avg.txt
  Saving feature scores to file scored_features-Iter1V31_cLas_aA_wRS2_m1_fZ12.txt
--2 of 10
--elapsed time: 0.00 (h)

...
```

## Input/Output File Formats

### Network files

A network is provided by the user as two tab-delimited files: an edge file and a keep file. Examples can be found in the ./networks directory.

The edge file specifies edges in the network. Each line has four columns specifying an origin node, a terminal node, a weight, and an edge type. Some lines from "example_network.edge.txt" are shown below. Three edge types are shown: GO_MolFunc, pfam_domain, and String_coexpression. Gene names begin with "ENSG", while gene ontology terms begin with "GO_" and protein families with "pfam_".

The STRING_coexpression edges are direct gene to gene edges. As such, the first two columns contain gene names. Both GO_MolFunc and pfam_domain edge types group genes into shared terms. For those, the first column contains the term (eg. Pdom_Ank) while the second column is one of the genes in that term. The third column scores the strength of that particular edge, or connection. Note that the way scores are calculated and defined may vary greatly from one edge type to another. MAPR will normalize the scores for each edge type to allow more equivalent comparison of weights across types.

```
ENSG00000004779	ENSG00000006715	681	STRING_coexpression
ENSG00000004779	ENSG00000005249	537	STRING_coexpression
ENSG00000004779	ENSG00000007923	681	STRING_coexpression
ENSG00000004779	ENSG00000008018	647	STRING_coexpression
GO_0001085	ENSG00000005339	2	GO_MolFunc
GO_0001085	ENSG00000004487	1	GO_MolFunc
GO_0001102	ENSG00000005339	2	GO_MolFunc
Pdom_Ank	ENSG00000001629	7.39	pfam_domain
Pdom_Ank	ENSG00000001631	7.25	pfam_domain
Pdom_Ank	ENSG00000005700	7.48	pfam_domain
Pdom_SH3_1	ENSG00000005020	6.61	pfam_domain
Pdom_SH3_1	ENSG00000005379	7.86	pfam_domain
Pdom_SH3_1	ENSG00000006432	6.55	pfam_domain
Pdom_SH3_1	ENSG00000006453	4.22	pfam_domain
Pdom_SH3_1	ENSG00000007237	5.82	pfam_domain
Pdom_SH3_1	ENSG00000007264	5.33	pfam_domain
Pdom_SH3_1	ENSG00000008735	4.85	pfam_domain
Pdom_SH3_2	ENSG00000000938	6.73	pfam_domain
Pdom_SH3_2	ENSG00000002834	5.25	pfam_domain
```

The keep file tells MAPR how to distinguish between gene and term nodes, as well as indicate which edges to keep or discard when processing the network. An example follows below. The keep file consists of three sections, indicated by the required headers "GENE TYPES", "EDGE TYPES", and "CUTOFF RANGE". Under "GENE TYPES" are three columns indicating species, the pattern of characters occurring at the start of each gene of that type (for use by regex), and the indicator whether to keep or discard the genes in that row. Setting the indicator column to "keep" or "yes" will keep genes of that type, while "no" will discard them.

Note that genes must start with some identifying set of characters. In the provided example network, all genes used either the Ensemble Gene ID or the Locus Reference Genomic identifier. Therefore, every gene name began with either "ENSG" or "LRG". If you use gene names with much wider variation, you may wish to use a prefix such as "g_" to distinguish genes from non-gene terms.

The EDGE TYPES section has three columns: the name of the edge type, whether it is direct (gene-to-gene connection) or indirect (genes belong to a shared term), and an indicator whether to keep that edge type (ie: "keep" or "yes"). The CUTOFF RANGE section is specific to indirect edge types. The three columns there are: edge type, minimum considered term size, and maximum considered term size. For instance, the file example_alternate.keep.txt has the row "GO_MolFunc    10    3000", indicating that all terms containing less than 10 genes or more than 3000 will be ignored. One may wish to do this to filter out terms that are considered either too noisy and subjective, or too broad to be useful.

Part of example_alternate.keep.txt is shown, note the three sections and the columns within each section:
```
GENE TYPES
human1	ENSG	keep
human2	LRG_	no

EDGE TYPES
GO_MolFunc	indirect	keep
kegg_pathway	indirect	no
pfam_domain	indirect	keep
STRING_coexpression	direct	no

CUTOFF RANGE
GO_MolFunc	10	3000
kegg_pathway	10	3000
pfam_domain	10	3000
```

By default, the MAPR scripts will look for a keep file with the same name as the edge file. For example, if the provided edge file is named "network_name.edge.txt", the script will look for "network_name.keep.txt". This can be changed using the '-k' command-line argument.


### Gene sets

Gene sets should be provided as text files (examples shown in ./samples). They may be given as one or two files. In the case that up- and down-regulated genes are provided as two separate files to be treated as one gene set, the files should begin with the same name and end with either '_DN.txt' or '_UP.txt'.

Genes need not be sorted. The script will remove any redundant entries, and ignore genes that don't appear in the network.

An example of the first several lines in a sample gene set:
```
ENSG00000007047
ENSG00000008294
ENSG00000002919
ENSG00000005206
ENSG00000002726
ENSG00000006534
ENSG00000006712
...
```

### Output Files

TODO

## Required Python packages

The final version of GeneSet MAPR was written in Python 3.5. Some of the text file reading may break under version 2.7.

The only non-standard python packages used were Numpy and Scikit-Learn.
