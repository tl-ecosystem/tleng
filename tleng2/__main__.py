# for running examples!
# $ tleng2 example 1
# $ tleng2 example 2
# $ tleng2 example --help
# $ Tleng2 Examples:
# $ 1 - Simple Static platformer
# $ 2 - Camera movements
# $ n - etc..

# or better to run the tests of the engine
# $ tleng2 test

# and creating projects
# $ tleng2 new pixel-wheel platformer
# or
# $ tleng2 new pixel-wheel (empty)
# or
# $ tleng2 new
# $ Creating a tleng2 project, CLI wizard.
# $ What is the name of the project: pixel-wheel
# $ What is the type of this project: sprite-stacking
# $ Who is the author of this game: Theolaos
# $ 

import argparse
import sys
from tleng2 import __name__, __doc__, __version__

def main() -> None:

    print("hello")

    parser = argparse.ArgumentParser(
        prog=__name__.name, 
        description=__doc__.description,
        epilog="Check the repo in: https://github.com/tl-ecosystem/tleng"
    )


    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{__version__}",
        help="To see the version of the Game Engine"
    )

    parser.add_argument(
        "--license",
        action="version",
        version="MIT license",
        help="To see the license of the Game Engine"
    )
    return 0

if __name__ == "__main__":
    sys.exit(main())