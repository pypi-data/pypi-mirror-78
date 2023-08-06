import argparse
import sys

import simplejson
from piri.process import Process
from returns.curry import partial
from returns.result import safe

from piri_cli.common import read_file, write_file


def parse_args() -> argparse.Namespace:
    """Parse piri args."""
    desc = 'Transforms input json with provided cfg file to output.json'
    parser = argparse.ArgumentParser(
        description=desc,
    )

    parser.add_argument(
        'configuration',
        type=str,
        help='Path to configuration.json',
    )

    parser.add_argument(
        'input',
        type=str,
        help='Path to input.json',
    )

    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='Path and name of file to write',
        default='output.json',
    )

    return parser.parse_args()


def on_failure(failure):
    """Print out reason for failure and exit."""
    sys.exit('Execution failed.\nError type {0}\nError msg: {1}'.format(
        type(failure),
        failure,
    ))


def main():
    """Run piri with given args."""
    args = parse_args()

    configuration = read_file(
        args.configuration, 'r',
    ).bind(
        safe(simplejson.loads),
    ).alt(on_failure).unwrap()

    input_data = read_file(
        args.input, 'r',
    ).bind(
        safe(simplejson.loads),
    ).alt(on_failure).unwrap()

    Process()(
        input_data,
        configuration,
    ).bind(
        safe(simplejson.dumps),
    ).bind(
        partial(write_file, file_path=args.output),
    ).alt(on_failure)
