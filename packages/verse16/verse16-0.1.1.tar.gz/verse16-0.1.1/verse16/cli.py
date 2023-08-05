"""Console script for verse16."""
import argparse
import sys
from verse16.verse16 import Generator

def main():
    """
    Console script for verse16.
    options (with defaults):
        --log_level INFO    # log level
        --lines 16          # how many lines to generate
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--line_count", type=int,
                        default=16,
                        help="number of lines to generate")
    parser.add_argument("-v", "--log_level", type=str,
                        default="INFO",
                        help="set log level [DEBUG, INFO]")
    args = parser.parse_args()

    print("Arguments: " + str(args))

    gen = Generator(log_level=args.log_level)
    gen.generate(args.line_count)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
