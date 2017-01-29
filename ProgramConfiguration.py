from SingleConfiguration import *


class ProgramConfigurationList:

    def __init__(self, params, out):
        """
        Initialise a Configuration object.
        :param params: Parameters to supply to the program.
        :param out: Program to use in this configuration.
        """
        self.configurations = []
        self.out = out
        self.add_configuration(params)

    def add_configuration(self, params):
        """
        Add a configuration.
        :param params: Dictionary of parameter flags and values.
        :return: None
        """
        config_out = "config_{0}".format(len(self.configurations)+1)
        self.configurations.append(SingleConfiguration(params, config_out))

    def make_dir_structure(self, out):
        """
        Create the folder to store outputs of all configurations for this program.
        :param out: Root folder to store outputs of the benchmark.
        :return: None
        """
        self.make_output_dir(out)
        self.make_config_dirs(os.path.join(out, self.out))
        return None

    def make_output_dir(self, out):
        """
        :param out: Root folder to store outputs of the benchmark.
        :return:
        """
        program_folder = os.path.join(out, self.out)
        logging.info("Create program output folder: {0}".format(program_folder))
        os.mkdir(program_folder)
        return None

    def make_config_dirs(self, out):
        """
        Create a folder for each configuration under the folder for the corresponding program.
        :param out: Root folder to store outputs of the program.
        :return: None
        """
        for config in self.configurations:
            config.make_dir_structure(out)
        return None
