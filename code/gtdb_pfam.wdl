workflow gtdb_map {

  Array[File] input_genomes_list

  scatter (g in input_genomes_list) {
    call preprocess_genomes {
      input:
        genome=g
    }
  }
}


task preprocess_genomes {
  File genome
  String genome_id = basename(genome, "_protein.faa")
  String output_path

  command {
    hmmsearch -o ${output_path}${genome_id}_hmm_output.txt --tblout ${output_path}${genome_id}_tblout.txt --cpu 2 --notextw ~/db/pfam/Pfam-A.hmm ${genome}
  }

  output {
    # File hmm_outfile = "${genome_id}_hmm_output.txt"
    # File tbl_outfile = "${genome_id}_tblout.txt"
  }
}
