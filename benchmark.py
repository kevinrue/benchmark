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
        help='a file of software and configurations to run'
    )
    parser.add_argument(
        'out', metavar='./benchmark', type=str,
        help='overall output folder for the benchmark'
    )
    parser.add_argument(
        'files1', metavar='normal1.bam,...',
        help='Comma-separated list of reference files to concatenated'
    )
    parser.add_argument(
        'files2', metavar='tumour1.bam,...',
        help='Comma-separated list of target files to concatenate'
    )
    args = parser.parse_args()
    logging.info("Current working directory: {0}".format(os.getcwd()))
    configs = BenchmarkConfiguration(args.config, args.out)
    configs.make_dir_structure()
