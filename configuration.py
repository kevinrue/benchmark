import argparse
import logging
import os.path

expectedFieldCount = 2

logging.basicConfig(level=logging.DEBUG)


class Configuration:

    def __init__(self, program, params):
        """
        Initialise a Configuration object.
        :param program: Program to use in this configuration.
        :param params: Parameters to supply to the program.
        """
        self.program = program
        self.params = parse_params(params)
        self.out = os.path.join(os.getcwd(), program)


def parse_params(params):
    """
    Parse benchmark parameters.
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


def parse_file(file):
    """
    Parses a configuration file into Configuration objects.
    :type file: str
    :param file:
    :return: A list of Configuration objects.
    """
    logging.info("Parsing configuration file: {0}".format(file))
    with open(file) as stream:
        # Index of the line being processed
        tmpLineIndex = 0
        # List of configurations
        config_list = []
        for tmpLine in stream:
            tmpLineIndex += 1
            # Split line into fields
            tmp_fields = tmpLine.strip().split("\t")
            tmp_count_fields = len(tmp_fields)
            # Check count of fields
            if expectedFieldCount != tmp_count_fields:
                raise ValueError(
                    'Unexpected count of fields at line {0}: {1}'.format(
                        tmpLineIndex, tmp_count_fields
                    )
                )
            tmp_config = Configuration(program=tmp_fields[0],params=tmp_fields[1])
            config_list.append(tmp_config)
    logging.info("{0} lines parsed in {1}.".format(tmpLineIndex, file))
    logging.info("{0} configurations imported.".format(len(config_list)))
    return config_list

if __name__ == '__main__':
    # Parse command line
    parser = argparse.ArgumentParser(
        description='Parse a configuration file for to benchmarkk software.'
    )
    parser.add_argument(
        'config', metavar='file.tab', type=str,
        help='a file of software and configurations to run'
    )
    args = parser.parse_args()
    parse_file(args.config)
