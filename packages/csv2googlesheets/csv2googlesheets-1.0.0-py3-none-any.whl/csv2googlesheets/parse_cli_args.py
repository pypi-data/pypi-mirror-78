import os
import sys
import argparse

# What about an optional argument to pass a config file containing
# a custom delimiter and sheet range?


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv',
                        help='Provide path to an csv file')
    parser.add_argument('credentials_json',
                        help='Provide path to Google Api credentials.json')

    args = parser.parse_args()

    if not os.path.exists(args.csv):
        sys.exit(f'File {args.csv} does not exist.')
    if not os.path.exists(args.credentials_json):
        sys.exit(f'File {args.credentials_json} does not exist')

    return args
