# Official
import argparse
import os
import os.path
import logging

# Custom
import configuration

logging.basicConfig(level=logging.DEBUG)


def write_config_file(config):
    """
    Write the configuration parameters in a file in the corresponding folder.
    :param config:
    :return: None
    """
    file = os.path.join(config.out, 'config.txt')
    logging.info("Create configuration log file: {0}".format(file))
    with open(file, 'w') as stream:
        for key in config.params.keys():
            stream.write("{0}\t{1}\n".format(key, config.params[key]))
    return None


def make_config_dirs(benchmark_dir, program, configs):
    """
    Create a folder for each configuration under the folder for the corresponding program.
    :param benchmark_dir: Root folder for all outputs of the benchmark.
    :param program: Folder for all outputs of a program.
    :param configs: All configurations, including those associated with other programs.
    :return: Configurations updated to define the output folder for each configuration.
    """
    config_index = 0
    for config in configs:
        if config.program == program:
            config_index += 1
            config_folder = os.path.join(benchmark_dir, program, "config_{0}".format(config_index))
            logging.info("Create configuration output folder: {0}".format(config_folder))
            os.mkdir(config_folder)
            config.out = config_folder
            write_config_file(config)
    return configs


def make_program_dirs(benchmark_dir, configs):
    """
    Create a folder for each program tested;
    delegate creation of folders for each configuration tested.
    :param benchmark_dir: Root folder for all outputs of the benchmark.
    :param configs: All configurations to be tested.
    :return: Configurations updated to define the output folder for each configuration.
    """
    all_programs= []
    for config in configs:
        all_programs.append(config.program)
    unique_programs = set(all_programs)
    for program in unique_programs:
        program_folder = os.path.join(benchmark_dir, program)
        logging.info("Create program output folder: {0}".format(program_folder))
        os.mkdir(program_folder)
        # Make config dirs
        configs = make_config_dirs(benchmark_dir, program, configs)
    return configs


def make_benchmark_dir(folder):
    """
    Create the root folder for all outputs of this benchmark run.
    :param folder: Root folder for all outputs of the benchmark.
    :return: None
    """
    logging.info("Create benchmark output folder: {0}".format(os.path.join(os.getcwd(), folder)))
    os.makedirs(folder)
    return None


def make_dir_structure(benchmark_dir, configs):
    """
    Create the directory structure for the benchmark.
    :param benchmark_dir: Root folder for all outputs of the benchmark.
    :param configs: All configurations to be tested.
    :return: Configurations updated to define the output folder for each configuration.
    """
    make_benchmark_dir(benchmark_dir)
    configs = make_program_dirs(benchmark_dir, configs)
    return configs


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
    configs = configuration.parse_file(args.config)
    configs = make_dir_structure(args.out, configs)

