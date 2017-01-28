import argparse
import logging
import os.path

logging.basicConfig(level=logging.DEBUG)


class ProgramConfiguration:

    def __init__(self, out, params):
        """
        Initialise a Configuration object.
        :param program: Program to use in this configuration.
        :param params: Parameters to supply to the program.
        """
        self.exe = None
        self.params = parse_params(params)
        self.out = os.path.join(os.getcwd(), program)


class BenchmarkConfiguration:

    def __init__(self, file, out=None):
        """
        Initialise a BenchmarkConfiguration object.
        :type file: str
        :param file: Input file that defines the programs and configurations to benchmark.
        :param out: Root folder to store all outputs of the benchmark.
        """
        self.file = file
        self.configurations = self.parse_tsv()
        self.out = out

    def parse_tsv(self):
        """
        Parses a configuration file into Configuration objects.
        :type file: str
        :param file:
        :return: A list of Configuration objects.
        """
        logging.info("Parse configuration file: {0}".format(self.file))
        parsed_configurations = {}
        count_config = 0
        with open(self.file) as stream:
            tmp_line_index = 0
            for tmp_line in stream:
                tmp_line_index += 1
                count_config += self.add_configuration(parsed_configurations, tmp_line)
        logging.info("{0} lines parsed in {1}.".format(tmp_line_index, self.file))
        logging.info("{0} configurations imported.".format(count_config))
        return parsed_configurations

    def add_configuration(self, configurations, config_line):
        """
        Add a program with an empty list of configurations to a set of configurations if is not present yet.
        :param configurations: A dictionary of configurations.
        :param config_line: One line of the input configuration file.
        :return: Count of configurations added; always 1.
        """
        (program, params) = config_line.split('\t')
        if program in configurations.keys():
            configurations[program].append(self.parse_params(params))
        else:
            configurations[program] = [self.parse_params(params)]
        return 1

    @staticmethod
    def parse_params(params):
        """
        Parse benchmark parameters. Expected format: '--flag1=value1;-flag2=value2;...'.
        :type params: str
        :param params: Parameters to supply to the program.
        :return: None
        """
        parsed_params = {}
        keys_values = params.split(';')
        for kv in keys_values:
            (k, v) = kv.split('=')
            parsed_params[k] = v
        return parsed_params

    @staticmethod
    def write_config_file(config, folder):
        """
        Write the configuration parameters in a file in the corresponding folder.
        :return: None
        """
        file = os.path.join(folder, 'config.txt')
        logging.info("Create configuration log file: {0}".format(file))
        with open(file, 'w') as stream:
            for key in config:
                stream.write("{0}\t{1}\n".format(key, config[key]))
        return None

    def make_config_dirs(self, program):
        """
        Create a folder for each configuration under the folder for the corresponding program.
        Side-effect: update configurations to define the individual output folder for each configuration.
        :param program: Process only configurations of this program.
        :return: None
        """
        config_index = 0
        for config in self.configurations[program]:
            config_index += 1
            config_folder = os.path.join(self.out, program, "config_{0}".format(config_index))
            logging.info("Create configuration output folder: {0}".format(config_folder))
            os.mkdir(config_folder)
            # config.out = config_folder
            self.write_config_file(config, config_folder)
        return None

    def make_program_dirs(self):
        """
        Create a folder for each program tested;
        delegate creation of folders for each configuration tested.
        Side-effect: update configurations to define the individual output folder for each configuration.
        :return: None
        """
        unique_programs = self.configurations.keys()
        for program in unique_programs:
            program_folder = os.path.join(self.out, program)
            logging.info("Create program output folder: {0}".format(program_folder))
            os.mkdir(program_folder)
            configs = self.make_config_dirs(program)
        return None

    def make_benchmark_dir(self):
        """
        Create the root folder for all outputs of this benchmark run.
        :return: None
        """
        logging.info("Create benchmark output folder: {0}".format(self.out))
        os.makedirs(self.out)
        return None

    def make_dir_structure(self):
        """
        Create the directory structure for the benchmark.
        Side-effect: update configurations to define the individual output folder for each configuration.
        :return: None
        """
        self.make_benchmark_dir()
        self.make_program_dirs()
        return None


if __name__ == '__main__':
    # Parse command line
    parser = argparse.ArgumentParser(
        description='Parse a configuration file for to benchmark software.'
    )
    parser.add_argument(
        'config', metavar='config.txt', type=str,
        help='a file of software and configurations to run'
    )
    args = parser.parse_args()
    bc = BenchmarkConfiguration(args.config)
    bc.parse_tsv()
    # print(bc.out)
    # print(bc.configurations['Mutect'])
    # print(bc.configurations['Strelka'])
