import subprocess
import argparse
import logging
from timeit import default_timer as timer
from datetime import timedelta

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    filename='log.txt',
)


def calc_time(func):
    def wrapper(*args, **kwargs):
        logging.info(f'Compile started: {args}, {kwargs}')
        start = timer()
        func(*args, **kwargs)
        finish = timer()
        logging.info(f'Compile finished; time duration, s: {timedelta(seconds=finish-start)}')
    return wrapper


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_compiler',
                        type=str,
                        help='Command to invoke compiler',
                        )
    parser.add_argument('args',
                        help='List all flags to compiler, including path to source file',
                        type=str,
                        )
    return parser.parse_args()


@calc_time
def compile(command_line: list):
    subprocess.run(command_line, check=True)


def main():
    args = get_args()
    command_line = [f'{args.path_to_compiler}'] + args.args.split()
    compile(command_line)


if __name__ == '__main__':
    main()