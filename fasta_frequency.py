#!/usr/local/bin/python3

def parse_sequence_counts(filename):
    """
    Parses sequence counts from a fasta file.

    >>> parse_sequence_counts('./test_files/fasta/doc_test.fasta')['AGGCGC']
    3
    >>> parse_sequence_counts('./test_files/fasta/doc_test.fasta')['TGCATC']
    2
    >>> parse_sequence_counts('./test_files/fasta/doc_test.fasta')['ATAGGG']
    1
    """

    seq_counts = {}
    with open(filename) as f:
        for line in f:
            if not line.startswith('>'):
                seq = line.strip()
                if seq:
                  current_count = seq_counts.get(seq, 0)
                  seq_counts[seq] = current_count + 1
    return seq_counts

def sort_sequence_counts(sequence_counts):
    """
    Sorts sequence_count dict by count descending.

    >>> sort_sequence_counts({'AGG':2, 'CAT': 3, 'GGC': 10, 'AAT': 5})[0]['sequence']
    'GGC'
    >>> sort_sequence_counts({'AGG':2, 'CAT': 3, 'GGC': 10, 'AAT': 5})[1]['sequence']
    'AAT'
    >>> sort_sequence_counts({'AGG':2, 'CAT': 3, 'GGC': 10, 'AAT': 5})[2]['sequence']
    'CAT'
    >>> sort_sequence_counts({'AGG':2, 'CAT': 3, 'GGC': 10, 'AAT': 5})[3]['sequence']
    'AGG'
    """

    count_iter = ({'sequence': seq, 'count': count} for seq, count in sequence_counts.items())
    return sorted(count_iter, key=lambda x: x['count'], reverse=True)

def print_sequence_count_report(filename, top_count):
    """
    Prints sequence count report for fasta file.

    >>> print_sequence_count_report('./test_files/fasta/doc_test.fasta', 10)
    Top 3 sequences:
    AGGCGC : 3
    TGCATC : 2
    ATAGGG : 1
    >>> print_sequence_count_report('./test_files/fasta/doc_test.fasta', 2)
    Top 2 sequences:
    AGGCGC : 3
    TGCATC : 2
    """

    seq_counts = parse_sequence_counts(filename)
    print("Top %i sequences:" % min(top_count, len(seq_counts)))
    for idx, seq_count in enumerate(sort_sequence_counts(seq_counts)):
        if idx == top_count:
            break
        print("%(sequence)s : %(count)i" % seq_count)

if __name__ == "__main__":
    import argparse
    import doctest
    doctest.testmod()

    parser = argparse.ArgumentParser(description='Count full sequence occurances in a fasta file.')
    parser.add_argument('filename', nargs='?', type=argparse.FileType('r'),
                        help='Fasta file to read.',
                        default='./sample_files/fasta/sample.fasta')
    parser.add_argument('--top', dest='top_count', type=int, default=10,
                       help='Number of sequence counts to report.')
    args = parser.parse_args()

    print_sequence_count_report(args.filename.name, args.top_count)
