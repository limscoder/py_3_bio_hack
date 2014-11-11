#!/usr/local/bin/python3

import csv

def parse_annotations(annotations):
    """
    Parse annotations cell from .gtf and return as dictionary.

    >>> annotations = parse_annotations('gene_id "CACFD1"; transcript_id "NM_001242370"; exon_number "5"; exon_id "NM_001242370.5"; gene_name "CACFD1";')
    >>> annotations['gene_id']
    'CACFD1'
    >>> annotations['exon_id']
    'NM_001242370.5'
    """

    annotation_items = [item.strip().split(' "') for item in annotations[0:-1].split(';')]
    return dict((annotation, value[0:-1]) for annotation, value in annotation_items)

def parse_gene_locations(filepath):
    """
    Parses gene locations from an annotation file.

    >>> gene_locations = parse_gene_locations('./test_files/gtf/doc_test.gtf')
    >>> gene_locations['chr3']['ANAPC13']['start']
    134196546
    >>> gene_locations['chr3']['ANAPC13']['end']
    134204866
    >>> gene_locations['chr9']['CACFD1']['start']
    136325087
    >>> gene_locations['chr9']['CACFD1']['end']
    136335910
    """

    gene_locations = {}
    with open(filepath) as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            chromosome = row[0]
            start = int(row[3])
            end = int(row[4])
            annotations = parse_annotations(row[8])
            chromosome_map = gene_locations.setdefault(chromosome, {})
            gene_map = chromosome_map.setdefault(annotations['gene_name'],
                                                 {'start': start, 'end': end})
            if start < gene_map['start']:
                gene_map['start'] = start
            if end > gene_map['end']:
                gene_map['end'] = end
    return gene_locations

def parse_chromosome_locations(filepath):
    """
    Parses chromosome locations from a file.

    >>> parse_chromosome_locations('./test_files/annotate/doc_test_coordinates.txt')
    [('chr3', 134196550), ('chr3', 135), ('chr9', 136335909)]
    """

    with open(filepath) as f:
        return [(chromosome, int(location)) for chromosome, location in csv.reader(f, delimiter="\t")]

def get_gene_name(chromosome_location, gene_locations):
    """
    Returns a gene name for a chromosome location.

    >>> get_gene_name(('chr5', 1024), {'chr5': {'MYGENE': {'start': 100, 'end': 2000}}})
    'MYGENE'
    >>> get_gene_name(('chr5', 1024), {})
    'UNKNOWN'
    """

    chromosome, location = chromosome_location
    gene_name_match = 'UNKNOWN'
    chromosome_map = gene_locations.get(chromosome, {})
    for gene_name, coordinates in chromosome_map.items():
        if location >= coordinates['start'] and location <= coordinates['end']:
           gene_name_match = gene_name
           break

    return gene_name_match

def write_chromosome_annotations(chromosome_filepath, gtf_filepath, out_filepath):
    """Write chromosome annotations to outfilepath."""

    gene_locations = parse_gene_locations(gtf_filepath)
    chromosome_locations = parse_chromosome_locations(chromosome_filepath)

    with open(out_filepath, 'w') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for chromosome_location in chromosome_locations:
            gene_name = get_gene_name(chromosome_location, gene_locations)
            writer.writerow((chromosome_location[0], chromosome_location[1], gene_name))

if __name__ == "__main__":
    import argparse
    import doctest
    doctest.testmod()

    parser = argparse.ArgumentParser(description='Match chromosome locations to gene names')
    parser.add_argument('chromosome_filepath', nargs='?', type=str,
                        help='Chromosome location file.',
                        default='./sample_files/annotate/coordinates_to_annotate.txt')
    parser.add_argument('--gtf', dest='gtf_filepath', type=str, default='./sample_files/gtf/hg19_annotations.gtf',
                        help='Annotations file.')
    parser.add_argument('--out', dest='out_filepath', type=str, default='./annotated_output.txt',
                        help='Output file.')
    args = parser.parse_args()

    write_chromosome_annotations(args.chromosome_filepath, args.gtf_filepath, args.out_filepath)
