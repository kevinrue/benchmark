import argparse

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
    print(args)