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
    logging.info("Create benchmark output folder: {0}".format(os.path.join(os.getcwd(), folder)))
    os.makedirs(folder)  # Error if folder already exists
    return None


def make_software_dirs(benchmarkDir, configs):
    """Create a folder for each software tested."""
    all_programs= []
    for config in configs:
        all_programs.append(config['program'])
    unique_programs = set(all_programs)
    for program in unique_programs:
        program_folder = os.path.join(benchmarkDir, program)
        logging.info("Create program output folder: {0}".format(program_folder))
        os.mkdir(program_folder)
    return None

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
    logging.info("Current working directory: {0}".format(os.getcwd()))
    make_benchmark_dir(args.out)
    configs = configuration.parseFile(args.config)
    make_software_dirs(args.out, configs)
    print(configs)
