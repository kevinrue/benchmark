from ProgramConfiguration import *


class PairedBenchmarkConfiguration:
    """
    A class to store configurations to benchmark programs that require paired input files (e.g. normal treated).
    """

    def __init__(self, file, out):
        """
        Initialise a BenchmarkConfiguration object.
        :param file: Input file that defines the programs and configurations to benchmark.
        :param out: Root folder to store all outputs of the benchmark.
        """
        self.file = file
        self.configurations = {}
        self.out = out
        self.parse_tsv()

    def parse_tsv(self):
        """
        Parse a predefined configuration file.
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
        Initialise a ProgramConfiguration or append a new configuration to an existing one.
        :param config_line: One line of the input configuration file.
        :return: Count of configurations added.
        """
        if not len(config_line):
            return 0
        config_split = config_line.split('\t')
        config_num_fields = len(config_split)
        if config_num_fields == 2:
            (program, params) = config_split
            parsed_params = self.parse_params(params)
        elif config_num_fields == 1:
            logging.info("No parameters detected. Default settings will apply.")
            program = config_split[0]; parsed_params = {}
        else:
            raise ValueError("Invalid number of TAB-separated fields in config line: {0}".format(config_num_fields))
        if program in self.configurations.keys():
            self.configurations[program].add_configuration(parsed_params)
        else:
            self.configurations[program] = self.select_program_config(parsed_params, program)
        return 1

    @staticmethod
    def parse_params(params):
        """
        Parse benchmark parameters. Expected format: '--flag1=value1;-flag2=value2;flag3;flag4=value4'.
        :param params: Parameters to supply to the program.
        :return: None
        """
        parsed_params = {}
        keys_values = params.split(';')
        logging.info("{0} parameters detected".format(len(keys_values)))
        for kv in keys_values:
            if '=' in kv:
                (k, v) = kv.split('=')
            else:
                (k, v) = (kv, None)
            parsed_params[k] = v
        return parsed_params

    @staticmethod
    def select_program_config(params, program):
        """
        Create a ProgramConfiguration object adapted to a given program.
        :param params: Dictionary of flag/value pairs. Toggle flags are assigned None value.
        :param program: Name of the program to benchmark.
        :return: An object that extends the ProgramConfiguration class.
        """
        if program == "MuTect2":
            return MuTect2PairedConfiguration(params, program)
        elif program == "Strelka":
            return StrelkaPairedConfiguration(params, program)
        elif program == "Virmid":
            return VirmidPairedConfiguration(params, program)
        elif program == "EBCall":
            return EBCallPairedConfiguration(params, program)
        elif program == "VarScan":
            return VarScanPairedConfiguration(params, program)
        elif program == "CaVEMan":
            return CaVEManPairedConfiguration(params, program)
        else:
            raise ValueError('Invalid program keyword: {0}'.format(program))

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
        Create a folder for each program tested; delegate creation of folders for each configuration tested.
        Side-effect: update configurations to define the individual output folder for each configuration.
        :return: None
        """
        for program in self.configurations.values():
            program.make_dir_structure(self.out)
        return None

    def write_scripts(self, ref, file1, file2):
        """
        Write a shell script for each configuration.
        :param ref: Reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :return: None
        """
        for program in self.configurations.values():
            program.write_scripts(self.out, ref, file1, file2)
        return None

    def submit_scripts(self):
        """
        Run all benchmark scripts.
        :return:
        """
        for program in self.configurations.values():
            program.submit_scripts(self.out)
        return None
