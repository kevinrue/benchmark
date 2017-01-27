# Official
import argparse
import os
import os.path
import logging

# Custom
import configuration

logging.basicConfig(level=logging.DEBUG)


def make_benchmark_dir(folder):
    """ Create the root folder for all outputs of this benchmark run."""
    logging.info("Create benchmark output folder: {0}".format(os.path.join(os.getcwd(), folder)))
    os.makedirs(folder)  # Error if folder already exists
    return None


def make_program_dirs(benchmark_dir, configs):
    """Create a folder for each software tested. Delegate creation of folders for each configuration tested."""
    all_programs= []
    for config in configs:
        all_programs.append(config['program'])
    unique_programs = set(all_programs)
    for program in unique_programs:
        #
        program_folder = os.path.join(benchmark_dir, program)
        logging.info("Create program output folder: {0}".format(program_folder))
        os.mkdir(program_folder)
        # Make config dirs
        make_config_dirs(benchmark_dir, program, configs)
    return None


def make_config_dirs(benchmark_dir, program, configs):
    """Create a folder for each configuration under the folder for the corresponding program."""
    config_index = 0
    for config in configs:
        if config["program"] == program:
            config_index += 1
            config_folder = os.path.join(benchmark_dir, program, "config_{0}".format(config_index))
            logging.info("Create configuration output folder: {0}".format(config_folder))
            os.mkdir(config_folder)
    return None


def make_dir_structure(benchmark_dir, configs):
    # Make one folder for the benchmark outputs
    make_benchmark_dir(benchmark_dir)
    # Make one folder per program tested, and one sub-folder per configuration tested
    make_program_dirs(benchmark_dir, configs)
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
    configs = configuration.parseFile(args.config)
    make_dir_structure(args.out, configs)
