

# installation
# install.packages('devtools')

devtools::install_github("jlw-ecoevo/gRodon2")

library('gRodon')
library('coRdon')
library('matrixStats')
library('Biostrings')

paths <- Sys.glob('/data/mhoffert/genomes/GTDB_r207/grodon_format/*.fna.gz')
result_list <- list()
counter <- 0
for (p in paths) {
  # Load in example genome (Streptococcus pyogenes M1, downloaded from RefSeq)
  # included with gRodon
  genes <- readDNAStringSet(p)
  
  # Search pre-existing annotations for ribosomal proteins, which we
  # will use as our set of highly expressed genes
  highly_expressed_genes <- grepl("ribosomal_protein", names(genes), ignore.case = T)
  
  pass_filter <- (width(genes) > 240) & ((width(genes) %% 3) == 0)
  highly_expressed_filtered <- highly_expressed_genes[pass_filter]
  genes_filtered <- genes[pass_filter]

  # Remove genes containing ambiguous bases
  ambiguous_bases <- grepl("K|M|R|S|W|Y|N|V|H|D|B",genes_filtered)
  highly_expressed_final <- highly_expressed_filtered[!ambiguous_bases]
  
  # print(sum(na.omit(highly_expressed_final)))
  
  if (sum(na.omit(highly_expressed_final)) > 0) {
    # Run the gRodon growth prediction pipeline
    result <- predictGrowth(genes, highly_expressed_genes, mode='metagenome_v1')
    new_names <- append(names(result), 'path')
    new_result <- append(result, p)
    names(new_result) <- new_names
    result_list[[length(result_list)+1]] <- new_result
  }
  
  counter <- counter + 1
  if ((counter %% 10) == 0) {
    print(counter)
    df <- do.call(rbind, result_list)
    write.csv(file='/data/mhoffert/fiererlab/periodic_phyla/results/gRodon_result_list.tsv', x=df, sep='\t')
  }
  
}

df <- do.call(rbind, result_list)
write.csv(file='test.csv', x=df)
