import os

from ProgramConfiguration import *


class BenchmarkConfiguration:

    def __init__(self, file, out):
        """
        Initialise a BenchmarkConfiguration object.
        :type file: str
        :param file: Input file that defines the programs and configurations to benchmark.
        :param out: Root folder to store all outputs of the benchmark.
        """
        self.file = file
        self.configurations = {}
        self.out = out
        self.parse_tsv()

    def parse_tsv(self):
        """
        Parse a configuration file.
        :return: None
        """
        logging.info("Parse configuration file: {0}".format(self.file))
        count_config = 0
        with open(self.file) as stream:
            tmp_line_index = 0
            for tmp_line in stream:
                tmp_line_index += 1
                count_config += self.add_configuration(tmp_line.strip())
        logging.info("{0} lines parsed in {1}.".format(tmp_line_index, self.file))
        logging.info("{0} configurations imported.".format(count_config))
        return None

    def add_configuration(self, config_line):
        """
        Initialise a ProgramConfigurationList or append a new configuration to an existing one.
        :param config_line: One line of the input configuration file.
        :return: Count of configurations added.
        """
        if not len(config_line):
            return 0
        (program, params) = config_line.split('\t')
        parsed_params = self.parse_params(params)
        if program in self.configurations.keys():
            self.configurations[program].add_configuration(parsed_params)
        else:
            self.configurations[program] = ProgramConfigurationList(parsed_params, program)
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

    def make_dir_structure(self):
        """
        Create the directory structure for the benchmark.
        Side-effect: update configurations to define the individual output folder for each configuration.
        :return: None
        """
        self.make_output_dir()
        self.make_program_dirs()
        return None

    def make_output_dir(self):
        """
        Create the root folder for all outputs of this benchmark run.
        :return: None
        """
        logging.info("Create benchmark output folder: {0}".format(self.out))
        os.makedirs(self.out)
        return None

    def make_program_dirs(self):
        """
        Create a folder for each program tested;
        delegate creation of folders for each configuration tested.
        Side-effect: update configurations to define the individual output folder for each configuration.
        :return: None
        """
        for program in self.configurations.values():
            program.make_dir_structure(self.out)
        return None
