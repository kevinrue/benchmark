#!/usr/bin/env python

# Official
import argparse

# Custom
from BenchmarkConfiguration import *

# Note that by default, logging prints message on "stderr"
# For more control over logging, see link below
# http://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Benchmark a selection of software and configurations.'
    )
    parser.add_argument(
        'config', metavar='config.txt', type=str,
        help='A file of programs and configurations to run. The file is TAB-separated.'
             ' Column 1 must be one of the following program names:'
             ' {MuTect2, Strelka, Virmid, EBCall, VarScan, CaVEMan}.'
             ' Column 2 must be a semicolon-separated list of "flag=value" pairs (unquoted); except for "flag"-only'
             ' toggle options (e.g. "--flag1=value1;-flag2=value3;--flag3;flag4=value4").'
             ' Those flags and values (where applicable) are subsequently adapted to the program command line format.'
    )
    parser.add_argument(
        'out', metavar='./benchmark', type=str,
        help='Overall output folder for the benchmark.'
    )
    parser.add_argument(
        'ref', metavar='reference.fa',
        help='Reference genome Fasta file.'
    )
    parser.add_argument(
        'file1', metavar='normal.bam',
        help='Input file for reference group (e.g. normal.bam).'
    )
    parser.add_argument(
        'file2', metavar='tumour.bam',
        help='Input file for target group (e.g. tumour.bam).'
    )
    parser.add_argument(
        '-d', '--dry-run', action='store_true',
        help='Do not submit scripts as jobs.'
    )
    args = parser.parse_args()
    logging.info("Current working directory: {0}".format(os.getcwd()))
    bc = PairedBenchmarkConfiguration(args.config, args.out)
    bc.make_dir_structure()
    bc.write_scripts(args.ref, args.file1, args.file2)
    if not args.dry_run:
        bc.submit_scripts()
    logging.info('Main script completed.')
