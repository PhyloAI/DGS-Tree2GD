# DGS Tree2GD
We have extensively modified the original scripts to accommodate Deep Genome Skimming (DGS) data, focusing mainly on the sequence analysis of closely related species. After installing Tree2GD, please replace all the original scripts with our modified versions, which include:
* **DGS-tree2gd_main.py**: This script has been optimized to effectively utilize the ‘--cds2tree’ parameter, facilitating the seamless incorporation of nuclear coding sequences (nuclear CDSs) into the gene tree inference process. By utilizing nuclear CDSs sequence alignments instead of protein sequences, this enhancement significantly improves the analysis of closely related species, especially those within the same genus.
* **DGS-kaks.py**: In this script, we modified the code to exclude alignments of extremely low quality and to eliminate blank files post-trimming.
* **DGS-Tree2GD_draw.R**: The visualization process has been enhanced to ensure compatibility with multiple species. To improve device compatibility and minimize disruptions by errors in any single component, we have segmented the visualization procedure into multiple batches.
## Dependencies
Tree2GD;  
TransDecoder;  
R
## Input
Fasta file, output from 'paralog_retriever' of HybPiper 2;  
Rooted species tree without bootstrap scores and branch lengths, newick format.
## Running the pipeline
### Step 1: Formating the sequence names
Original:  
\>Prunus_gongshanensis single_hit  
AGTC...  
Notes: To format the sequences run the loop below in the directory where the fasta files are locaded.

```
for i in $(ls *.fasta); do sed -i -E 's/(>.+)\.(.+)\s(.+)/\1@paralog_\2/' $i;done && for i in $(ls *.fasta);do awk '{print $1}' < $i > $i.fas;done && for i in $(ls *.fas); do sed -i '/>/ {/@/! s/$/@unique/}' $i;done && rename "s/_paralogs_no_chimeras.fasta.fas/.fasta/" *.fas
```
The output of this will be:  
\>Prunus_gongshanensis@unique  
AGTC...
### Step 2: Formating the name of each gene
Original:  
\>Prunus_gongshanensis@unique  
AGTC...  
The fasta files are named in the format “gene1234.fasta”  
The format_gene_name.py script appends the gene name to the end of the sequence name. Consequently, the sequence name consists of both the species name and the gene name.
```
python format_gene_name.py <"@" formated fasta files directory > <output directory>
```
### Step 3: Extracting sequences with the same species into one file
Original:  
\>Prunus_gongshanensis@unique_gene1234  
AGTC...  
\>Prunus_fujianensis@paralog_1_gene1234  
AGTC...  
The fasta files are named in the format “gene1234.fasta”  
The sorted_by_species.py script extracts the sequences of the same species into a single fasta file and replaces the "@" in the sequence name with "_". The new fasta file is named after the species.
```
python sorted_by_species.py <"species@unique/paralog_gene" formated fasta files directory > <output directory>
```
The output of this will be:  
\>Prunus_gongshanensis_unique_gene1234  
AGTC...  
\>Prunus_fujianensis_paralog_1_gene1234  
AGTC...  
These sequences are deposited in the files "Prunus_gongshanensis.fasta" and "Prunus_fujianensis.fasta", respectively.  
### Step 4: Translate DNA into protein
Notes: Format the sequences and run the loop below in the directory where the "species name" formatted fasta files are located.
```
for i in *.fasta; do TransDecoder.LongOrfs -t $i; done
```
Format file name:  
Write all species names into a text file (namelist.txt) and rename directories or files based on the species names listed in “namelist.txt”.
```
cat namelist.txt | while read name; do cd $name/; mv longest_orfs.cds $name.cds; cd ../; done
cat namelist.txt | while read name; do cd $name/; mv longest_orfs.pep $name.pep; cd ../; done
cat namelist.txt | while read name; do cd $name/; cp $name* /path/to/target/directory; cd ../; done 
python delete_redundant_information.py <*.cds and *.pep directory> <output directory>
```
### Step5: Replace the scripts and run DGS-Tree2GD
Note: After installing Tree2GD, please replace the original script with our modified versions.
```
Tree2gd -i <fatsa file directory> -tree <species tree> --cds2tree
--cds2tree: use CDS sequence to infer gene trees
```
## Citation
Chen DY, Zhang TK, Chen YM, Ma H, Qi J. 2022. Tree2GD: A phylogenomic method to detect large-scale gene duplication events. Bioinformatics 38: 5317–5321.




