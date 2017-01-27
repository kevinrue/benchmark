import argparse
import logging

expectedFieldCount = 4

logging.basicConfig(level=logging.DEBUG)

def parseFile(file):
    """
    Parses a configuration file into commands to run.
    :type file: str
    """
    logging.info("Parsing configuration file: {0}".format(file))
    with open(file) as stream:
        # Index of the line being processed
        tmpLineIndex = 0
        # List of configurations
        configList = []
        for tmpLine in stream:
            tmpLineIndex += 1
            # Split line into fields
            tmpFields = tmpLine.strip().split("\t")
            tmpCountFields = len(tmpFields)
            # Check count of fields
            if expectedFieldCount != tmpCountFields:
                raise ValueError(
                    'Unexpected count of fields at line {0}: {1}'.format(
                        tmpLineIndex, tmpCountFields
                    )
                )
            tmpConfig = dict(
                program=tmpFields[0],
                file1=tmpFields[1],
                file2=tmpFields[2],
                args=tmpFields[3]
            )
            configList.append(tmpConfig)
    logging.info("{0} lines parsed in {1}.".format(tmpLineIndex, file))
    logging.info("{0} configurations imported.".format(len(configList)))
    return(configList)

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
    parseFile(args.config)
