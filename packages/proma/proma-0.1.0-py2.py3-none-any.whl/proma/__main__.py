"""Console script for proma"""

# import argparse
import sys

from proma.proma import create, test, build, install, develop


def main():
    action = sys.argv[1]
    param = sys.argv[2:]
    # parser = argparse.ArgumentParser()
    # parser.add_argument("action", type=str)
    # parser.add_argument("_", nargs="*")
    # args = parser.parse_args()

    # param = args._

    if action == "new":
        create(param[0])
    elif action == "test":
        test(param)
    elif action == "build":
        build(param)
    elif action == "install":
        install(param)
    elif action == "develop":
        develop(param)
    else:
        print("[ERREUR]Action inconnue : '%s'" % action)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
