#!/usr/local/bin/python3

import os

def parse_sequence_lengths(filepath, base_pair_limit):
    """
    Parses fastq file and returns percentage of sequences with base pair count over base_pair_limit.

    >>> parse_sequence_lengths('./test_files/fastq/read1/doc_test_R1.fastq', 1)
    1.0
    >>> parse_sequence_lengths('./test_files/fastq/read1/doc_test_R1.fastq', 150)
    0.25
    >>> parse_sequence_lengths('./test_files/fastq/read2/doc_test_R2.fastq', 69)
    0.5
    """

    total_count = 0
    limit_count = 0
    with open(filepath) as f:
        line = f.readline()
        while line:
            if line.startswith('@'):
                total_count += 1
                seq = f.readline()
                sep = f.readline()
                qual = f.readline()
                if len(seq.strip()) > base_pair_limit:
                    limit_count += 1
            line = f.readline()

    return limit_count / total_count

def find_fastq_files(directory):
    """
    Recursively find all fastq files in a directory and return list of file paths.

    >>> find_fastq_files('./test_files/fastq')
    ['./test_files/fastq/read1/doc_test_R1.fastq', './test_files/fastq/read2/doc_test_R2.fastq', './test_files/fastq/read2/nested_read/doc_test_R2.fastq']
    """

    filepaths = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.fastq'):
                filepaths.append(os.path.join(dirpath, filename))
    return filepaths

def print_sequence_length_report(directory, base_pair_limit):
    """
    Prints sequence length report for fastq files.

    >>> print_sequence_length_report('./test_files/fastq', 50)
    ./test_files/fastq/read1/doc_test_R1.fastq
    0.75% sequences over 50
    <BLANKLINE>
    ./test_files/fastq/read2/doc_test_R2.fastq
    0.50% sequences over 50
    <BLANKLINE>
    ./test_files/fastq/read2/nested_read/doc_test_R2.fastq
    0.50% sequences over 50
    <BLANKLINE>
    """

    for filepath in find_fastq_files(directory):
        print("%(filepath)s\n%(percent)1.2f%% sequences over %(base_pair_limit)i\n" %
              {
                  'filepath': filepath,
                  'percent': parse_sequence_lengths(filepath, base_pair_limit),
                  'base_pair_limit': base_pair_limit
              })

if __name__ == "__main__":
    import argparse
    import doctest
    doctest.testmod()

    parser = argparse.ArgumentParser(description='Find sequence length limits percentages in a fastq file.')
    parser.add_argument('directorypath', nargs='?', type=str,
                        help='Directory to search for fastq files to read.',
                        default='./sample_files/fastq')
    parser.add_argument('--basepairs', dest='base_pair_limit', type=int, default=30,
                       help='Report percentages of sequences with base pairs over limit.')
    args = parser.parse_args()

    print_sequence_length_report(args.directorypath, args.base_pair_limit)
