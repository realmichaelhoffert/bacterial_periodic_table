import pandas as pd

def load_gtdb(fp):
    """
    Function for loading and formatting the GTDB metadata
    """
    # read in gtdb metadata
    md = pd.read_csv(fp, sep='\t')

    # filter to representatives
    md = md[md.gtdb_representative.eq('t')].copy(deep=True)
    md['Phylum'] = md.gtdb_taxonomy.apply(lambda x: x.split(';')[1].split('__')[-1])
    md['Class'] = md.gtdb_taxonomy.apply(lambda x: x.split(';')[2].split('__')[-1])
    md['Order'] = md.gtdb_taxonomy.apply(lambda x: x.split(';')[3].split('__')[-1])
    md['Family'] = md.gtdb_taxonomy.apply(lambda x: x.split(';')[4].split('__')[-1])
    md['Genus'] = md.gtdb_taxonomy.apply(lambda x: x.split(';')[5].split('__')[-1])
    md['Species'] = md.gtdb_taxonomy.apply(lambda x: x.split(';')[6].split('__')[-1])

    # subset to phyla with at least 100 representatives
    phylum_counts = md.groupby('Phylum').count()
    top_phyla = phylum_counts[phylum_counts['accession'] > 100].index.unique()
    md_top_phyla = md[md['Phylum'].isin(top_phyla)].copy(deep=True)

    # additional columns
    phylum_counts = md_top_phyla.groupby('Phylum').count()['accession']
    class_counts = md_top_phyla.groupby('Class').count()['accession']

    # parsing to make plot of isolate vs. environmental
    md_top_phyla['ncbi_genome_category_grouped'] = md_top_phyla['ncbi_genome_category'].apply(lambda x: 'Isolate' if x=='none' else 'MAG/SAG/environmental')

    md_top_phyla['accession_reformat'] = md_top_phyla['accession'].apply(lambda x: x.replace('.', '_'))
    
    return md, md_top_phyla