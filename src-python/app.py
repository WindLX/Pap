from argparse import ArgumentParser

from backend import start_backend


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dev", type=bool, default=False)
    args = parser.parse_args()

    start_backend(args.dev)
