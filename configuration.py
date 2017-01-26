import argparse
import logging

expectedFieldCount = 4

def parseFile(file):
    """
    Parses a configuration file into commands to run.
    :type file: str
    """
    logging.info("Parsing configuration file: {0}".format(file))
    with open(file) as strean:
        # Index of the line being processed
        lineIndex = 0
        for line in strean:
            lineIndex += 1
            # Split line into fields
            fields = line.split("\t")
            countFields = len(fields)
            # Check count of fields
            if expectedFieldCount != countFields:
                raise ValueError(
                    'Unexpected count of fields at line {0}: {1}'.format(
                    lineIndex, countFields)
                )
    logging.info("{0} lines parsed in {1}.".format(lineIndex, file))

if __name__ == '__main__':
    # Set logging level
    logging.basicConfig(level=logging.INFO)
    # Parse command line
    parser = argparse.ArgumentParser(
        description='Parse a configuration file for to benchmarkk software.'
    )
    parser.add_argument(
        'config', metavar='file.tab', type=str,
        help='a file of software and configurations to run'
    )
    args = parser.parse_args()
    parseFile(args.config)
