# Official
import argparse
import os
import os.path
import logging

# Custom
import configuration

logging.basicConfig(level=logging.DEBUG)


def make_benchmark_dir(folder):
    """ Create the directory where all benchmarks"""
    logging.info("Creating benchmark folder: {0}".format(os.path.join(os.getcwd(), folder)))
    os.makedirs(folder)  # Error if folder already exists
    return None


def make_software_dirs(configs):
    """Create a folder for each software tested."""
    allPrograms = []
    for config in configs:
        allPrograms.append(config['program'])
    print(allPrograms)
    uniquePrograms = set(allPrograms)
    print(uniquePrograms)
    print(len(uniquePrograms))

def config2command_line(config):
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Benchmark a selection of software and configurations.'
    )
    parser.add_argument(
        'config', metavar='file.tab', type=str,
        help='a file of software and configurations to run'
    )
    parser.add_argument(
        'out',
        help='overall output folder for the benchmark'
    )
    args = parser.parse_args()
    make_benchmark_dir(args.out)
    configs = configuration.parseFile(args.config)
    make_software_dirs(configs)
    print(configs)
