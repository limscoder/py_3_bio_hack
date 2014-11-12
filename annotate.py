#!/usr/local/bin/python3

import csv
import bisect

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
    return {annotation: value[0:-1] for annotation, value in annotation_items}

def parse_gene_locations(filepath):
    """
    Parses gene locations from an annotation file.
    >>> gene_locations = parse_gene_locations('./test_files/gtf/doc_test.gtf')
    >>> gene_locations['chr3']['ANAPC13']['start']
    134196546
    >>> gene_locations['chr3']['ANAPC13']['name']
    'ANAPC13'
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
            gene_name = annotations.get('gene_name', 'NOT_NAMED')
            gene_defaults = {'name': gene_name, 'start': start, 'end': end}
            gene_map = chromosome_map.setdefault(gene_name, gene_defaults)

            if start < gene_map['start']:
                gene_map['start'] = start
            if end > gene_map['end']:
                gene_map['end'] = end
    return gene_locations

def sort_gene_locations(gene_locations):
    """
    Sorts gene locations from parse_gene_locations.

    >>> gene_locations = parse_gene_locations('./test_files/gtf/doc_test.gtf')
    >>> sorted_locations = sort_gene_locations(gene_locations)
    >>> sorted_locations['chr3']['start_locations'][0]
    134196546
    >>> sorted_locations['chr3']['genes'][0]['name']
    'ANAPC13'
    >>> sorted_locations['chr3']['start_locations'][1]
    144204162
    >>> sorted_locations['chr3']['genes'][1]['name']
    'ANAPC14'
    """

    sorted_locations = {}
    for chromosome, chromosome_map in gene_locations.items():
        sorted_genes = sorted(chromosome_map.values(), key=lambda x: x['start'])
        sorted_locations[chromosome] = {
            'genes': sorted_genes,
            'start_locations': [gene['start'] for gene in sorted_genes]
        }

    return sorted_locations

def get_gene_name(chromosome, location, gene_locations):
    """
    Returns a gene name for a chromosome location.

    >>> gene_locations = {'chr5': {'start_locations': [100, 3000], 'genes': [{'name': 'MYGENE', 'start': 100, 'end': 2000}, {'name': 'MYGENE2', 'start': 3000, 'end': 3500}]}}
    >>> get_gene_name('chr5', 1024, gene_locations)
    'MYGENE'
    >>> get_gene_name('chr5', 50, gene_locations)
    'UNKNOWN'
    >>> get_gene_name('chr5', 3010, gene_locations)
    'MYGENE2'
    >>> get_gene_name('chr5', 2500, gene_locations)
    'UNKNOWN'
    >>> get_gene_name('chr6', 1024, gene_locations)
    'UNKNOWN'
    """

    if chromosome in gene_locations:
        chromosome_map = gene_locations[chromosome]
        gene_idx = bisect.bisect_right(chromosome_map['start_locations'], location) - 1
        if gene_idx > -1:
            gene = chromosome_map['genes'][gene_idx]
            if location <= gene['end']:
                return gene['name']

    return 'UNKNOWN'

def write_chromosome_annotations(chromosome_filepath, gtf_filepath, out_filepath):
    """
    Write chromosome annotations to outfilepath.

    We make 3 optimizations to improve annotation lookup performance.

    1. Annotations are indexed by chromosome.
    2. We treat genes as a single annotation with a single start and end,
        instead of treating each exon/intron/other as a separate annotation.
    3. We use a binary search to locate annotations.

    These optimizations will cause incorrect results when a position has multiple
    annotations due to nested or overlapping annotation spans, so additional work
    is required to correctly handle that use case.
    """

    gene_locations = sort_gene_locations(parse_gene_locations(gtf_filepath))

    with open(chromosome_filepath) as infile:
        reader = csv.reader(infile, delimiter="\t")

        with open(out_filepath, 'w') as outfile:
            writer = csv.writer(outfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)

            for chromosome, location in reader:
                gene_name = get_gene_name(chromosome, int(location), gene_locations)
                writer.writerow((chromosome, location, gene_name))

if __name__ == "__main__":
    import argparse
    import doctest
    doctest.testmod()

    parser = argparse.ArgumentParser(description='Match chromosome locations to gene names.')
    parser.add_argument('chromosome_filepath', nargs='?', type=str,
                        help='Chromosome location file.',
                        default='./sample_files/annotate/coordinates_to_annotate.txt')
    parser.add_argument('--gtf', dest='gtf_filepath', type=str, default='./sample_files/gtf/hg19_annotations.gtf',
                        help='Annotations file.')
    parser.add_argument('--out', dest='out_filepath', type=str, default='./annotated_output.txt',
                        help='Output file.')
    args = parser.parse_args()

    write_chromosome_annotations(args.chromosome_filepath, args.gtf_filepath, args.out_filepath)
