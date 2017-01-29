
import logging
import os.path

logging.basicConfig(level=logging.DEBUG)


class SingleConfiguration:

    def __init__(self, params, out):
        self.params = params
        self.out = out

    def make_dir_structure(self, out):
        """
        :param out: Root folder to store outputs of the program.
        :return: None
        """
        config_folder = os.path.join(out, self.out)
        logging.info("Create configuration output folder: {0}".format(config_folder))
        os.mkdir(config_folder)
        self.write_config_file(config_folder)
        return None

    def write_config_file(self, out):
        """
        Write the configuration parameters in a file in the corresponding folder.
        :param out: Folder to store outputs of the configuration.
        :return: None
        """
        config_file = os.path.join(out, 'config.txt')
        logging.info("Create configuration log file: {0}".format(config_file))
        with open(config_file, 'w') as stream:
            for key in self.params.keys():
                stream.write("{0}\t{1}\n".format(key, self.params[key]))
        return None