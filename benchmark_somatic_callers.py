# Official
import argparse

# Custom
from BenchmarkConfiguration import *

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Benchmark a selection of software and configurations.'
    )
    parser.add_argument(
        'config', metavar='config.txt', type=str,
        help='A file of programs and configurations to run. The file is TAB-separated.'
             ' Column 1 must be one of the following program names:'
             ' {Mutect2, Strelka}.'
             ' Column 2 must be a semicolon-separated list of --flag=value pairs.'
             ' Those pairs are subsequently adapted to the program command line format.'
    )
    parser.add_argument(
        'out', metavar='./benchmark', type=str,
        help='Overall output folder for the benchmark'
    )
    parser.add_argument(
        'ref', metavar='reference.fa',
        help='Path to reference genome fasta'
    )
    parser.add_argument(
        'file1', metavar='normal.bam',
        help='Input file for reference group (e.g. normal)'
    )
    parser.add_argument(
        'file2', metavar='tumour.bam',
        help='Input file for target group (e.g. tumour)'
    )
    args = parser.parse_args()
    logging.info("Current working directory: {0}".format(os.getcwd()))
    bc = PairedBenchmarkConfiguration(args.config, args.out)
    bc.make_dir_structure()
    bc.write_scripts(args.ref, args.file1, args.file2)
    bc.submit_scripts()
